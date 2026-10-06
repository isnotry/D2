# -*- coding: utf-8 -*-
"""把 d2data(权威属性) + 多个中文译名来源合并为 build_site.py 可用的数据表。
输出：d2_chronicle_data.py  (CHRONICLE = {"runewords":[...], "sets":[...], "uniques":[...]})
数据基准：blizzhackers/d2data @ patch 3.3 (2026-08-21)
"""
import json, re, html, os, sys
from opencc import OpenCC

CC = OpenCC('t2s')
def s2s(x):
    return CC.convert(x) if x else x

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, 'ref')     # d2r.world 官方繁体译名表（抓取存档，随仓库提交）

def _find(name, env=None):
    """定位外部数据源：环境变量 > 本目录 > /tmp（d2data 有 1.2G，不入库）。"""
    cands = []
    if env and os.environ.get(env):
        cands.append(os.environ[env])
    cands += [os.path.join(HERE, name), os.path.join('/tmp', name)]
    for c in cands:
        if os.path.exists(c):
            return c
    raise SystemExit('找不到数据源 %s，请把它放到 %s 或 /tmp 下（或用 %s 指定路径）'
                     % (name, HERE, env or 'N/A'))

DD = os.path.join(_find('d2data'), 'json')
TK = os.path.join(_find('d2tracker'), 'src', 'data')

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

def load_opt(p):
    """可选文件：不存在时返回空。"""
    return load(p) if os.path.exists(p) else {}

# ---------------------------------------------------------------------------
# d2r.world 官方译名（繁→简），权威来源，优先于 tracker
# ---------------------------------------------------------------------------
OFF_BASE = load(os.path.join(REF, 'd2rworld_base_zh_s.json'))       # 底材 英文→简中
OFF_SET = load(os.path.join(REF, 'd2rworld_sets_zh_s.json'))        # 套装 英文→简中
OFF_PART = load(os.path.join(REF, 'd2rworld_setparts_zh_s.json'))   # 套装部件 英文→简中
OFF_UNI = load(os.path.join(REF, 'd2rworld_uniques_zh_s.json'))     # 独特道具 英文→简中

def _norm(s):
    """归一化英文名用于宽松比对：去掉撇号/连字符/空格并小写。"""
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

# d2data 内部名 → 官方显示名：先用归一化自动匹配（Bloodraven's Charge → Blood Raven's Charge），
# 匹配不到的手工补（多为内部代号或历史名）。
_off_by_norm = {}
for _en in list(OFF_UNI) + list(OFF_PART) + list(OFF_SET) + list(OFF_BASE):
    _off_by_norm.setdefault(_norm(_en), _en)

MANUAL_ALIAS = {
    # 独特道具：d2data 内部名 → 官方名
    # War Bonnet 属性与官方 Biggin's Bonnet 完全一致（+15 生命/+30 准确/+30% 伤害/+15 法力），
    # 是同一件的老版本内部名；d2data 里反而没有 Biggin's Bonnet 这一条。
    'War Bonnet': "Biggin's Bonnet",
    'Valkiry Wing': 'Valkyrie Wing', 'Peasent Crown': 'Peasant Crown',
    'Fathom': "Death's Fathom", 'Wisp': 'Wisp Projector', 'Razoredge': "Razor's Edge",
    'Bonesob': 'Bonesnap', 'Cerebus': "Cerebus' Bite", 'Deaths\'s Web': "Death's Web",
    'The Minataur': 'The Minotaur', 'Victors Silk': "Victor's Silk",
    'Skin of the Flayerd One': 'Skin of the Flayed One',
    'Thudergod\'s Vigor': "Thundergod's Vigor", 'Que-Hegan\'s Wisdon': "Que-Hegan's Wisdom",
    'Steel Carapice': 'Steel Carapace', 'Lenyms Cord': 'Lenymo',
    'Verdugo\'s Hearty Cord': "Verdungo's Hearty Cord", 'Maelstromwrath': 'Maelstrom',
    'Iros Torch': "Iros' Torch", 'Rimeraven': 'Rimeraven', 'Piercerib': 'Piercerib',
    'Pullspite': 'Pullspite', 'Doomspittle': 'Doomspittle', 'Pus Spiter': 'Pus Spitter',
    'Whichwild String': 'Witherstring', 'Godstrike Arch': 'Goldstrike Arch',
    'Souldrain': 'Soul Drainer', 'Darkforge Spawn': 'Darkforce Spawn',
    'Pompe\'s Wrath': "Pompeii's Wrath", 'The Humongous': 'The Humongous',
    'The Chieftan': 'The Chieftain', 'Fechmars Axe': "Fechmar's Axe",
    'The Reedeemer': 'The Redeemer', 'Ironward': 'Ironward',
    'Lazarus Spire': 'Lazarus Spire', 'Krintizs Skewer': "Krintiz's Skewer",
    'Irices Shard': "Irice's Shard", 'Radimant\'s Sphere': "Radament's Sphere",
    'Kerke\'s Sanctuary': "Kerke's Sanctuary", 'The Atlantian': 'The Atlantean',
    'Venomsward': 'Venom Ward', 'Amulet of the Viper': 'Amulet of the Viper',
}

def official_name(en):
    """d2data 名 → 官方显示名（找不到就原样返回）。"""
    if en in MANUAL_ALIAS:
        return MANUAL_ALIAS[en]
    n = _norm(en)
    if n in _off_by_norm:
        cand = _off_by_norm[n]
        if cand != en:
            return cand
    return en

# 任务物品：只在任务中临时存在，玩家无法「收藏」，不进清单。
# 特征：lvl=0 且 lvl req=0（赫拉迪克杖三件、可汗之锤两件、地狱熔炉锤）。
TASK_ITEM_KEYS = {
    'Amulet of the Viper', 'Staff of Kings', 'Horadric Staff',
    'Hell Forge Hammer', 'KhalimFlail', 'SuperKhalimFlail',
}

# ---------------------------------------------------------------------------
# d2data 用的是「游戏内部名」，与官方显示名不同。必须映射，否则英文显示名
# 玩家对不上（如内部名 McAuley's Folly 实为官方 Sander's Folly 山德的愚行）。
# ---------------------------------------------------------------------------
SET_ALIAS = {
    "Angelical Raiment": "Angelic Raiment",
    "Berserker's Garb": "Berserker's Arsenal",
    "Naj's Ancient Set": "Naj's Ancient Vestige",
    "McAuley's Folly": "Sander's Folly",
}
PART_ALIAS = {
    "Aldur's Gauntlet": "Aldur's Rhythm",
    "Spiritual Custodian": "Dark Adherent",
    "Tal Rasha's Fire-Spun Cloth": "Tal Rasha's Fine-Spun Cloth",
    "Tal Rasha's Howling Wind": "Tal Rasha's Guardianship",
    "Haemosu's Adament": "Haemosu's Adamant",
    "Heaven's Taebaek": "Taebaek's Glory",
    "Hwanin's Seal": "Hwanin's Blessing",
    "Wihtstan's Guard": "Whitstan's Guard",
    "Cow King's Hoofs": "Cow King's Hooves",
    "Griswolds's Redemption": "Griswold's Redemption",
    "McAuley's Paragon": "Sander's Paragon",
    "McAuley's Riprap": "Sander's Riprap",
    "McAuley's Superstition": "Sander's Superstition",
    "McAuley's Taboo": "Sander's Taboo",
}
# d2data 底材名的拼写/转义偏差 → 官方底材名
BASE_ALIAS = {
    "2-Handed Sword": "Two-Handed Sword",
    "AncientArmor": "Ancient Armor",
    "Balista": "Ballista",
    "Battle Guantlets": "Battle Gauntlets",
    "Bracers": "Heavy Bracers",
    "CedarBow": "Cedar Bow",
    "Espadon": "Espandon",
    "Hard Leather": "Hard Leather Armor",
    "Heirophant Trophy": "Hierophant Trophy",
    "Hunter\\92s Bow": "Hunter's Bow",
    "Jo Stalf": "Jo Staff",
    "Kriss": "Kris",
    "Saber": "Sabre",
    "Stilleto": "Stiletto",
    "Tresllised Armor": "Trellised Armor",
    "succubae skull": "Succubus Skull",
    "flying axe": "Francisca",
    "winged axe": "Francisca",
}
# 官方表没有的通用/新增底材（RotW 术士典籍等）手工补
BASE_EXTRA = {
    "Amulet": "项链", "amulet": "项链", "Ring": "戒指", "ring": "戒指",
    "jewel": "珠宝", "Jewel": "珠宝", "charm": "护符", "Gloves": "手套",
    "Greaves": "护胫", "Girdle": "束带", "Hammer": "战锤", "Staff": "法杖",
    "Leather Boots": "皮靴", "Plate Boots": "铠甲靴", "Light Plate Boots": "轻铠甲靴",
    "Long Siege Bow": "长攻城弓", "Ornate Armor": "华丽战甲",
    "Occult Codex": "神秘法典", "occult tome": "神秘典籍",
    "blasphemous grimoire": "亵渎魔典", "blasphemous compendium": "亵渎汇编",
    "burnt text": "焚毁的典籍", "mithril point": "秘银尖刀",
}

uni_raw = load(os.path.join(DD, 'uniqueitems.json'))
rw_raw = load(os.path.join(DD, 'runes.json'))
sets_raw = load(os.path.join(DD, 'sets.json'))
setitems_raw = load(os.path.join(DD, 'setitems.json'))
tk_uni = load(os.path.join(TK, 'uniques.json'))
tk_rw = load(os.path.join(TK, 'runewords.json'))
tk_sets = load(os.path.join(TK, 'sets.json'))
tk_sets_en = load(os.path.join(TK, 'sets_en.json'))

# ---------------------------------------------------------------------------
# 译名来源合并
# ---------------------------------------------------------------------------
EN2ZH = {}
# ① 官方译名最先放入（setdefault 保证后来源不覆盖它）
for _en, _zh in OFF_SET.items():
    EN2ZH.setdefault(_en, _zh)
for _en, _zh in OFF_PART.items():
    EN2ZH.setdefault(_en, _zh)
for _en, _zh in OFF_UNI.items():
    EN2ZH.setdefault(_en, _zh)
# d2data 内部名也要能查到官方中文（显示名会换成官方名，但兜底查询仍需要）
for _d2, _off in list(SET_ALIAS.items()) + list(PART_ALIAS.items()) + list(MANUAL_ALIAS.items()):
    if _off in EN2ZH:
        EN2ZH.setdefault(_d2, EN2ZH[_off])
# ② 再合并 tracker / 其他来源（繁体→简体）
for x in tk_uni:
    EN2ZH.setdefault(x['en'], s2s(x['zh']))
for k, v in tk_rw.items():
    EN2ZH.setdefault(k, s2s(v['中文名']))
for k, v in tk_sets.items():
    EN2ZH.setdefault(k, s2s(v['chinese_name']))
    for it in v.get('items', []):
        EN2ZH.setdefault(it['name'], s2s(it['name_zh']))

# 网易 wiki：底材英文 → 中文暗金（仅用于「暗金名与底材名相同」的条目）
# 可选数据源：抓取产物，不入库，缺失时自动跳过
WK = load_opt(os.path.join(HERE, 'wiki_zh_by_base.json'))

# shitieshou 国服译名（可选）
_ss = {}
if os.path.exists(os.path.join(HERE, 'ss.html')):
    _t = html.unescape(open(os.path.join(HERE, 'ss.html'), encoding='utf-8', errors='ignore').read())
    _txt = re.sub(r'<[^>]+>', '', _t)
    for m in re.finditer(r'\[([^\]\n]{2,20})\]\s*\([^)\n]*\)\s*([A-Z][A-Za-z\'\-\.\s]{2,45})', _txt):
        z, en = m.group(1).strip(), m.group(2).strip()
        if en and not z.startswith('i '):
            _ss[en] = z
for k, v in _ss.items():
    EN2ZH.setdefault(k, v)

# 人工核对补齐（经 WebSearch/WebFetch 核对国服译名）
MANUAL_UNI = {
 "Mindrend":"心灵之刃","Fechmars Axe":"费屈玛之斧","The Chieftan":"族长","The Humongous":"巨大无比",
 "Iros Torch":"衣洛的火炬","Maelstromwrath":"漩涡","Umes Lament":"乌米的恸哭","Bonesob":"碎骨",
 "Rixots Keen":"瑞克撒特的挽歌","Krintizs Skewer":"格林提斯的肉叉","Griswolds Edge":"格瑞斯华尔德的锐利",
 "Culwens Point":"库尔温的尖端","Kinemils Awl":"金麦尔的锥子","Irices Shard":"艾里斯的碎片",
 "Dimoaks Hew":"迪马克之劈砍","Lazarus Spire":"拉撒罗斯之螺旋","Rimeraven":"时光之鸦",
 "Piercerib":"穿刺之肋","Pullspite":"复仇之钩","Doomspittle":"毁灭之唾",
 "Blinkbats Form":"闪蝠之形","Venomsward":"毒液护符","Victors Silk":"胜利者之丝绸",
 "Lenyms Cord":"雷尼摩绳索","Amulet of the Viper":"蝮蛇护符","Staff of Kings":"国王之杖",
 "Horadric Staff":"赫拉迪克之杖","Hell Forge Hammer":"地狱熔炉之锤","Pompe's Wrath":"庞贝之怒",
 "The Minataur":"牛头怪","The Atlantian":"亚特兰提斯","Skullcollector":"骷髅收集者",
 "Whichwild String":"狂野之弦","Godstrike Arch":"神击之弓","Pus Spiter":"脓毒喷吐",
 "Skin of the Flayerd One":"剥皮者之皮","Ironpelt":"铁毛","Spiritforge":"灵魂熔炉",
 "Que-Hegan's Wisdon":"魁黑刚的智慧","Mosers Blessed Circle":"摩西的祝福之环",
 "Kerke's Sanctuary":"克尔的圣所","Radimant's Sphere":"罗迪门特的球体","Lavagout":"熔岩角羊",
 "Wartraveler":"战争旅者","Gorerider":"蚀肉骑士","Thudergod's Vigor":"雷神之力",
 "Bul Katho's Wedding Band":"布尔凯索之戒","Cutthroat1":"巴特克的猛击","Djinnslayer":"魔灵杀手",
 "Gutsiphon":"内脏吸管","Razoredge":"刀锋边缘","Gore Ripper":"血肉撕裂者","Demonlimb":"恶魔残肢",
 "Steelshade":"钢之暗影","Deaths's Web":"死亡之网","Zakarum's Salvation":"撒卡兰姆的救赎",
 "Odium":"憎恶","Jadetalon":"碧玉爪","Shadowdancer":"暗影舞者","Cerebus":"地狱三头犬",
 "Souldrain":"汲魂者","Runemaster":"符文大师","Deathcleaver":"死亡之刀","Larzuk's Champion":"拉苏克的勇士",
 "Wisp":"鬼火","Spiritkeeper":"灵魂看守者","Darkforge Spawn":"魔力肇生","Bloodraven's Charge":"血鸦的袭击",
 "Shadowkiller":"影杀者","Giantmaimer":"巨人杀手","Steelpillar":"铁柱","Darkfear":"黑暗恐惧",
 "Steel Carapice":"钢铁甲胄","Nethercrow":"冥鸦","Fathom":"死亡深度","Warriv's Warder":"瓦瑞夫的守护",
 "Eschuta's temper":"艾丝屈塔的脾气","Merman's Speed":"鱼人之力","Verdugo's Hearty Cord":"维尔登戈的强韧绳索",
 "Sigurd's Staunch":"西格urd的坚定","Sigurd's Staunch":"西古德之固","Giantskull":"巨骷髅",
 "Ironward":"铁卫","Earthshifter":"大地撼动者","Wraithflight":"幽魂飞行","The Reedeemer":"救赎者",
 "Headhunter's Glory":"猎头者的荣耀","Ars Al'Diablolos":"迪亚波罗斯邪术","Ars Tor'Baalos":"巴洛斯邪术",
 "Ars Dul'Mephistos":"墨菲斯托斯邪术","Measured Wrath":"有度之怒","Dreadfang":"惧牙",
 "Wraithstep":"幽魂步","Bloodpact Shard":"血契碎片","Sling":"投石索","Opalvein":"蛋白石脉",
 "Entropy Locket":"熵之坠饰","Gheed's Wager":"基德的赌注","Unique Warlock Helm":"术士专属头盔",
 "Defender's Bile":"防御者之胆","Guardian's Thunder":"守护者之雷","Protector's Frost":"保护者之霜",
 "Defender's Fire":"防御者之火","Protector's Stone":"保护者之石","Guardian's Light":"守护者之光",
 "PreCrafted Cold Rupture":"潜伏的冰冷迸裂","Crafted Cold Rupture":"冰冷的迸裂",
 "PreCrafted Flame Rift":"潜伏的火焰裂隙","Crafted Flame Rift":"火焰裂隙",
 "PreCrafted Crack of the Heavens":"潜伏的天堂之裂","Crafted Crack of the Heavens":"天堂之裂",
 "PreCrafted Rotting Fissure":"潜伏的腐朽裂隙","Crafted Rotting Fissure":"腐朽裂隙",
 "PreCrafted Bone Break":"潜伏的断骨","Crafted Bone Break":"断骨",
 "PreCrafted Black Cleft":"潜伏的黑色裂口","Crafted Black Cleft":"黑色裂口",
}
# ⚠️ 必须用 setdefault：官方译名（OFF_*）在前面已放入，这些手工表只是补缺口。
# 早先用 `EN2ZH[k] = v` / `EN2ZH.update(...)` 直接覆盖，把官方译名顶掉了
# （如 Horazon's Splendor 被写成「霍拉森之荣光」，官方是「赫拉森的辉煌」）。
for k, v in MANUAL_UNI.items():
    EN2ZH.setdefault(k, v)

# 符文之语缺口
MANUAL_RW = {
 "Ancients' Pledge":"远古誓约","Authority":"权威","Coven":"契约",
 "Hustle (armor)":"匆忙(甲)","Hustle (weapon)":"匆忙(武器)","King's Grace":"国王恩典",
 "Ritual":"仪式","Vigilance":"警觉","Void":"虚空",
}
for k, v in MANUAL_RW.items():
    EN2ZH.setdefault(k, v)

# 套装缺口：官方表未收录的才需要（Warlord's Glory 已整组过滤，不需要译名）
MANUAL_SETS = {
 "Angelical Raiment": "Angelic Raiment",   # d2data 内部名，中文在官方表里
 "Berserker's Garb": "Berserker's Arsenal",
 "Naj's Ancient Set": "Naj's Ancient Vestige",
 "McAuley's Folly": "Sander's Folly",
}
for k, v in MANUAL_SETS.items():
    if v in EN2ZH:
        EN2ZH.setdefault(k, EN2ZH[v])

# ---------------------------------------------------------------------------
# 属性代码 → 中文（129 个）
# ---------------------------------------------------------------------------
PROP_ZH = {
 'ac':'防御', 'ac%':'增强防御', 'ac-miss':'远程防御', 'ac/lvl':'每级防御',
 'all-stats':'全属性', 'allskills':'全技能等级', 'att':'准确率', 'att%':'增强准确率',
 'att-demon':'对恶魔伤害', 'att-skill':'技能准确率', 'att-undead':'对不死伤害',
 'aura':'光环', 'balance2':'格挡率', 'balance3':'格挡率',
 'bar':'定身(打断)', 'block':'格挡', 'block2':'格挡',
 'cast1':'施法速度', 'cast2':'施法速度', 'cast3':'施法速度',
 'charge-noconsume':'不消耗充能', 'charged':'充能次数', 'cheap':'低需求', 'crush':'压碎',
 'deadly':'致命一击', 'deadly/lvl':'每级致命一击', 'death-skill':'击杀时施放',
 'demon-heal':'恶魔治疗', 'dex':'敏捷', 'dmg':'伤害', 'dmg%':'增强伤害',
 'dmg-ac':'无视防御', 'dmg-cold':'冰伤害', 'dmg-dem/lvl':'每级对恶魔伤害',
 'dmg-demon':'对恶魔伤害', 'dmg-elem':'元素伤害', 'dmg-fire':'火伤害',
 'dmg-ltng':'电伤害', 'dmg-mag':'魔法伤害', 'dmg-max':'最大伤害', 'dmg-min':'最小伤害',
 'dmg-pois':'毒伤害', 'dmg-to-mana':'偷取法力', 'dmg-undead':'对不死伤害',
 'ethereal':'无形', 'explosivearrow':'爆炸箭', 'extra-cold':'冰冷', 'extra-fire':'火焰',
 'extra-ltng':'闪电', 'extra-mag':'魔法', 'extra-pois':'毒素',
 'fireskill':'火焰技能等级', 'freeze':'冻结', 'gethit-skill':'受击时施放',
 'gold%':'金币获取', 'gold%/lvl':'每级金币获取', 'half-freeze':'半冻结',
 'heal-kill':'击杀回复生命', 'hit-skill':'命中时施放', 'hp':'生命', 'hp%':'生命加成',
 'hp/lvl':'每级生命', 'ignore-ac':'无视目标防御', 'indestruct':'无法破坏',
 'kill-skill':'击杀时施放', 'knock':'击退', 'levelup-skill':'升级时施放',
 'lifesteal':'生命偷取', 'light':'光源半径', 'mag%':'魔法吸收', 'mag%/lvl':'每级魔法吸收',
 'mana':'法力', 'mana%':'法力加成', 'mana-kill':'击杀回复法力', 'mana/lvl':'每级法力',
 'manasteal':'法力偷取', 'move2':'移动速度', 'move3':'跑步速度',
 'nofreeze':'无法冰冻', 'noheal':'无法治疗', 'openwounds':'撕裂伤口',
 'oskill':'指定技能等级', 'pierce':'穿透', 'pierce-cold':'冰穿透',
 'pierce-fire':'火穿透', 'pierce-ltng':'电穿透', 'pierce-pois':'毒穿透',
 'reanimate':'复活怪物', 'red-dmg':'伤害减少', 'red-dmg%':'伤害减免',
 'red-mag':'魔法伤害减少', 'reduce-ac':'目标防御降低', 'regen':'生命回复',
 'regen-mana':'法力回复', 'rep-dur':'自动回复耐久', 'res-all':'全抗性',
 'res-cold':'冰抗', 'res-fire':'火抗', 'res-ltng':'电抗', 'res-ltng-max':'最大电抗',
 'res-pois':'毒抗', 'res-pois-len':'毒素持续', 'rip':'撕裂',
 'skill':'技能等级', 'skilltab':'技能等级', 'slow':'减速', 'stam':'耐力',
 'stamdrain':'耐力消耗', 'str':'力量', 'str/lvl':'每级力量', 'stupidity':'眩晕',
 'swing1':'攻击速度', 'swing2':'攻击速度', 'swing3':'攻击速度',
 'vit':'体力', 'vit/lvl':'每级体力', 'war':'武器格挡',
 'abs-cold%':'冰冷吸收', 'abs-fire':'火焰吸收', 'abs-fire%':'火焰吸收',
 'abs-ltng%':'闪电吸收', 'abs-mag':'魔法吸收',
 'ama':'亚马逊技能等级', 'ass':'刺客技能等级', 'dru':'德鲁伊技能等级',
 'nec':'亡灵法师技能等级', 'pal':'圣骑士技能等级', 'sor':'法师技能等级',
}
CLASS_PROP = {'ama':'Amazon','ass':'Assassin','dru':'Druid','nec':'Necromancer',
              'pal':'Paladin','sor':'Sorceress'}

def fmt_prop(code, mn, mx, param=None):
    """返回中文属性描述，如「+2 全技能等级」「+750~775 防御」。"""
    if mn > mx:
        mn, mx = mx, mn
    if code == 'oskill':
        return '%s 技能等级 +%d' % (param or '指定', mn)
    if code in ('skilltab', 'skill'):
        return '%s技能等级 +%d~%d' % (param, mn, mx) if param else '技能等级 +%d~%d' % (mn, mx)
    if code in CLASS_PROP:
        return '%s 技能等级 +%d~%d' % (CLASS_PROP[code], mn, mx)
    if code == 'aura':
        return '%s 光环（等级 %d）' % (param or '', mn) if param else '光环等级 +%d' % mn
    if code == 'charged':
        return '%s 充能 %d 次' % (param or '', mn) if param else '充能次数 +%d' % mn
    if code in ('hit-skill', 'gethit-skill', 'kill-skill', 'death-skill', 'levelup-skill'):
        base = {'hit-skill': '命中时施放', 'gethit-skill': '受击时施放',
                'kill-skill': '击杀时施放', 'death-skill': '死亡时施放',
                'levelup-skill': '升级时施放'}[code]
        if isinstance(param, str) and param:
            return '%s %s（%d 级）' % (base, param, mn)
        return '%s %d 级技能' % (base, mn)
    base = PROP_ZH.get(code)
    if not base:
        return None
    if mn == mx:
        body = '%s +%d' % (base, mn)
    else:
        body = '%s +%d~%d' % (base, mn, mx)
    if code.endswith('/lvl'):
        body += '（按等级）'
    return body

def props_of(obj, pre=None):
    """抽取属性描述列表。两种字段命名：
       - pre='prop'   → prop1 / min1 / max1 / param1（独特道具、套装部件）
       - pre='T1Code' → T1Code1 / T1Min1 / T1Max1 / T1Param1（符文之语）
    """
    out = []
    if pre is None:
        pat = re.compile(r'^prop(\d+)$')
        code_f = lambda i: 'prop' + i
        min_f, max_f, par_f = (lambda i: 'min' + i), (lambda i: 'max' + i), (lambda i: 'param' + i)
    else:
        pat = re.compile(r'^' + re.escape(pre) + r'(\d+)$')
        tail = pre[:-4] if pre.endswith('Code') else pre
        code_f = lambda i: pre + i
        min_f = lambda i: tail + 'Min' + i
        max_f = lambda i: tail + 'Max' + i
        par_f = lambda i: tail + 'Param' + i
    for k in sorted(obj.keys()):
        m = pat.match(k)
        if not m:
            continue
        i = m.group(1)
        code = obj.get(code_f(i))
        mn, mx, par = obj.get(min_f(i)), obj.get(max_f(i)), obj.get(par_f(i))
        if code is None or mn is None:
            continue
        d = fmt_prop(code, int(mn), int(mx if mx is not None else mn), par)
        if d:
            out.append(d)
    return out

# ---------------------------------------------------------------------------
# 部位 / 类型映射
# ---------------------------------------------------------------------------
SLOT_ZH = {}
_slot_tbl = [
 # (code, zh)
 ('hax','手斧'),('axe','斧'),('2hand','双手斧'),('swrd','剑'),('2hsword','双手剑'),
 ('club','棍棒'),('mace','钉头锤'),('flail','连枷'),('hammer','战锤'),('maul','巨槌'),
 ('sword','弯刀'),('spear','长矛'),('lance','长柄'),('jsp','刺枪'),('wsp','爪'),
 ('xbow','弩'),('bow','弓'),('sorc','法杖'),('staff','法杖'),('staf','法杖'),
 ('wand','魔杖'),('orb','宝珠'),('shld','盾'),('ashd','盾牌'),('bkld','大盾'),
 ('helm','头盔'),('cap','帽子'),('circ','头环'),('hood','兜帽'),('mask','面具'),
 ('helm','头盔'),('glov','手套'),('boot','靴'),('belt','腰带'),('amul','项链'),
 ('ring','戒指'),('tors','铠甲'),('brac','护腕'),('chest','铠甲'),('shad','骨盾'),
 ('pell','灰狼头盔'),('nef','护身符'), ('charms','小护符'),('gem','宝石'),('jewel','珠宝'),
]
for c, z in _slot_tbl:
    SLOT_ZH.setdefault(c, z)

# ---------------------------------------------------------------------------
# 部位归类：基于 items.json 的 type 字段（比 uniqueitems 的 code 精确）
# ---------------------------------------------------------------------------
TYPE_MAP = {
    'tors': ('armor', '盔甲'), 'swor': ('swords', '剑'), 'axe': ('axes', '斧'),
    'helm': ('helms', '头盔'), 'shie': ('shields', '盾牌'), 'bow': ('bows', '弓'),
    'pole': ('polearms', '长柄武器'), 'staf': ('staves', '法杖'), 'boot': ('boots', '靴子'),
    'belt': ('belts', '腰带'), 'amul': ('amulets', '项链'), 'spea': ('spears', '长矛'),
    'glov': ('gloves', '手套'), 'lcha': ('charms', '小护符'), 'hamm': ('melee', '钝器'),
    'knif': ('daggers', '匕首'), 'mace': ('melee', '钝器'), 'ring': ('rings', '戒指'),
    'wand': ('wands', '魔杖'), 'xbow': ('crossbows', '弩'), 'scep': ('scepters', '权杖'),
    'jewl': ('jewels', '珠宝'), 'club': ('melee', '钝器'), 'cjwl': ('jewels', '巨型珠宝'),
    'csch': ('charms', '破免护符'), 'phlm': ('helms', '盔帽'), 'h2h': ('claws', '爪'),
    'h2h2': ('claws', '利爪'), 'pelt': ('helms', '兽首头盔'), 'grim': ('tomes', '典籍'),
    'head': ('shields', '战利品'), 'orb': ('orbs', '宝珠'), 'ashd': ('shields', '圣骑士盾'),
    'jave': ('javelins', '标枪'), 'ajav': ('javelins', '亚马逊标枪'),
    'abow': ('bows', '亚马逊弓'), 'aspe': ('spears', '亚马逊长矛'), 'tkni': ('claws', '符文爪'),
    'circ': ('helms', '头环'), 'scha': ('shields', '圣骑士小盾'), 'mcha': ('charms', '大型护符'),
}

def slot_group(code, item_name='', item_type=''):
    """优先用 items.json 的 type 精确判定，退化到 code / 底材名关键字。"""
    if item_type and item_type in TYPE_MAP:
        return TYPE_MAP[item_type]
    c = (code or '').lower()
    n = (item_name or '').lower()
    for t, g in TYPE_MAP.items():
        if c == t:
            return g
    if not n and code and code in TYPE_MAP:
        return TYPE_MAP[code]
    # d2data 有拼写错误（如 Battle Guantlets）与少量缺失底材，手工补关键字
    EXTRA = [
        ('guantlet', 'gloves', '手套'), ('bracer', 'gloves', '护腕'),
        ('gauntlet', 'gloves', '手套'), ('succubae skull', 'shields', '女妖之骨'),
        ('bloodlord skull', 'shields', '血王之骨'), ('skull', 'shields', '骷髅'),
        ('mithril point', 'spears', '秘银长矛'), ('francisca', 'axes', 'Francisca 斧'),
        ('espadon', 'swords', '大剑'), ('balista', 'crossbows', '弩炮'),
        ('jo stalf', 'staves', '乔木棍'), ('kris', 'daggers', '克里刀'),
        ('hard leather', 'armor', '硬皮甲'), ('leather', 'armor', '皮甲'),
        ('tome', 'tomes', '典籍'), ('codex', 'tomes', '典籍'), ('compendium', 'tomes', '典籍'),
        ('hammer', 'melee', '锤'), ('maul', 'melee', '巨槌'), ('mace', 'melee', '钉头锤'),
        ('club', 'melee', '棍棒'), ('flail', 'melee', '连枷'), ('sledge', 'melee', '钉头锤'),
    ]
    for key, g, gl in EXTRA:
        if key in n:
            return g, gl
    if 'ring' in n: return 'rings', '戒指'
    if 'amulet' in n: return 'amulets', '项链'
    if 'boot' in n or 'greave' in n: return 'boots', '靴子'
    if 'glove' in n or 'gauntlet' in n or 'mitten' in n: return 'gloves', '手套'
    if 'shield' in n or 'buckler' in n or 'kite' in n or 'targe' in n: return 'shields', '盾牌'
    if 'sash' in n or 'belt' in n or 'girdle' in n: return 'belts', '腰带'
    if 'helm' in n or 'hood' in n or 'mask' in n or 'cap' in n or 'crown' in n: return 'helms', '头盔'
    if 'javelin' in n: return 'javelins', '标枪'
    if 'spear' in n or 'pike' in n: return 'spears', '长矛'
    if 'claw' in n or 'talon' in n or 'cesta' in n: return 'claws', '爪'
    if 'orb' in n or 'sphere' in n or 'globe' in n: return 'orbs', '宝珠'
    if 'wand' in n: return 'wands', '魔杖'
    if 'staff' in n or 'stave' in n or 'battle staff' in n: return 'staves', '法杖'
    if 'bow' in n: return 'bows', '弓'
    if 'crossbow' in n: return 'crossbows', '弩'
    if 'sword' in n or 'blade' in n or 'dirk' in n: return 'swords', '剑'
    if 'axe' in n or 'cleaver' in n or 'axe' in n: return 'axes', '斧'
    if 'armor' in n or 'armour' in n or 'plate' in n or 'mail' in n or 'hide' in n or 'shell' in n:
        return 'armor', '盔甲'
    if 'jewel' in n: return 'jewels', '珠宝'
    if 'charm' in n: return 'charms', '护符'
    if 'scepter' in n: return 'scepters', '权杖'
    if 'polearm' in n or 'scythe' in n or 'bill' in n or 'voulge' in n: return 'polearms', '长柄武器'
    return 'misc', '其他'

# ---------------------------------------------------------------------------
# 底材英文 → 中文译名（国服简体，来自网易 wiki + 人工核对）
# 搜索需要中文底材（玩家习惯搜"军帽"而不是 Shako），所以这里必须覆盖到常用底材。
# ---------------------------------------------------------------------------
BASE_ZH = {
 # 头盔
 'Cap':'帽子','Skull Cap':'骷髅帽','Helm':'头盔','Full Helm':'高级头盔','Great Helm':'巨头盔',
 'Crown':'头冠','Circlet':'头环','Coronet':'冠冕','Diadem':'权冠','Tiara':'三重冠',
 'Bone Helm':'骷髅头盔','Casque':'无颊头盔','Visored Cap':'护面帽','Spiked Helm':'尖钉头盔',
 'Armet':'头盔','Basinet':'BASINET 头盔','Armet':'头盔','Fur Cap':'毛皮帽','Bone Visage':'骨面盔',
 'Deicide Cap':'弑神帽','Dream Visor':'梦境面罩','Gargoyle Face':'石像鬼面','Grim Visor':'冷酷面罩',
 'Hunter Visor':'猎人面罩','Rage Visor':'狂怒面罩','Royal Circlet':'皇家头环','Diadem':'权冠',
 'Assault Helmet':'突击盔','Avenger Guard':'复仇者面甲','Carnage Helm':'屠杀头盔',
 'Conqueror Crown':'征服者皇冠面甲','Destroyer Helm':'毁灭者头盔','Fanged Helm':'尖牙盔',
 'Sallet':'盔帽','Visored Cap':'护面帽','Shamaness Helmet':'萨满头盔','Fury Visor':'暴怒面甲',
 # 盔甲
 'Plate Mail':'铠甲','Full Plate Mail':'全身板甲','Ring Mail':'环甲','Chain Mail':'锁子甲',
 'Splint Mail':'夹克铠甲','Gothic Plate':'哥德铠甲','Sacred Armor':'神圣盔甲',
 'Ancient Armor':'古代盔甲','Leather Armor':'皮甲','Demonhide Armor':'恶魔皮甲',
 'Dusk Shroud':'灰暮寿衣','Shroud':'寿衣','Wyrmhide':'古龙皮','Scarab Husk':'圣甲虫壳',
 'Wire Fleece':'羊毛皮甲','Diamond Mail':'钻石甲','Loricated Mail':'甲壳铠鳞甲',
 'Great Hauberk':'巨型鳞甲','Boneweave':'骸骨链甲','Balrog Skin':'炎魔皮','Archon Plate':'执政官铠甲',
 'Kraken Shell':'海妖壳甲','Hellforge Plate':'地狱煅甲','Lacquered Plate':'漆甲',
 'Shadow Plate':'阴影铠甲','Bloodskin':'血皮','Umberlay':'棕榈皮',' Russet Armor':'赤褐皮甲',
 # 盾牌
 'Shield':'盾','Goblin Shield':'哥布林盾','Bone Shield':'骨盾','Wooden Shield':'木盾',
 'Buckler':'小盾牌','Sword Guard':'剑盾','Knuckles':'指节套','Targe':'圆盾',
 'Bracteate':'装饰圆盾','Bronze Targes':'青铜圆盾','Kite Shield':'鸢盾','Mace Shield':'钉头盾',
 'Defender':'防御者盾','Round Shield':'圆盾','Demon Skin Shield':'恶魔皮盾','Curved Shield':'弧形盾',
 'Skull Shield':'骷髅盾','Gothic Shield':'哥德盾','Crown Shield':'皇冠盾','Pavise':'大盾',
 'Tower Shield':'塔盾','Pavise Shield':'大盾','Sacred Rondache':'神圣轻圆盾',
 'Bone Wall Shield':'骨墙盾','Cantor Trophy':'领唱者骨','Cantor Trophy Shield':'圣坛骨盾',
 'Hyperion Shield':'海伯利安盾','Gilded Shield':'饰金盾牌','Monarch':'君王的盾',
 'Sacred Targe':'神圣小圆盾','Ancient Shield':'古代之盾','Aegis':'神盾',
 # 手套
 'Gloves':'手套','Leather Gloves':'皮手套','Heavy Gloves':'重手套','Chain Gloves':'锁链手套',
 'Light Gauntlets':'轻护手','Gauntlets':'护手','Demonhide Gloves':'恶魔皮手套',
 'Sharkskin Gloves':'鲨皮手套','Heavy Bracers':'重护腕','Battle Gauntlets':'战斗护手',
 'War Gauntlets':'战护手','Bramble Mitts':'荆棘手套','Spellwrap':'法术缠绕',
 'Crusader Gauntlets':'十字军护手','Bone Gauntlets':'骸骨护手',
 # 靴子
 'Boots':'靴子','Light Boots':'轻型靴','Heavy Boots':'重靴','Chain Boots':'锁链靴',
 'Warpaint Boots':'疾行靴','Greaves':'护胫','Boneweave Boots':'骸骨长靴','Demonhide Boots':'恶魔皮靴',
 'Wyrmhide Boots':'古龙皮靴','Sharkskin Boots':'鲨皮靴','Mesh Armor Boots':'织网战靴',
 'Guardian Greaves':'守护者护胫','Sabaton':'钢制战靴','Scarabshell Boots':'圣甲虫壳靴',
 # 腰带
 'Belt':'腰带','Light Belt':'轻型腰带','Heavy Belt':'重型腰带','Plated Belt':'镶板腰带',
 'Demonhide Sash':'恶魔皮腰带','Sash':'饰带','Girdle':'束带','Whisp Guard':'鬼影护符带',
 'Vitality Sash':'活力腰带','Mystic Belt':'神秘腰带','Lycant Loop':'狼人环带',
 # 项链
 'Amulet':'项链','Tantalum Amulet':'钽项链','Angelic Pendant':'天使吊坠',
 'Cloak Pendant':'斗篷吊坠','Demon Pendant':'恶魔吊坠','Lapidary Locket':'宝石坠饰',
 # 戒指
 'Ring':'戒指','Band':'指环','Signet':'印章戒指','Ring':'戒指',
 # 宝箱类（战利品，不是装备）
 'Cloak':'披风','Gloves':'手套','Crown':'头冠',
}

BASE_TYPE = {}
def load_base_type():
    items = load(os.path.join(DD, 'items.json'))
    m = {}
    for k, v in items.items():
        n = v.get('name')
        if n:
            m[n] = v.get('type', '')
            # d2data 里部分底材是小写（armet / corona），统一补一份规范化 key
            m.setdefault(n.lower(), v.get('type', ''))
            m.setdefault(n.title(), v.get('type', ''))
            m.setdefault(n.capitalize(), v.get('type', ''))
    return m
BASE_TYPE = load_base_type()

# 网易 wiki 抓到的底材中文（122 条），按小写 key 合并
_wb = os.path.join(HERE, 'wiki_base_zh.json')
if os.path.exists(_wb):
    for _en, _zhs in load(_wb).items():
        _z = _zhs[0] if isinstance(_zhs, list) and _zhs else _zhs
        if _z:
            BASE_ZH.setdefault(_en, _z)
            BASE_ZH.setdefault(_en.lower(), _z)
            BASE_ZH.setdefault(_en.title(), _z)

def base_official(en, typ=''):
    """底材英文 → (官方英文名, 中文名)。

    优先级：官方表(d2r.world) > 手工补充 > 旧 wiki 表 > 按 type 的通称。
    d2data 的拼写偏差先过 BASE_ALIAS 归一化。
    """
    if not en:
        return '', ''
    off = BASE_ALIAS.get(en, en)
    for k in (off, off.lower(), off.title(), off.capitalize()):
        z = OFF_BASE.get(k)
        if z:
            return off, z
    for k in (en, off):
        z = BASE_EXTRA.get(k)
        if z:
            return off, z
    for k in (en, en.lower(), en.title(), en.capitalize()):
        z = BASE_ZH.get(k)
        if z:
            return off, z
    g = TYPE_MAP.get(typ)
    return off, (g[1] if g else '')

def base_zh(en, typ=''):
    """兼容旧调用：只取中文。"""
    return base_official(en, typ)[1]

# ---------------------------------------------------------------------------
# 符文之语
# ---------------------------------------------------------------------------
RUNE_IDX = {
 1:'El',2:'Eld',3:'Tir',4:'Nef',5:'Eth',6:'Ith',7:'Tal',8:'Ral',9:'Ort',10:'Thul',
 11:'Amn',12:'Sol',13:'Shael',14:'Dol',15:'Hel',16:'Io',17:'Lum',18:'Ko',19:'Fal',
 20:'Lem',21:'Pul',22:'Um',23:'Mal',24:'Ist',25:'Gul',26:'Vex',27:'Ohm',28:'Lo',
 29:'Sur',30:'Ber',31:'Jah',32:'Cham',33:'Zod',
}

def rune_seq(rw):
    """按 Rune1..RuneN 字段取符文顺序（保留重复，如 Last Wish 的 Jah 三个）。"""
    out = []
    for i in range(1, 8):
        code = rw.get('Rune%d' % i)
        if not code:
            break
        idx = int(code[1:])
        out.append(RUNE_IDX.get(idx, code))
    if out:
        return out
    # 回退：解析 *RunesUsed
    s = rw.get('*RunesUsed') or ''
    R = sorted(RUNE_IDX.values(), key=len, reverse=True)
    out, i = [], 0
    while i < len(s):
        for r in R:
            if s.startswith(r, i):
                out.append(r); i += len(r); break
        else:
            i += 1
    return out

def build_runewords():
    out = []
    for rw in rw_raw.values():
        if not rw.get('complete'):
            continue
        en = rw['*Rune Name']
        runes = rune_seq(rw)
        sockets = len(runes)
        itype = rw.get('itype1', '')
        # 底材：itype 映射
        base_map = {
          'tors':'铠甲', 'shld':'盾牌', 'bkld':'大盾', 'ashd':'圣骑士盾',
          'helm':'头盔', 'circ':'头环', 'weap':'武器', 'pole':'长柄武器',
          'swor':'剑', 'mace':'钝器', 'axe':'斧',
          'scep':'权杖', 'staf':'法杖', 'wand':'魔杖', 'club':'棍棒',
          'miss':'远程武器', 'mele':'近战武器', 'h2h':'双手近战武器',
          'grim':'连枷', 'knif':'匕首', 'pala':'长柄武器', 'thro':'投掷武器',
        }
        base = base_map.get(itype, itype)
        effects = props_of(rw, 'T1Code')
        out.append({
            'id': 'rw:' + en,
            'en': en,
            'zh': EN2ZH.get(en, en),
            'sockets': sockets,
            'runes': runes,
            'base': base,
            'base_raw': itype,
            'req': rw.get('lvl', 0) or 0,
            'effects': effects,
            # 天梯专属判定：d2data 用 firstLadderSeason/lastLadderSeason。
            # 有 lastLadderSeason = 已在该赛季后开放给非天梯（如 season14→15 转正）；
            # 只有 firstLadderSeason、没有 lastLadderSeason = 仍是天梯专属。
            # 另兼容旧字段名 'ladder only'。
            'ladder_only': bool(
                rw.get('firstLadderSeason') is not None
                and rw.get('lastLadderSeason') is None
            ) or bool(rw.get('ladder only') or rw.get('ladder_only')),
            'ladder_from': rw.get('firstLadderSeason'),
            'ladder_to': rw.get('lastLadderSeason'),
            'patch': rw.get('*Patch Release', ''),
        })
    out.sort(key=lambda x: (-x['sockets'], x['en']))
    return out

# ---------------------------------------------------------------------------
# 套装
# ---------------------------------------------------------------------------
def build_sets():
    # setitems 按 set 分组
    byset = {}
    for si in setitems_raw.values():
        # disableChronicle=1 = 游戏内标记「不计入图鉴」，实际无法掉落获取
        # （Warlord's Glory 整套 5 件都是），不能进收藏清单。
        if si.get('disableChronicle'):
            continue
        byset.setdefault(si.get('set'), []).append(si)
    out = []
    for s in sets_raw.values():
        en_raw = s['index']
        # d2data 内部名 → 官方显示名（McAuley's Folly → Sander's Folly 等）
        en = SET_ALIAS.get(en_raw, en_raw)
        items = byset.get(en_raw, [])
        if not items:
            continue                      # 全被过滤（不可获取套装）
        pieces = []
        for it in items:
            p_en = PART_ALIAS.get(it['index'], it['index'])
            _bt = BASE_TYPE.get(it.get('*ItemName', ''), '')
            grp, grpzh = slot_group(it.get('item'), it.get('*ItemName', ''), _bt)
            b_off, b_zh = base_official(it.get('*ItemName', ''), _bt)
            pieces.append({
                'en': p_en,
                'zh': EN2ZH.get(p_en, EN2ZH.get(it['index'], p_en)),
                'base': b_off,
                'base_zh': b_zh,
                'group': grp,
                'group_zh': grpzh,
                'req': it.get('lvl req', 0),
                'props': props_of(it),
            })
        # 套装 2/4/6 件效果
        bonus = []
        for i in range(1, 8):
            c = s.get('FCode%d' % i)
            mn = s.get('FMin%d' % i)
            mx = s.get('FMax%d' % i)
            par = s.get('FParam%d' % i)
            if not c or mn is None:
                continue
            if c == 'state':
                # fullsetgeneric 等：按件数计
                continue
            d = fmt_prop(c, int(mn), int(mx if mx is not None else mn), par)
            if d:
                bonus.append({'pieces': (2, 4, 6)[min(i - 1, 2)], 'text': d})
        # 2 件套（Part-a 类）
        pre = []
        for i, suf in enumerate(['', 'a', 'b', 'c', 'd']):
            c = s.get('PCode%d%s' % (i + 1, suf))
            mn = s.get('PMin%d%s' % (i + 1, suf))
            mx = s.get('PMax%d%s' % (i + 1, suf))
            par = s.get('PParam%d%s' % (i + 1, suf))
            if not c or mn is None:
                continue
            d = fmt_prop(c, int(mn), int(mx if mx is not None else mn), par)
            if d:
                pre.append(d)
        out.append({
            'id': 'set:' + en,
            'en': en,
            'zh': EN2ZH.get(en, en),
            'count': len(pieces),
            'req': max([p['req'] for p in pieces] or [0]),
            'pieces': pieces,
            'bonus2': pre,
            'bonus': bonus,
            'cls': s.get('UIClass', ''),
        })
    out.sort(key=lambda x: (-x['count'], x['en']))
    return out

# ---------------------------------------------------------------------------
# 独特道具
# ---------------------------------------------------------------------------
# 需要排除的非收藏条目（任务物品 / 内部占位 / 重复的 Crafted 变体另计）
SKIP_EXACT = {'Cutthroat1'}
SKIP_SUBSTR = ('PreCrafted', 'Crafted Black', 'Crafted Bone', 'Crafted Cold',
               'Crafted Crack', 'Crafted Flame', 'Crafted Rotting')

def build_uniques():
    out = []
    for u in uni_raw.values():
        if u.get('enabled', 1) != 1 or u.get('spawnable', 1) != 1:
            continue
        # disableChronicle=1 是游戏内标记的「不计入图鉴」条目（多为已被删除/替换的旧暗金，
        # d2data 里只剩空壳：无底材、无属性、无等级），不作为收藏目标。
        if u.get('disableChronicle'):
            continue
        en = u['index']
        # 任务物品只存在于任务流程里，无法收藏
        if en in TASK_ITEM_KEYS:
            continue
        base = u.get('*ItemName', '')
        code = u.get('code', '')
        _bt = BASE_TYPE.get(base, BASE_TYPE.get(code, ''))
        grp, grpzh = slot_group(code, base, _bt)
        # 显示名换成官方名（玩家认官方名；d2data 用的是内部代号）
        off_en = official_name(en)
        zh = EN2ZH.get(off_en) or EN2ZH.get(en)
        if not zh:
            c = WK.get(base, [])
            zh = c[0] if len(c) == 1 else off_en
        b_off, b_zh = base_official(base, _bt)
        props = props_of(u)
        out.append({
            'id': 'uni:' + off_en,
            'en': off_en,
            'zh': zh,
            'base': b_off,
            'base_zh': b_zh,
            'group': grp,
            'group_zh': grpzh,
            'req': u.get('lvl req', 0),
            'qlvl': u.get('lvl', 0),
            'eth': bool(u.get('ethereal')),
            'props': props[:6],
            'tier': u.get('lvl', 0) and ('elite' if u.get('lvl', 0) >= 60 else ('exceptional' if u.get('lvl', 0) >= 25 else 'normal')) or '',
        })
    out.sort(key=lambda x: (x['group_zh'], -x['req'], x['en']))
    return out

RWS = build_runewords()
SETS = build_sets()
UNIS = build_uniques()

# 只保留唯一收藏条目（去重 + 排除任务/内部物品）
def is_collectible(u):
    en = u['en']
    if en in SKIP_EXACT:
        return False
    for s in SKIP_SUBSTR:
        if en.startswith(s):
            return False
    return True

UNIQ_C = []
_seen = set()
for u in UNIS:
    if u['en'] in _seen:
        continue
    _seen.add(u['en'])
    UNIQ_C.append(u)

if __name__ == '__main__':
    print('runewords', len(RWS))
    print('sets', len(SETS), 'pieces', sum(len(s['pieces']) for s in SETS))
    print('uniques(all)', len(UNIQ_C))
    print('collectible', len([u for u in UNIQ_C if is_collectible(u)]))
    miss = [u['en'] for u in UNIQ_C if u['zh'] == u['en']]
    print('no-zh', len(miss), miss[:40])
    for r in RWS[:3]:
        print(r['en'], r['zh'], r['runes'], r['sockets'], r['base'], r['effects'][:3])
    for s in SETS[:2]:
        print(s['en'], s['zh'], s['count'], [p['zh'] for p in s['pieces']][:3])
# ---------------------------------------------------------------------------
# 输出 Python 数据模块
# ---------------------------------------------------------------------------
def pyrepr(o):
    if isinstance(o, str):
        return '"' + o.replace('\\', '\\\\').replace('"', '\\"') + '"'
    if isinstance(o, bool):
        return 'True' if o else 'False'
    if isinstance(o, (int, float)):
        return str(o)
    if isinstance(o, list):
        return '[' + ','.join(pyrepr(x) for x in o) + ']'
    if isinstance(o, dict):
        return '{' + ','.join('%s:%s' % (pyrepr(k), pyrepr(v)) for k, v in o.items()) + '}'
    raise TypeError(o)

def emit(path):
    rw_simple = []
    for r in RWS:
        rw_simple.append({
            'id': r['id'], 'en': r['en'], 'zh': r['zh'], 'sockets': r['sockets'],
            'runes': r['runes'], 'base': r['base'], 'effects': r['effects'],
            'ladder_only': r['ladder_only'],
        })

    # ---------------- 符文需求统计 ----------------
    # 集齐全部符文之语，每种符文要几个；并按孔数分档（低阶先凑）。
    RUNE_ALL = [
        ('El',1),('Eld',2),('Tir',3),('Nef',4),('Eth',5),('Ith',6),('Tal',7),('Ral',8),
        ('Ort',9),('Thul',10),('Amn',11),('Sol',12),('Shael',13),('Dol',14),('Hel',15),
        ('Io',16),('Lum',17),('Ko',18),('Fal',19),('Lem',20),('Pul',21),('Um',22),
        ('Mal',23),('Ist',24),('Gul',25),('Vex',26),('Ohm',27),('Lo',28),('Sur',29),
        ('Ber',30),('Jah',31),('Cham',32),('Zod',33),
    ]
    import collections as _co
    def _tally(seq):
        c = _co.Counter()
        for r in seq:
            for x in r['runes']:
                c[x] += 1
        return c
    # 全量
    total_cnt = _tally(RWS)
    # 非天梯（集齐常驻的那批）
    nonlad_cnt = _tally([r for r in RWS if not r['ladder_only']])
    # 按孔数分档
    tiers = []
    for sk in range(2, 7):
        g = [r for r in RWS if r['sockets'] == sk]
        gc = _tally(g)
        tiers.append({'sockets': sk, 'count': len(g), 'runes': dict(gc)})

    RUNE_NEED = []
    for name, idx in RUNE_ALL:
        RUNE_NEED.append({
            'name': name, 'idx': idx,
            'total': total_cnt.get(name, 0),
            'nonlad': nonlad_cnt.get(name, 0),
            'by_tier': [t['runes'].get(name, 0) for t in tiers],
        })

    set_simple = []
    for s in SETS:
        set_simple.append({
            'id': s['id'], 'en': s['en'], 'zh': s['zh'], 'count': s['count'],
            'req': s['req'],
            'pieces': [{'en': p['en'], 'zh': p['zh'], 'base': p['base'], 'base_zh': p['base_zh'],
                        'group_zh': p['group_zh'], 'req': p['req'], 'props': p['props']} for p in s['pieces']],
            'bonus2': s['bonus2'],
            'bonus': [{'pieces': b['pieces'], 'text': b['text']} for b in s['bonus']],
        })
    uni_simple = []
    for u in UNIQ_C:
        if not is_collectible(u):
            continue
        uni_simple.append({
            'id': u['id'], 'en': u['en'], 'zh': u['zh'], 'base': u['base'],
            'base_zh': u['base_zh'],
            'group': u['group'], 'group_zh': u['group_zh'], 'req': u['req'],
            'eth': u['eth'], 'props': u['props'][:5],
        })
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('"""收藏编年史数据（自动生成，勿手改）。\n\n')
        f.write('数据来源：blizzhackers/d2data @ Diablo II Resurrected patch 3.3\n')
        f.write('符文之语 %d 条 / 套装 %d 套（%d 件部件）/ 独特道具 %d 件\n"""\n' % (
            len(rw_simple), len(set_simple), sum(len(s['pieces']) for s in set_simple), len(uni_simple)))
        f.write('RUNEWORDS = ' + pyrepr(rw_simple) + '\n\n')
        f.write('# 符文需求统计：集齐全部符文之语每种符文要几个\n')
        f.write('RUNE_TIERS = ' + pyrepr([{'sockets': t['sockets'], 'count': t['count']} for t in tiers]) + '\n\n')
        f.write('RUNE_NEED = ' + pyrepr(RUNE_NEED) + '\n\n')
        f.write('SETS = ' + pyrepr(set_simple) + '\n\n')
        f.write('UNIQUES = ' + pyrepr(uni_simple) + '\n')
    print('written', path)
    print('  runewords', len(rw_simple), '| sets', len(set_simple),
          '(pieces %d)' % sum(len(s['pieces']) for s in set_simple), '| uniques', len(uni_simple))
