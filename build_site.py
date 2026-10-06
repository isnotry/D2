# -*- coding: utf-8 -*-
"""Generate a static, content-rich Diablo II: Resurrected guide site (v2, concatenation-based)."""
import os
import sys
import datetime

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, OUT)
os.makedirs(os.path.join(OUT, "css"), exist_ok=True)
os.makedirs(os.path.join(OUT, "js"), exist_ok=True)
os.makedirs(os.path.join(OUT, "classes"), exist_ok=True)
os.makedirs(os.path.join(OUT, "guides"), exist_ok=True)

# 收藏编年史数据（自动生成，见 tools_build_chronicle.py）
from d2_chronicle_data import RUNEWORDS, SETS, UNIQUES, RUNE_NEED, RUNE_TIERS

# ---------------------------------------------------------------------------
# 术语翻译表（大陆/国服版：中文为主，英文为辅）
# 键为英文原文，值为大陆版中文译名；渲染时统一翻转为「中文 英文」。
# ---------------------------------------------------------------------------
ZH_PAIRS = [
    # 流派昵称（放在通用技能前，保证长串优先匹配）
    ("Javazon", "标枪亚马逊"), ("Bowazon", "弓亚马逊"), ("Blizzard Sorceress", "暴风雪法师"),
    ("Lightning / Nova Sorceress", "闪电/新星法师"), ("Meteorb Sorceress", "火冰双修法师"),
    ("Summoner", "召唤流"), ("Poison Necromancer", "毒亡灵法师"), ("Bone Necromancer", "骨亡灵法师"),
    ("Hammerdin", "祝福之锤圣骑士"), ("Zealot", "热诚圣骑士"),
    ("FoH / Smiter", "天堂之拳/盾击圣骑士"), ("Whirlwind Barbarian", "旋风野蛮人"),
    ("Pitzerker", "寻物狂战"), ("Singer", "战吼野蛮人"), ("Wind Druid", "风德"), ("Fire Druid", "火德"),
    ("Werewolf Fury", "狼人狂怒"), ("Trapsin", "陷阱刺客"), ("Mosaic 武学刺客", "马赛克武学刺客"),
    # 亚马逊技能
    ("Lightning Fury", "闪电之怒"), ("Charged Strike", "充能一击"), ("Lightning Strike", "闪电打击"),
    ("Power Strike", "强力打击"), ("Poison Javelin", "毒枪"), ("Plague Javelin", "瘟疫标枪"),
    ("Freezing Arrow", "冰冻箭"), ("Cold Arrow", "冰箭"), ("Multishot", "多重箭"), ("Strafe", "扫射"),
    ("Guided Arrow", "导引箭"), ("Immolation Arrow", "爆裂箭"), ("Magic Arrow", "魔法箭"),
    ("Dodge", "躲避"), ("Evade", "回避"), ("Avoid", "闪避"), ("Critical Strike", "致命打击"),
    ("Penetration", "穿透"), ("Valkyrie", "瓦尔基里"), ("Decoy", "诱饵"), ("Slow Missiles", "慢速箭"),
    # 法师技能
    ("Frozen Orb", "冰封球"), ("Blizzard", "暴风雪"), ("Ice Blast", "冰风暴"), ("Glacial Spike", "冰尖柱"),
    ("Frozen Armor", "碎冰甲"), ("Cold Mastery", "冰冷支配"), ("Lightning", "闪电"), ("Chain Lightning", "闪电链"),
    ("Nova", "新星"), ("Static Field", "静态力场"), ("Lightning Mastery", "闪电支配"),
    ("Telekinesis", "心灵传动"), ("Teleport", "传送"), ("Fire Ball", "火球"), ("Meteor", "陨石"),
    ("Hydra", "九头蛇"), ("Enchant", "附魔"), ("Warmth", "温暖"), ("Fire Mastery", "火焰支配"),
    ("Fire Bolt", "火弹"), ("Ice Bolt", "冰弹"), ("Frost Nova", "霜之新星"),
    # 亡灵法师技能
    ("Raise Skeleton", "复活骷髅"), ("Skeleton Mastery", "骷髅掌握"), ("Clay Golem", "黏土石魔"),
    ("Iron Golem", "钢铁石魔"), ("Revive", "重生"), ("Summon Resist", "召唤抵抗"),
    ("Poison Dagger", "毒牙"), ("Poison Nova", "剧毒新星"), ("Bone Spear", "骨矛"), ("Bone Spirit", "骨魂"),
    ("Bone Prison", "骨牢"), ("Bone Wall", "骨墙"), ("Corpse Explosion", "尸体爆炸"), ("Teeth", "牙"),
    ("Amplify Damage", "伤害加深"), ("Decrepify", "衰老"), ("Dim Vision", "微暗灵视"),
    ("Lower Resist", "降低抵抗"), ("Iron Maiden", "钢铁处女"), ("Life Tap", "偷取生命"),
    ("Bone Armor", "白骨装甲"), ("Golem Mastery", "石魔掌握"),
    # 圣骑士技能
    ("Sacrifice", "牺牲"), ("Zeal", "热诚"), ("Smite", "盾击"), ("Charge", "冲锋"),
    ("Holy Shield", "神圣之盾"), ("Vengeance", "复仇"), ("Conversion", "转换"), ("Might", "力量"),
    ("Holy Fire", "神圣火焰"), ("Holy Frost", "神圣冰冻"), ("Holy Shock", "神圣冲击"),
    ("Fanaticism", "狂热"), ("Conviction", "信念"), ("Sanctuary", "庇护所"), ("Blessed Aim", "祝福瞄准"),
    ("Prayer", "祈祷"), ("Cleansing", "净化"), ("Meditation", "冥思"), ("Concentration", "专注"),
    ("Blessed Hammer", "祝福之锤"), ("Vigor", "活力"), ("Fist of the Heavens", "天堂之拳"),
    ("Redemption", "救赎"), ("Defiance", "防御"), ("Thorns", "刺针"), ("Holy Bolt", "神圣之箭"),
    ("Battle Orders", "战斗体制"), ("Shout", "呐喊"), ("Battle Command", "战斗指挥"),
    # 野蛮人技能
    ("Whirlwind", "旋风"), ("Frenzy", "狂乱"), ("Berserk", "狂暴"), ("Concentrate", "专注"),
    ("Double Throw", "双手投掷"), ("Throw", "投掷"), ("Leap", "跳跃"), ("Leap Attack", "跳跃攻击"),
    ("Iron Skin", "铁皮"), ("Natural Resistance", "自然抵抗"), ("Increased Speed", "加速"),
    ("Increased Stamina", "增加耐力"), ("Battle Cry", "战吼"), ("War Cry", "战争狂嚎"),
    ("Find Item", "寻物"), ("Taunt", "嘲讽"), ("Weapon Mastery", "武器精通"),
    # 德鲁伊技能
    ("Tornado", "龙卷风"), ("Hurricane", "飓风"), ("Cyclone Armor", "旋风甲"), ("Fissure", "裂缝"),
    ("Volcano", "火山"), ("Armageddon", "末日审判"), ("Firestorm", "火风暴"), ("Molten Boulder", "熔岩巨石"),
    ("Werewolf", "狼人"), ("Werebear", "熊人"), ("Fury", "狂怒"), ("Maul", "重殴"),
    ("Feral Rage", "野性狂暴"), ("Rabies", "狂犬病"), ("Shock Wave", "震波"), ("Lycanthropy", "变身体质"),
    ("Oak Sage", "橡木贤者"), ("Heart of Wolverine", "狼獾之心"), ("Spirit of Barbs", "荆棘灵"),
    ("Summon Grizzly", "灰熊"), ("Vines", "藤蔓"),
    # 刺客技能
    ("Lightning Sentry", "电哨"), ("Death Sentry", "死亡守卫"), ("Fire Sentry", "火哨"),
    ("Shock Web", "闪电陷阱"), ("Charged Bolt Sentry", "充能箭守卫"), ("Wake of Fire", "火焰守卫"),
    ("Inferno Sentry", "地狱火守卫"), ("Phoenix Strike", "凤凰击"), ("Claws of Thunder", "雷爪"),
    ("Blades of Ice", "冰刃"), ("Fists of Fire", "焰拳"), ("Tiger Strike", "猛虎击"),
    ("Cobra Strike", "眼镜蛇击"), ("Dragon Talon", "龙爪"), ("Dragon Claw", "龙拳"),
    ("Dragon Tail", "龙尾"), ("Dragon Flight", "龙跃"), ("Burst of Speed", "速度爆发"),
    ("Fade", "消退"), ("Cloak of Shadows", "魔影斗篷"), ("Mind Blast", "心灵爆震"),
    ("Venom", "毒素"), ("Weapon Block", "武器格挡"), ("Shadow Master", "影子大师"),
    ("Shadow Warrior", "影子战士"),
    # 补充技能（国服译名）
    ("Conversion", "转换"), ("Leap", "跳跃"), ("Leap Attack", "跳跃攻击"),
    ("Dragon Claw", "龙拳"), ("Dragon Tail", "龙尾"), ("Dragon Flight", "龙跃"),
    ("Twister", "旋风"),
    # 符文之语
    ("Mosaic", "马赛克"), ("Flickering Flame", "摇曳火焰"), ("Mist", "薄雾"), ("Obsession", "痴迷"),
    ("Plague", "瘟疫"), ("Pattern", "韵律"), ("Unbending Will", "不屈意志"), ("Wisdom", "智慧"),
    ("Bulwark", "壁垒"), ("Cure", "治愈"), ("Ground", "大地"), ("Hearth", "壁炉"),
    ("Temper", "锻造"), ("Hustle", "匆忙"), ("Metamorphosis", "蜕变"), ("Enigma", "谜团"),
    ("Infinity", "无限"), ("Spirit", "精神"), ("Heart of the Oak", "橡树之心"), ("Fortitude", "刚毅"),
    ("Call to Arms", "战争召唤"), ("Grief", "悲伤"), ("Chains of Honor", "荣耀之链"),
    ("Death's Web", "死亡之网"), ("Stealth", "潜行"), ("Ancient's Pledge", "远古誓约"),
    ("Lore", "学识"), ("Smoke", "烟雾"), ("Treachery", "背叛"), ("Spirit Monarch", "精神君主盾"),
    # 暗金/装备
    ("Titan's Revenge", "泰坦标枪"), ("Griffon's Eye", "格里芬之眼"), ("Mara's Kaleidoscope", "马拉"),
    ("Razortail", "剃刀尾"), ("SoJ", "乔丹之石"), ("Shako", "军帽"), ("Nightwing's Veil", "夜翼面纱"),
    ("Tal Rasha's", "塔拉夏"), ("Arachnid Mesh", "蜘蛛之网"), ("Magefist", "法师之拳"),
    ("Homunculus", "侏儒"), ("Peasant Crown", "农民皇冠"), ("Beast", "野兽"),
    ("Skin of Vipermagi", "蛇魔之皮"), ("Herald of Zakarum", "撒卡兰姆使者"),
    ("Guillaume's", "纪尧姆之颅"), ("String of Ears", "耳串"), ("Dracul's Grasp", "卓古拉之握"),
    ("Gore Rider", "蚀肉骑士"), ("Arreat's Face", "亚瑞特之脸"), ("Highlord's Wrath", "大君之怒"),
    ("Stormshield", "暴风之盾"), ("Ali Baba", "阿里巴巴"), ("Gull", "海鸥"), ("Goldwrap", "金色包袱"),
    ("Chance Guards", "运气守护"), ("War Traveler", "战争旅者"), ("Nagelring", "拿各之戒"),
    ("Jalal's Mane", "加洛之鬃"), ("Bartuc's", "巴图克"), ("Shadow Dancer", "暗影舞者"),
    ("Phoenix", "凤凰"), ("Skullder's", "斯凯林之愤怒"), ("Stealskull", "偷颅"),
    ("Andariel's Visage", "安达利尔的面容"), ("Windforce", "风之力"), ("Faith", "信心"),
    ("Crown of Ages", "年纪"), ("Trang-Oul's", "特朗奥"), ("Stone of Jordan", "乔丹之石"),
    # 地点/专有
    ("Terror Zones", "恐怖地带"), ("Ladder", "天梯"), ("Sunder Charm", "破免护符"),
    ("Sunder Charms", "破免护符"), ("Cold Sunder Charm", "冰破免护符"),
    ("Lightning Sunder Charm", "电破免护符"), ("Fire Sunder Charm", "火破免护符"),
    ("Poison Sunder Charm", "毒破免护符"), ("Physical Sunder", "物破免"), ("Magic Sunder", "魔破免"),
    ("The Pit", "彼特"), ("Chaos Sanctuary", "混沌避难所"), ("Ancient Tunnels", "远古通道"),
    ("Cows", "牛场"), ("Countess", "女伯爵"), ("Tristram", "崔斯特姆"), ("Mephisto", "墨菲斯托"),
    ("Diablo", "迪亚波罗"), ("Baal", "巴尔"), ("Andariel", "安达利尔"), ("Duriel", "都瑞尔"),
    ("Nihlathak", "尼拉塞克"), ("Uber", "超级"), ("Worldstone Chamber", "世界之石大殿"),
    ("Blood Moor", "血腥荒地"), ("Arcane Sanctuary", "神秘避难所"), ("Maggot Lair", "蛆虫巢穴"),
    ("Tombs", "墓穴"), ("Stony Field", "石头旷野"), ("Underground Passage", "地下通道"),
    ("Blood Raven", "血鸦"), ("Smith", "铁匠"), ("Hellfire Torch", "地狱火火炬"),
    ("Annihilus", "毁灭"), ("Token of Absolution", "赦罪令牌"),     ("Diablo Clone", "迪亚波罗克隆"),
    # 术士（2026「术士君临」新职业）技能/专有
    ("Chaos", "混沌"), ("Demon", "恶魔"), ("Eldritch", "邪术"),
    ("Goatmen", "羊头人"), ("Tainted", "污堕者"), ("Defiler", "污秽者"),
    ("Miasma", "瘴气"), ("Apocalypse", "天启"), ("Abyss", "深渊"),
    ("Echoing Strike", "回响打击"), ("Colossal Ancients", "巨型先祖"), ("Chronicle", "编年史"),
    # —— 2026-08-10 补充：修复全站纯英文术语（仅补源里纯英文者，源已「中文 英文」的树名不补以免重复）——
    # 术士（Warlock）专属与新增终局
    ("Reign of the Warlock", "术士君临"), ("Demon Warlock", "恶魔术士"), ("Demon Mastery", "恶魔精通"),
    ("Eldritch Warlock", "邪术术士"), ("Eldritch Mastery", "邪术精通"), ("Chaos Warlock", "混沌术士"),
    ("Chaos Mastery", "混沌精通"), ("Hex Weapon", "妖术武器"), ("Ethereal Duplicate", "虚幻分身"),
    ("Two-Handed Mastery", "双手精通"), ("Two-Handed", "双手"), ("Weapon Levitation", "武器浮空"),
    ("Entropy Mastery", "熵之精通"), ("Throw Weapon", "投掷武器"), ("Offhand", "副手"),
    ("Bind Single Demon", "绑定单体恶魔"), ("Defiler Bind Single Demon", "污秽者绑定单体恶魔"),
    ("Consume", "吞噬"), ("Goatmen Summon", "羊头人召唤"), ("Tainted Summon", "污堕者召唤"),
    ("Sword/Mace/Axe/ Polearm Mastery", "剑/锤/斧/长柄精通"), ("Polearm Mastery", "长柄精通"),
    ("Sword", "剑"), ("Mace", "锤"), ("Axe", "斧"),
    ("Loot Filter", "战利品筛选"), ("Hellfire", "地狱火"), ("Void", "虚空"),
    ("The Flame Rift", "烈焰裂隙"), ("The Cold Rupture", "寒冰裂断"),
    ("The Crack of the Heavens", "天穹裂隙"), ("The Bone Break", "碎骨之地"),
    ("The Black Cleft", "幽黑裂谷"), ("The Rotting Cairn", "腐臭石冢"), ("The Rotting Fissure", "腐臭裂隙"), ("The Rotting", "腐臭"),
    # —— 2026-09-30 补充：Patch 3.3 / 天梯第 15 赛季术语 ——
    ("Latent Sunder Charm", "潜伏破免护符"), ("Herald of Terror", "恐惧先驱"),
    ("Colossal Ancients", "巨型先祖"), ("Grimoire", "魔典"),
    ("Worldstone Shard", "世界之石碎片"), ("Ancient Statue", "古代雕像"),
    ("Sigil: Death", "死亡印记"), ("Bind Demon", "束缚恶魔"), ("Miasma Chain", "瘴气锁链"),
    ("Ladder Season 15", "天梯第 15 赛季"), ("Patch 3.3", "3.3 补丁"),
    # Patch 3.3 重做/加强的练级暗金与套装
    ("Angelic Raiment", "天使之袍"), ("Angelic Sickle", "天使之镰"), ("Angelic Mantle", "天使披风"),
    ("Bloodletter", "放血者"), ("The Battlebranch", "战枝"), ("Blinkbat's Form", "闪蝠之形"),
    ("Manald Heal", "玛那德之愈"), ("Rogue's Bow", "罗格之弓"), ("Bane Ash", "灰烬灾星"),
    ("Gravenspine", "孤坟之脊"), ("Pluckeye", "啄目弓"), ("The Ward", "守望之盾"),
    # 通用机制 / 破免 / 缩写
    ("Sunder", "破免"), ("Sunder Charms", "破免护符"), ("Cold Sunder", "破冰免"), ("Lightning Sunder", "破电免"),
    ("Fire Sunder", "破火免"), ("Magic Sunder", "破魔免"), ("Poison Sunder", "破毒免"),
    ("Magic Find", "魔法寻获"), ("Hardcore", "专家模式"), ("Uber Smiter", "超级盾击丁"),
    ("Ubers", "超级场景"), ("Boss", "首领"), ("Resurrected", "重制版"),
    # 通用名词（源里纯英文）
    ("Summon", "召唤"), ("Summoner", "召唤师"), ("Energy Shield", "能量护盾"),
    ("Attract", "吸引"), ("Craft", "制作"), ("Passive", "被动"), ("Crossbow", "弩"),
    ("Farming", "速刷"), ("Leveling", "升级"), ("Runewords", "符文之语"), ("Runeword", "符文之语"),
    ("Tips", "技巧"), ("Merc", "佣兵"), ("Insight", "洞察"), ("Grand Charm", "大型护符"),
    # 地点 / 装备（个别未译）
    ("Raven Frost", "霜之乌鸦"), ("Titans", "泰坦标枪"), ("Honor", "荣耀"),
    ("Tamoe Highland", "塔莫高地"), ("Lost City", "失落城市"), ("Pindle", "平德尔"),
    ("Cain", "凯恩"), ("The Cold Plains", "寒冷平原"), ("Pits", "深坑"),
    # 技能树标题（默认中文显示，英文切换可见；Lightning/Demon/Eldritch/Chaos 已在上方）
    ("Javelin & Spear", "标枪与长矛"), ("Bow & Crossbow", "弓与弩"),
    ("Passive & Magic", "被动与魔法"), ("Cold", "冰冷"), ("Fire", "火焰"),
    ("Summoning", "召唤"), ("Poison & Bone", "毒与骨"), ("Curses", "诅咒"),
    ("Combat", "战斗"), ("Offensive", "攻击"), ("Defensive", "防御"),
    ("Combat Masteries", "战斗精通"), ("Warcries", "战吼"), ("Elemental", "元素"),
    ("Shape Shifting", "变身"), ("Traps", "陷阱"), ("Martial Arts", "武学"),
    ("Shadow Disciplines", "影子训练"),
    # —— 2026-10-06 补充：收藏编年史属性里的技能名 / 职业名 ——
    # 属性描述由 d2data 的技能 param 生成，术语表覆盖不到时中文模式下只有英文。
    # ⚠️ 含 Fire/Cold 等短词的长名（Ring of Fire / Resist Fire）必须整条列出：
    #    否则会被拆成「Ring of」+「火焰」，渲染成半截英文。
    # ⚠️ d2data 里部分技能名连写或拼错（IronGolem / BloodGolem / Wearbear），
    #    与词表里的规范拼写是不同 key，需各列一条。
    ("Ring of Fire", "火环"), ("Resist Fire", "抗火"), ("Fire Wall", "火墙"),
    ("Holy Freeze", "神圣冰冻"), ("Chilling Armor", "寒冰装甲"),
    ("Charged Bolt", "充能弹"), ("Blaze", "烈焰"), ("Raven", "乌鸦"),
    ("Summon Spirit Wolf", "召唤幽灵狼"),
    ("Mark of the Wolf", "狼之印记"), ("Mark of the Bear", "熊之印记"),
    ("Wearbear", "熊人"),
    ("IronGolem", "钢铁石魔"), ("BloodGolem", "血魔"), ("ClayGolem", "黏土石魔"),
    ("Confuse", "混乱"), ("Terror", "恐惧"), ("Weaken", "削弱"),
    ("Howl", "嚎叫"), ("Quickness", "迅捷"), ("Psychic Ward", "心灵守护"),
    ("Miasma Chains", "瘴气锁链"),
    ("Sigil Death", "死亡印记"), ("Sigil Lethargy", "迟滞印记"),
    ("Delerium Change", "迪勒瑞姆变身"), ("enchant", "附魔"),
    # 职业名（属性里的「XX 技能等级」）
    ("Amazon", "亚马逊"), ("Assassin", "刺客"), ("Barbarian", "野蛮人"),
    ("Druid", "德鲁伊"), ("Necromancer", "亡灵法师"), ("Paladin", "圣骑士"),
    ("Sorceress", "法师"), ("Warlock", "术士"),
]

import re as _re
_ZH_MAP = {}
_ZH_PATS = []
_i = 0
for _en, _zh in sorted(ZH_PAIRS, key=lambda kv: -len(kv[0])):
    _e = _re.escape(_en); _z = _re.escape(_zh); _sep = r"\s*[（(]?\s*"; _close = r"[）)]?"
    _ZH_PATS.append(r"(?P<g%d>%s%s%s%s(?![A-Za-z])|%s%s%s%s(?![A-Za-z])|%s(?![A-Za-z])(?<!ec\">)(?:[（(]\s*%s\s*[）)])?)" % (_i, _z, _sep, _e, _close, _e, _sep, _z, _close, _e, _z))
    _ZH_MAP["g%d" % _i] = (_zh, _en); _i += 1
# 全局否定向后查找：已处于 .zt 内部（.zc 或 .ec）的文本不再二次包裹，
# 防止 build_card()/page() 多次 zh() 造成嵌套 span。
_ZH_RE = _re.compile(r"(?<!zc\"\>)(?<!ec\"\>)(?:" + "|".join(_ZH_PATS) + r")")

# 两类区域必须原样保留，不能被术语表改写：
#   1) localStorage 的 key / 搜索索引 —— data-* 属性值，被 span 污染后打勾状态就存不下来；
#   2) 条目译名 —— data-zh-is-name 标记的 span，译名已由数据层给定，
#      再被术语表包一层会渲染成「谜团 谜团 Enigma」。
# 做法：先把这两类片段挖成占位符，整串替换完再原样填回。
_ATTR_RE = _re.compile(r'\s(?:data-[a-z-]+|placeholder)="[^"]*"')
# 注意：条目名 span 自带 data-zh-is-name 属性，必须在 _ATTR_RE 之前整段挖走，
# 否则属性先被挖成占位、span 结构断裂，这条就匹配不到了。
_NAME_SPAN_RE = _re.compile(r'<span[^>]*data-zh-is-name="1"[^>]*>[^<]*</span>')
_HOLE_RE = _re.compile(r'\x00(\d+)\x00')

def zh(text):
    """将英文术语包成可切换的「中文/英文」双 span（默认中文，加 html.en 切英文）。

    data-* / placeholder 属性值与 data-zh-is-name 标记的译名原样保留，
    其余文本节点照常做术语替换（保持既有渲染行为不变）。
    """
    if not text:
        return text
    holes = []
    def _stash(m):
        holes.append(m.group(0))
        return "\x00%d\x00" % (len(holes) - 1)
    # 顺序要紧：先挖译名 span（内含 data-zh-is-name 属性），再挖剩余属性。
    if 'data-zh-is-name' in text:
        text = _NAME_SPAN_RE.sub(_stash, text)
    if '="' in text:
        text = _ATTR_RE.sub(_stash, text)
    def _repl(m):
        for _n, (_z, _e) in _ZH_MAP.items():
            if m.group(_n) is not None:
                return '<span class="zt"><span class="zc">%s </span><span class="ec" lang="en">%s</span></span>' % (_z, _e)
        return m.group(0)
    text = _ZH_RE.sub(_repl, text)
    if holes:
        text = _HOLE_RE.sub(lambda m: holes[int(m.group(1))], text)
    return text

def bi(zh_text, en_text):
    """双语块：默认中文（.zc），EN 模式显示英文（.ec）为主文本。
    用于正文、标题、说明等无法被 zh() 术语表覆盖的纯中文内容。"""
    if not zh_text:
        return en_text or ""
    return '<span class="zt"><span class="zc">%s </span><span class="ec" lang="en">%s</span></span>' % (zh_text, en_text)

def en_title(t):
    """从「中文 English」标题里取最长的纯英文词，用于 EN 模式的浏览器标签。"""
    cands = [tok for tok in t.replace("·", " ").split() if tok.isascii() and tok.isalpha()]
    if cands:
        return max(cands, key=len)
    return "Diablo II: Resurrected Guide"

def _is_cjk_only(s):
    if not s:
        return False
    has_cjk = any("一" <= c <= "鿿" for c in s)
    has_alpha = any(c.isascii() and c.isalpha() for c in s)
    return has_cjk and not has_alpha

def zh_title(t):
    """流派标题：去掉末尾中文描述，仅保留「中文 英文」翻译。"""
    toks = t.rsplit(" ", 1)
    if len(toks) == 2 and _is_cjk_only(toks[1]):
        return zh(toks[0])
    return zh(t)

# ---------------------------------------------------------------------------
# 符文编号（Rune order #1–#33）：图鉴与配方中给符文名加 #编号，如 Ist -> #24 Ist
# ---------------------------------------------------------------------------
RUNE_ORDER = {
    "El":1,"Eld":2,"Tir":3,"Nef":4,"Eth":5,"Ith":6,"Tal":7,"Ral":8,"Ort":9,"Thul":10,
    "Amn":11,"Sol":12,"Shael":13,"Dol":14,"Hel":15,"Io":16,"Lum":17,"Ko":18,"Fal":19,
    "Lem":20,"Pul":21,"Um":22,"Mal":23,"Ist":24,"Gul":25,"Vex":26,"Ohm":27,"Lo":28,
    "Sur":29,"Ber":30,"Jah":31,"Cham":32,"Zod":33,
}
# 边界：① 前不能是 ASCII 字母；② 后不能是 ASCII 字母；③ 后若是「空格+大写字母」则不匹配
# （避免把套装名 Tal Rasha's 里的 Tal 误当成符文 #7）。
_RUNE_RE = _re.compile(
    r"(?<![A-Za-z])(%s)(?![A-Za-z])(?! [A-Z])" % "|".join(
        _re.escape(k) for k in sorted(RUNE_ORDER, key=lambda x: -len(x))
    )
)
# 已经编过号的「#24 Ist」整段（含符文名一起捕获）挖走，避免再加一遍。
# 必须连符文名一起吃掉，只挖「#24 」的话占位符后紧跟的 Ist 仍会被再匹配。
_RUNE_DONE_RE = _re.compile(
    r"#\d+\s+(%s)\b" % "|".join(
        _re.escape(k) for k in sorted(RUNE_ORDER, key=lambda x: -len(x))
    )
)
# 畸形串防护：数字紧贴符文名（如「#1 El9921222」）视为已在编号语境，不再加号
_RUNE_JUNK_RE = _re.compile(r"#\d+\s*(?:%s)(?=[0-9])" % "|".join(
    _re.escape(k) for k in sorted(RUNE_ORDER, key=lambda x: -len(x))
))

def rune_no(text):
    """给符文名加 #编号（如 Ist -> #24 Ist，数字在前）。属性值与译名区域跳过。

    已经是「#24 Ist」形态的不重复加编号 —— page() 里可能对同一段文本多次调用。
    """
    if not text:
        return text
    def _sub(s):
        # 已编号的整段（含符文名）先挖走，剩下的才加
        keep = []
        def _hide(m):
            keep.append(m.group(0))
            return "\x01%d\x01" % (len(keep) - 1)
        s = _RUNE_DONE_RE.sub(_hide, s)
        s = _RUNE_JUNK_RE.sub(_hide, s)
        s = _RUNE_RE.sub(lambda m: "#%d %s" % (RUNE_ORDER[m.group(1)], m.group(1)), s)
        for i, seg in enumerate(keep):
            s = s.replace("\x01%d\x01" % i, seg)
        return s
    sub = _sub
    if '="' not in text and 'data-zh-is-name' not in text:
        return sub(text)
    holes = []
    def _stash(m):
        holes.append(m.group(0))
        return "\x00%d\x00" % (len(holes) - 1)
    if 'data-zh-is-name' in text:
        text = _NAME_SPAN_RE.sub(_stash, text)
    if '="' in text:
        text = _ATTR_RE.sub(_stash, text)
    text = sub(text)
    if holes:
        text = _HOLE_RE.sub(lambda m: holes[int(m.group(1))], text)
    return text

# ---------------------------------------------------------------------------
# Shared CSS
# ---------------------------------------------------------------------------
CSS = r'''
:root{
  --bg:#0c0a09; --bg2:#15110d; --panel:#1c1712; --panel2:#241d16;
  --ink:#e9dfce; --muted:#a99a82; --gold:#c8a24a; --gold2:#e8c97a;
  --blood:#a3302e; --blood2:#c8413c; --line:#3a2f22; --good:#6fae5b; --bad:#c0504d;
  --maxw:1180px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
/* 中英文切换：默认中文（隐藏 .ec 英文），<html class="en"> 切英文（隐藏 .zc 中文，.ec 作为主文本正常显示） */
.zt .ec{margin-left:2px}
html:not(.en) .zt .ec{display:none}
html.en .zt .zc{display:none}
html.en .zt .ec{font-size:1em;color:inherit}
.lang-toggle{margin-left:auto;background:var(--panel);border:1px solid var(--line);color:var(--gold2);border-radius:7px;padding:6px 13px;cursor:pointer;font-size:13px;font-family:inherit;font-weight:600;letter-spacing:.5px}
.lang-toggle:hover{background:var(--panel2);border-color:var(--gold);text-decoration:none}
body{
  margin:0;background:
    radial-gradient(1200px 600px at 50% -10%, #2a1c12 0%, transparent 60%),
    radial-gradient(900px 500px at 100% 0%, #1a1410 0%, transparent 55%),
    var(--bg);
  color:var(--ink);
  font-family:"Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  line-height:1.7;font-size:16px;
}
h1,h2,h3,h4{font-family:"Cinzel","Trajan Pro",Georgia,"Songti SC","STSong",serif;color:var(--gold2);line-height:1.25;letter-spacing:.5px}
a{color:var(--gold);text-decoration:none}
a:hover{color:var(--gold2);text-decoration:underline}
img{max-width:100%}
code{background:#000;color:#e8c97a;padding:1px 6px;border-radius:4px;font-size:.92em}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 18px}
.hero{
  position:relative;overflow:hidden;border-bottom:1px solid var(--line);
  background:linear-gradient(180deg,#1d130b 0%,#0c0a09 100%);
}
.hero .wrap{padding:54px 18px 40px;text-align:center}
.hero h1{font-size:clamp(28px,5vw,52px);margin:.2em 0;color:var(--gold2);text-shadow:0 2px 18px rgba(200,162,74,.25)}
.hero .sub{color:var(--muted);max-width:760px;margin:0 auto;font-size:17px}
.sigil{width:120px;height:120px;margin:0 auto 6px;opacity:.9;filter:drop-shadow(0 0 12px rgba(200,162,74,.35))}

nav.topbar{position:sticky;top:0;z-index:50;background:rgba(12,10,9,.92);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
nav.topbar .wrap{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:10px 18px}
.brand{font-family:"Cinzel",Georgia,serif;color:var(--gold2);font-weight:700;font-size:18px;display:flex;align-items:center;gap:8px}
.brand .dot{width:10px;height:10px;border-radius:50%;background:var(--blood2);box-shadow:0 0 10px var(--blood2)}
.navlinks{display:flex;gap:0;justify-content:center;align-items:center;flex-wrap:wrap;flex:1}
.navlinks a{padding:6px 11px;border-radius:7px;color:var(--muted);font-size:14px;border:1px solid transparent}
.navlinks a + a{margin-left:8px}
.navlinks a:hover{color:var(--ink);background:var(--panel);text-decoration:none}
.navlinks a.active{color:var(--bg);background:linear-gradient(180deg,var(--gold2),var(--gold));font-weight:700}
.menu-toggle{display:none;background:var(--panel);border:1px solid var(--line);color:var(--gold2);border-radius:7px;padding:6px 12px;cursor:pointer;font-size:18px}

.layout{display:grid;grid-template-columns:240px 1fr;gap:28px;max-width:var(--maxw);margin:0 auto;padding:28px 18px 60px}
.sidebar{position:sticky;top:64px;align-self:start;height:max-content;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px}
.sidebar h4{margin:6px 8px 8px;font-size:13px;color:var(--muted);letter-spacing:1px;text-transform:uppercase}
.sidebar a{display:block;padding:7px 10px;border-radius:8px;color:var(--ink);font-size:14px;border:1px solid transparent}
.sidebar a:hover{background:var(--panel2);text-decoration:none}
.sidebar a.active{background:linear-gradient(180deg,var(--panel2),var(--panel));border-color:var(--line);color:var(--gold2)}
.sidebar .grp{margin-bottom:14px;border-bottom:1px dashed var(--line);padding-bottom:8px}
.sidebar .grp:last-child{border-bottom:none;margin-bottom:0}
.content{min-width:0}
.breadcrumb{color:var(--muted);font-size:13px;margin-bottom:10px}
.breadcrumb a{color:var(--muted)}
.breadcrumb a:hover{color:var(--gold2)}

.card{background:linear-gradient(180deg,var(--panel),var(--bg2));border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:16px 0}
.card h3{margin-top:0}
.grid{display:grid;gap:16px}
.grid.cols2{grid-template-columns:repeat(2,1fr)}
.grid.cols3{grid-template-columns:repeat(3,1fr)}
.grid.cls{grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
@media(max-width:820px){.grid.cols2,.grid.cols3{grid-template-columns:1fr}.layout{grid-template-columns:1fr}.sidebar{position:static;top:0}.menu-toggle{display:inline-block}.navlinks{display:none;width:100%}.navlinks.open{display:flex}}

.cls-card{display:block;background:linear-gradient(180deg,var(--panel),var(--bg2));border:1px solid var(--line);border-radius:14px;padding:16px;color:var(--ink);transition:.18s;position:relative;overflow:hidden}
.cls-card:hover{transform:translateY(-3px);border-color:var(--gold);text-decoration:none;box-shadow:0 8px 26px rgba(0,0,0,.45)}
.cls-card .em{font-size:30px}
.cls-card h3{margin:.3em 0 .2em;font-size:19px}
.cls-card p{margin:0;color:var(--muted);font-size:13.5px}
.cls-card .role{display:inline-block;margin-top:8px;font-size:12px;color:var(--gold2);border:1px solid var(--line);padding:2px 8px;border-radius:20px}

.badge{display:inline-block;font-size:12px;padding:2px 9px;border-radius:20px;border:1px solid var(--line);color:var(--gold2);background:var(--panel2);margin-bottom:8px}
.tag{display:inline-block;font-size:11.5px;padding:1px 8px;border-radius:6px;background:#2a2118;color:var(--muted);margin:0 4px 4px 0;border:1px solid var(--line)}

table{width:100%;border-collapse:collapse;margin:10px 0;font-size:14.5px}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--panel2);color:var(--gold2);font-family:"Cinzel",Georgia,serif;font-weight:600}
tr:nth-child(even) td{background:rgba(255,255,255,.02)}

.callout{border-left:4px solid var(--gold);background:var(--panel);border-radius:0 10px 10px 0;padding:12px 16px;margin:14px 0}
.callout.tip{border-color:var(--good)}
.callout.warn{border-color:var(--bad)}
.callout.info{border-color:#5b8db8}
.callout b{color:var(--gold2)}

.two{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:820px){.two{grid-template-columns:1fr}.kv{grid-template-columns:120px 1fr}}
ul.clean{list-style:none;padding-left:0;margin:8px 0}
ul.clean li{padding:5px 0 5px 22px;position:relative;border-bottom:1px dashed var(--line)}
ul.clean li:before{content:"▸";position:absolute;left:0;color:var(--gold)}
.skills{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
@media(max-width:820px){.skills{grid-template-columns:1fr}}
.skilltree{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px}
.skilltree h4{margin:0 0 8px;color:var(--gold2);border-bottom:1px solid var(--line);padding-bottom:6px}
.skilltree ul{margin:0;padding-left:18px;font-size:14px}
.skilltree li{margin:3px 0}

footer{border-top:1px solid var(--line);background:#0a0807;margin-top:30px}
footer .wrap{padding:22px 18px;color:var(--muted);font-size:13px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
footer .disc{padding:0 18px 22px;font-size:12px;color:#8a7c66;display:block;border-top:1px solid var(--line)}
footer .repo{color:var(--gold2);text-decoration:underline;text-decoration-color:var(--line);text-underline-offset:2px}
footer .repo:hover{color:var(--gold)}
@media(hover:none){footer .repo{text-decoration-color:var(--gold2)}}

.pager{display:flex;justify-content:space-between;gap:12px;margin-top:26px}
.pager a{flex:1;text-align:center;padding:12px;border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--ink)}
.pager a:hover{text-decoration:none;border-color:var(--gold);color:var(--gold2)}
.pager a small{display:block;color:var(--muted);font-size:12px}
.section-id{scroll-margin-top:70px}

/* ==========================================================================
   收藏编年史 Chronicle
   ========================================================================== */
.ch-hero{background:linear-gradient(180deg,#1d130b 0%,#0c0a09 100%);border-bottom:1px solid var(--line)}
.ch-hero .wrap{padding:34px 18px 26px}
.ch-hero h1{margin:.1em 0 .3em;font-size:clamp(24px,4vw,38px)}
.ch-hero .sub{color:var(--muted);max-width:820px;margin:0 0 18px;font-size:15px}

.ch-total{display:flex;align-items:center;gap:18px;flex-wrap:wrap;background:var(--panel);border:1px solid var(--gold);border-radius:14px;padding:16px 20px;margin:6px 0 20px}
.ch-total .num{font-family:"Cinzel",Georgia,serif;font-size:30px;color:var(--gold2);font-weight:700;line-height:1}
.ch-total .num small{font-size:15px;color:var(--muted);font-weight:400}
.ch-total .meta{color:var(--muted);font-size:13px}
.ch-total .meta b{color:var(--ink);display:block;font-size:14px;font-family:inherit}

.ch-bar{height:10px;background:#0a0807;border:1px solid var(--line);border-radius:6px;overflow:hidden;flex:1;min-width:180px}
.ch-bar > i{display:block;height:100%;background:linear-gradient(90deg,var(--blood2),var(--gold));border-radius:6px;transition:width .3s ease}

.ch-toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:0 0 18px;position:sticky;top:56px;z-index:20;background:var(--bg);padding:10px 0}
.ch-toolbar input[type=search]{background:var(--panel);border:1px solid var(--line);color:var(--ink);border-radius:9px;padding:8px 12px;font-size:14px;font-family:inherit;min-width:180px;flex:1;max-width:280px}
.ch-toolbar input[type=search]:focus{outline:none;border-color:var(--gold)}
.ch-tab{background:var(--panel);border:1px solid var(--line);color:var(--muted);border-radius:8px;padding:7px 13px;cursor:pointer;font-size:13px;font-family:inherit}
.ch-tab:hover{color:var(--ink);border-color:var(--gold)}
.ch-tab.on{background:linear-gradient(180deg,var(--gold2),var(--gold));color:var(--bg);font-weight:700;border-color:var(--gold)}
.ch-reset{margin-left:auto;background:transparent;border:1px solid var(--line);color:var(--muted);border-radius:8px;padding:7px 13px;cursor:pointer;font-size:13px;font-family:inherit}
.ch-reset:hover{color:var(--bad);border-color:var(--bad)}
.ch-reset.armed{color:var(--bg);background:var(--bad);border-color:var(--bad);font-weight:700}

/* 导出 / 导入 */
.ch-io{display:inline-flex;gap:8px;position:relative;padding-left:10px;border-left:1px solid var(--line)}
.ch-btn{background:var(--panel);border:1px solid var(--line);color:var(--muted);border-radius:8px;
  padding:7px 13px;cursor:pointer;font-size:13px;font-family:inherit;line-height:1.35;display:inline-flex;align-items:center}
.ch-btn:hover{color:var(--ink);border-color:var(--gold)}
.ch-btn.primary{background:linear-gradient(180deg,var(--gold2),var(--gold));color:var(--bg);font-weight:700;border-color:var(--gold)}
.ch-btn.ghost{background:transparent}
.ch-io-bar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:-8px 0 18px;padding:11px 14px;
  border:1px solid var(--gold);border-radius:10px;background:linear-gradient(180deg,#1d1710,var(--bg2));
  font-size:13px;color:#cbbda4;line-height:1.5}
.ch-io-bar[hidden]{display:none}
.ch-io-msg{flex:1;min-width:220px}
.ch-io-acts{display:flex;gap:8px;flex-wrap:wrap;margin-left:auto}

.ch-sec{margin:0 0 30px}
.ch-sec > header{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding-bottom:8px;border-bottom:1px solid var(--line);margin-bottom:12px}
.ch-sec h2{margin:0;font-size:22px}
.ch-sec .cnt{color:var(--muted);font-size:13px;font-family:"Cinzel",Georgia,serif}
.ch-sec .grow{margin-left:auto;width:150px;height:8px}

.ch-grid{display:grid;gap:10px}
.ch-set-head{display:flex;align-items:flex-start;gap:11px;background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--gold);border-radius:11px;padding:12px 14px;margin-top:16px}
.ch-set-head .ch-name{font-size:16px}
.ch-pieces{margin:10px 0 0 26px}
.ch-item{display:flex;align-items:flex-start;gap:11px;background:linear-gradient(180deg,var(--panel),var(--bg2));border:1px solid var(--line);border-radius:11px;padding:11px 14px;cursor:pointer;transition:.15s}
.ch-item:hover{border-color:var(--gold)}
.ch-item.done{border-color:var(--good);background:linear-gradient(180deg,#16201310,var(--bg2));opacity:.62}
.ch-item.done .ch-name{text-decoration:line-through;color:var(--muted)}
.ch-box{flex:0 0 auto;width:19px;height:19px;border:2px solid var(--gold);border-radius:5px;margin-top:2px;display:flex;align-items:center;justify-content:center;font-size:13px;color:var(--bg);font-weight:700}
.ch-item.done .ch-box{background:var(--good);border-color:var(--good)}
.ch-box span{opacity:0;line-height:1}
.ch-item.done .ch-box span{opacity:1}
.ch-main{min-width:0;flex:1}
.ch-name{font-size:15px;color:var(--ink);font-weight:600;line-height:1.45}
.ch-name .zt .zc{color:var(--gold2);font-weight:700}
.ch-sub{font-size:12.5px;color:var(--muted);margin-top:3px;line-height:1.55}
.ch-sub code{font-size:11.5px;background:#000;padding:0 5px;border-radius:4px;color:var(--gold2)}
.ch-sub .rw{color:#8fb8d8}
.ch-props{margin-top:5px;font-size:12px;color:#9a8b73;line-height:1.6}
.ch-props span{display:inline-block;background:#201a13;border:1px solid var(--line);border-radius:5px;padding:0 6px;margin:2px 4px 0 0}
.ch-req{flex:0 0 auto;font-size:11.5px;color:var(--muted);border:1px solid var(--line);border-radius:20px;padding:1px 8px;margin-top:2px;white-space:nowrap}
.ch-ladder{font-size:11px;color:#e8a04a;border:1px solid #5a4326;border-radius:5px;padding:0 5px;margin-left:6px}
.ch-eth{font-size:11px;color:#7fc8e8;border:1px solid #2c4d5a;border-radius:5px;padding:0 5px;margin-left:5px}

.ch-subgrp{margin:14px 0 8px;font-size:14px;color:var(--gold);font-family:"Cinzel",Georgia,serif;letter-spacing:.5px}
.ch-bonus{font-size:12.5px;color:#b9a88c;background:#1a150f;border:1px dashed var(--line);border-radius:8px;padding:7px 11px;margin-top:6px}
.ch-empty{color:var(--muted);font-size:14px;padding:20px 0;text-align:center}

/* 符文需求统计 */
.rune-need-card{padding-top:6px}
.rune-need-card .fold-body{margin-top:12px}
.fold-toggle{display:flex;align-items:center;gap:10px;width:100%;background:none;border:0;
  padding:12px 4px;color:var(--gold2);cursor:pointer;font-family:inherit;font-size:17px;
  font-weight:700;text-align:left;line-height:1.3}
.fold-toggle:hover{color:var(--gold)}
.fold-toggle:focus-visible{outline:2px solid var(--gold);outline-offset:2px;border-radius:6px}
.fold-arrow{width:0;height:0;flex:0 0 auto;border-left:6px solid currentColor;
  border-top:4.5px solid transparent;border-bottom:4.5px solid transparent;
  transition:transform .2s ease;transform-origin:38% 50%}
.fold-toggle[aria-expanded="false"] .fold-arrow{transform:rotate(-90deg)}
.fold-title{flex:0 0 auto}
.fold-hint{margin-left:auto;font-size:12px;font-weight:400;color:var(--muted);text-align:right}
.fold-body{border-top:1px dashed var(--line);padding-top:12px}
.rune-need-card p{margin:0 0 14px;font-size:14px;color:#b9a88c;line-height:1.75}
.rune-need-card .callout{margin:12px 0 0}
.table-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
table.rune-need{width:100%;border-collapse:collapse;font-size:13.5px;margin:0}
table.rune-need th,table.rune-need td{border:1px solid var(--line);padding:6px 8px;text-align:center;white-space:nowrap}
table.rune-need th:first-child,table.rune-need td:first-child{text-align:left}
table.rune-need thead th{background:var(--panel2);color:var(--gold2);font-family:"Cinzel",Georgia,serif;font-weight:600}
table.rune-need th.tier-head{border-left:1px solid var(--gold)}
table.rune-need .tier-subhead th{background:#241d16;color:var(--muted);font-size:12px;padding:3px 8px;font-weight:500}
table.rune-need .tier-subhead th:first-child,table.rune-need .tier-subhead th:nth-child(2),table.rune-need .tier-subhead th:nth-child(3){background:transparent;border:none}
table.rune-need tbody td[data-sk]{border-left:1px solid var(--gold);color:#9a8b73;font-size:12.5px}
table.rune-need code.rn{background:#000;color:#8fb8d8;padding:1px 6px;border-radius:4px;font-size:12.5px}
table.rune-need td.num{font-family:"Cinzel",Georgia,serif;font-weight:700;font-size:15px;color:var(--ink)}
table.rune-need td.num.left{color:var(--gold2)}
table.rune-need tr.done td.num.left{color:var(--good)}
table.rune-need td.num.left.zero{color:#5f564a;text-decoration:line-through}
table.rune-need tr.done{background:rgba(111,174,91,.06)}
.ch-bar.tiny{height:5px;min-width:70px;width:100%;display:block}
td.col-bar{width:90px;padding:4px 8px}
.tier-sum{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px;font-size:12.5px;color:var(--muted)}
.tier-sum b{color:var(--gold2);font-family:"Cinzel",Georgia,serif;font-size:14px}
.tier-sum .ts{padding:4px 10px;background:#1a150f;border:1px solid var(--line);border-radius:20px}
.ch-io input[type=file]{display:none}


@media(max-width:820px){
  .ch-toolbar{position:static}
  .ch-total{gap:12px;padding:14px}
  .ch-total .num{font-size:24px}
  .ch-sec .grow{margin-left:0;width:100%}
  .ch-req{display:none}
  table.rune-need{font-size:12.5px}
  table.rune-need th,table.rune-need td{padding:4px 6px}
}
'''

JS = r'''
// ==========================================================================
// 站点本地存储：全站共用一份 d2r_site_v1
//   { lang: "zh"|"en", ui: { 折叠状态... }, chronicle: { 条目id: 时间戳 } }
// 旧的 lang / d2r_chronicle_v1 会自动迁移进来，迁移后不再单独写。
// ==========================================================================
var SiteStore=(function(){
  var KEY="d2r_site_v1";
  var mem=null;                 // 内存缓存，避免反复 JSON.parse
  function blank(){return {lang:"zh",ui:{},chronicle:{}};}
  function migrate(raw){
    var d=blank();
    if(!raw||typeof raw!=="object")return d;
    if(raw.lang==="en")d.lang="en";
    if(raw.ui&&typeof raw.ui==="object")d.ui=raw.ui;
    if(raw.chronicle&&typeof raw.chronicle==="object")d.chronicle=raw.chronicle;
    return d;
  }
  function load(){
    if(mem)return mem;
    var raw=null;
    try{raw=localStorage.getItem(KEY);}catch(e){}
    if(raw){
      try{mem=migrate(JSON.parse(raw));}catch(e){mem=blank();}
    }else{
      mem=blank();
      // 迁移旧key
      try{
        var l=localStorage.getItem("lang");
        if(l==="en")mem.lang="en";
        var c=localStorage.getItem("d2r_chronicle_v1");
        if(c){var o=JSON.parse(c);if(o&&typeof o==="object")mem.chronicle=o;}
      }catch(e){}
    }
    return mem;
  }
  function save(){
    try{localStorage.setItem(KEY,JSON.stringify(load()));}catch(e){}
  }
  return {
    // 取整个对象（引用，可直接改后调 commit）
    get:function(){return load();},
    commit:save,
    lang:function(){return load().lang;},
    setLang:function(v){load().lang=v?"en":"zh";save();},
    chronicle:function(){return load().chronicle;},
    saveChronicle:function(){save();},
    // 清空打勾记录：原地清空对象，**不要重新赋值**，
    // 否则调用方持有的引用会脱钩，之后再打勾就写不回存储了。
    resetChronicle:function(){
      var c=load().chronicle, k=Object.keys(c);
      for(var i=0;i<k.length;i++){delete c[k[i]];}
      save();
    },
    ui:function(k){return load().ui[k];},
    setUi:function(k,v){load().ui[k]=v;save();}
  };
})();

// 中英文切换：默认中文，点击切英文并记住选择（存站点统一存储）
(function(){
  var bar=document.querySelector("nav.topbar .wrap");
  if(bar){
    var btn=document.createElement("button");
    btn.id="langToggle";btn.className="lang-toggle";
    btn.setAttribute("aria-label","切换中英文");
    bar.appendChild(btn);
    var en=SiteStore.lang()==="en";
    var origTitle=document.title;
    function set(v){document.documentElement.classList.toggle("en",v);SiteStore.setLang(v);btn.textContent=v?"中文":"EN";document.title=v?(document.documentElement.getAttribute("data-en-title")||origTitle):origTitle;}
    set(en);
    btn.addEventListener("click",function(){set(!document.documentElement.classList.contains("en"));});
  }
})();

// 移动端菜单 + 返回顶部
(function(){
  var t=document.querySelector(".menu-toggle");
  var n=document.querySelector(".navlinks");
  if(t&&n){t.addEventListener("click",function(){n.classList.toggle("open");});}
  if(n){n.querySelectorAll("a").forEach(function(a){a.addEventListener("click",function(){n.classList.remove("open");});});}
  var b=document.createElement("button");
  b.textContent="↑ 顶部";b.className="totop";
  b.style.cssText="position:fixed;right:16px;bottom:16px;z-index:60;display:none;background:#241d16;color:#e8c97a;border:1px solid #3a2f22;border-radius:10px;padding:8px 12px;cursor:pointer;font-size:13px";
  document.body.appendChild(b);
  window.addEventListener("scroll",function(){b.style.display=window.scrollY>400?"block":"none";});
  b.addEventListener("click",function(){window.scrollTo({top:0,behavior:"smooth"});});
})();

// ==========================================================================
// 收藏编年史：打勾状态与界面折叠状态存站点统一存储 SiteStore（d2r_site_v1）
// 纯本地浏览器，不上传任何服务器
// ==========================================================================
(function(){
  var root=document.querySelector("[data-chronicle]");
  if(!root)return;
  var items=Array.prototype.slice.call(root.querySelectorAll(".ch-item"));
  if(!items.length)return;

  // 打勾状态（与全站共用同一份存档）
  var state=SiteStore.chronicle();
  function save(){SiteStore.saveChronicle();}

  // 孔数分档表头（2/3/4/5/6 孔），给符文预算分档用。必须在 refresh 之前就绪。
  var rwTierCounts=Array.prototype.slice.call(
    (root.querySelector(".rune-need .tier-subhead")||{children:[]}).children
  ).map(function(th){return parseInt(th.getAttribute("data-sk")||"",10)||0;}).filter(function(n){return n>=2&&n<=6;});

  // 打勾/取消（用事件委托，动态筛选后依然有效）
  root.addEventListener("click",function(ev){
    var el=ev.target.closest(".ch-item");
    if(!el||!root.contains(el))return;
    var id=el.getAttribute("data-id");
    if(!id)return;
    // 套装头部是批量开关：一次勾/取消整套部件
    if(el.getAttribute("data-role")==="set-all"){
      var wrap=el.parentNode;
      var kids=wrap?wrap.querySelectorAll(".ch-pieces .ch-item"):[];
      var allOn=true;
      for(var i=0;i<kids.length;i++){if(!state[kids[i].getAttribute("data-id")]){allOn=false;break;}}
      for(var j=0;j<kids.length;j++){
        var kid=kids[j],kidId=kid.getAttribute("data-id");
        if(allOn){delete state[kidId];}else{state[kidId]=Date.now();}
        kid.classList.toggle("done",!allOn);
        kid.setAttribute("aria-checked",allOn?"false":"true");
      }
      if(allOn){delete state[id];}else{state[id]=Date.now();}
      el.classList.toggle("done",!allOn);
      el.setAttribute("aria-checked",allOn?"false":"true");
      save();syncSetHeads();refresh();
      return;
    }
    if(state[id]){delete state[id];}else{state[id]=Date.now();}
    el.classList.toggle("done",!!state[id]);
    el.setAttribute("aria-checked",state[id]?"true":"false");
    save();
    syncSetHeads();
    refresh();
  });

  // 统计：按 data-cat 分组 + 总计（套装头是批量开关，不计入进度）
  var counters={};
  function refresh(){
    var total=0,done=0;
    counters={};
    items.forEach(function(it){
      if(it.getAttribute("data-role")==="set-all")return;
      if(it.style.display==="none")return;      // 被搜索/筛选隐藏的不计入
      var cat=it.getAttribute("data-cat")||"other";
      counters[cat]=counters[cat]||{t:0,d:0};
      counters[cat].t++;
      total++;
      if(state[it.getAttribute("data-id")]){counters[cat].d++;done++;}
    });
    var pct=total?Math.round(done/total*100):0;
    var num=document.getElementById("chTotal");
    if(num)num.firstChild.nodeValue=String(done);
    var small=document.getElementById("chTotalOf");
    if(small)small.textContent="/ "+total;
    var meta=document.getElementById("chPct");
    if(meta)meta.textContent=pct+"%";
    var bar=document.getElementById("chBar");
    if(bar)bar.style.width=pct+"%";
    // 各分类进度
    Object.keys(counters).forEach(function(cat){
      var c=counters[cat];
      var pct2=c.t?Math.round(c.d/c.t*100):0;
      var e1=document.querySelector('[data-catbar="'+cat+'"]');
      if(e1)e1.style.width=pct2+"%";
      var e2=document.querySelector('[data-catnum="'+cat+'"]');
      if(e2)e2.textContent=c.d+" / "+c.t;
    });
    refreshRuneBudget();
  }

  // 符文预算：已勾选的符文之语扣掉对应符文，算出每种符文「还缺几个」
  var runeRows=Array.prototype.slice.call(root.querySelectorAll(".rune-need tbody tr"));
  var runeFold=null;   // 折叠句柄，后面的 initFold 赋值；refreshRuneBudget 要用
  var tierSumEl=document.getElementById("rwTierSum");
  function refreshRuneBudget(){
    if(!runeRows.length)return;
    // 已完成条目涉及的符文（按出现次数累计）与按孔数分档
    var used={}, usedTier={};
    Array.prototype.slice.call(root.querySelectorAll('.ch-item[data-cat="rw"]')).forEach(function(it){
      if(!state[it.getAttribute("data-id")])return;
      var seq=(it.getAttribute("data-runes")||"").split(",").filter(Boolean);
      var sk=it.getAttribute("data-sockets")||"0";
      seq.forEach(function(rn){
        used[rn]=(used[rn]||0)+1;
        usedTier[sk+"-"+rn]=(usedTier[sk+"-"+rn]||0)+1;
      });
    });
    runeRows.forEach(function(tr){
      var rn=tr.getAttribute("data-rune");
      var leftEl=tr.querySelector("td.num.left");
      var totEl=tr.querySelector("td.num.tot");
      var tot=parseInt(totEl.textContent,10)||0;
      var left=Math.max(0,tot-(used[rn]||0));
      leftEl.textContent=left;
      leftEl.classList.toggle("zero",left===0);
      tr.classList.toggle("done",left===0&&tot>0);
      // 分档列也要扣减（第 4 列起是各孔数档位，末列是进度条）
      var cells=tr.querySelectorAll("td[data-sk]");
      cells.forEach(function(td){
        var sk=td.getAttribute("data-sk")||"0";
        var n=parseInt(td.textContent,10)||0;
        td.textContent=Math.max(0,n-(usedTier[sk+"-"+rn]||0));
      });
      // 迷你进度条按完成比例
      var bar=tr.querySelector(".ch-bar.tiny > i");
      if(bar){bar.style.width=(tot?Math.round((tot-left)/tot*100):0)+"%";}
    });
    // 收起时在标题旁给个摘要：还缺几种符文、共多少个
    if(runeFold&&runeFold.setHint){
      var lack=0,sumLeft=0;
      runeRows.forEach(function(tr){
        var l=parseInt(tr.querySelector("td.num.left").textContent,10)||0;
        if(l>0){lack++;sumLeft+=l;}
      });
      runeFold.setHint(lack?("还缺 "+lack+" 种 · "+sumLeft+" 个"):"已集齐");
    }
    // 顶部按孔数小结
    if(tierSumEl){
      var parts=[];
      var rwItems=Array.prototype.slice.call(root.querySelectorAll('.ch-item[data-cat="rw"]'));
      rwTierCounts.forEach(function(sk){
        var inTier=rwItems.filter(function(x){return (x.getAttribute("data-sockets")||"")===String(sk);});
        var dn=inTier.filter(function(x){return !!state[x.getAttribute("data-id")];}).length;
        if(inTier.length)parts.push(sk+"孔 "+dn+"/"+inTier.length);
      });
      tierSumEl.innerHTML=parts.map(function(p){return '<span class="ts">'+p+"</span>";}).join("");
    }
  }

  // 初始渲染勾选态；套装头按「部件是否集齐」自动同步
  function syncSetHeads(){
    Array.prototype.slice.call(root.querySelectorAll('[data-role="set-all"]')).forEach(function(head){
      var wrap=head.parentNode;
      var kids=wrap?wrap.querySelectorAll(".ch-pieces .ch-item"):[];
      var allOn=kids.length>0;
      for(var i=0;i<kids.length;i++){if(!state[kids[i].getAttribute("data-id")]){allOn=false;break;}}
      var on=allOn||!!state[head.getAttribute("data-id")];
      head.classList.toggle("done",on);
      head.setAttribute("aria-checked",on?"true":"false");
    });
  }
  // 按 state 重渲染所有勾选态（初始化 / 导入 / 清空后共用）
  function renderAll(){
    items.forEach(function(it){
      var on=!!state[it.getAttribute("data-id")];
      it.classList.toggle("done",on);
      it.setAttribute("aria-checked",on?"true":"false");
    });
    syncSetHeads();
  }
  renderAll();

  // 分类切换
  var tabs=Array.prototype.slice.call(document.querySelectorAll(".ch-tab"));
  var activeCat="all";
  function applyFilter(){
    var q=(document.getElementById("chSearch")||{}).value||"";
    q=q.trim().toLowerCase();
    items.forEach(function(it){
      var catOk=(activeCat==="all"||it.getAttribute("data-cat")===activeCat);
      var txt=(it.getAttribute("data-search")||"").toLowerCase();
      var qOk=!q||txt.indexOf(q)>=0;
      var show=catOk&&qOk;
      it.style.display=show?"":"none";
    });
    // 隐藏无结果的分组标题
    Array.prototype.slice.call(root.querySelectorAll(".ch-sec")).forEach(function(sec){
      var any=Array.prototype.slice.call(sec.querySelectorAll(".ch-item")).some(function(x){return x.style.display!=="none";});
      sec.style.display=any?"":"none";
    });
    Array.prototype.slice.call(root.querySelectorAll(".ch-subwrap")).forEach(function(w){
      var any=Array.prototype.slice.call(w.querySelectorAll(".ch-item")).some(function(x){return x.style.display!=="none";});
      w.style.display=any?"":"none";
    });
    refresh();
  }
  tabs.forEach(function(btn){
    btn.addEventListener("click",function(){
      tabs.forEach(function(b){b.classList.remove("on");});
      btn.classList.add("on");
      activeCat=btn.getAttribute("data-filter")||"all";
      applyFilter();
    });
  });
  var search=document.getElementById("chSearch");
  if(search)search.addEventListener("input",applyFilter);

  // 重置（需二次确认，避免误清）
  var rst=document.getElementById("chReset");
  if(rst){
    // 文案按当前语言现场生成（按钮初始是 bi() 的 span，不能直接读 textContent）
    var isEn=function(){return document.documentElement.classList.contains("en");};
    var TXT={reset:["清空打勾","Reset"],confirm:["再点一次确认清空","Click again to confirm"]};
    function rstText(key){return TXT[key][isEn()?1:0];}
    var armed=false,timer=null;
    rst.addEventListener("click",function(){
      if(!armed){
        armed=true;
        rst.textContent=rstText("confirm");
        rst.classList.add("armed");
        clearTimeout(timer);
        timer=setTimeout(function(){armed=false;rst.textContent=rstText("reset");rst.classList.remove("armed");},4000);
        return;
      }
clearTimeout(timer);armed=false;
// 清空打勾记录（SiteStore 内部原地清空，state 引用保持有效）
      SiteStore.resetChronicle();
      items.forEach(function(it){it.classList.remove("done");it.setAttribute("aria-checked","false");});
      syncSetHeads();
      rst.textContent=rstText("reset");rst.classList.remove("armed");
      refresh();
    });
  }

  // 折叠区块：状态存站点统一存储的 ui 里，全站共用一份
  function initFold(btnId, bodyId, uiKey, hintId){
    var btn=document.getElementById(btnId);
    var body=document.getElementById(bodyId);
    if(!btn||!body)return;
    var open=SiteStore.ui(uiKey);
    // 没存过：默认收起（大表格默认不挡内容），给个首访提示
    if(open===undefined)open=false;
    function apply(){
      btn.setAttribute("aria-expanded",open?"true":"false");
      body.style.display=open?"":"none";
    }
    apply();
    btn.addEventListener("click",function(){
      open=!open;
      SiteStore.setUi(uiKey,open);
      apply();
    });
    return {setHint:function(t){var h=document.getElementById(hintId);if(h)h.textContent=t;}};
  }
  var runeFold=initFold("runeNeedToggle","runeNeedBody","runeNeedOpen","runeNeedHint");

  // ==========================================================================
  // 导出 / 导入：把打勾记录带走（换浏览器），或做成图片分享出去
  //   导出图片 —— canvas 画一张成绩卡，直接发群/朋友圈
  //   导出 JSON —— 全量完整备份（含时间戳），可再导入
  //   导入      —— 只吃本站导出的 JSON，写回 SiteStore（localStorage），不上传
  // 为便于端到端测试，关键纯函数挂在 window.__chronicleIO（无副作用）。
  // ==========================================================================
  function L(a,b){return document.documentElement.classList.contains("en")?b:a;}

  // 本页认得的所有条目 id（套装头是批量开关，不是可收集项，排除）
  var knownIds={};
  items.forEach(function(it){
    if(it.getAttribute("data-role")==="set-all")return;
    knownIds[it.getAttribute("data-id")]=1;
  });

  function pad2(n){return (n<10?"0":"")+n;}
  function nowStr(){var d=new Date();return d.getFullYear()+"-"+pad2(d.getMonth()+1)+"-"+pad2(d.getDate());}

  // ---- 统计（永远按全量算，不受当前分类 / 搜索影响）----
  var CAT_ORDER=[["rw",["符文之语","Runewords"]],["set",["套装部件","Set pieces"]],["uni",["独特道具","Unique items"]]];
  function fullStats(){
    var cats={},total=0,done=0;
    CAT_ORDER.forEach(function(p){cats[p[0]]={t:0,d:0};});
    items.forEach(function(it){
      if(it.getAttribute("data-role")==="set-all")return;
      var cat=it.getAttribute("data-cat");
      if(!cats[cat])cats[cat]={t:0,d:0};
      cats[cat].t++;total++;
      if(state[it.getAttribute("data-id")]){cats[cat].d++;done++;}
    });
    return {cats:cats,total:total,done:done,pct:total?Math.round(done/total*1000)/10:0};
  }
  // 符文预算：还缺几种、共几个（从 data-runes 重算，不读被扣减过的 DOM）
  function runeSummary(){
    var tot={},used={};
    runeRows.forEach(function(tr){
      var rn=tr.getAttribute("data-rune");
      tot[rn]=parseInt(tr.querySelector("td.num.tot").textContent,10)||0;
      used[rn]=0;
    });
    items.forEach(function(it){
      if(it.getAttribute("data-cat")!=="rw")return;
      if(!state[it.getAttribute("data-id")])return;
      (it.getAttribute("data-runes")||"").split(",").filter(Boolean).forEach(function(rn){
        if(rn in used)used[rn]++;
      });
    });
    var lack=0,left=0,all=0;
    Object.keys(tot).forEach(function(rn){
      all+=tot[rn];
      var l=Math.max(0,tot[rn]-used[rn]);
      if(l>0){lack++;left+=l;}
    });
    return {lack:lack,left:left,total:all};
  }

  // ---- JSON 备份 ----
  function buildJson(){
    return JSON.stringify({
      app:"d2r-chronicle",version:1,
      site:"https://kingsir.work/D2/chronicle.html",
      exported:new Date().toISOString(),
      count:Object.keys(state).length,
      chronicle:state
    },null,2);
  }
  // 只认本站导出的 JSON：{ chronicle:{...} }，也容忍裸的 { "rw:xx": 时间戳 }
  function parseJsonImport(text){
    var s=String(text||"").replace(/^\ufeff/,"").trim();
    if(s.charAt(0)!=="{")return null;
    var o;
    try{o=JSON.parse(s);}catch(e){return null;}
    if(!o||typeof o!=="object")return null;
    if(o.chronicle&&typeof o.chronicle==="object")return o.chronicle;
    var ks=Object.keys(o);
    if(ks.length&&ks.every(function(k){return /^(rw|uni|piece):/.test(k);}))return o;
    return null;
  }
  // merge：只加不删（换浏览器迁移的正解）；replace：先清空再写入文件里的记录
  function applyImport(records,mode){
    var ids=Object.keys(records),applied=0;
    if(mode==="replace")SiteStore.resetChronicle();
    ids.forEach(function(id){
      if(!knownIds[id])return;
      if(mode!=="replace"&&state[id])return;
      var v=records[id];
      // 时间戳要像个真时间（>2000-01-01），否则记为现在
      state[id]=(typeof v==="number"&&v>946684800000)?v:Date.now();
      applied++;
    });
    save();
    return applied;
  }

  // ---- 存文件 ----
  function saveUrl(url,name){
    var a=document.createElement("a");
    a.href=url;a.download=name;a.style.display="none";
    document.body.appendChild(a);a.click();
    setTimeout(function(){
      if(a.parentNode)a.parentNode.removeChild(a);
      try{URL.revokeObjectURL(url);}catch(e){}
    },0);
  }
  function downloadText(name,text,mime){
    try{
      var blob=new Blob([text],{type:(mime||"text/plain")+";charset=utf-8"});
      saveUrl(URL.createObjectURL(blob),name);
      return true;
    }catch(e){return false;}
  }

  // ---- 分享图片：canvas 画一张成绩卡 ----
  var CARD={w:1200,h:800,s:2};
  var FONT='"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif';
  var COL={bg1:"#241810",bg2:"#0c0a09",panel:"#171009",gold:"#e8c97a",gold2:"#c8a24a",
           ink:"#efe6d6",muted:"#9a8b73",line:"#3a2f22",track:"#0a0807",
           good:"#7fbf6a",blood:"#a3302e"};
  function rr(ctx,x,y,w,h,r){
    r=Math.min(r,w/2,h/2);
    ctx.beginPath();
    ctx.moveTo(x+r,y);
    ctx.arcTo(x+w,y,x+w,y+h,r);
    ctx.arcTo(x+w,y+h,x,y+h,r);
    ctx.arcTo(x,y+h,x,y,r);
    ctx.arcTo(x,y,x+w,y,r);
    ctx.closePath();
  }
  // 把卡片画到 ctx 上。ctx 由调用方传入，测试时可传桩对象。
  function drawShareCard(ctx,st,rs){
    var W=CARD.w,H=CARD.h,pad=72,i;
    var g=ctx.createLinearGradient(0,0,0,H);
    g.addColorStop(0,COL.bg1);g.addColorStop(1,COL.bg2);
    ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
    ctx.lineWidth=2;ctx.strokeStyle=COL.gold2;
    rr(ctx,24,24,W-48,H-48,22);ctx.stroke();

    // 标题 + 日期
    ctx.textBaseline="alphabetic";
    ctx.textAlign="left";ctx.fillStyle=COL.gold;ctx.font="600 46px "+FONT;
    ctx.fillText(L("收藏编年史","Collection Chronicle"),pad,128);
    ctx.fillStyle=COL.muted;ctx.font="400 22px "+FONT;
    ctx.fillText("Diablo II: Resurrected",pad,164);
    ctx.textAlign="right";ctx.fillStyle=COL.muted;ctx.font="400 22px "+FONT;
    ctx.fillText(nowStr(),W-pad,128);
    ctx.fillStyle=COL.line;ctx.fillRect(pad,190,W-pad*2,1);

    // 大数字
    ctx.textAlign="left";ctx.fillStyle=COL.muted;ctx.font="400 24px "+FONT;
    ctx.fillText(L("已收集","Collected"),pad,240);
    ctx.fillStyle=COL.gold;ctx.font="700 84px "+FONT;
    var big=String(st.done);
    ctx.fillText(big,pad,322);
    var bw=ctx.measureText(big).width;
    ctx.fillStyle=COL.muted;ctx.font="400 32px "+FONT;
    ctx.fillText("/ "+st.total,pad+bw+16,316);
    ctx.textAlign="right";ctx.fillStyle=COL.gold;ctx.font="700 56px "+FONT;
    ctx.fillText(st.pct+"%",W-pad,318);

    // 总进度条
    var barY=352,barH=16,barW=W-pad*2;
    ctx.fillStyle=COL.track;ctx.strokeStyle=COL.line;ctx.lineWidth=1;
    rr(ctx,pad,barY,barW,barH,8);ctx.fill();ctx.stroke();
    if(st.done>0){
      var gg=ctx.createLinearGradient(pad,0,pad+barW,0);
      gg.addColorStop(0,COL.blood);gg.addColorStop(1,COL.gold);
      ctx.fillStyle=gg;
      rr(ctx,pad,barY,Math.max(barH,barW*st.done/st.total),barH,8);ctx.fill();
    }

    // 三个分类
    var y=420;
    for(i=0;i<CAT_ORDER.length;i++){
      var key=CAT_ORDER[i][0],lbl=CAT_ORDER[i][1];
      var c=st.cats[key]||{t:0,d:0};
      var pct=c.t?Math.round(c.d/c.t*1000)/10:0;
      ctx.textAlign="left";ctx.fillStyle=COL.ink;ctx.font="500 26px "+FONT;
      ctx.fillText(L(lbl[0],lbl[1]),pad,y);
      ctx.textAlign="right";ctx.fillStyle=COL.muted;ctx.font="400 24px "+FONT;
      ctx.fillText(c.d+" / "+c.t+"   "+pct+"%",W-pad,y);
      var by=y+15;
      ctx.fillStyle=COL.track;
      rr(ctx,pad,by,barW,10,5);ctx.fill();
      if(c.d>0){
        ctx.fillStyle=COL.good;
        rr(ctx,pad,by,Math.max(10,barW*c.d/c.t),10,5);ctx.fill();
      }
      y+=64;
    }

    // 符文预算摘要
    var boxY=y+8;
    ctx.fillStyle=COL.panel;ctx.strokeStyle=COL.line;ctx.lineWidth=1;
    rr(ctx,pad,boxY,W-pad*2,80,14);ctx.fill();ctx.stroke();
    ctx.textAlign="left";ctx.fillStyle=COL.ink;ctx.font="500 24px "+FONT;
    // 全收集齐时不能再说「还缺」，否则「还缺 → 已集齐」自相矛盾
    ctx.fillText(rs.lack?L("集齐全部符文之语还缺","Still missing to craft every runeword")
                       :L("符文之语所需符文","Runes needed for every runeword"),pad+24,boxY+30);
    ctx.fillStyle=COL.gold;ctx.font="700 30px "+FONT;
    ctx.fillText(rs.lack?(rs.lack+L(" 种 · "," kinds · ")+rs.left+L(" 个"," runes"))
                       :L("已集齐 · 全部 "+rs.total+" 个","Complete · all "+rs.total+" runes"),
                 pad+24,boxY+64);

    // 页脚
    ctx.fillStyle=COL.line;ctx.fillRect(pad,716,W-pad*2,1);
    ctx.textAlign="left";ctx.fillStyle=COL.gold2;ctx.font="500 22px "+FONT;
    ctx.fillText("kingsir.work/D2/chronicle.html",pad,754);
    ctx.textAlign="right";ctx.fillStyle=COL.muted;ctx.font="400 20px "+FONT;
    ctx.fillText(L("打勾数据仅保存在浏览器本地","Progress is stored locally in your browser"),W-pad,754);
    return true;
  }
  function exportImage(){
    var cv=document.createElement("canvas");
    cv.width=CARD.w*CARD.s;cv.height=CARD.h*CARD.s;
    var ctx=cv.getContext&&cv.getContext("2d");
    if(!ctx){
      showBar(L("当前浏览器不支持 canvas，无法生成图片。","This browser cannot render a canvas image."),false);
      return false;
    }
    ctx.scale(CARD.s,CARD.s);
    drawShareCard(ctx,fullStats(),runeSummary());
    var name="d2r-chronicle-"+nowStr()+".png";
    if(cv.toBlob){
      cv.toBlob(function(blob){
        if(blob)saveUrl(URL.createObjectURL(blob),name);
        else saveUrl(cv.toDataURL("image/png"),name);
      },"image/png");
    }else{
      saveUrl(cv.toDataURL("image/png"),name);
    }
    return true;
  }

  // ---- 导入确认条 ----
  var ioBar=document.getElementById("chIoBar");
  var ioMsg=document.getElementById("chIoMsg");
  var ioMerge=document.getElementById("chIoMerge");
  var ioReplace=document.getElementById("chIoReplace");
  var ioCancel=document.getElementById("chIoCancel");
  var pending=null;
  function hideBar(){if(ioBar)ioBar.hidden=true;pending=null;}
  function showBar(msg,withActions){
    if(!ioBar)return;
    ioMsg.textContent=msg;
    if(ioMerge)ioMerge.hidden=!withActions;
    if(ioReplace)ioReplace.hidden=!withActions;
    if(withActions){
      if(ioMerge)ioMerge.textContent=L("合并","Merge");
      if(ioReplace)ioReplace.textContent=L("覆盖","Replace");
    }
    if(ioCancel)ioCancel.textContent=L("取消","Cancel");
    ioBar.hidden=false;
  }
  function afterImport(msg){
    renderAll();refresh();
    showBar(msg,false);
  }
  function handleImportText(text){
    var rec=parseJsonImport(text);
    if(!rec){
      showBar(L("无法识别这个文件：请选择本站「导出 JSON」生成的备份文件。",
               "Unrecognised file — pick the JSON backup created by Export JSON on this page."),false);
      return null;
    }
    var ids=Object.keys(rec);
    var known=ids.filter(function(id){return knownIds[id];});
    var unknown=ids.length-known.length;
    var have=Object.keys(state).length;
    if(!known.length){
      showBar(L("文件里没有本页能识别的收藏记录"+(unknown?"（"+unknown+" 条不认识，已忽略）":"")+"。",
               "No records here match this page"+(unknown?" ("+unknown+" unknown, ignored)":"")+"."),false);
      return {known:0,unknown:unknown,records:rec};
    }
    pending={records:rec,known:known.length};
    showBar(L("这个文件有 "+known.length+" 条已收集记录"
              +(unknown?"（另有 "+unknown+" 条本页不认识，会忽略）":"")
              +"，你当前已收集 "+have+" 条。",
              "This file has "+known.length+" collected item(s)"
              +(unknown?" ("+unknown+" unknown here, ignored)":"")
              +"; you currently have "+have+"."),true);
    return {known:known.length,unknown:unknown,records:rec};
  }
  if(ioMerge)ioMerge.addEventListener("click",function(){
    if(!pending)return;
    var n=applyImport(pending.records,"merge");
    pending=null;
    afterImport(L("已合并 "+n+" 条新记录，当前共 "+Object.keys(state).length+" 条。",
                  "Merged "+n+" new record(s); "+Object.keys(state).length+" collected now."));
  });
  if(ioReplace)ioReplace.addEventListener("click",function(){
    if(!pending)return;
    var n=applyImport(pending.records,"replace");
    pending=null;
    afterImport(L("已按文件覆盖，当前共 "+Object.keys(state).length+" 条。",
                  "Replaced with the file's records; "+Object.keys(state).length+" collected now."));
  });
  if(ioCancel)ioCancel.addEventListener("click",hideBar);

  // ---- 文件选择 ----
  var fileInput=document.getElementById("chImport");
  if(fileInput){
    fileInput.addEventListener("change",function(){
      var f=fileInput.files&&fileInput.files[0];
      fileInput.value="";              // 允许连续导入同一个文件
      if(!f)return;
      if(typeof FileReader==="undefined"){
        showBar(L("当前浏览器不支持读取本地文件。","This browser cannot read local files."),false);
        return;
      }
      var rd=new FileReader();
      rd.onload=function(){handleImportText(rd.result);};
      rd.onerror=function(){showBar(L("读取文件失败。","Could not read the file."),false);};
      rd.readAsText(f,"utf-8");
    });
  }

  // ---- 导出按钮 ----
  var shareBtn=document.getElementById("chShare");
  if(shareBtn)shareBtn.addEventListener("click",exportImage);
  var exBtn=document.getElementById("chExport");
  if(exBtn)exBtn.addEventListener("click",function(){
    downloadText("d2r-chronicle-backup-"+nowStr()+".json",buildJson(),"application/json");
  });

  // 测试钩子（纯逻辑，不改变页面状态）
  window.__chronicleIO={
    buildJson:buildJson,parseJsonImport:parseJsonImport,
    applyImport:applyImport,handleImportText:handleImportText,
    fullStats:fullStats,runeSummary:runeSummary,
    drawShareCard:drawShareCard,exportImage:exportImage,
    knownIds:knownIds,nowStr:nowStr
  };

  applyFilter();
})();
'''

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
CLASS_LIST = [
    ("amazon", "亚马逊", "Amazon"),
    ("sorceress", "法师", "Sorceress"),
    ("necromancer", "亡灵法师", "Necromancer"),
    ("paladin", "圣骑士", "Paladin"),
    ("barbarian", "野蛮人", "Barbarian"),
    ("druid", "德鲁伊", "Druid"),
    ("warlock", "术士", "Warlock"),
    ("assassin", "刺客", "Assassin"),
]
GUIDE_LIST = [
    ("runewords", "符文之语图鉴", "Runewords"),
    ("leveling", "练级与开荒", "Leveling & Early Game"),
    ("terror-zones", "恐怖地带 & Sunder", "Terror Zones & Sunder"),
    ("uber", "Uber 终局", "Uber Endgame"),
    ("tips", "综合技巧", "General Tips"),
    ("farming", "速刷与 MF 指南", "Farming & MF Guide"),
]

def nav_html(depth, active):
    p = "../" if depth else ""
    parts = ['<a href="' + p + 'index.html"' + (' class="active"' if active == "home" else "") + '>' + bi("首页", "Home") + '</a>']
    parts.append('<a href="' + p + 'classes/amazon.html"' + (' class="active"' if active.startswith("c:") else "") + '>' + bi("职业", "Classes") + '</a>')
    parts.append('<a href="' + p + 'guides/runewords.html"' + (' class="active"' if active.startswith("g:") else "") + '>' + bi("攻略", "Guides") + '</a>')
    parts.append('<a href="' + p + 'chronicle.html"' + (' class="active"' if active == "chronicle" else "") + '>' + bi("编年史", "Chronicle") + '</a>')
    return '<nav class="topbar" aria-label="主导航"><div class="wrap"><div class="brand"><span class="dot"></span> ' + bi("暗黑 II 攻略站", "Diablo II Guide") + '</div>' \
           '<button class="menu-toggle" aria-label="菜单">☰</button><div class="navlinks">' + "".join(parts) + '</div></div></nav>'

def sidebar_html(depth, active):
    p = "../" if depth else ""
    out = ['<aside class="sidebar" aria-label="站点导航"><div class="grp"><h4>' + bi("职业 Classes", "Classes") + '</h4>']
    for cid, cn, en in CLASS_LIST:
        cls = ' class="active"' if active == "c:" + cid else ""
        out.append('<a href="' + p + 'classes/' + cid + '.html"' + cls + '>' + bi(cn, en) + '</a>')
    out.append('</div><div class="grp"><h4>' + bi("攻略 Guides", "Guides") + '</h4>')
    for gid, name, en in GUIDE_LIST:
        cls = ' class="active"' if active == "g:" + gid else ""
        out.append('<a href="' + p + 'guides/' + gid + '.html"' + cls + '>' + bi(name, en) + '</a>')
    out.append('</div><div class="grp"><h4>' + bi("收藏 Collection", "Collection") + '</h4>')
    out.append('<a href="' + p + 'chronicle.html"' + (' class="active"' if active == "chronicle" else "") + '>' + bi("编年史 Checklist", "Chronicle") + '</a>')
    out.append('</div></aside>')
    return "".join(out)

SITE_URL = "https://kingsir.work/D2/"
SITE_NAME = "暗黑破坏神 II：复活攻略站"
SITE_NAME_EN = "Diablo II: Resurrected Guide"
SITE_DESC = "Diablo II: Resurrected 全职业加点与流派攻略的中英双语静态站，零依赖零构建，打开即用。"
OG_IMAGE = SITE_URL + "docs/og-image.png"
OG_IMAGE_ALT = "暗黑破坏神 II：复活攻略站 · 职业总览与攻略入口"

HOME_DESC = "暗黑破坏神 II：复活（D2R）全职业攻略站：八大职业技能树加点、主流流派 Build、装备思路与开荒/终局技巧，附符文之语图鉴、恐怖地带、Uber 终局与速刷 MF 指南。已同步 Patch 3.3 / 天梯第 15 赛季，中英双语、纯静态零依赖。"
HOME_KW = "暗黑破坏神2,暗黑2重制版,Diablo II Resurrected,D2R,职业加点,流派Build,符文之语,恐怖地带"

CLASS_DESC = {
    "amazon": "亚马逊（Amazon）暗黑2重制版攻略：标枪亚马逊 Javazon 与弓亚马逊 Bowazon 的技能加点、属性点分配、核心装备搭配与电免处理要点，含 Lightning Fury 流派的加点思路，适配 Patch 3.3。",
    "sorceress": "法师（Sorceress）暗黑2重制版攻略：暴风雪/冰封球纯冰法、闪电新星法与火冰双修的技能加点、FCR 档位、MF 配装与瞬移手感优化，开荒最速职业，适配 Patch 3.3。",
    "necromancer": "亡灵法师（Necromancer）暗黑2重制版攻略：召唤流、毒亡灵法师与骨系的技能加点、尸体爆炸清场、破免与 MF 配置，单人通关最省心职业，适配 Patch 3.3。",
    "paladin": "圣骑士（Paladin）暗黑2重制版攻略：祝福之锤 Hammerdin、热诚 Zealot 与天堂之拳/盾击的技能加点、FCR 与抗性档位、廉价开荒配装，新手首选职业，适配 Patch 3.3。",
    "barbarian": "野蛮人（Barbarian）暗黑2重制版攻略：旋风 Whirlwind、狂乱 Frenzy、寻物 Pitzerker 与战吼 Singing 的技能加点、武器选择、AR 与 MF 平衡思路，适配 Patch 3.3。",
    "druid": "德鲁伊（Druid）暗黑2重制版攻略：风德、火德与狼人狂怒变身的技能加点、破免前的ç ´免思路、武器攻速档位与佣兵搭配，适配 Patch 3.3。",
    "warlock": "术士（Warlock）暗黑2重制版攻略：2026 资料片第八职业 Chaos / Eldritch / Demon 三系技能树、Sigil: Death 主推流派、束缚恶魔辅助定位与 Patch 3.3 修正说明。",
    "assassin": "刺客（Assassin）暗黑2重制版攻略：陷阱 Trapsin、马赛克 Mosaic 武学与飞刀的技能加点、IAS 档位、无限 Anya 项链等核心装备与破免配法，适配 Patch 3.3。",
}
CLASS_KW = {
    "amazon": "亚马逊,Amazon,Javazon,标枪亚马逊,加点,流派",
    "sorceress": "法师,Sorceress,暴风雪,冰封球,法师加点,MF",
    "necromancer": "亡灵法师,Necromancer,召唤流,骨系,尸体爆炸,加点",
    "paladin": "圣骑士,Paladin,祝福之锤,Hammerdin,新手职业,加点",
    "barbarian": "野蛮人,Barbarian,旋风,Whirlwind,寻物,战吼,加点",
    "druid": "德鲁伊,Druid,风德,狼人变化,加点",
    "warlock": "术士,Warlock,Sigil Death,新职业,2026资料片,加点",
    "assassin": "刺客,Assassin,陷阱,Mosaic,马赛克,武学,加点",
}

GUIDE_DESC = {
    "runewords": "符文之语图鉴：常用符文之语配方、符文序号、底材与孔数需求、适用职业与定位速查，含天梯专属轮换到非天梯的说明，一张表格看全部。",
    "leveling": "练级与开荒指南：1-85 级路线规划、效率练级点、Patch 3.3 加强后的练级暗金推荐与开荒职业起步流程。",
    "terror-zones": "恐怖地带与破免护符攻略：恐怖地带解锁与轮换规则、等级随动机制、Herald of Terror 掉落优先级，以及六系破免护符的获取条件与 Patch 3.3 改动。",
    "uber": "Uber 终局攻略：钥匙与传送门获取、三大 Uber boss 打法、盾击 Smiter 配装与抗性堆叠要求、掉落的暗金与地狱火炬属性。",
    "tips": "综合技巧汇总：技能与属性点重置（赦罪令牌 / 赫拉迪克方块）、方块合成配方、掉落与 MF 常识、常用交易术语与暗语速查。",
    "farming": "速刷与 MF 指南：85 场景推荐表、纯冰法高 MF 配装模板、佣兵 Infinity 破冰免、劳模/安姐/暗黑速刷循环与卓古拉之握掉落路线。",
}
GUIDE_KW = {
    "runewords": "符文之语,Runewords,配方,Ist,Ber,Mosaic,底材",
    "leveling": "练级,开荒,1-85级,练级路线,练级暗金",
    "terror-zones": "恐怖地带,Terror Zones,破免护符,Sunder Charms,Herald of Terror",
    "uber": "Uber,Uber终局,地狱火炬,Smiter,盾击,超级boss",
    "tips": "综合技巧,赫拉迪克方块,重置属性,赦罪令牌,交易术语,MF常识",
    "farming": "速刷,MF,Magic Find,85场景,劳模,安姐,卓古拉之握",
}

CHRONICLE_DESC = ("暗黑破坏神 II：复活（D2R）收藏编年史：99 条符文之语配方、34 套套装共 135 件部件与 388 件独特道具"
                  "打勾清单，逐条记录你已获得的收藏，分类进度条统计完成度。打勾数据仅保存在浏览器本地（localStorage），不上传服务器。")
CHRONICLE_KW = "暗黑2,Diablo2收藏清单,D2R符文之语,D2R套装,D2R暗金,编年史,收集进度,localStorage"

def _esc_attr(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def _page_rel(active):
    if active.startswith("c:"):
        return "classes/" + active[2:] + ".html"
    if active.startswith("g:"):
        return "guides/" + active[2:] + ".html"
    if active == "chronicle":
        return "chronicle.html"
    return ""

def seo_meta(depth, active, title, en_t, desc, keywords):
    """每页唯一的 description / canonical / Open Graph / Twitter Card / JSON-LD。"""
    p = "../" if depth else ""
    rel = _page_rel(active)
    url = SITE_URL + rel
    pg_name = _esc_attr(title)
    pg_desc = _esc_attr(desc)
    crumbs = [("首页", SITE_URL)]
    if rel == "chronicle.html":
        crumbs.append(("收藏", ""))
        crumbs.append(("编年史", ""))
    elif rel:
        if rel.startswith("classes/"):
            cid = rel[len("classes/"):-5]
            nm = next((n for c, n, e in CLASS_LIST if c == cid), "职业")
            crumbs.append(("职业", ""))
        else:
            gid = rel[len("guides/"):-5]
            nm = next((n for g, n, e in GUIDE_LIST if g == gid), "攻略")
            crumbs.append(("攻略", ""))
        label = _esc_attr(nm)
        crumbs.append((label, ""))
    items = []
    for i, (nm, href) in enumerate(crumbs, 1):
        it = '{"@type":"ListItem","position":%d,"name":"%s"' % (i, _esc_attr(nm))
        if href:
            it += ',"item":"%s"' % href
        items.append(it + "}")
    graph = [
        '{"@type":"WebSite","@id":"%s#website","url":"%s","name":"%s","description":"%s","inLanguage":["zh-CN","en-US"],"publisher":{"@id":"%s#organization"}}' % (
            SITE_URL, SITE_URL, _esc_attr(SITE_NAME), _esc_attr(SITE_DESC), SITE_URL),
        '{"@type":"Organization","@id":"%s#organization","name":"%s","url":"%s"}' % (
            SITE_URL, _esc_attr(SITE_NAME), SITE_URL),
        '{"@type":"WebPage","@id":"%s","url":"%s","name":"%s","description":"%s","isPartOf":{"@id":"%s#website"},"inLanguage":["zh-CN","en-US"],"breadcrumb":{"@id":"%s#breadcrumb"}}' % (
            url, url, pg_name, pg_desc, SITE_URL, url),
        '{"@type":"BreadcrumbList","@id":"%s#breadcrumb","itemListElement":[%s]}' % (url, ",".join(items)),
    ]
    ld = '<script type="application/ld+json">{"@context":"https://schema.org","@graph":[' + ",".join(graph) + "]}</script>"
    og_type = "website" if not rel else "article"
    return (''  # canonical
            '<link rel="canonical" href="' + url + '">\n'
            '<meta name="description" content="' + pg_desc + '">\n'
            '<meta name="keywords" content="' + _esc_attr(keywords) + '">\n'
            '<meta name="robots" content="index,follow,max-image-preview:large">\n'
            '<meta name="theme-color" content="#0c0a09">\n'
            '<link rel="icon" href="' + p + 'favicon.svg" type="image/svg+xml">\n'
            '<link rel="apple-touch-icon" href="' + p + 'docs/apple-touch-icon.png">\n'
            # Open Graph
            '<meta property="og:type" content="' + og_type + '">\n'
            '<meta property="og:site_name" content="' + _esc_attr(SITE_NAME) + '">\n'
            '<meta property="og:locale" content="zh_CN">\n'
            '<meta property="og:locale:alternate" content="en_US">\n'
            '<meta property="og:url" content="' + url + '">\n'
            '<meta property="og:title" content="' + pg_name + '">\n'
            '<meta property="og:description" content="' + pg_desc + '">\n'
            '<meta property="og:image" content="' + OG_IMAGE + '">\n'
            '<meta property="og:image:alt" content="' + _esc_attr(OG_IMAGE_ALT) + '">\n'
            # Twitter / X
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="twitter:title" content="' + pg_name + '">\n'
            '<meta name="twitter:description" content="' + pg_desc + '">\n'
            '<meta name="twitter:image" content="' + OG_IMAGE + '">\n'
            '<meta name="twitter:image:alt" content="' + _esc_attr(OG_IMAGE_ALT) + '">\n'
            + ld + '\n')

def page(title, depth, body, active, sub_layout=False, desc="", en_t=None, keywords=""):
    p = "../" if depth else ""
    nav = nav_html(depth, active)
    side = sidebar_html(depth, active) if sub_layout else ""
    if sub_layout:
        main_open = '<div class="layout">' + side + '<main class="content">'
        main_close = '</main></div>'
    else:
        main_open = '<main class="home"><div class="wrap" style="padding:30px 18px 60px">'
        main_close = '</div></main>'
    foot = '<footer><div class="wrap"><span>' + bi("暗黑破坏神 II：复活 · 静态攻略站", "Diablo II: Resurrected · Static Guide") + '</span>' \
           '<span>' + bi("基于 D2R 最新 meta（Sunder Charms / Terror Zones / Mosaic 等）整理", "Built around the latest D2R meta (Sunder Charms / Terror Zones / Mosaic Runewords, Ladder seasons).") + '</span></div>' \
           '<div class="wrap disc"><span>' + bi("非官方粉丝站 · 与暴雪娱乐无关。Diablo / Diablo II: Resurrected 为 Blizzard Entertainment, Inc. 的商标，本站仅作指示性引用。", "Unofficial fan site, not affiliated with Blizzard Entertainment. Diablo / Diablo II: Resurrected are trademarks of Blizzard Entertainment, Inc.; used here for identification only.") + '</span><br />' \
           + '<span class="zt"><a class="zc repo" href="https://github.com/isnotry/D2" target="_blank" rel="noopener noreferrer">GitHub 开源仓库</a><a class="ec repo" href="https://github.com/isnotry/D2" target="_blank" rel="noopener noreferrer">Open source on GitHub</a></span></div></footer>'
    raw_title = title
    body = zh(body)
    body = rune_no(body)
    et = en_t or en_title(raw_title)
    seo = seo_meta(depth, active, raw_title, et, desc or SITE_DESC, keywords or HOME_KW)
    return "<!DOCTYPE html>\n<html lang=\"zh-CN\" data-en-title=\"" + _esc_attr(et) + "\">\n<head>\n<meta charset=\"utf-8\">\n" \
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n<title>" + raw_title + "</title>\n" \
           + seo + \
           "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n" \
           "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n" \
           "<link href=\"https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Noto+Sans+SC:wght@400;500;700&display=swap\" rel=\"stylesheet\">\n" \
           "<link rel=\"stylesheet\" href=\"" + p + "css/style.css\">\n</head>\n<body>\n" + nav + "\n" \
           + main_open + "\n" + body + "\n" + main_close + "\n" + foot + "\n" \
           "<script src=\"" + p + "js/main.js\"></script>\n</body>\n</html>"

def build_card(title, badge, summary, skill_rows, stat_rows, gear_items, tip_items):
    sk = "".join("<tr><td>%s</td><td>%s</td></tr>" % (k, v) for k, v in skill_rows)
    st = "".join("<tr><td>%s</td><td>%s</td></tr>" % (k, v) for k, v in stat_rows)
    gear = "".join("<li>%s</li>" % g for g in gear_items)
    tips = "".join("<li>%s</li>" % t for t in tip_items)
    return "\n<div class=\"card\">\n  <span class=\"badge\">" + badge + "</span>\n  <h3>" + title + "</h3>\n" \
           "  <p style=\"color:var(--muted)\">" + summary + "</p>\n  <div class=\"two\">\n    <div>\n" \
           "      <h4 style=\"color:var(--gold2)\">" + bi("技能加点", "Skills") + "</h4>\n      <table><tbody>" + sk + "</tbody></table>\n" \
           "    </div>\n    <div>\n      <h4 style=\"color:var(--gold2)\">" + bi("属性加点", "Stats") + "</h4>\n      <table><tbody>" + st + "</tbody></table>\n" \
           "    </div>\n  </div>\n  <div class=\"two\" style=\"margin-top:6px\">\n    <div>\n" \
           "      <h4 style=\"color:var(--gold2)\">" + bi("核心装备", "Core Gear") + "</h4>\n      <ul class=\"clean\">" + gear + "</ul>\n" \
           "    </div>\n    <div>\n      <h4 style=\"color:var(--gold2)\">" + bi("玩法要点", "Playstyle Tips") + "</h4>\n      <ul class=\"clean\">" + tips + "</ul>\n" \
           "    </div>\n  </div>\n</div>"

def skilltrees(trees):
    out = ['<div class="skills">']
    for name, desc, skills in trees:
        li = "".join("<li>%s</li>" % s for s in skills)
        out.append('<div class="skilltree"><h4>' + name + '</h4><p style="color:var(--muted);font-size:13px;margin:0 0 8px">' + desc + '</p><ul>' + li + '</ul></div>')
    out.append('</div>')
    return "".join(out)

SIGIL = '<svg class="sigil" viewBox="0 0 100 100" aria-hidden="true"><polygon points="50,6 61,38 95,38 67,59 78,92 50,71 22,92 33,59 5,38 39,38" fill="none" stroke="#c8a24a" stroke-width="2.5"/><circle cx="50" cy="50" r="6" fill="#a3302e"/></svg>'

# ===========================================================================
# HOME
# ===========================================================================
def home():
    cls_cards = []
    emojis = {"amazon":"🏹","sorceress":"❄️","necromancer":"💀","paladin":"🛡️","barbarian":"🪓","druid":"🐺","warlock":"🔮","assassin":"🗡️"}
    roles = {
        "amazon": bi("远程物理/元素", "Ranged Physical/Elemental"),
        "sorceress": bi("法系爆发/机动", "Caster Burst/Mobility"),
        "necromancer": bi("召唤/毒骨法系", "Summons/Poison & Bone Caster"),
        "paladin": bi("锤丁/辅助", "Hammerdin/Support"),
        "barbarian": bi("近战/呐喊", "Melee/Warcries"),
        "druid": bi("元素/变身", "Elemental/Shapeshifter"),
        "warlock": bi("恶魔/邪术/混沌", "Demon/Eldritch/Chaos"),
        "assassin": bi("陷阱/武学", "Traps/Martial Arts"),
    }
    for cid, cn, en in CLASS_LIST:
        cls_cards.append('<a class="cls-card" href="classes/' + cid + '.html"><div class="em">' + emojis[cid] + '</div><h3><span class="zt"><span class="zc">' + cn + ' </span><span class="ec" lang="en">' + en + '</span></span></h3><p><span class="role">' + roles[cid] + '</span></p></a>')
    feat = [
        ("☀️ " + bi("破免护符", "Sunder Charms"), "",
         bi("六系破免大型护符（火/冰/电/毒/物理/魔法），打破怪物免疫，让更多流派能 farm 全图。<b>3.3 补丁起</b>获取门槛提高：潜伏破免最低掉落等级 69→75，靠 Magic Find 刷取掉率下调且<b>仅限地狱难度</b>。",
            "Six Grand Charms (Fire/Cold/Lightning/Poison/Physical/Magic) that break monster immunities, letting far more builds farm every zone. <b>Since patch 3.3</b> they are harder to get: the Latent Sunder minimum drop level went 69→75, and Magic Find drops were reduced and are now <b>Hell-only</b>.")),
        ("🌑 " + bi("恐怖地带", "Terror Zones"), "",
         bi("击败对应难度 Baal 后解锁，每小时轮换，怪物等级随你提升。<b>3.3 补丁</b>把 <b>Herald of Terror</b>（恐惧先驱）3 层以上的稀有及以上掉率调高，掉落重心从堆 MF 转向打 Herald。",
            "Unlocked after killing Baal on that difficulty. Zones rotate hourly and monster levels scale with you. <b>Patch 3.3</b> raised the Rare-or-better drop rate on tier-3+ <b>Heralds of Terror</b>, shifting rewards from stacking MF toward actually fighting Heralds.")),
        ("🔮 " + bi("术士君临", "Reign of the Warlock"), "",
         bi("2026 年资料片加入的第八职业<b>术士 Warlock</b>，Chaos / Eldritch / Demon 三系。<b>3.3 补丁</b>修正 Sigil: Death（失败不再耗蓝、火焰技能加成生效）后成为术士主推；束缚恶魔伤害被下修，转辅助定位。",
            "The 2026 expansion added the eighth class, the <b>Warlock</b>, with Chaos / Eldritch / Demon trees. <b>Patch 3.3</b> fixed Sigil: Death (no mana burn on failed casts, fire-skill bonuses now apply), making it the class's top build; Bind Demon damage was tuned down into a support role.")),
        ("⚔️ " + bi("练级暗金重做", "Leveling Uniques Reworked"), "",
         bi("3.3 补丁集中加强一批冷门低级暗金：Bloodletter 加跑速、The Battlebranch 需求等级 25→17、Bane Ash 改施法速度、Blinkbat's Form 跑速翻倍、The Ward 自带一孔，天使之袍全套额外 <b>+1 全技能</b>。",
            "Patch 3.3 buffed a batch of overlooked low-level uniques: Bloodletter gains run speed, The Battlebranch's required level drops 25→17, Bane Ash pivots to cast rate, Blinkbat's Form doubles its run speed, The Ward comes with a socket, and full Angelic Raiment adds <b>+1 to all skills</b>.")),
        ("🧿 " + bi("赛季符文之语轮转", "Seasonal Runeword Rotation"), "",
         bi("上一批天梯专属符文之语 Mania、Hysteria、Metamorphosis、Ground、Temper、Hearth、Cure、Bulwark 已在第 15 赛季<b>开放给非天梯</b>；本赛季另有经过平衡调整的<b>新版天梯专属</b>替换。",
            "Last expansion's ladder-only runewords — Mania, Hysteria, Metamorphosis, Ground, Temper, Hearth, Cure and Bulwark — are now <b>available in non-ladder</b> for Season 15; this season ships rebalanced <b>new ladder-only versions</b> instead.")),
        ("🏆 " + bi("天梯第 15 赛季", "Ladder Season 15"), "",
         bi("2026 年 8 月 21 日开启（3.3 补丁同步上线）。定期重置的天梯赛季，冲级、竞速、专属奖励，是新 meta 的试验场。",
            "Opened 21 August 2026 alongside patch 3.3. Ladder seasons reset periodically — leveling races, speed runs and ladder-only rewards make them the proving ground for every new meta.")),
    ]
    feat_cards = "".join('<div class="card"><h3>' + a + '</h3><p style="color:var(--muted)">' + c + '</p></div>' for a, b, c in feat)
    guides = [
        ("📜", bi("符文之语图鉴", "Runewords Codex"),
         bi("经典与新版符文之语汇总", "Classic and new runewords in one table"), "guides/runewords.html"),
        ("⚔️", bi("练级与开荒", "Leveling & Early Game"),
         bi("1-99 路线与效率点", "1–99 route and the most efficient spots"), "guides/leveling.html"),
        ("🌑", bi("恐怖地带 & Sunder", "Terror Zones & Sunder"),
         bi("破免护符与刷图", "Sunder Charms and where to farm"), "guides/terror-zones.html"),
        ("👹", bi("Uber 终局", "Uber Endgame"),
         bi("超级 boss 与暗金", "Uber bosses and their uniques"), "guides/uber.html"),
        ("💡", bi("综合技巧", "General Tips"),
         bi("重置、配方、交易等", "Respecs, cube recipes, trading and more"), "guides/tips.html"),
        ("🪙", bi("速刷与 MF 指南", "Farming & MF Guide"),
         bi("纯冰法速刷与暗金路线", "Pure cold sorc farming and unique-hunting routes"), "guides/farming.html"),
        ("🛡️", bi("新手推荐", "Beginner Pick"),
         bi("从祝福之锤圣骑士入手", "Start with the Hammerdin"), "classes/paladin.html"),
    ]
    guide_cards = "".join('<a class="cls-card" href="' + u + '"><div class="em">' + e + '</div><h3>' + t + '</h3><p>' + d + '</p></a>' for e, t, d, u in guides)
    body = ""
    body += '<section class="hero"><div class="wrap">\n' + SIGIL + '\n<h1>' \
            + bi("暗黑破坏神 II：复活", "Diablo II: Resurrected") + '</h1>\n' \
            '<p class="sub">' \
            + bi("Diablo II: Resurrected 全职业玩法加点 · 流派 Build · 游戏技巧静态攻略站。涵盖八大职业的详细技能树、主流流派、装备思路与开荒/终局技巧。已同步 <b>Patch 3.3 / 天梯第 15 赛季</b>。",
                 "A static Diablo II: Resurrected guide site for skill allocation, builds and gameplay tips — detailed skill trees, meta builds, gear plans and leveling/endgame tricks for all eight classes. Updated for <b>Patch 3.3 / Ladder Season 15</b>.") \
            + '</p>\n' \
            '<div style="margin-top:18px">\n  <a class="btn" href="classes/amazon.html">' \
            + bi("浏览职业", "Browse Classes") + '</a>\n' \
            '  <a class="btn" href="guides/runewords.html">' \
            + bi("符文之语图鉴", "Runewords Codex") + '</a>\n</div>\n</div></section>\n'
    body += '<div class="wrap" style="padding:34px 18px 10px">\n' \
            '  <h2 class="section-id" id="feat">' + bi("当前版本核心机制", "Core Mechanics This Patch") + ' <small style="font-weight:400;color:var(--muted)">· ' + bi("Patch 3.3 / 天梯第 15 赛季（2026-08-21 开启）", "Patch 3.3 / Ladder Season 15 (opened 21 Aug 2026)") + '</small></h2>\n  <div class="grid cols2">' + feat_cards + '</div>\n' \
            '  <h2 class="section-id" id="classes" style="margin-top:30px">' + bi("八大职业总览", "All Eight Classes") + '</h2>\n  <div class="grid cls">' + "".join(cls_cards) + '</div>\n' \
            '  <h2 class="section-id" id="guides" style="margin-top:30px">' + bi("攻略专题", "Guide Topics") + '</h2>\n  <div class="grid cols3">' + guide_cards + '</div>\n' \
            '  <div class="callout info" style="margin-top:30px">\n    <b>' \
            + bi("关于本攻略：", "About this guide:") + '</b>' \
            + bi("内容基于 D2R <b>Patch 3.3 / 天梯第 15 赛季</b>（2026-08-21 开启）的 meta 整理：破免获取被推回地狱难度、Herald 掉落上位、练级暗金集体加强、上一批天梯符文之语转入非天梯、术士经历一轮修正。偏向 PvM 单人/组队开荒与终局 farm。技能与属性点现在均可重置（赦罪令牌 / 工坊），大胆尝试不同流派即可。",
                 "Everything here is built around the <b>Patch 3.3 / Ladder Season 15</b> meta (opened 21 Aug 2026): Sunder access pushed back into Hell, Heralds promoted as the farming target, leveling uniques buffed across the board, last season's ladder runewords moved to non-ladder, and the Warlock going through a round of corrections. The focus is PvM — solo/party progression and endgame farming. Skills and stats can be respecced freely (Token of Absolution / Horadric Cube), so feel free to experiment with builds.") \
            + '\n  </div>\n</div>\n'
    return page("暗黑破坏神 II：复活攻略站 · 全职业加点与流派 Build", 0, body, "home",
                desc=HOME_DESC, en_t="Diablo II: Resurrected Guide — Builds, Skills & Tips", keywords=HOME_KW)

# ===========================================================================
# CLASS PAGES
# ===========================================================================
def _class_page(title, active, intro, trees, builds, tips_html, prev_href, prev_name, next_href, next_name):
    _pn = prev_name if prev_name.startswith("<") else _wrap_name(prev_name)
    _nn = next_name if next_name.startswith("<") else _wrap_name(next_name)
    pager = '<div class="pager"><a href="' + prev_href + '">' + _pn + bi("上一页", "Previous") + '</a>' \
            '<a href="' + next_href + '">' + _nn + bi("下一页", "Next") + '</a></div>'


    _cid = active.split(":", 1)[1] if active.startswith("c:") else ""
    _cn = _en = title
    for _c, _n, _e in CLASS_LIST:
        if _c == _cid:
            _cn, _en = _n, _e
            break
    _crumb = '<span class="zt"><span class="zc">%s </span><span class="ec" lang="en">%s</span></span>' % (_cn, _en)
    body = '<div class="breadcrumb"><a href="../index.html">' + bi("首页", "Home") + '</a> / ' + _crumb + '</div>\n' \
           + intro + '\n<h2 class="section-id" id="trees">' + bi("技能树", "Skill Trees") + '</h2>\n' + trees + '\n' \
           + '<h2 class="section-id" id="builds">' + bi("主流流派", "Meta Builds") + '</h2>\n' + builds + '\n' \
           + '<h2 class="section-id" id="tips">' + bi("开荒与通用技巧", "Progression & General Tips") + '</h2>\n' + tips_html + '\n' + pager
    return page(_cn + "（" + _en + "）加点与流派 Build · 暗黑破坏神 II 攻略站", 1, body, active, True,
                desc=CLASS_DESC.get(_cid, SITE_DESC), en_t=_en + " Builds & Skill Guide | Diablo II: Resurrected",
                keywords=CLASS_KW.get(_cid, HOME_KW))


def _wrap_name(name):
    """把「中文 English」分页名包成可切换 span（无空格则原样返回）。"""
    if " " in name:
        cn, en = name.split(" ", 1)
        return '<span class="zt"><span class="zc">%s </span><span class="ec" lang="en">%s</span></span>' % (cn, en)
    return name

def amazon():
    intro = '<h1><span class="zt"><span class="zc">亚马逊 </span><span class="ec" lang="en">Amazon</span></span></h1>\n' \
            '<p>' + bi("亚马逊是远程输出的多面手，三大系分别对应 <b>标枪/长矛</b>、<b>弓/十字弓</b> 与 <b>被动闪避</b>。她拥有游戏里最强的范围电系输出（Lightning Fury），同时被动系提供极高生存，是最适合开荒与终局 farm 的职业之一。",
                       "The Amazon is the all-round ranged damage dealer. Her three trees cover <b>Javelin/Spear</b>, <b>Bow/Crossbow</b> and <b>passive evasion</b>. She has the best AoE lightning damage in the game (Lightning Fury) while her passives give huge survivability, making her one of the best classes for both progression and endgame farming.") + '</p>\n' \
            '<div class="callout tip"><b>' + bi("定位：", "Role:") + '</b>' \
            + bi("远程物理/元素输出 · 优势：高机动、高生存、Lightning Fury 清屏极强 · 劣势：单体 boss 与电免处理需要 Infinity/破免。",
                 "Ranged physical/elemental damage · Pros: high mobility, high survivability, Lightning Fury shreds packs · Cons: single-target bosses and lightning immunes need Infinity/Sunder.") + '</div>'
    trees = skilltrees([
        ("Javelin & Spear", bi("以闪电之怒为核心的范围电系爆发，兼具体伤。", "AoE lightning burst built around Lightning Fury, with solid single-target too."),
         [bi("Lightning Fury（21 级可学，核心 AoE）", "Lightning Fury (level 21, core AoE)"),
          bi("Charged Strike（单体电系）", "Charged Strike (single-target lightning)"),
          "Power Strike / Lightning Strike",
          bi("Poison Javelin（备选）", "Poison Javelin (optional)"), "Plague Javelin"]),
        ("Bow & Crossbow", bi("物理/冰远程路线，依赖高伤弓与攻速。", "Physical/cold ranged route that relies on a high-damage bow and IAS breakpoints."),
         ["Freezing Arrow", "Multishot / Strafe", "Guided Arrow / Immolation Arrow",
          bi("Magic Arrow（省箭）", "Magic Arrow (saves arrows)")]),
        ("Passive & Magic", bi("提供闪避、暴击与雇佣兵增益，是生存核心。", "Evasion, crits and Valkyrie support — the core of her survivability."),
         [bi("Dodge / Evade / Avoid（三闪）", "Dodge / Evade / Avoid (the three D/E/A)"), "Critical Strike",
          bi("Penetration（AR）", "Penetration (attack rating)"), "Valkyrie", "Decoy / Slow Missiles"]),
    ])
    builds = build_card(
        bi("标枪亚马逊", "Javelin Amazon"),
        bi("S 级 · 范围电系", "S-Tier · AoE Lightning"),
        bi("游戏最强清屏流派之一。Lightning Fury 对成群敌人造成毁灭性电伤，Charged Strike 处理单体 boss；不吃命中率，开荒到终局通吃。",
           "One of the strongest screen-clearing builds in the game. Lightning Fury deals devastating lightning damage to packed enemies while Charged Strike handles single bosses; it ignores attack rating and works from leveling all the way to endgame."),
        [("Lightning Fury", "20"), ("Charged Strike", "20"),
         (bi("Lightning Strike（协同）", "Lightning Strike (synergy)"), "0~20"),
         (bi("Power Strike（协同）", "Power Strike (synergy)"), "0~20"),
         ("Valkyrie", bi("1（或 17+）", "1 (or 17+)")),
         ("Dodge/Evade/Avoid", bi("各 1", "1 each")),
         ("Critical Strike", "1"), ("Decoy", "1"),
         (bi("其余→协同/女武神", "Rest → synergies/Valkyrie"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备（约 100-156）", "Just enough for gear (≈100–156)")),
         (bi("敏捷", "Dexterity"), bi("刚好穿装备或堆格挡", "Enough for gear, or stack block")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("不加（靠装备/吸蓝）", "None (gear/mana leech)"))],
        [bi("武器：Titan's Revenge（泰坦标枪）", "Weapon: Titan's Revenge"),
         bi("头盔：Griffon's Eye（电珠） / +2 标枪头环", "Helm: Griffon's Eye (lightning facet) / +2 javelin circlet"),
         bi("项链：Mara's Kaleidoscope / 高施项链", "Amulet: Mara's Kaleidoscope / caster amulet"),
         bi("腰带：Razortail（穿刺）", "Belt: Razortail (pierce)"),
         bi("戒指：SoJ + 婚戒 / 乌鸦", "Rings: SoJ + Bul-Kathos' Wedding Band / Raven Frost"),
         bi("甲：Enigma / Chains of Honor", "Armor: Enigma / Chains of Honor"),
         bi("手套：+标枪技能手套", "Gloves: +javelin skill gloves"),
         bi("雇佣兵：力量光环（Might）/ Infinity 破免", "Merc: Might aura / Infinity to break immunes")],
        [bi("进门先放 Valkyrie 与 Decoy 拉怪", "Drop Valkyrie and Decoy on entry to pull aggro"),
         bi("队形密集时放 Lightning Fury 一次清场", "When enemies bunch up, one Lightning Fury clears the screen"),
         bi("boss 用 Charged Strike 贴脸输出", "Use Charged Strike point-blank on bosses"),
         bi("配 Infinity 雇佣兵 + 闪电 Sunder 处理电免", "Pair an Infinity merc with a Lightning Sunder for lightning immunes"),
         bi("Pet/怪贴脸时靠三闪与女武神保命", "Rely on Dodge/Evade/Avoid and the Valkyrie when you get swarmed")],
    )
    builds += build_card(
        bi("弓亚马逊", "Bow Amazon"),
        bi("A 级 · 物理/冰远程", "A-Tier · Physical/Cold Ranged"),
        bi("以 Freezing Arrow 控场、Multishot/Strafe 输出的物理路线，手感爽快但装备门槛较高，需要高伤弓与攻速档位支撑。",
           "A physical route that locks packs down with Freezing Arrow and burns them with Multishot/Strafe. It feels great but is gear hungry — you need a high-damage bow and the right IAS breakpoints."),
        [("Freezing Arrow", "20"), (bi("Cold Arrow（协同）", "Cold Arrow (synergy)"), "1"),
         ("Multishot / Strafe", "20"),
         (bi("Guided Arrow（协同）", "Guided Arrow (synergy)"), "0~20"),
         ("Critical Strike", "1+"), ("Dodge/Evade/Avoid", bi("各 1", "1 each")),
         ("Valkyrie", "1+"), ("Penetration", "1+"),
         (bi("其余→协同", "Rest → synergies"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("堆到命中/格挡需求，其余加敏提伤害", "Up to the AR/block you need, then more Dex for damage")),
         (bi("体力", "Vitality"), bi("保证生存", "Enough to stay alive")),
         (bi("能量", "Energy"), bi("不加", "None"))],
        [bi("武器：Windforce / Faith 符文之语弓", "Weapon: Windforce / a Faith runeword bow"),
         bi("头盔：Stealskull / Andariel's Visage / 头环", "Helm: Stealskull / Andariel's Visage / circlet"),
         bi("甲：Fortitude / Chains of Honor", "Armor: Fortitude / Chains of Honor"),
         bi("腰带：Razortail（穿刺）", "Belt: Razortail (pierce)"),
         bi("弓袋：配合高伤箭", "Quiver: high-damage arrows"),
         bi("戒指：Raven Frost（防冻）+ 婚戒", "Rings: Raven Frost (cannot be frozen) + Bul-Kathos' Wedding Band"),
         bi("手套：配合 IAS 与弓技", "Gloves: IAS plus bow skills")],
        [bi("注意武器攻速（IAS）档位", "Mind your weapon IAS breakpoints"),
         bi("Freezing Arrow 控场后 Multishot 输出", "Lock packs with Freezing Arrow, then burst with Multishot"),
         bi("冰免怪切 Guided Arrow 或物理", "Swap to Guided Arrow or pure physical against cold immunes"),
         bi("需配合破物/破冰护符处理免疫", "Use a Physical/Cold Sunder Charm for immunes"),
         bi("生存靠走位与三闪，别硬刚", "Survive by kiting and Dodge/Evade/Avoid — never tank")],
    )
    tips = '<div class="card"><ul class="clean">' \
           '<li><b>' + bi("Javazon 起步最稳：", "Javazon is the safest start:") + '</b>' \
           + bi("前期用 Power Strike / Charged Strike 清场，30 级后转 Lightning Fury，配合 Titans 标枪即可横扫。",
                "Use Power Strike / Charged Strike early, switch to Lightning Fury at level 30, and with Titan's Revenge you steamroll everything.") + '</li>' \
           '<li><b>' + bi("破电免：", "Breaking lightning immunes:") + '</b>' \
           + bi("终局建议配 Infinity（惩罚）雇佣兵 + 闪电 Sunder Charm，几乎无盲点。",
                "For endgame run an Infinity merc (Conviction) plus a Lightning Sunder Charm and almost nothing resists you.") + '</li>' \
           '<li><b>' + bi("被动系必点：", "Always invest in passives:") + '</b>' \
           + bi("Dodge/Evade/Avoid 提供巨额闪避，Valkyrie 是优秀肉盾，建议至少 1 点。",
                "Dodge/Evade/Avoid give huge evasion and the Valkyrie is a great meat shield — at least 1 point each.") + '</li>' \
           '<li><b>' + bi("标枪无 AR 需求：", "Javelins need no attack rating:") + '</b>' \
           + bi("Lightning Fury 与 Charged Strike 不吃命中率，开荒体验远好于物理系。",
                "Lightning Fury and Charged Strike ignore AR, which makes leveling far smoother than the physical trees.") + '</li>' \
           '<li><b>' + bi("Bowazon 备选：", "Bowazon as an alternative:") + '</b>' \
           + bi("Freezing Arrow / Multishot（或 Strafe）物理+冰，需要深造武器（Windforce / Faith）与攻速档位。",
                "Freezing Arrow with Multishot (or Strafe) mixes cold and physical, but needs an endgame bow (Windforce / Faith) and proper IAS breakpoints.") + '</li>' \
           '</ul></div>'
    return _class_page("亚马逊 Amazon", "c:amazon", intro, trees, builds, tips, "../index.html", bi("返回首页", "Back to Home"), "sorceress.html", "法师 Sorceress")

def sorceress():
    intro = '<h1><span class="zt"><span class="zc">法师 </span><span class="ec" lang="en">Sorceress</span></span></h1>\n' \
            '<p>' + bi("法师是法系的标杆，唯一拥有 <b>Teleport</b> 的职业，刷图效率与机动性无人能及。三系（冰/电/火）各有强力 build，是开荒、MF 与 boss rush 的核心。她也是新手最推荐的起手职业之一。",
                       "The Sorceress is the benchmark caster and the only class with <b>Teleport</b>, giving her unmatched farming speed and mobility. All three trees (Cold/Lightning/Fire) have strong builds, making her the go-to for progression, MF and boss rushes — and one of the best starter classes for new players.") + '</p>\n' \
            '<div class="callout tip"><b>' + bi("定位：", "Role:") + '</b>' \
            + bi("远程法系爆发 + 传送机动 · 优势：最快刷图、三系皆强、MF 之王 · 劣势：脆皮、遇到对应免疫需副手/佣兵。",
                 "Ranged caster burst with Teleport mobility · Pros: fastest farmer, all three trees are strong, king of MF · Cons: squishy, needs a weapon swap or merc against matching immunes.") + '</div>'
    trees = skilltrees([
        ("Cold", bi("控制与范围兼备，暴风雪是经典开荒王。", "Control plus AoE — Blizzard is the classic progression king."),
         ["Frozen Orb", "Blizzard", bi("Ice Blast / Glacial Spike（协同）", "Ice Blast / Glacial Spike (synergies)"),
          "Frozen Armor", "Cold Mastery"]),
        ("Lightning", bi("单体与 AoE 爆发最高，但吃 -% 电抗。", "Highest single-target and AoE burst, but needs -% enemy lightning resist."),
         ["Lightning", "Chain Lightning", "Nova", bi("Static Field（削血）", "Static Field (percent life burn)"),
          "Lightning Mastery", "Telekinesis / Teleport"]),
        ("Fire", bi("火球主力，火冰双修常见。", "Fire Ball carries; the Meteorb hybrid is very common."),
         ["Fire Ball", "Meteor", "Hydra", bi("Enchant（给佣兵/队友加火伤）", "Enchant (fire damage for your merc/party)"),
          bi("Warmth（回蓝）", "Warmth (mana regen)"), "Fire Mastery"]),
    ])
    builds = build_card(
        bi("暴风雪法师", "Blizzard Sorceress"),
        bi("S 级 · 冰系 AoE", "S-Tier · Cold AoE"),
        bi("经典开荒与 MF 之王。暴雪大范围高伤并减速，配合传送风筝海量怪物，拿到 Cold Sunder 后连冰免也能打。",
           "The classic progression and MF queen. Blizzard hits a huge area for big damage and chills everything; teleport-kite whole packs, and once you own a Cold Sunder even cold immunes go down."),
        [("Blizzard", "20"), ("Ice Blast", bi("20（协同）", "20 (synergy)")),
         ("Glacial Spike", bi("20（协同）", "20 (synergy)")),
         ("Cold Mastery", bi("1→满（建议 -100%~-150% 含装备）", "1 → max (aim for -100% to -150% with gear)")),
         ("Frozen Armor", "1"), ("Teleport/Static", bi("各 1", "1 each")),
         (bi("其余→Ice Blast 或 Glacial Spike", "Rest → Ice Blast or Glacial Spike"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备（约 156 穿 Monarch）", "Just enough for gear (≈156 for a Monarch)")),
         (bi("敏捷", "Dexterity"), bi("不加（或少量格挡）", "None (or a little for block)")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量或不加（靠回蓝装）", "Little to none (use mana regen gear)"))],
        [bi("武器：Spirit 符文之语（剑）/ Heart of the Oak，副手 Call to Arms（CTA）", "Weapon: Spirit runeword sword / Heart of the Oak, with Call to Arms on swap"),
         bi("盾：Spirit Monarch", "Shield: Spirit Monarch"),
         bi("头盔：Nightwing's Veil / +2 冰 20FCR 头环", "Helm: Nightwing's Veil / +2 cold, 20 FCR circlet"),
         bi("甲：Enigma / Tal Rasha's 套", "Armor: Enigma / Tal Rasha's set"),
         bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
         bi("项链：Mara's / +2 冰 20FCR", "Amulet: Mara's / +2 cold, 20 FCR"),
         bi("戒指：SoJ + 婚戒 / 乔丹", "Rings: SoJ + Bul-Kathos' Wedding Band"),
         bi("手套：Magefist 等", "Gloves: Magefist or similar"),
         bi("破免：Cold Sunder Charm", "Sunder: Cold Sunder Charm")],
        [bi("传送卡位把怪聚到暴雪范围", "Teleport to herd monsters into the Blizzard area"),
         bi("先 Static Field 削血再暴雪收尾", "Open with Static Field, then finish with Blizzard"),
         bi("冰免切副手或靠佣兵", "Against cold immunes swap weapons or let the merc work"),
         bi("堆 FCR 档位（117/200 等）提速", "Hit the FCR breakpoints (117/200) for casting speed"),
         bi("Cold Mastery 减抗是伤害核心", "Cold Mastery's resist reduction is the core of your damage")],
    )
    builds += build_card(
        bi("闪电/新星法师", "Lightning / Nova Sorceress"),
        bi("S 级 · 电系爆发", "S-Tier · Lightning Burst"),
        bi("全游戏最高 DPS 路线之一，但严重依赖 -% 敌方电抗（Infinity）。Lightning 打单体、Nova 清屏，终局 farm 效率顶级。",
           "One of the highest DPS builds in the game, but heavily dependent on -% enemy lightning resist (Infinity). Lightning kills single targets, Nova clears screens — top-tier endgame farming speed."),
        [("Lightning", "20"), ("Chain Lightning", bi("20（协同）", "20 (synergy)")),
         ("Nova", bi("20（清屏）", "20 (screen clear)")),
         ("Lightning Mastery", bi("1→满", "1 → max")),
         ("Teleport/Static", bi("各 1", "1 each")),
         (bi("其余→Chain Lightning 协同", "Rest → Chain Lightning synergy"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("不加", "None")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量（Energy Shield 流派可多加）", "A little (more if you run Energy Shield)"))],
        [bi("武器：Infinity（自己拿，破免+光环）/ 或 Heart of the Oak", "Weapon: Infinity (self-wielded for the aura and immunity break) or Heart of the Oak"),
         bi("盾：Spirit Monarch / Stormshield", "Shield: Spirit Monarch / Stormshield"),
         bi("头盔：Griffon's Eye（电珠）", "Helm: Griffon's Eye (lightning facet)"),
         bi("甲：Enigma / Chains of Honor", "Armor: Enigma / Chains of Honor"),
         bi("项链：Mara's / +2 电 20FCR", "Amulet: Mara's / +2 lightning, 20 FCR"),
         bi("戒指：SoJ + 婚戒", "Rings: SoJ + Bul-Kathos' Wedding Band"),
         bi("破免：Lightning Sunder Charm", "Sunder: Lightning Sunder Charm"),
         bi("佣兵：祈祷/防御（不拿 Infinity 时）", "Merc: Prayer/Defiance if he isn't carrying Infinity")],
        [bi("核心靠 Infinity 的 Conviction 降抗", "Your damage lives on Infinity's Conviction aura"),
         bi("Nova 在密集怪中贴脸放", "Cast Nova point-blank inside dense packs"),
         bi("boss 用 Lightning 远程点", "Snipe bosses from range with Lightning"),
         bi("脆皮需靠传送走位保命", "You are squishy — Teleport is your defence"),
         bi("可点 Energy Shield 提升容错", "A point in Energy Shield adds a safety net")],
    )
    builds += build_card(
        bi("火冰双修法师", "Meteorb Sorceress"),
        bi("A 级 · 双系开荒", "A-Tier · Dual-Element Progression"),
        bi("Fire Ball + Frozen Orb 双修，单系免疫可切换另一系，单机/开荒最稳，无需破免也能通全剧。",
           "Fire Ball plus Frozen Orb: whenever one element is immune you just switch to the other. The safest solo/progression pick — it clears the whole game without any Sunder Charm."),
        [("Fire Ball", "20"), ("Meteor", bi("20（协同）", "20 (synergy)")), ("Frozen Orb", "20"),
         ("Fire/Cold Mastery", bi("各 1→满", "1 → max each")),
         ("Teleport/Static/Warmth", bi("各 1", "1 each")),
         (bi("其余→Fire Bolt 协同", "Rest → Fire Bolt synergy"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("不加", "None")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量", "A little"))],
        [bi("武器：Spirit / Heart of the Oak", "Weapon: Spirit / Heart of the Oak"),
         bi("盾：Spirit Monarch", "Shield: Spirit Monarch"),
         bi("头盔：+2 火/冰 头环 / Shako", "Helm: +2 fire/cold circlet / Harlequin Crest"),
         bi("甲：Skin of the Vipermagi / Enigma", "Armor: Skin of the Vipermagi / Enigma"),
         bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
         bi("项链：Mara's / 拼FCR", "Amulet: Mara's / anything with FCR"),
         bi("戒指：SoJ + 婚戒", "Rings: SoJ + Bul-Kathos' Wedding Band")],
        [bi("冰免切 Fire Ball，火免切 Frozen Orb", "Cold immune? Use Fire Ball. Fire immune? Use Frozen Orb."),
         bi("开荒最稳，不依赖破免", "The safest progression build — no Sunder needed"),
         bi("传送风筝，Static 削血", "Teleport-kite and soften targets with Static Field"),
         bi("适合 MF 与通关", "Great for MF runs and clearing the game"),
         bi("终局可转纯冰或纯电", "Respec to pure cold or pure lightning at endgame")],
    )
    tips = '<div class="card"><ul class="clean">' \
           '<li><b>' + bi("起手推荐 Blizzard：", "Start with Blizzard:") + '</b>' \
           + bi("冰系起步最顺，30 级后暴雪成型，靠传送风筝，开荒到地狱中期都很强。",
                "Cold is the smoothest opener; Blizzard comes online at level 30 and teleport-kiting carries you well into Hell.") + '</li>' \
           '<li><b>' + bi("破冰免：", "Breaking cold immunes:") + '</b>' \
           + bi("拿到 Cold Sunder Charm 后冰法也能打冰免；或用副手 Infinity（自己拿）降低火/电抗。",
                "A Cold Sunder Charm lets a cold sorc kill cold immunes; a self-wielded Infinity also strips fire/lightning resist.") + '</li>' \
           '<li><b>' + bi("闪电法刚需 Infinity：", "Lightning needs Infinity:") + '</b>' \
           + bi("Lightning / Nova 靠 -% 电抗（Infinity 佣兵或自己拿）才能打高，否则伤害骤降。",
                "Lightning and Nova only hit hard with -% enemy lightning resist from Infinity (merc or self-wielded); without it damage collapses.") + '</li>' \
           '<li><b>' + bi("Teleport 是灵魂：", "Teleport is everything:") + '</b>' \
           + bi("全场景跳点、躲怪、卡位，MF 效率的关键。",
                "Jump across zones, dodge packs and position monsters — it is the key to MF efficiency.") + '</li>' \
           '<li><b>' + bi("Meteorb 双修：", "The Meteorb hybrid:") + '</b>' \
           + bi("Fire Ball + Frozen Orb，单系免疫也能切换，单机/开荒友好。",
                "Fire Ball plus Frozen Orb covers single-element immunes and is very solo/progression friendly.") + '</li>' \
           '</ul></div>'
    return _class_page("法师 Sorceress", "c:sorceress", intro, trees, builds, tips, "amazon.html", "亚马逊 Amazon", "necromancer.html", "亡灵法师 Necromancer")

def necromancer():
    intro = '<h1><span class="zt"><span class="zc">亡灵法师 </span><span class="ec" lang="en">Necromancer</span></span></h1>\n' \
            '<p>' + bi("亡灵法师是「让别人干活」的大师：召唤亡灵大军、施放毒与骨系法术、并用诅咒削弱敌人。召唤流是新手最友好的开荒流派（安全、省力），毒系与骨系则在终局拥有不俗输出。",
                       "The Necromancer is the master of letting others do the work: raise an undead army, sling poison and bone spells, and cripple enemies with curses. Summoner is the most beginner-friendly progression build (safe and low effort), while Poison and Bone deliver solid endgame damage.") + '</p>\n' \
            '<div class="callout tip"><b>' + bi("定位：", "Role:") + '</b>' \
            + bi("召唤 / 毒 / 骨系 · 优势：召唤流极安全、毒系 AoE 强 · 劣势：召唤清 boss 慢、骨系依赖 Death's Web。",
                 "Summons / Poison / Bone · Pros: Summoner is extremely safe, Poison has great AoE · Cons: Summoner kills bosses slowly, Bone depends on Death's Web.") + '</div>'
    trees = skilltrees([
        ("Summoning", bi("亡灵大军作战，最安全的路线。", "Let the undead army fight for you — the safest route."),
         ["Raise Skeleton", "Skeleton Mastery", "Clay Golem / Iron Golem", "Revive",
          bi("Summon Resist（抗）", "Summon Resist (minion resistances)")]),
        ("Poison & Bone", bi("直接伤害系，骨矛/骨魂与毒 nova。", "Direct damage: Bone Spear/Spirit plus Poison Nova."),
         ["Poison Dagger / Poison Nova", "Bone Spear / Bone Spirit", "Bone Prison / Bone Wall", "Corpse Explosion", "Teeth"]),
        ("Curses", bi("削弱敌人，全流派通用。", "Weaken enemies — useful for every build."),
         ["Amplify Damage", "Decrepify", "Dim Vision / Attract",
          bi("Lower Resist（毒系核心）", "Lower Resist (core for poison)"), "Iron Maiden / Life Tap"]),
    ])
    builds = build_card(
        bi("召唤流死灵", "Summoner Necromancer"),
        bi("S 级 · 安全开荒", "S-Tier · Safe Progression"),
        bi("最友好的开荒流派：骷髅战士+法师+石魔+重生组成大军，自己全程划水。Hardcore 与新手的理想选择。",
           "The friendliest progression build: skeleton warriors, skeleton mages, a golem and revives form an army while you coast behind them. Ideal for Hardcore and for new players."),
        [("Raise Skeleton", "20"), ("Skeleton Mastery", "20"), ("Clay Golem", "1"), ("Golem Mastery", "1"),
         ("Summon Resist", "1+"), ("Revive", bi("1→满（剩余点）", "1 → max (leftover points)")),
         ("Amplify/Decrepify", bi("各 1", "1 each")), ("Corpse Explosion", "1"),
         (bi("Teleport（骨牢/传送杖）", "Teleport (Bone Prison / teleport staff)"), bi("可选", "Optional"))],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("不加（或格挡）", "None (or enough to block)")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("不加", "None"))],
        [bi("武器：Beast（狂热光环，给大军加攻速）/ 召唤杖", "Weapon: Beast (Fanaticism aura for your army's attack speed) / +summon staff"),
         bi("盾：Homunculus（骷髅法杖盾）", "Shield: Homunculus"),
         bi("头盔：Peasant Crown / +2 召唤头环", "Helm: Peasant Crown / +2 summoning circlet"),
         bi("甲：Enigma / Skin of the Vipermagi", "Armor: Enigma / Skin of the Vipermagi"),
         bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
         bi("项链：Mara's / +2 召唤", "Amulet: Mara's / +2 summoning"),
         bi("戒指：SoJ + 婚戒", "Rings: SoJ + Bul-Kathos' Wedding Band"),
         bi("手套：Magefist", "Gloves: Magefist")],
        [bi("黏土石魔用 Decrepify 减速 boss", "Clay Golem plus Decrepify slows bosses to a crawl"),
         bi("先放 Amplify 给物理召唤增伤", "Cast Amplify Damage first to boost your physical minions"),
         bi("自己躲后方，靠大军推进", "Stay behind and let the army push"),
         bi("Revive 拉强力怪当打手", "Revive strong monsters as extra muscle"),
         bi("尸体爆炸清密集小怪", "Corpse Explosion melts dense trash")],
    )
    builds += build_card(
        bi("毒系死灵", "Poison Necromancer"),
        bi("A 级 · 毒系 AoE", "A-Tier · Poison AoE"),
        bi("Poison Nova 范围毒伤，配合 Lower Resist 与毒 Sunder，Terror Zone 清场效率极高，是 2.5+ 赛季强势流派。",
           "Poison Nova blankets packs in poison; combined with Lower Resist and a Poison Sunder it clears Terror Zones extremely fast — a strong pick since patch 2.5."),
        [("Poison Nova", "20"), ("Poison Dagger", bi("20（协同）", "20 (synergy)")),
         ("Lower Resist", bi("1→满", "1 → max")), ("Corpse Explosion", "1"),
         ("Bone Armor/Prison", "1"), ("Amplify/Decrepify", bi("各 1", "1 each")),
         (bi("其余→Teeth/骨盾", "Rest → Teeth / Bone Armor"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("不加", "None")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量", "A little"))],
        [bi("武器：Death's Web（死灵法杖，核心）/ 副手 CTA", "Weapon: Death's Web (core) with Call to Arms on swap"),
         bi("盾：Homunculus / Spirit", "Shield: Homunculus / Spirit"),
         bi("头盔：Craft 头环（+毒/技能）", "Helm: crafted circlet (+poison skills)"),
         bi("甲：Enigma / Trang-Oul's 套（毒伤）", "Armor: Enigma / Trang-Oul's set (poison damage)"),
         bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
         bi("项链：Mara's / +2 毒", "Amulet: Mara's / +2 poison & bone"),
         bi("破免：Poison Sunder Charm", "Sunder: Poison Sunder Charm"),
         bi("手套：Trang-Oul's 手", "Gloves: Trang-Oul's Claws")],
        [bi("Lower Resist 先降毒抗再放 Nova", "Curse with Lower Resist before casting Nova"),
         bi("毒 Sunder 处理毒免怪", "A Poison Sunder handles poison immunes"),
         bi("Corpse Explosion 补刀", "Finish packs with Corpse Explosion"),
         bi("Trang-Oul 套装加成毒伤", "Trang-Oul's set pieces boost poison damage"),
         bi("配合 Iron Golem 与召唤更稳", "An Iron Golem and a few minions make it much safer")],
    )
    builds += build_card(
        bi("骨系死灵", "Bone Necromancer"),
        bi("A 级 · 骨系单体", "A-Tier · Bone Single-Target"),
        bi("Bone Spirit / Bone Spear 远程高伤，不吃免疫（魔法伤害，仅少数魔法免疫需破免）。依赖 Death's Web 与暗金项链堆技能。",
           "Bone Spirit and Bone Spear deal heavy ranged magic damage that almost nothing resists (only the rare magic immune needs a Sunder). It leans hard on Death's Web and a +skills amulet."),
        [("Bone Spear", "20"), ("Bone Spirit", "20"), ("Bone Prison/Wall", "1"), ("Corpse Explosion", "1"),
         ("Bone Armor", "1+"), ("Lower Resist/Amplify", bi("各 1", "1 each")),
         (bi("剩余→Teeth", "Rest → Teeth"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("不加", "None")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量", "A little"))],
        [bi("武器：Death's Web + 暗金项链（核心）", "Weapon: Death's Web plus a +skills unique amulet (core)"),
         bi("盾：Homunculus / Spirit", "Shield: Homunculus / Spirit"),
         bi("头盔：Craft 头环（+骨/技能）", "Helm: crafted circlet (+bone skills)"),
         bi("甲：Enigma / Skin of Vipermagi", "Armor: Enigma / Skin of the Vipermagi"),
         bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
         bi("戒指：SoJ + 婚戒", "Rings: SoJ + Bul-Kathos' Wedding Band"),
         bi("破免：Magic Sunder（魔法免疫怪）", "Sunder: Magic Sunder for magic immunes")],
        [bi("Bone Spear 直线穿透清线", "Bone Spear pierces in a line to clear corridors"),
         bi("Bone Spirit 自动追踪单体", "Bone Spirit homes in on single targets"),
         bi("魔法伤害对多数怪有效", "Magic damage works on almost every monster"),
         bi("遇到魔法免疫需破免/换路线", "Magic immunes need a Sunder or a different route"),
         bi("靠走位与骨甲保命", "Stay alive with positioning and Bone Armor")],
    )
    tips = '<div class="card"><ul class="clean">' \
           '<li><b>' + bi("新手首选召唤：", "Summoner first for beginners:") + '</b>' \
           + bi("骷髅海 + 黏土石魔 + 重生，自己躲在后面，几乎零风险通关。",
                "A wall of skeletons, a Clay Golem and revives let you hide in the back and clear the game with almost no risk.") + '</li>' \
           '<li><b>' + bi("诅咒位核心：", "Curses are core:") + '</b>' \
           + bi("Amplify Damage（增伤）给物理召唤用，Decrepify（衰老）减速+易伤，Uber 也靠它。",
                "Amplify Damage boosts your physical minions, while Decrepify slows and softens — it is also the key curse for Ubers.") + '</li>' \
           '<li><b>' + bi("毒系需 -% 毒抗：", "Poison needs -% poison resist:") + '</b>' \
           + bi("Lower Resist（降抗）+ 毒 Sunder，配合 Death's Web / Trang-Oul 大幅提升。",
                "Lower Resist plus a Poison Sunder, backed by Death's Web / Trang-Oul's, multiplies your damage.") + '</li>' \
           '<li><b>' + bi("骨系标杆装备：", "Bone's benchmark gear:") + '</b>' \
           + bi("Death's Web 死灵法杖 + 暗金项链，Bone Spirit / Bone Spear 高伤。",
                "Death's Web plus a +skills unique amulet pushes Bone Spirit / Bone Spear damage sky-high.") + '</li>' \
           '<li><b>' + bi("Corpse Explosion：", "Corpse Explosion:") + '</b>' \
           + bi("尸体爆炸是强力 AoE，群怪时让召唤先杀几个再连环爆。",
                "It is a monster AoE tool — let your minions kill a few, then chain-detonate the corpses.") + '</li>' \
           '</ul></div>'
    return _class_page("亡灵法师 Necromancer", "c:necromancer", intro, trees, builds, tips, "sorceress.html", "法师 Sorceress", "paladin.html", "圣骑士 Paladin")

def paladin():
    intro = '<h1><span class="zt"><span class="zc">圣骑士 </span><span class="ec" lang="en">Paladin</span></span></h1>\n' \
            '<p>' + bi("圣骑士是「光环 + 祝福之锤」的代名词，也是开荒与终局最稳的近战/法系混合职业。祝福之锤圣骑士几乎能单人打通全剧并高效 farm，是新手与老玩家共同的首选。",
                       "The Paladin is synonymous with auras and Blessed Hammer, and he is the most reliable melee/caster hybrid for both progression and endgame. A Hammerdin can solo the entire game and farm efficiently, which is why veterans and beginners alike pick him first.") + '</p>\n' \
            '<div class="callout tip"><b>' + bi("定位：", "Role:") + '</b>' \
            + bi("魔法锤 / 近战 / 辅助 · 优势：祝福之锤全能、光环团队增益、盾击专克超级Boss · 劣势：锤子需练手（螺旋弹道）、近战流吃装备。",
                 "Magic hammers / melee / support · Pros: Blessed Hammer does everything, auras buff the party, Smite hard-counters Uber bosses · Cons: hammers take practice (spiral trajectory) and melee builds are gear hungry.") + '</div>'
    trees = skilltrees([
        ("Combat", bi("近战攻击技能，含盾击与热诚。", "Melee attacks, including Smite and Zeal."),
         ["Sacrifice / Zeal", bi("Smite（必中）", "Smite (always hits)"), "Charge", "Holy Shield", "Vengeance / Conversion"]),
        ("Offensive", bi("光环为主，强化自身与队伍。", "Mostly auras that buff you and your party."),
         ["Might", bi("Holy Fire / Holy Frost / Holy Shock（元素光环）", "Holy Fire / Holy Frost / Holy Shock (elemental auras)"),
          "Fanaticism", bi("Conviction（降抗）", "Conviction (resist reduction)"), "Sanctuary / Blessed Aim"]),
        ("Defensive", bi("祝福之锤与防护光环所在系。", "Home of Blessed Hammer and the protective auras."),
         [bi("Prayer / Cleansing / Meditation（回复光环）", "Prayer / Cleansing / Meditation (recovery auras)"),
          "Defiance / Thorns", bi("Concentration（锤丁核心）", "Concentration (Hammerdin core)"),
          "Blessed Hammer", "Vigor", "Fist of the Heavens"]),
    ])
    builds = build_card(
        bi("祝福之锤圣骑士", "Hammerdin"),
        bi("S 级 · 全能魔法", "S-Tier · All-Round Magic"),
        bi("最经典的圣骑士流派。祝福之锤造成魔法伤害，几乎无视所有免疫（仅魔法免疫怪需破免），配合 Concentration 光环大幅提升伤害与命中，单人通全剧 + 高效 farm。",
           "The most iconic Paladin build. Blessed Hammer deals magic damage that bypasses nearly every immunity (only magic immunes need a Sunder), and the Concentration aura massively boosts its damage — perfect for soloing the game and farming fast."),
        [("Blessed Hammer", "20"), ("Concentration", bi("20（光环）", "20 (aura)")),
         ("Vigor", bi("20（锤速/机动）", "20 (hammer speed/mobility)")),
         ("Blessed Aim", bi("0~20（若用 BH 命中）", "0–20 (if you want extra hammer damage)")),
         ("Holy Shield", "1+"), ("Redemption/Cleansing", "1"),
         (bi("其余→Vigor/协同", "Rest → Vigor/synergies"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备（约 156 穿 Monarch）", "Just enough for gear (≈156 for a Monarch)")),
         (bi("敏捷", "Dexterity"), bi("少量（开圣盾后堆格挡到 75%）", "A little (75% block with Holy Shield up)")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("不加", "None"))],
        [bi("武器：Heart of the Oak", "Weapon: Heart of the Oak"),
         bi("盾：Spirit Monarch", "Shield: Spirit Monarch"),
         bi("头盔：Shako / +2 锤 头环", "Helm: Harlequin Crest / +2 hammer circlet"),
         bi("甲：Enigma / Chains of Honor", "Armor: Enigma / Chains of Honor"),
         bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
         bi("项链：Mara's / +2 锤 20FCR", "Amulet: Mara's / +2 combat skills, 20 FCR"),
         bi("戒指：SoJ + 婚戒 / 乔丹", "Rings: SoJ + Bul-Kathos' Wedding Band"),
         bi("手套：Magefist / 拼 FCR", "Gloves: Magefist / anything with FCR"),
         bi("破免：Magic Sunder（魔法免疫）", "Sunder: Magic Sunder for magic immunes")],
        [bi("Concentration 光环下丢锤子", "Always cast hammers under Concentration"),
         bi("Vigor 提升移速与锤飞行速度", "Vigor boosts run speed and hammer travel speed"),
         bi("练习螺旋弹道覆盖怪群", "Practise the spiral so hammers sweep through packs"),
         bi("圣盾保证格挡生存", "Holy Shield keeps your block and defence high"),
         bi("遇到魔法免疫切副手/破免", "Against magic immunes use a weapon swap or a Sunder")],
    )
    builds += build_card(
        bi("热诚圣骑士", "Zealot"),
        bi("A 级 · 物理近战", "A-Tier · Physical Melee"),
        bi("Zeal 多段攻 + Fanaticism 狂热光环，高攻速高爆发单体与清场兼具，是经典的物理近战路线。",
           "Zeal's multi-hit swings plus the Fanaticism aura give huge attack speed and burst for both single targets and packs — the classic physical melee route."),
        [("Zeal", "20"), ("Fanaticism", bi("20（光环）", "20 (aura)")),
         ("Holy Shield", bi("20（格挡/伤害）", "20 (block/defence)")),
         ("Sacrifice", bi("1（协同）", "1 (synergy)")),
         ("Defiance/Cleansing", "1"),
         (bi("剩余→Holy Shield/协同", "Rest → Holy Shield/synergies"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("开圣盾后堆格挡 75%，其余加敏提伤害", "75% block with Holy Shield up, then more Dex for damage")),
         (bi("体力", "Vitality"), bi("保证生存", "Enough to stay alive")),
         (bi("能量", "Energy"), bi("不加", "None"))],
        [bi("武器：Grief（悲伤，核心）/ 死灵法杖备选", "Weapon: Grief (core) / a phase blade alternative"),
         bi("盾：Herald of Zakarum / 暗金圣盾（击回）", "Shield: Herald of Zakarum / a unique paladin shield with hit recovery"),
         bi("头盔：Guillaume's / 头环", "Helm: Guillaume's Face / a rare circlet"),
         bi("甲：Fortitude / Chains of Honor", "Armor: Fortitude / Chains of Honor"),
         bi("腰带：String of Ears / 临别赠礼", "Belt: String of Ears / Verdungo's Hearty Cord"),
         bi("戒指：Raven Frost + 婚戒", "Rings: Raven Frost + Bul-Kathos' Wedding Band"),
         bi("手套：Dracul's Grasp（偷血）", "Gloves: Dracul's Grasp (life tap)"),
         bi("靴：Gore Rider", "Boots: Gore Rider")],
        [bi("Fanaticism 提升攻速与伤害", "Fanaticism boosts attack speed and damage"),
         bi("Holy Shield 保格挡", "Holy Shield keeps your block up"),
         bi("物理免疫需破物/切元素光环", "Physical immunes need a Physical Sunder or an elemental aura"),
         bi("靠 Dracul's 偷血续航", "Dracul's life tap keeps you topped up"),
         bi("适合 boss 与高密度区域", "Great for bosses and dense areas")],
    )
    builds += build_card(
        bi("天堂之拳/盾击圣骑士", "FoH / Smiter"),
        bi("S 级 · Uber 专杀", "S-Tier · Uber Killer"),
        bi("Fist of the Heavens（天堂之拳）魔法+电混合 AoE，配合 Conviction 在混沌圣所等地极强；Smiter 用 Smite 必中打 Uber。",
           "Fist of the Heavens mixes magic and lightning AoE and, backed by Conviction, shreds places like the Chaos Sanctuary; the Smiter variant uses Smite's guaranteed hits to kill Ubers."),
        [("Fist of the Heavens", "20"), ("Holy Bolt", bi("20（协同）", "20 (synergy)")),
         ("Conviction", bi("20（降抗光环）", "20 (resist-reduction aura)")), ("Holy Shield", "1+"),
         (bi("Smite（Uber 版）", "Smite (Uber variant)"), bi("20（备选）", "20 (alternative)")),
         ("Sanctuary", "1"), (bi("剩余→协同", "Rest → synergies"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("格挡 75% / 或穿装备", "75% block, or just enough for gear")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("不加", "None"))],
        [bi("武器（FoH）：Herald of Zakarum / Spirit", "Weapon (FoH): Herald of Zakarum / Spirit"),
         bi("盾：Herald of Zakarum（FoH 核心）", "Shield: Herald of Zakarum (FoH core)"),
         bi("头盔：+2 战斗 头环 / Shako", "Helm: +2 combat circlet / Harlequin Crest"),
         bi("甲：Enigma / Chains of Honor", "Armor: Enigma / Chains of Honor"),
         bi("项链：Mara's / +2 战斗", "Amulet: Mara's / +2 combat skills"),
         bi("破免：Lightning/Magic Sunder", "Sunder: Lightning/Magic Sunder"),
         bi("（Uber Smiter）武器：Grief + 暗金圣盾 + 击回装", "(Uber Smiter) Weapon: Grief plus a unique paladin shield and faster hit recovery gear")],
        [bi("FoH 靠 Conviction 降电抗打群怪", "FoH relies on Conviction to strip lightning resist from packs"),
         bi("Holy Bolt 给自身/队友回血", "Holy Bolt heals you and your party"),
         bi("混沌圣所密度高时极强", "It shines in the dense Chaos Sanctuary"),
         bi("Smite 必中、无视格挡，专杀 Uber", "Smite always hits and ignores block — the Uber killer"),
         bi("Uber 需 Decrepify/衰老配合", "Ubers also want a Decrepify source")],
    )
    tips = '<div class="card"><ul class="clean">' \
           '<li><b>' + bi("新手必练 Hammerdin：", "Every beginner should try a Hammerdin:") + '</b>' \
           + bi("祝福之锤（魔法伤害）绕开绝大多数免疫，光环提供续航，开荒到终局通吃。",
                "Blessed Hammer's magic damage bypasses nearly all immunities and the auras keep you going from leveling to endgame.") + '</li>' \
           '<li><b>' + bi("锤子弹道：", "Hammer trajectory:") + '</b>' \
           + bi("祝福之锤沿螺旋轨迹飞行，需练习站位让锤子扫过怪群；Vigor 提升移动与锤速。",
                "Hammers spiral outward, so you must position yourself for them to sweep through the pack; Vigor speeds up both you and the hammers.") + '</li>' \
           '<li><b>' + bi("Smiter 打 Uber：", "Smiters for Ubers:") + '</b>' \
           + bi("盾击（Smite）必中且无视格挡，配合 Grief + 暗金圣盾专杀超级 boss。",
                "Smite always hits and ignores block; with Grief and a unique paladin shield it deletes Uber bosses.") + '</li>' \
           '<li><b>' + bi("Fanaticism / Conviction：", "Fanaticism / Conviction:") + '</b>' \
           + bi("狂热给物理输出，信念降抗，是组队核心光环。",
                "Fanaticism for physical damage, Conviction for resist reduction — the two key party auras.") + '</li>' \
           '<li><b>' + bi("Holy Shield：", "Holy Shield:") + '</b>' \
           + bi("大幅提升格挡与防御，近战/盾击流必点。",
                "A huge boost to block and defence — mandatory for melee and Smiter builds.") + '</li>' \
           '</ul></div>'
    return _class_page("圣骑士 Paladin", "c:paladin", intro, trees, builds, tips, "necromancer.html", "亡灵法师 Necromancer", "barbarian.html", "野蛮人 Barbarian")

def barbarian():
    intro = '<h1><span class="zt"><span class="zc">野蛮人 </span><span class="ec" lang="en">Barbarian</span></span></h1>\n' \
            '<p>' + bi("野蛮人是近战与「战吼」大师，拥有全游戏最强的光环类增益（Battle Orders 提升生命/法力上限）与独特的 Find Item（寻物）双倍掉落机制。虽然开荒偏慢，但终局 Whirlwind 与 Pitzerker 都是顶级 farm 流派。",
                       "The Barbarian is the master of melee and warcries. He brings the strongest party buff in the game (Battle Orders raises max life and mana) and the unique Find Item mechanic that rolls loot a second time. Leveling is slow, but at endgame both Whirlwind and the Pitzerker are top-tier farming builds.") + '</p>\n' \
            '<div class="callout warn"><b>' + bi("定位：", "Role:") + '</b>' \
            + bi("近战 / 战吼辅助 · 优势：BO 团队增益、Find Item 双倍掉落、WW 清场爽快 · 劣势：开荒慢、吃装备、需要解决命中率。",
                 "Melee / warcry support · Pros: Battle Orders for the party, Find Item double drops, Whirlwind clears feel great · Cons: slow leveling, gear hungry, needs attack rating.") + '</div>'
    trees = skilltrees([
        ("Combat", bi("近战攻击技能，含旋风与狂乱。", "Melee attacks, including Whirlwind and Frenzy."),
         ["Whirlwind", "Frenzy", bi("Berserk（魔法伤）", "Berserk (magic damage)"), "Concentrate",
          "Double Throw / Throw", "Leap / Leap Attack"]),
        ("Combat Masteries", bi("武器精通与生存被动。", "Weapon masteries and defensive passives."),
         ["Sword/Mace/Axe/ Polearm Mastery", "Iron Skin / Natural Resistance", "Increased Speed / Stamina",
          bi("Battle Cry（减防）", "Battle Cry (reduces enemy defence)")]),
        ("Warcries", bi("增益与控场，野蛮人特色。", "Buffs and crowd control — the Barbarian's signature."),
         [bi("Battle Orders（+生命/法力）", "Battle Orders (+life/mana)"), "Shout / Battle Command",
          bi("War Cry（眩晕）", "War Cry (stun)"), bi("Find Item（双倍掉落）", "Find Item (extra loot roll)"),
          bi("Taunt / Concentrate 相关", "Taunt / Concentrate and related skills")]),
    ])
    builds = build_card(
        bi("旋风野蛮人", "Whirlwind Barbarian"),
        bi("A 级 · 近战清场", "A-Tier · Melee Clear"),
        bi("Whirlwind 边转边打，清场爽快、机动强。配合 Battle Orders 与 high IAS 装备，是经典的近战 farm 流派。",
           "Whirlwind lets you spin through packs while dealing damage — fast, mobile and satisfying. With Battle Orders and high IAS gear it is the classic melee farming build."),
        [("Whirlwind", "20"), ("Battle Orders", "20"), ("Battle Command", "1"),
         (bi("Weapon Mastery（依武器）", "Weapon Mastery (match your weapon)"), "20"),
         ("Shout", "1+"), ("Natural Resistance/Iron Skin", bi("各 1", "1 each")), ("Find Item", "1+"),
         (bi("剩余→Shout/战吼", "Rest → Shout/warcries"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("穿装备 / 或堆格挡（剑盾）", "Enough for gear, or block if you use a shield")),
         (bi("体力", "Vitality"), bi("其余全加（BO 已提上限）", "Everything else (BO already raises the cap)")),
         (bi("能量", "Energy"), bi("不加", "None"))],
        [bi("武器：Grief（双持）/ 死亡呼吸", "Weapons: dual Grief / Breath of the Dying"),
         bi("盾（剑盾流）：Stormshield", "Shield (sword & board): Stormshield"),
         bi("头盔：Arreat's Face（亚瑞特脸）", "Helm: Arreat's Face"),
         bi("甲：Fortitude / Enigma", "Armor: Fortitude / Enigma"),
         bi("腰带：String of Ears", "Belt: String of Ears"),
         bi("项链：Highlord's Wrath / Mara's", "Amulet: Highlord's Wrath / Mara's"),
         bi("戒指：Raven Frost + 婚戒 / 双吸", "Rings: Raven Frost + Bul-Kathos' Wedding Band / dual leech rares"),
         bi("靴：Gore Rider / 战旅", "Boots: Gore Rider / War Traveler"),
         bi("手套：配合 IAS/致命", "Gloves: IAS and deadly strike")],
        [bi("WW 持续旋转清怪", "Keep whirling through the pack"),
         bi("Battle Orders 先开提升血上限", "Always cast Battle Orders first for the life buff"),
         bi("注意 IAS 档位与命中", "Watch your IAS breakpoints and attack rating"),
         bi("物理免疫切 Berserk（魔法伤）", "Swap to Berserk (magic damage) against physical immunes"),
         bi("靠吸血与高血生存", "Survive on leech and a big life pool")],
    )
    builds += build_card(
        bi("寻物狂战", "Pitzerker"),
        bi("S 级 · MF 双倍掉落", "S-Tier · MF Double Drops"),
        bi("Berserk 造成魔法伤害（无视物理免疫），击杀后用 Find Item 对尸体再 roll 一次掉落，是 The Pit 等区域的 MF 效率之王。",
           "Berserk deals magic damage (ignoring physical immunity), and after each kill Find Item rolls the corpse for a second drop — the most efficient MF build for zones like The Pit."),
        [("Berserk", "20"), ("Battle Orders", "20"), ("Find Item", bi("20（hork）", "20 (hork)")),
         ("Weapon Mastery", "20"), ("Battle Command/Shout", bi("各 1", "1 each")), ("Natural Resistance", "1"),
         (bi("剩余→Shout", "Rest → Shout"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("穿装备", "Just enough for gear")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("不加", "None"))],
        [bi("武器：高 MF 副手（Ali Baba / Gull）+ Grief 主手", "Weapons: high-MF offhand (Ali Baba / Gull) with Grief in the main hand"),
         bi("头盔：Shako（镶 Ist 加 MF）", "Helm: Harlequin Crest socketed with Ist"),
         bi("甲：Enigma（传送 MF）", "Armor: Enigma (Teleport plus MF)"),
         bi("腰带：Goldwrap（MF）", "Belt: Goldwrap (MF)"),
         bi("手套：Chance Guards（MF）", "Gloves: Chance Guards (MF)"),
         bi("靴：War Traveler（MF 鞋）", "Boots: War Traveler (MF)"),
         bi("戒指：Nagelring / 婚戒（MF）", "Rings: Nagelring / MF rares"),
         bi("项链：高 MF 项链", "Amulet: high-MF amulet"),
         bi("佣兵：Infinity/力量", "Merc: Infinity / Might")],
        [bi("Berserk 打 boss 与精英", "Use Berserk on bosses and champions"),
         bi("击杀后立即 Find Item hork 尸体", "Hork the corpse with Find Item right after the kill"),
         bi("堆 MF 到 300%+ 仍保持效率", "Stack 300%+ MF and still keep good clear speed"),
         bi("Enigma 传送快速跑图", "Enigma's Teleport speeds up every run"),
         bi("魔法伤害无视物理免疫", "Magic damage ignores physical immunity")],
    )
    builds += build_card(
        bi("战吼野蛮人", "Singer Barbarian"),
        bi("A 级 · 控场开荒", "A-Tier · Crowd Control Progression"),
        bi("War Cry 眩晕 + Battle Orders 增益，不吃命中率、装备门槛低，是开荒与 solo 通关最稳的野蛮人流派。",
           "War Cry stuns while Battle Orders buffs; it needs no attack rating and very little gear, making it the safest Barbarian build for leveling and solo clears."),
        [("War Cry", "20"), ("Battle Orders", "20"), ("Battle Command", "1"), ("Find Item", "1"),
         ("Shout", "1+"), ("Weapon Mastery", "1"),
         (bi("剩余→Shout/战吼", "Rest → Shout/warcries"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("穿装备", "Just enough for gear")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量（回蓝）", "A little (for mana)"))],
        [bi("武器：精神剑 / 高 FCR 武器", "Weapon: Spirit sword / any high-FCR weapon"),
         bi("盾：Spirit Monarch / 高 FCR 盾", "Shield: Spirit Monarch / high-FCR shield"),
         bi("头盔：+战吼头环 / Shako", "Helm: +warcries circlet / Harlequin Crest"),
         bi("甲：Enigma / Smoke", "Armor: Enigma / Smoke"),
         bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
         bi("项链：Mara's / +战吼", "Amulet: Mara's / +warcries"),
         bi("戒指：SoJ + 婚戒", "Rings: SoJ + Bul-Kathos' Wedding Band"),
         bi("手套：Magefist（FCR）", "Gloves: Magefist (FCR)")],
        [bi("War Cry 眩晕群怪后补刀", "Stun packs with War Cry, then finish them off"),
         bi("BO 提升全队血上限", "Battle Orders raises the whole party's life"),
         bi("不吃命中率，开荒友好", "No attack rating needed — very leveling friendly"),
         bi("适合 solo 通关与辅助", "Great for solo clears and party support"),
         bi("配合 Find Item 也能 MF", "Add Find Item and you can MF too")],
    )
    tips = '<div class="card"><ul class="clean">' \
           '<li><b>' + bi("开荒偏慢：", "Slow to level:") + '</b>' \
           + bi("野蛮人前期脆、命中率低，建议先练个小号或借装备；可用 Singer（战吼）过渡。",
                "Early Barbarians are squishy with poor attack rating, so twink some gear from another character or level as a Singer first.") + '</li>' \
           '<li><b>' + bi("Battle Orders 是灵魂：", "Battle Orders is everything:") + '</b>' \
           + bi("大幅提升全队生命/法力上限，组队必带。",
                "It massively raises the party's max life and mana — a must-have in groups.") + '</li>' \
           '<li><b>' + bi("Find Item（hork）：", "Find Item (horking):") + '</b>' \
           + bi("杀死 boss 后对尸体用寻物，有几率再掉一次，MF 机核心。",
                "After killing a boss, hork the corpse for a chance at a second drop — the heart of the MF Barb.") + '</li>' \
           '<li><b>' + bi("Whirlwind 吃攻速与命中：", "Whirlwind wants IAS and AR:") + '</b>' \
           + bi("用 Arreat's Face、Highlord's 等堆 IAS 与致命。",
                "Stack IAS and deadly strike with pieces like Arreat's Face and Highlord's Wrath.") + '</li>' \
           '<li><b>' + bi("Pitzerker 双倍掉落：", "Pitzerker double drops:") + '</b>' \
           + bi("Berserk（魔法伤，无视免疫）+ Find Item，The Pit 刷装备效率第一。",
                "Berserk (magic damage, ignores physical immunity) plus Find Item makes The Pit the fastest gear farm in the game.") + '</li>' \
           '<li><b>' + bi("Patch 3.3 让野蛮人变强了：", "Patch 3.3 made the Barbarian stronger:") + '</b>' \
           + bi("<b>Bloodletter（放血者）</b>新增 +20% 跑速且能更早拿到（物品等级 34→30、需求等级 25→17），<b>Manald Heal（玛那德之愈）</b>新增 +10% 施法速度，两条加起来让「双持放血者旋风」第一次成为有竞争力的<b>天梯起步</b>路线；此外 <b>Leap 落地动画卡死</b>的 bug 也已修复。往年想练野蛮人但嫌开荒太吃装备的话，本季是个好时机。",
                "<b>Bloodletter</b> gains +20% run speed and drops much earlier (item level 34→30, required level 25→17), and <b>Manald Heal</b> gains +10% faster cast rate — together they make dual-Bloodletter Whirlwind a genuinely competitive <b>Ladder starter</b> for the first time. The Leap landing-animation lock was also fixed. If you've always wanted to play a Barbarian but found the early Ladder too gear-dependent, this is the season to try it.") + '</li>' \
           '</ul></div>'
    return _class_page("野蛮人 Barbarian", "c:barbarian", intro, trees, builds, tips, "paladin.html", "圣骑士 Paladin", "druid.html", "德鲁伊 Druid")

def druid():
    intro = '<h1><span class="zt"><span class="zc">德鲁伊 </span><span class="ec" lang="en">Druid</span></span></h1>\n' \
            '<p>' + bi("德鲁伊是元素与变身的双修者：风德（Tornado + Hurricane）远程范围控场，火德（Fissure/Volcano/Armageddon）暴力 AoE，狼人/熊人则化身近战猛兽。Mosaic 与 Flickering Flame 等新符文之语也让他如虎添翼。",
                       "The Druid mixes elemental magic with shapeshifting: the Wind Druid (Tornado + Hurricane) controls the field from range, the Fire Druid (Fissure/Volcano/Armageddon) unleashes brutal AoE, and Werewolf/Werebear forms turn him into a melee beast. New runewords like Mosaic and Flickering Flame have pushed him even further.") + '</p>\n' \
            '<div class="callout tip"><b>' + bi("定位：", "Role:") + '</b>' \
            + bi("元素远程 / 变身近战 · 优势：风德安全高效、火德 AoE 爆炸、变身流爽快 · 劣势：火系吃免疫、变身流吃装备。",
                 "Elemental ranged / shapeshift melee · Pros: Wind is safe and efficient, Fire has explosive AoE, shapeshifting feels great · Cons: fire struggles with immunes and shapeshifters are gear hungry.") + '</div>'
    trees = skilltrees([
        ("Elemental", bi("远程范围法术，风/火双线。", "Ranged AoE spells split between wind and fire."),
         ["Tornado", bi("Hurricane（冰）", "Hurricane (cold)"), "Cyclone Armor", bi("Fissure（火）", "Fissure (fire)"),
          "Volcano", "Armageddon", "Firestorm / Molten Boulder"]),
        ("Shape Shifting", bi("狼人/熊人近战形态。", "Werewolf and Werebear melee forms."),
         [bi("Werewolf / Werebear（变身）", "Werewolf / Werebear (forms)"),
          bi("Fury / Maul（攻击）", "Fury / Maul (attacks)"), "Feral Rage / Rabies", "Shock Wave", "Lycanthropy"]),
        ("Summoning", bi("灵体与熊，提供增益与肉盾。", "Spirits and a grizzly for buffs and a meat shield."),
         [bi("Oak Sage（+生命）", "Oak Sage (+life)"),
          bi("Heart of Wolverine（+伤害/命中）", "Heart of Wolverine (+damage/AR)"),
          "Spirit of Barbs", "Summon Grizzly", bi("Vines（回蓝/吸血）", "Vines (mana/life recovery)")]),
    ])
    builds = build_card(
        bi("风德鲁伊", "Wind Druid"),
        bi("S 级 · 元素控场", "S-Tier · Elemental Control"),
        bi("Tornado（物理） + Hurricane（冰）双范围伤害，配合 Cyclone Armor 与 Oak Sage，安全高效，是德鲁伊最强 PvM 路线。",
           "Tornado (physical) and Hurricane (cold) give you two damage types at once; with Cyclone Armor and Oak Sage it is safe, efficient and the Druid's best PvM build."),
        [("Tornado", "20"), ("Hurricane", "20"), ("Cyclone Armor", "1+"),
         ("Oak Sage", bi("20（或 Heart of Wolverine）", "20 (or Heart of Wolverine)")),
         ("Twister", bi("1（协同）", "1 (synergy)")),
         (bi("剩余→Twister/熊", "Rest → Twister/Grizzly"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("不加（或少量格挡）", "None (or a little for block)")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量或不加", "Little to none"))],
        [bi("武器：Heart of the Oak（橡树之心）", "Weapon: Heart of the Oak"),
         bi("盾：Spirit Monarch", "Shield: Spirit Monarch"),
         bi("头盔：Jalal's Mane（加洛面具）/ +2 风 头环", "Helm: Jalal's Mane / +2 elemental circlet"),
         bi("甲：Enigma / Skin of Vipermagi", "Armor: Enigma / Skin of the Vipermagi"),
         bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
         bi("项链：Mara's / +2 风 20FCR", "Amulet: Mara's / +2 elemental, 20 FCR"),
         bi("戒指：SoJ + 婚戒", "Rings: SoJ + Bul-Kathos' Wedding Band"),
         bi("手套：Magefist（FCR）", "Gloves: Magefist (FCR)"),
         bi("破免：物理/冰 Sunder", "Sunder: Physical/Cold Sunder")],
        [bi("Tornado 远程追踪打单体/线", "Tornado tracks targets for single-target and lines"),
         bi("Hurricane 持续冰伤覆盖", "Hurricane keeps constant cold damage around you"),
         bi("Cyclone Armor 吸收元素伤", "Cyclone Armor absorbs elemental damage"),
         bi("Oak Sage 提升血上限保命", "Oak Sage raises your max life"),
         bi("堆 FCR 档位提升手感", "Hit the FCR breakpoints for smoother casting")],
    )
    builds += build_card(
        bi("火德鲁伊", "Fire Druid"),
        bi("A 级 · 火系 AoE", "A-Tier · Fire AoE"),
        bi("Fissure / Volcano / Armageddon 大范围火伤，拿到 Flickering Flame + Infinity 后配合 Fire Sunder，AoE 爆炸、farm 效率顶级。",
           "Fissure, Volcano and Armageddon cover huge areas in fire. Once you own Flickering Flame and an Infinity merc — plus a Fire Sunder — the AoE is explosive and farming is top tier."),
        [("Fissure", "20"), ("Volcano", bi("20（协同）", "20 (synergy)")),
         ("Armageddon", bi("20（协同）", "20 (synergy)")),
         ("Firestorm/Molten", bi("1（协同）", "1 (synergy)")),
         ("Oak Sage", "1+"), ("Cyclone Armor", "1"),
         (bi("剩余→协同", "Rest → synergies"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("不加", "None")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量", "A little"))],
        [bi("武器：Heart of the Oak", "Weapon: Heart of the Oak"),
         bi("盾：Spirit Monarch / 凤凰（凤凰盾，火系）", "Shield: Spirit Monarch / Phoenix shield (fire)"),
         bi("头盔：Flickering Flame（火珠头，核心）", "Helm: Flickering Flame (core fire helm)"),
         bi("甲：Enigma / Chains of Honor", "Armor: Enigma / Chains of Honor"),
         bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
         bi("项链：Mara's / +2 火", "Amulet: Mara's / +2 elemental"),
         bi("破免：Fire Sunder Charm", "Sunder: Fire Sunder Charm"),
         bi("佣兵：Infinity（降火抗）", "Merc: Infinity (lowers fire resist)")],
        [bi("Flickering Flame 提供火技能与降抗光环", "Flickering Flame gives +fire skills and a resist-lowering aura"),
         bi("Infinity 佣兵进一步降抗", "An Infinity merc strips even more resistance"),
         bi("Fire Sunder 处理火免", "A Fire Sunder handles fire immunes"),
         bi("Armageddon 持续范围灼烧", "Armageddon rains constant fire around you"),
         bi("注意自身火抗（会被削）", "Watch your own fire resist — the Sunder lowers it")],
    )
    builds += build_card(
        bi("狼人狂怒德鲁伊", "Werewolf Fury Druid"),
        bi("A 级 · 变身近战", "A-Tier · Shapeshift Melee"),
        bi("变身为狼，Fury 多段高攻速攻击，配合 Heart of Wolverine 增伤与橡木保命，是爽快的近战路线。",
           "Shift into a wolf and let Fury's rapid multi-hits fly; Heart of Wolverine adds damage while Oak Sage keeps you alive — a very satisfying melee route."),
        [("Werewolf", "20"), ("Fury", "20"), ("Lycanthropy", "1+"), ("Heart of Wolverine", "20"),
         ("Feral Rage", bi("1（吸血）", "1 (life steal)")), ("Oak Sage", "1+"),
         (bi("剩余→Rabies/熊", "Rest → Rabies/Grizzly"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("穿装备 / 堆命中", "Enough for gear, or more for attack rating")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("不加", "None"))],
        [bi("武器：Grief / 死亡呼吸（双持爪/斧）", "Weapon: Grief / Breath of the Dying (dual claws or axes)"),
         bi("盾（剑盾）：Stormshield / Phoenix", "Shield: Stormshield / Phoenix"),
         bi("头盔：Jalal's Mane / 狼头", "Helm: Jalal's Mane / a druid pelt"),
         bi("甲：Fortitude / Enigma", "Armor: Fortitude / Enigma"),
         bi("腰带：String of Ears", "Belt: String of Ears"),
         bi("项链：Highlord's / Mara's", "Amulet: Highlord's Wrath / Mara's"),
         bi("戒指：Raven Frost + 婚戒", "Rings: Raven Frost + Bul-Kathos' Wedding Band"),
         bi("靴：Gore Rider", "Boots: Gore Rider"),
         bi("手套：Dracul's（偷血）", "Gloves: Dracul's Grasp (life tap)")],
        [bi("变身狼后 Fury 高速连击", "Shift to wolf form and chain Fury attacks"),
         bi("Heart of Wolverine 增伤命中", "Heart of Wolverine adds damage and attack rating"),
         bi("Feral Rage 吸血续航", "Feral Rage sustains you with life steal"),
         bi("物理免疫切元素/破物", "Against physical immunes swap to elemental or use a Physical Sunder"),
         bi("靠高血与偷血硬刚", "Tank through fights with big life and leech")],
    )
    tips = '<div class="card"><ul class="clean">' \
           '<li><b>' + bi("风德开荒最顺：", "Wind Druid levels smoothest:") + '</b>' \
           + bi("Tornado + Hurricane 双元素范围，前期用火，30 级后洗成风德，安全性高。",
                "Tornado plus Hurricane covers two elements; level with fire early, respec to wind around level 30 for a very safe ride.") + '</li>' \
           '<li><b>' + bi("火德需破火免：", "Fire Druid must break fire immunes:") + '</b>' \
           + bi("拿 Flickering Flame（火珠头） + Infinity 佣兵 + Fire Sunder，AoE 爆炸极强。",
                "Flickering Flame, an Infinity merc and a Fire Sunder together make the AoE devastating.") + '</li>' \
           '<li><b>' + bi("橡木贤者 Oak Sage：", "Oak Sage:") + '</b>' \
           + bi("提升生命上限，是元素流的重要保命召唤。",
                "It raises your max life and is the key survival summon for elemental builds.") + '</li>' \
           '<li><b>' + bi("狼人 Fury：", "Werewolf Fury:") + '</b>' \
           + bi("高攻速近战，配合风灵（Heart of Wolverine）与狂犬病可选。",
                "Very fast melee; pair it with Heart of Wolverine and optionally Rabies.") + '</li>' \
           '<li><b>' + bi("熊人 Shock Wave：", "Werebear Shock Wave:") + '</b>' \
           + bi("眩晕控场 + Maul 高伤，适合硬刚。",
                "Stun-lock packs with Shock Wave and crush them with Maul if you like tanking.") + '</li>' \
           '</ul></div>'
    return _class_page("德鲁伊 Druid", "c:druid", intro, trees, builds, tips, "barbarian.html", "野蛮人 Barbarian", "warlock.html", "术士 Warlock")

def warlock():
    intro = '<h1><span class="zt"><span class="zc">术士 </span><span class="ec" lang="en">Warlock</span></span></h1>\n' \
            '<p>' + bi("术士是《暗黑破坏神 II：复活》「术士君临（Reign of the Warlock）」资料片在 2026 年新增的第八个职业，也是原版发售 25 年来首次加入的新职业。他是一位钻研禁忌恶魔之术的黑暗学者，通过束缚、奴役甚至吞噬恶魔来获取力量。三大技能树分别为 <b>Chaos（混沌）</b>、<b>Eldritch（邪术）</b> 与 <b>Demon（恶魔）</b>。",
                       "The Warlock is the eighth class, added to Diablo II: Resurrected by the 2026 <i>Reign of the Warlock</i> expansion — the first new class in the 25 years since the original release. He is a dark scholar of forbidden demonic arts who gains power by binding, enslaving and even devouring demons. His three skill trees are <b>Chaos</b>, <b>Eldritch</b> and <b>Demon</b>.") + '</p>\n' \
            '<div class="callout tip"><b>' + bi("定位：", "Role:") + '</b>' \
            + bi("恶魔召唤 / 邪术近战 / 混沌远程 · 优势：独有双持机制、恶魔奴役玩法、三系皆强 · 劣势：核心伤害仅魔法+火焰（无冰/电/毒），部分免疫需针对性处理。",
                 "Demon summoner / Eldritch melee / Chaos ranged · Pros: a unique two-handed-plus-offhand mechanic, demon enslavement gameplay, all three trees are strong · Cons: his core damage is only magic and fire (no cold/lightning/poison), so some immunes need special handling.") + '</div>'
    trees = skilltrees([
        ("Demon", bi("奴役与吞噬恶魔，提供强力盟友与临时增益。", "Enslave and devour demons for powerful allies and temporary buffs."),
         ["Bind Demon / Summon Goatmen", "Summon Tainted", "Summon Defiler",
          bi("Bind Single Demon（30 级解锁，绑定单只恶魔取其技能）", "Bind Single Demon (unlocks at 30; bind one demon and borrow its skills)"),
          bi("Consume Demon（吞噬恶魔，吸取生命力换增益）", "Consume Demon (devour a demon, trading its life force for a buff)")]),
        ("Eldritch", bi("以意念操控武器，施加咒术强化攻击。", "Control weapons with your mind and hex them to empower your attacks."),
         [bi("Hex Weapon（咒武：削弱/吸血/爆裂）", "Hex Weapon (weaken / leech / explode)"),
          bi("Ethereal Duplicate（幻影分身武器）", "Ethereal Duplicate (a phantom copy of your weapon)"),
          bi("Throw Weapon（远程投掷）", "Throw Weapon (ranged toss)"),
          bi("Two-Handed + Offhand（单手拿双手武器+副手）", "Two-Handed + Offhand (wield a two-hander one-handed with an offhand)"),
          bi("Weapon Levitation（武器悬浮被动）", "Weapon Levitation (the levitation passive)")]),
        ("Chaos", bi("操控地狱火与虚空，远程范围毁灭。", "Command hellfire and the void for ranged mass destruction."),
         [bi("Miasma（瘴气弹幕）", "Miasma (a barrage of miasma)"),
          bi("Apocalypse（天启焚尽）", "Apocalypse (burn everything down)"),
          bi("Abyss（深渊吞噬）", "Abyss (devour with the void)"),
          bi("Hellfire / Void（地狱火与虚空）", "Hellfire / Void"),
          bi("Entropy Mastery（熵能精通）", "Entropy Mastery")]),
    ])
    builds = build_card(
        bi("恶魔契约术士", "Demon Warlock"),
        bi("A 级 · 承压/辅助（3.3 下修）", "A-Tier · Tank/Support (nerfed in 3.3)"),
        bi("以 Demon 系为核心，奴役 Goatmen/Tainted/Defiler 组成恶魔大军，30 级后绑定单只恶魔取其专属技能，必要时吞噬恶魔换取临时增益。<b>Patch 3.3 下修了 Bind Demon 的额外伤害加成</b>，本季更适合做安全可靠的开荒脊梁与承压/辅助，而不是指望召唤物打满输出。",
           "Built around the Demon tree: enslave Goatmen, Tainted and Defilers into a demonic army, bind a single demon at level 30 to borrow its signature skill, and devour demons for temporary buffs when you need them. <b>Patch 3.3 tuned Bind Demon's bonus damage down</b>, so this season it excels as a safe progression backbone and a tank/support shell rather than a summon-based main damage source."),
        [("Bind Demon / Summon Goatmen", "20"), ("Summon Tainted", "20"),
         ("Summon Defiler", bi("20（或按需）", "20 (or as needed)")),
         ("Bind Single Demon", bi("1（30 级解锁，必点）", "1 (unlocks at 30, mandatory)")),
         ("Consume Demon", bi("1+（按需）", "1+ (as needed)")),
         ("Demon Mastery", bi("0~20（协同）", "0–20 (synergy)")),
         (bi("其余→恶魔协同", "Rest → Demon synergies"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("刚好穿装备或少量", "Just enough for gear, or a little")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量（靠装备回蓝）", "A little (rely on gear for mana)"))],
        [bi("武器：Heart of the Oak（橡树之心） / 术士专属暗金法杖", "Weapon: Heart of the Oak / a Warlock-only unique staff"),
         bi("盾：Spirit Monarch（精神）", "Shield: Spirit Monarch"),
         bi("头盔：+2 恶魔 头环 / Shako（军帽）", "Helm: +2 Demon circlet / Harlequin Crest"),
         bi("甲：Enigma（谜团）/ Chains of Honor（荣耀之链）", "Armor: Enigma / Chains of Honor"),
         bi("腰带：Arachnid Mesh（蜘蛛之网）", "Belt: Arachnid Mesh"),
         bi("项链：Mara's（马拉）/ +2 恶魔 20FCR", "Amulet: Mara's / +2 Demon, 20 FCR"),
         bi("戒指：SoJ（乔丹之石）+ 婚戒", "Rings: SoJ + Bul-Kathos' Wedding Band"),
         bi("手套：Magefist（法师之拳）", "Gloves: Magefist"),
         bi("佣兵：力量光环 / Infinity（无限）破免", "Merc: Might aura / Infinity to break immunes")],
        [bi("先召唤恶魔大军再进战，Goatmen 近战 + Tainted/Defiler 远程", "Summon the full army before engaging — Goatmen up front, Tainted/Defilers at range"),
         bi("30 级解锁 Bind Single Demon，绑定强力恶魔取其技能", "At level 30 use Bind Single Demon on a strong demon to borrow its skill"),
         bi("危急时 Consume Demon 吞噬恶魔换临时增益", "In an emergency, Consume Demon for a temporary buff"),
         bi("恶魔系提供 buff，配合 Enigma 机动与佣兵", "The Demon tree buffs you; add Enigma mobility and a merc"),
         bi("核心伤害魔法+火焰，遇魔免/火免用佣兵或副手", "Your damage is magic and fire, so lean on the merc or a weapon swap against those immunes")],
    )
    builds += build_card(
        bi("邪术武者术士", "Eldritch Warlock"),
        bi("A 级 · 近战流派", "A-Tier · Melee Build"),
        bi("以 Eldritch 系为核心，用意念操控武器、施加咒术（削弱/吸血/爆裂），并依靠独有机制「单手拿双手武器+副手」打出高额近战。幻影分身与投掷提升灵活。",
           "Built around the Eldritch tree: control your weapon with your mind, hex it (weaken / leech / explode), and exploit the unique ability to wield a two-hander one-handed alongside an offhand for huge melee damage. Ethereal Duplicate and Throw Weapon add flexibility."),
        [("Hex Weapon", "20"), ("Ethereal Duplicate", "20"),
         ("Throw Weapon", bi("1~20（按需）", "1–20 (as needed)")),
         ("Two-Handed Mastery", bi("0~20（协同）", "0–20 (synergy)")),
         ("Weapon Levitation", bi("1（被动，核心机制）", "1 (passive, the core mechanic)")),
         (bi("Demon / Chaos 协同", "Demon / Chaos synergies"), "0~20"),
         (bi("其余→邪术协同", "Rest → Eldritch synergies"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备（Enigma 等）", "Just enough for gear (Enigma etc.)")),
         (bi("敏捷", "Dexterity"), bi("刚好穿武器", "Just enough for your weapon")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("不加", "None"))],
        [bi("武器：高 ED 双手武器（Death / Grief（悲伤））或术士专属双手暗金", "Weapon: a high-ED two-hander (Death / Grief) or a Warlock-only two-handed unique"),
         bi("副手：Spirit Monarch（精神）/ 术士专属副手", "Offhand: Spirit Monarch / a Warlock-only offhand"),
         bi("头盔：Arreat's Face（亚瑞特之脸）/ Guillaume's（纪尧姆之颅）", "Helm: Arreat's Face / Guillaume's Face"),
         bi("甲：Fortitude（刚毅）/ Enigma（谜团）", "Armor: Fortitude / Enigma"),
         bi("腰带：String of Ears（耳串）", "Belt: String of Ears"),
         bi("项链：Highlord's Wrath（大君之怒）/ Mara's（马拉）", "Amulet: Highlord's Wrath / Mara's"),
         bi("戒指：Raven Frost + 婚戒 / SoJ（乔丹之石）", "Rings: Raven Frost + Bul-Kathos' Wedding Band / SoJ"),
         bi("靴：Gore Rider（蚀肉骑士）", "Boots: Gore Rider"),
         bi("手套：+邪术技能手套", "Gloves: +Eldritch skill gloves"),
         bi("佣兵：Infinity（无限）破免", "Merc: Infinity to break immunes")],
        [bi("核心机制：Weapon Levitation 单手拿双手武器+副手，攻防兼备", "Core mechanic: Weapon Levitation lets you hold a two-hander plus an offhand — offence and defence at once"),
         bi("Hex Weapon 附咒：削弱/吸血/爆裂，近战越打越爽", "Hex Weapon adds weaken / leech / explode effects that snowball in melee"),
         bi("Ethereal Duplicate 幻影分身武器协同攻击", "Ethereal Duplicate attacks alongside you"),
         bi("Throw Weapon 远程消耗配合近战节奏", "Throw Weapon chips targets between melee swings"),
         bi("无冰/电/毒伤，遇免疫靠 Infinity 与破免", "No cold/lightning/poison damage — rely on Infinity and Sunder Charms for immunes")],
    )
    builds += build_card(
        bi("混沌术士", "Chaos Warlock"),
        bi("S 级 · 远程 AoE", "S-Tier · Ranged AoE"),
        bi("以 Chaos 系为核心，操控地狱火与虚空，Miasma 弹幕清场、Apocalypse 焚尽全场、Abyss 撕裂现实吞噬一切。玻璃大炮，范围毁灭顶级。",
           "Built around the Chaos tree: command hellfire and the void — Miasma sprays packs down, Apocalypse burns the screen and Abyss tears reality open to swallow everything. A glass cannon with top-tier area destruction."),
        [("Miasma", "20"), ("Apocalypse", "20"), ("Abyss", bi("20（或 1 大招）", "20 (or 1 as an ultimate)")),
         ("Hellfire / Void", bi("0~20（协同）", "0–20 (synergy)")),
         ("Entropy Mastery", bi("1→满（增伤减抗）", "1 → max (damage and resist reduction)")),
         (bi("Demon 协同", "Demon synergies"), "0~20"),
         (bi("其余→混沌协同", "Rest → Chaos synergies"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("不加", "None")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量（靠回蓝装）", "A little (use mana regen gear)"))],
        [bi("武器：Heart of the Oak（橡树之心）/ Obsession（痴迷）", "Weapon: Heart of the Oak / Obsession"),
         bi("盾：Spirit Monarch（精神）", "Shield: Spirit Monarch"),
         bi("头盔：Nightwing's Veil（夜翼面纱）/ +2 混沌 头环", "Helm: Nightwing's Veil / +2 Chaos circlet"),
         bi("甲：Enigma（谜团）/ Tal Rasha's（塔拉夏）", "Armor: Enigma / Tal Rasha's"),
         bi("腰带：Arachnid Mesh（蜘蛛之网）", "Belt: Arachnid Mesh"),
         bi("项链：Mara's（马拉）/ +2 混沌 20FCR", "Amulet: Mara's / +2 Chaos, 20 FCR"),
         bi("戒指：SoJ（乔丹之石）+ 婚戒", "Rings: SoJ + Bul-Kathos' Wedding Band"),
         bi("手套：Magefist（法师之拳）", "Gloves: Magefist"),
         bi("破免：Magic/Fire Sunder（魔/火破免）", "Sunder: Magic/Fire Sunder"),
         bi("佣兵：Infinity（无限）", "Merc: Infinity")],
        [bi("Miasma 主力清场弹幕，Apocalypse 处理密集大群", "Miasma is your main clear tool; Apocalypse handles the biggest packs"),
         bi("Abyss 终极大招，撕裂现实吞噬范围内一切", "Abyss is the ultimate — it tears reality open and devours everything in range"),
         bi("核心伤害魔法+火焰，堆 Magic/Fire Sunder 处理对应免疫", "Damage is magic and fire, so carry Magic/Fire Sunders for immunes"),
         bi("脆皮靠走位与 Enigma 传送保命", "You are squishy — survive with positioning and Enigma's Teleport"),
         bi("Entropy Mastery 减抗是伤害核心，优先点满", "Entropy Mastery's resist reduction is your damage core — max it first")],
    )
    builds += build_card(
        bi("死亡印记术士", "Sigil of Death Warlock"),
        bi("S 级 · 第 15 赛季术士主推", "S-Tier · The Season 15 Warlock Pick"),
        bi("Patch 3.3 的最大受益者。原本 Sigil: Death 因为「施法失败照样耗蓝」和「+火焰技能不参与伤害计算」两个 bug 长期吃暗亏；3.3 一并修复后伤害与手感双双到位，成为本季术士的<b>输出主力</b>，也是想在本次资料片里玩新内容时最推荐的方向。",
           "The biggest winner of Patch 3.3. Sigil: Death had been quietly gimped by two bugs — burning mana even on failed casts, and ignoring +fire-skill bonuses. With both fixed in 3.3 its damage and feel are finally where they should be, making it the Warlock's <b>main damage build</b> this season and the best way to actually play the new expansion content."),
        [("Sigil: Death", "20"),
         (bi("火焰协同技能", "Fire synergies"), "20"),
         ("Entropy Mastery", bi("1→满（减抗核心）", "1 → max (resist reduction core)")),
         ("Hellfire / Void", bi("0~20（协同）", "0–20 (synergy)")),
         (bi("Demon 系承压（可选）", "Demon tree for tanking (optional)"), "1~10"),
         (bi("其余→混沌协同", "Rest → Chaos synergies"), "—")],
        [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")),
         (bi("敏捷", "Dexterity"), bi("不加", "None")),
         (bi("体力", "Vitality"), bi("其余全加", "Everything else")),
         (bi("能量", "Energy"), bi("少量（靠回蓝装）", "A little (use mana regen gear)"))],
        [bi("武器：Heart of the Oak（橡树之心）/ Obsession（痴迷）", "Weapon: Heart of the Oak / Obsession"),
         bi("副手：Grimoire（魔典，触发单手拿双手武器）", "Offhand: a Grimoire (enables holding a two-hander one-handed)"),
         bi("头盔：+2 混沌头环 / 火焰技能头环", "Helm: +2 Chaos circlet / a fire-skills circlet"),
         bi("甲：Enigma（谜团）/ Chains of Honor（荣耀之链）", "Armor: Enigma / Chains of Honor"),
         bi("腰带：Arachnid Mesh（蜘蛛之网，20% FCR）", "Belt: Arachnid Mesh (20% FCR)"),
         bi("项链：Mara's（马拉）/ +2 混沌 20FCR", "Amulet: Mara's / +2 Chaos, 20 FCR"),
         bi("戒指：SoJ（乔丹之石）×2 或 + 婚戒", "Rings: SoJ ×2, or SoJ + Bul-Kathos' Wedding Band"),
         bi("手套：Magefist（法师之拳，+火焰技能）", "Gloves: Magefist (+fire skills)"),
         bi("破免：Fire Sunder（火破免）", "Sunder: Fire Sunder"),
         bi("佣兵：Infinity（无限）降抗", "Merc: Infinity for resist reduction")],
        [bi("堆叠 +火焰技能与 FCR：3.3 修复后这些词缀终于对 Sigil: Death 生效", "Stack +fire skills and FCR — since the 3.3 fix these affixes finally apply to Sigil: Death"),
         bi("火免怪靠 Fire Sunder + 佣兵 Infinity 处理", "Fire immunes are handled with a Fire Sunder plus an Infinity merc"),
         bi("脆皮远程，用走位与 Enigma 传送拉开距离", "A squishy ranged build — create distance with positioning and Enigma's Teleport"),
         bi("可混搭 Demon 系召唤物当肉盾，开荒期非常安全", "Splash into the Demon tree for meat shields — very safe while progressing")],
    )
    tips = '<div class="card"><ul class="clean">' \
           '<li><b>' + bi("2026 新职业：", "New class in 2026:") + '</b>' \
           + bi("术士来自「术士君临（Reign of the Warlock）」资料片，是 D2R 时隔 25 年首个新职业，第八位登场角色。",
                "The Warlock arrives with the Reign of the Warlock expansion — D2R's first new class in 25 years and the eighth to join the roster.") + '</li>' \
           '<li><b>' + bi("三系定位：", "The three trees:") + '</b>' \
           + bi("Chaos（混沌）远程 AoE、Eldritch（邪术）近战咒武、Demon（恶魔）奴役召唤，构筑灵活。",
                "Chaos for ranged AoE, Eldritch for hexed melee weapons, Demon for enslaved summons — very flexible build options.") + '</li>' \
           '<li><b>' + bi("独有机制（已修正）：", "Unique mechanic (since patch 3.2):") + '</b>' \
           + bi("Weapon Levitation 让术士可单手装备双手武器并同时持副手，但<b>副手必须是 Grimoire（魔典）</b>才能触发——此前的「双手武器 + 精神盾」组合已被移除，配装时按魔典路线走。",
                "Weapon Levitation lets the Warlock wield a two-handed weapon in one hand while keeping an offhand — but <b>the offhand must be a Grimoire</b> to enable it. The old \"two-hander + Spirit shield\" combination has been removed, so build around a Grimoire offhand.") + '</li>' \
           '<li><b>' + bi("恶魔玩法：", "Demon gameplay:") + '</b>' \
           + bi("30 级解锁 Bind Single Demon，可绑定一只恶魔取其专属技能；Consume Demon 吞噬恶魔换临时增益。",
                "Bind Single Demon unlocks at level 30 and lets you borrow a demon's signature skill, while Consume Demon devours one for a temporary buff.") + '</li>' \
           '<li><b>' + bi("招牌技能：", "Signature skill:") + '</b>' \
           + bi("Echoing Strike 是术士招牌近战技，造成暗影伤害并在附近敌人间回响，被社区评为终局 S 级技能。",
                "Echoing Strike is his signature melee skill — it deals shadow damage that echoes between nearby enemies and the community rates it S-tier for endgame.") + '</li>' \
           '<li><b>' + bi("Patch 3.3 调整：", "Patch 3.3 adjustments:") + '</b>' \
           + bi("<b>Bind Demon（束缚恶魔）的额外伤害加成被下修</b>（原先高于设计值），纯召唤路线不再是输出主力，转向承压/辅助；作为补偿，<b>Sigil: Death（死亡印记）</b>修复了「施法失败仍耗蓝」与「+火焰技能不参与计算」两个 bug，一跃成为术士本季的输出主力。此外 Miasma Chain 的弹道判定、Leap 动画卡死等问题也已修复。",
                "<b>Bind Demon's bonus damage was tuned down</b> (it had been higher than intended), so pure summoning is no longer your main damage source and shifts into a tank/support role. In exchange, <b>Sigil: Death</b> got its \"mana burned on failed cast\" and \"fire-skill bonuses not applying\" bugs fixed, vaulting it to the Warlock's top damage build this season. Miasma Chain's missile collision and the Leap animation lock were also fixed.") + '</li>' \
           '<li><b>' + bi("本季推荐：", "Recommended this season:") + '</b>' \
           + bi("想玩新内容首选 <b>Sigil: Death</b>（远程、依赖 FCR 与火焰技能加成）；求稳开荒仍可用恶魔系承压 + 本体输出的混搭。术士不建议作为天梯开荒的第一个角色——先把机制摸清楚、攒到资源再练收益更高。",
                "To explore the new content, pick <b>Sigil: Death</b> (ranged, scales with FCR and fire-skill bonuses); for safe progression, still run a Demon-tree meat shield plus your own body damage. Don't make the Warlock your first Ladder character — learn the mechanics and bank resources first, then level one for much better returns.") + '</li>' \
           '<li><b>' + bi("伤害限制：", "Damage limitations:") + '</b>' \
           + bi("术士核心伤害为魔法与火焰（近战附带物理），无冰/电/毒属性，遇对应免疫需 Infinity 与 Sunder 护符。",
                "His core damage is magic and fire (melee adds physical) with no cold, lightning or poison, so those immunes require Infinity and Sunder Charms.") + '</li>' \
           '<li><b>' + bi("新终局内容：", "New endgame content:") + '</b>' \
           + bi("资料片同步加入 Colossal Ancients、Loot Filter（战利品过滤器）、Chronicle（编年史）收集系统与全新仓库分页。",
                "The expansion also adds the Colossal Ancients, a Loot Filter, the Chronicle collection system and new stash tabs.") + '</li>' \
           '</ul></div>'
    return _class_page("术士 Warlock", "c:warlock", intro, trees, builds, tips, "druid.html", "德鲁伊 Druid", "assassin.html", "刺客 Assassin")

def assassin():
    intro = '<h1><span class="zt"><span class="zc">刺客 </span><span class="ec" lang="en">Assassin</span></span></h1>\n' \
            '<p>' + bi("刺客是陷阱与武学的宗师。Trapsin（陷阱刺客）用闪电/死亡陷阱远程清场，是最强的 solo 通关流派之一；而 Mosaic 武学刺客凭借新符文之语实现了「永久蓄力」，化身全屏元素风暴，是当前版本的顶级战力。",
                       "The Assassin is the master of traps and martial arts. A Trapsin clears screens at range with Lightning and Death Sentries and is one of the safest solo-clearing builds; the Mosaic martial-arts Assassin uses the new runeword to make charges permanent, becoming a screen-wide elemental storm and a top-tier force in the current patch.") + '</p>\n' \
            '<div class="callout tip"><b>' + bi("定位：", "Role:") + '</b>' \
            + bi("陷阱远程 / 武学近战 · 优势：Trapsin 极安全、Mosaic 全屏 AoE 顶级 · 劣势：Mosaic 双爪难凑、武学需练习蓄力节奏。",
                 "Ranged traps / melee martial arts · Pros: Trapsin is extremely safe, Mosaic's screen-wide AoE is top-tier · Cons: a Mosaic claw pair is hard to assemble, martial arts needs practice on charge timing.") + '</div>'
    trees = skilltrees([
        ("Traps", bi("远程布置陷阱，主流输出系。", "Place traps at range; the primary damage tree."),
         ["Lightning Sentry", bi("Death Sentry（火/物+尸爆）", "Death Sentry (fire/phys + corpse explosion)"), "Fire Sentry", bi("Shock Web / Charged Bolt Sentry", "Shock Web / Charged Bolt Sentry"), bi("Wake of Fire / Inferno Sentry", "Wake of Fire / Inferno Sentry")]),
        ("Martial Arts", bi("蓄力 + 终结技的近战体系。", "Charge-up plus finisher melee system."),
         [bi("Phoenix Strike（多元素）", "Phoenix Strike (multi-element)"), bi("Claws of Thunder / Blades of Ice / Fists of Fire", "Claws of Thunder / Blades of Ice / Fists of Fire"), bi("Tiger Strike / Cobra Strike", "Tiger Strike / Cobra Strike"), bi("Dragon Talon / Dragon Claw / Dragon Tail（终结）", "Dragon Talon / Dragon Claw / Dragon Tail (finishers)"), bi("Dragon Flight（位移）", "Dragon Flight (dash)")]),
        ("Shadow Disciplines", bi("保命、控场与增益。", "Survival, crowd control and buffs."),
         ["Burst of Speed", bi("Fade（抗性与减伤）", "Fade (resists and damage reduction)"), bi("Cloak of Shadows（致盲）", "Cloak of Shadows (blind)"), bi("Mind Blast（眩晕/转化）", "Mind Blast (stun/convert)"), "Venom", bi("Weapon Block / Shadow Master", "Weapon Block / Shadow Master")]),
    ])
    builds = build_card(bi("陷阱刺客", "Trapsin"),
               bi("S 级 · 安全远程", "S-Tier · Safe Ranged"),
               bi("Lightning Sentry + Death Sentry 提供电/火/物三系混合伤害，配合 shadow 系控场，几乎无免疫盲点，是最强 solo 通关流派之一。",
                  "Lightning Sentry plus Death Sentry deal mixed lightning/fire/physical damage; with Shadow Disciplines for control there is almost no immunity blind spot, making Trapsin one of the strongest solo-clearing builds."),
               [("Lightning Sentry", "20"), ("Death Sentry", "20"), ("Fire Sentry", bi("20（或 1）", "20 (or 1)")), ("Shock Web", bi("1（协同）", "1 (synergy)")),
                ("Wake of Fire", bi("1（协同）", "1 (synergy)")), (bi("Cloak of Shadows/Mind Blast", "Cloak of Shadows/Mind Blast"), bi("各 1", "1 each")), (bi("Fade/Burst", "Fade/Burst"), bi("各 1", "1 each")), ("Venom", "1"),
                (bi("剩余→Death Sentry/火力", "Rest → Death Sentry / damage"), "—")],
               [(bi("力量", "Strength"), bi("刚好穿装备", "Just enough for gear")), (bi("敏捷", "Dexterity"), bi("刚好穿装备（或堆格挡）", "Just enough for gear (or max block)")), (bi("体力", "Vitality"), bi("其余全加", "Everything else")), (bi("能量", "Energy"), bi("不加", "None"))],
               [bi("武器：+3 陷阱爪 / Bartuc's / Spirit", "Weapon: +3 trap claws / Bartuc's / Spirit"),
                bi("盾：Spirit Monarch / 暗金爪盾", "Shield: Spirit Monarch / unique claw shield"),
                bi("头盔：Shako / +2 陷阱头环", "Helm: Harlequin Crest / +2 trap circlet"),
                bi("甲：Enigma / Chains of Honor / Skullder's", "Armor: Enigma / Chains of Honor / Skullder's"),
                bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
                bi("项链：Mara's / +2 陷阱 20FCR", "Amulet: Mara's / +2 traps, 20 FCR"),
                bi("戒指：SoJ + 婚戒", "Rings: SoJ + Bul-Kathos' Wedding Band"),
                bi("手套：Magefist（FCR）", "Gloves: Magefist (FCR)"),
                bi("破免：电/火/物 Sunder", "Sunder: lightning/fire/physical Sunder")],
               [bi("进门先放 Lightning Sentry 群电", "Drop Lightning Sentry at the door for chain lightning"),
                bi("Death Sentry 触发尸爆连锁", "Death Sentry triggers corpse-explosion chains"),
                bi("Cloak of Shadows 致盲保命", "Cloak of Shadows blinds for safety"),
                bi("Mind Blast 眩晕危险怪", "Mind Blast stuns dangerous foes"),
                bi("三系伤害几乎无免疫盲点", "Three damage types leave almost no immunity gap")])
    builds += build_card(bi("马赛克武学刺客", "Mosaic Martial Arts"),
               bi("S 级 · 全屏元素", "S-Tier · Screen-wide Elemental"),
               bi("双持 Mosaic 爪实现 100% 不消耗蓄力，蓄好 Phoenix Strike / Claws of Thunder / Blades of Ice 后狂踩 Dragon Talon，全屏火/电/冰齐发，当前版本顶级战力。",
                  "Dual Mosaic claws give a 100% chance not to consume charges; bank Phoenix Strike / Claws of Thunder / Blades of Ice, then spam Dragon Talon to unleash screen-wide fire/lightning/cold — a top-tier build in the current patch."),
               [("Phoenix Strike", "20"), ("Claws of Thunder", "20"), ("Blades of Ice", "20"), (bi("Fists of Fire", "Fists of Fire"), bi("1（可选）", "1 (optional)")),
                (bi("Dragon Talon", "Dragon Talon"), bi("1~5（终结）", "1–5 (finisher)")), ("Burst of Speed", "1"), (bi("Fade", "Fade"), bi("1+（抗/减伤）", "1+ (resist/DR)")), (bi("Cloak/Mind Blast", "Cloak/Mind Blast"), bi("各 1", "1 each")),
                (bi("Weapon Block", "Weapon Block"), "1"), (bi("剩余→Fade/Shadow", "Rest → Fade/Shadow"), "—")],
               [(bi("力量", "Strength"), bi("刚好穿装备（Enigma 等）", "Just enough for gear (Enigma, etc.)")), (bi("敏捷", "Dexterity"), bi("刚好穿爪", "Just enough for claws")), (bi("体力", "Vitality"), bi("其余全加", "Everything else")), (bi("能量", "Energy"), bi("不加", "None"))],
               [bi("武器：双持 Mosaic 爪（Mal+Gul+Amn，+3 Phoenix/Thunder 词缀最佳）", "Weapon: dual Mosaic claws (Mal+Gul+Amn, +3 Phoenix/Thunder affix preferred)"),
                bi("甲：Enigma（传送）", "Armor: Enigma (Teleport)"),
                bi("头盔：Griffon's Eye（电珠）/ 头环", "Helm: Griffon's Eye (lightning facet) / circlet"),
                bi("腰带：Arachnid Mesh", "Belt: Arachnid Mesh"),
                bi("项链：Mara's / +2 武学", "Amulet: Mara's / +2 martial arts"),
                bi("戒指：Raven Frost + SoJ/婚戒", "Rings: Raven Frost + SoJ/Wedding Band"),
                bi("靴：Shadow Dancer / Gore Rider", "Boots: Shadow Dancer / Gore Rider"),
                bi("手套：+武学技能手套", "Gloves: +martial-arts-skill gloves"),
                bi("佣兵：Infinity（降抗）", "Mercenary: Infinity (resist reduction)")],
               [bi("开局蓄好三个元素 charge", "Open by banking the three elemental charges"),
                bi("Dragon Talon 连踢触发全屏技能", "Chain Dragon Talon kicks to trigger screen-wide skills"),
                bi("每 ~14 秒接触敌人刷新计时", "Touch an enemy every ~14s to refresh the timer"),
                bi("Fade 提供抗性与减伤保命", "Fade gives resists and damage reduction to survive"),
                bi("四系伤害轻松应对免疫", "Four damage types handle immunities with ease"),
                bi("Uber 也适用，注意节奏", "Also works on Ubers; mind the timing")])
    tips = '<div class="card"><ul class="clean">' \
           '<li><b>' + bi("开荒首选 Trapsin：", "Trapsin for progression:") + '</b>' \
           + bi("Lightning Sentry + Death Sentry 三系混合伤害，几乎无免疫盲点，shadow 系控场保命。",
                "Lightning Sentry plus Death Sentry deal mixed damage across three elements with almost no immunity gap, and the Shadow tree controls and keeps you alive.") + '</li>' \
           '<li><b>' + bi("Mosaic 是革命：", "Mosaic is a revolution:") + '</b>' \
           + bi("双持 Mosaic 爪有 100% 概率不消耗蓄力，蓄好 Phoenix Strike 等后狂踩 Dragon Talon 即可全屏放技能。",
                "Dual Mosaic claws have a 100% chance not to consume charges, so bank Phoenix Strike and spam Dragon Talon to unleash screen-wide skills.") + '</li>' \
           '<li><b>' + bi("蓄力机制：", "Charge mechanic:") + '</b>' \
           + bi("武学刺客先蓄 charge-up 再放 finisher；Mosaic 下每 14 秒需接触敌人刷新计时。",
                "Martial-arts Assassins charge up before releasing a finisher; under Mosaic you must touch an enemy every 14s to refresh the timer.") + '</li>' \
           '<li><b>' + bi("Shadow 系保命：", "Shadow tree survival:") + '</b>' \
           + bi("Cloak of Shadows 致盲、Mind Blast 眩晕/转化、Fade 加抗减伤、Weapon Block 格挡。",
                "Cloak of Shadows blinds, Mind Blast stuns/converts, Fade adds resist and damage reduction, and Weapon Block gives blocking.") + '</li>' \
           '<li><b>' + bi("Death Sentry 尸爆：", "Death Sentry corpse explosion:") + '</b>' \
           + bi("死亡陷阱触发尸体爆炸，群怪清场利器。",
                "Death Sentry triggers corpse explosions — a great tool for clearing packs.") + '</li>' \
           '</ul></div>'
    return _class_page("刺客 Assassin", "c:assassin", intro, trees, builds, tips, "warlock.html", "术士 Warlock", "../index.html", bi("返回首页", "Back to Home"))

# ===========================================================================
# GUIDE PAGES
# ===========================================================================
def _guide_page(title, active, body_inner):
    _gid = active.split(":", 1)[1] if active.startswith("g:") else ""
    _gn = _ge = title
    for _g, _n, _e in GUIDE_LIST:
        if _g == _gid:
            _gn, _ge = _n, _e
            break
    body = '<div class="breadcrumb"><a href="../index.html">' + bi("首页", "Home") + '</a> / ' \
           + bi("攻略", "Guides") + ' / ' + bi(_gn, _ge) + '</div>\n' + body_inner
    return page(_gn.replace(" & ", "与") + " · 暗黑破坏神 II 攻略站", 1, body, active, True,
                desc=GUIDE_DESC.get(_gid, SITE_DESC), en_t=_ge + " | Diablo II: Resurrected Guide",
                keywords=GUIDE_KW.get(_gid, HOME_KW))

def g_runewords():
    rows = [
        ("Mosaic", "Mal + Gul + Amn", bi("3 孔 爪", "3-socket Claw"), bi("刺客武学革命：50% 不消耗蓄力（双持 100%），+2 武学、元素技能伤害，永久蓄力全屏。", "An Assassin martial-arts revolution: 50% chance not to consume charges (100% dual-wielded), +2 skills and elemental skill damage for permanent charges and screen-wide output.")),
        ("Flickering Flame", "Nef + Pul + Vex", bi("3 孔 头盔", "3-socket Helm"), bi("+3 火技能、火焰抗光环、-10~15% 敌方火抗，火德/火陷阱核心头盔。", "+3 fire skills, a fire-resist aura and -10~15% enemy fire resist — the core helm for fire Druids and fire traps.")),
        ("Mist", "Cham + Shael + Gul + Thul + Ith", bi("5 孔 远程武器", "5-socket Missile Weapon"), bi("专注光环、+3 全技能、100% 穿透、高伤，弓亚马逊/佣兵神器。", "Concentration aura, +3 all skills, 100% pierce and high damage — a god-tier weapon for bowazons and mercenaries.")),
        ("Obsession", "Zod + Ist + Lem + Lum + Io + Nef", bi("6 孔 法杖", "6-socket Staff"), bi("+4 全技能、65% FCR、高抗与 MF，法系终局武器（需 Zod）。", "+4 all skills, 65% FCR, high resists and MF — an endgame caster weapon (needs Zod).")),
        ("Plague", "Cham + Shael + Um", bi("3 孔 剑/爪/匕", "3-socket Sword/Claw/Dagger"), bi("击中触发 Lower Resist、毒新星、净化光环，给 Javazon/毒系佣兵极佳。", "On hit triggers Lower Resist, a poison nova and a Cleansing aura — excellent for Javazons and poison mercenaries.")),
        ("Pattern", "Tal + Ort + Thul", bi("3 孔 爪", "3-socket Claw"), bi("+格挡、元素伤害与全抗，武学刺客中期过渡。", "+block, elemental damage and all resists — a mid-game stepping stone for martial-arts Assassins.")),
        ("Unbending Will", "Fal + Io + Ith + Eld + El + Hel", bi("6 孔 剑", "6-socket Sword"), bi("+3 野蛮战斗技能、高 ED 与吸血，中期近战替代。", "+3 Barbarian combat skills, high ED and life steal — a mid-game melee alternative.")),
        ("Wisdom", "Pul + Ith + Eld", bi("3 孔 头盔", "3-socket Helm"), bi("33% 穿透、不能冰冻、回蓝，亚马逊远程实惠头盔。", "33% pierce, cannot be frozen and mana regen — a cheap missile helm for Amazons.")),
        ("Mania / Hysteria / Metamorphosis / Ground / Temper / Hearth / Cure / Bulwark", bi("第 15 赛季起开放非天梯", "Non-ladder since Season 15"), bi("多部位", "Various slots"), bi("「术士君临」时期的八个天梯专属符文之语，已在第 15 赛季转为非天梯；本赛季同时上线经过平衡调整的<b>新版天梯专属</b>替换（仅限术士君临内容，原版/毁灭之王模式不受影响）。", "Eight Reign of the Warlock ladder-only runewords became available in non-ladder for Season 15; this season also ships rebalanced <b>new ladder-only versions</b> to replace them (Reign of the Warlock content only — Diablo II Classic and Lord of Destruction are unaffected).")),
        ("Enigma", "Jah + Ith + Ber", bi("3 孔 甲", "3-socket Body Armor"), bi("+2 全技能、Teleport、MF，全职业终极致核心甲。", "+2 all skills, Teleport and MF — the ultimate core armor for every class.")),
        ("Infinity", "Ber + Mal + Ber + Ist", bi("4 孔 长柄/标枪", "4-socket Polearm/Javelin"), bi("Conviction 光环 -50% 敌电抗，电法/火德/武学刺客破免核心（佣兵拿）。", "Conviction aura at -50% enemy lightning resist — the core Sunder weapon for lightning casters, fire Druids and martial-arts Assassins (on a mercenary).")),
        ("Spirit", "Tal + Thul + Ort + Amn", bi("4 孔 剑 / 盾", "4-socket Sword / Shield"), bi("+2 技能、FCR、FHR、抗性，性价比之王（剑+盾常见）。", "+2 skills, FCR, FHR and resists — the king of value (sword + shield is common).")),
        ("Heart of the Oak", "Ko + Vex + Pul + Thul", bi("4 孔 法杖/杖", "4-socket Stave/Wand"), bi("+3 技能、全抗、回蓝、FHR，法系通用武器。", "+3 skills, all resists, mana regen and FHR — a general-purpose caster weapon.")),
        ("Fortitude", "El + Sol + Dol + Lo", bi("4 孔 甲/武器", "4-socket Armor/Weapon"), bi("300% ED、高抗、生命，近战/佣兵毕业甲。", "300% ED, high resists and life — the best-in-slot armor for melee and mercenaries.")),
        ("Call to Arms", "Amn + Ral + Mal + Ist + Ohm", bi("5 孔 武器", "5-socket Weapon"), bi("+战斗命令（BO），全队血/法上限，副手必备。", "+Battle Orders raises the whole party's life and mana — a must-have on your swap weapon.")),
        ("Grief", "Eth + Tir + Lo + Mal + Ral", bi("5 孔 剑/斧", "5-socket Sword/Axe"), bi("高 ED、无视目标防御、偷血，近战毕业武器。", "High ED, ignore target defense and life steal — the best-in-slot melee weapon.")),
        ("Chains of Honor", "Dol + Um + Ber + Ist", bi("4 孔 甲", "4-socket Body Armor"), bi("+2 技能、全抗、MF、偷血，全能甲。", "+2 skills, all resists, MF and life steal — an all-rounder armor.")),
        ("Death's Web", "Vex + Hel + El + Eld + Zod + Eth", bi("6 孔 死灵法杖", "6-socket Necro Head"), bi("+2 毒骨、敌方毒抗 -50%，毒/骨死灵核心。", "+2 poison/bone and -50% enemy poison resist — the core weapon for poison and bone Necromancers.")),
    ]
    tr = "".join("<tr><td><b>%s</b></td><td><code>%s</code></td><td>%s</td><td>%s</td></tr>" % r for r in rows)
    body = '<h1><span class="zt"><span class="zc">符文之语图鉴 </span><span class="ec" lang="en">Runewords</span></span></h1>\n' \
           '<p>' + bi("符文之语是将特定符文按顺序排列镶嵌到带孔装备中激活的强大词缀。下表汇集 D2R 当前版本最具代表性的符文之语，包括 2.4–2.6 赛季新增与经典终局装备。",
                      "Runewords are powerful affixes you unlock by socketing specific runes in the right order into a socketed item. The table below collects the most representative runewords of the current D2R patch, including the season 2.4–2.6 additions and classic endgame gear.") + '</p>\n' \
           '<div class="callout info"><b>' + bi("提示：", "Tip:") + '</b>' \
           + bi("符文顺序与孔数必须完全匹配，且底材类型/品质需符合（普通/卓越/精英）。高符文（Vex、Ohm、Lo、Ber、Jah、Cham、Zod）极其珍贵，优先用于 Enigma / Infinity / Grief 等核心。",
                "The rune order and socket count must match exactly, and the base type/quality must qualify (normal/exceptional/elite). High runes (Vex, Ohm, Lo, Ber, Jah, Cham, Zod) are extremely precious — prioritise them for core runewords like Enigma, Infinity and Grief.") + '</div>\n' \
           '<div class="callout info"><b>' + bi("第 15 赛季轮转：", "Season 15 rotation:") + '</b>' \
           + bi("每个新赛季开始时会例行把上一批「天梯专属」内容开放给非天梯。本季轮到的是 Mania、Hysteria、Metamorphosis、Ground、Temper、Hearth、Cure、Bulwark 这八个符文之语；<b>术士君临</b>资料片下另有经过数值调整的新版天梯专属接管，所以新旧版本的实际词缀会有差异。开局前先确认你手上的版本属于哪一批。",
                "At the start of each new season, the previous batch of \"ladder-only\" content is routinely opened up to non-ladder. This time it's the eight runewords Mania, Hysteria, Metamorphosis, Ground, Temper, Hearth, Cure and Bulwark; <b>Reign of the Warlock</b> ships numerically adjusted new ladder-only versions to take over, so the actual affixes differ between old and new. Check which batch you're holding before you commit resources.") + '</div>\n' \
           '<div class="card">\n<table><thead><tr><th>' + bi("符文之语", "Runeword") + '</th><th>' + bi("符文顺序", "Rune Order") + '</th><th>' + bi("底材", "Base") + '</th><th>' + bi("核心价值", "Core Value") + '</th></tr></thead><tbody>' + tr + '</tbody></table>\n</div>\n' \
           '<div class="callout tip"><b>' + bi("平民起步推荐：", "Budget starters:") + '</b>' \
           + bi("Spirit（剑+盾）、Stealth（Tal+Eth 甲，+25% 移速）、Ancient's Pledge、Lore（Ort+Sol 头盔，+1 技能）、Smoke、Treachery 等，开荒期极其实用。",
                "Spirit (sword + shield), Stealth (Tal+Eth armor, +25% run speed), Ancient's Pledge, Lore (Ort+Sol helm, +1 skill), Smoke and Treachery are all extremely useful during progression.") + '</div>\n' \
           '<div class="pager"><a href="../index.html"><small>' + bi("返回", "Back") + '</small>' + bi("首页", "Home") + '</a><a href="leveling.html"><small>' + bi("下一攻略", "Next Guide") + '</small>' + bi("练级与开荒", "Leveling") + '</a></div>'
    return _guide_page("符文之语图鉴", "g:runewords", body)

def g_leveling():
    body = '<h1><span class="zt"><span class="zc">练级与开荒 </span><span class="ec" lang="en">Leveling</span></span></h1>\n' \
           '<p>' + bi("从 1 级到 99 的高效路线，结合经典刷点与 Terror Zones（恐怖地带）。新手建议先用法师/召唤死灵/祝福之锤开荒，积累装备与符文。",
                      "An efficient route from level 1 to 99, mixing classic farming spots with Terror Zones. Beginners should start with a Sorceress, summon Necromancer or Hammerdin to stockpile gear and runes.") + '</p>\n' \
           '<h2 class="section-id" id="route">' + bi("分阶段路线", "Phased Route") + '</h2>\n<div class="card">\n<table><thead><tr><th>' + bi("阶段", "Phase") + '</th><th>' + bi("推荐地点", "Recommended Spot") + '</th><th>' + bi("要点", "Notes") + '</th></tr></thead><tbody>' \
           '<tr><td>1–15</td><td>' + bi("第一幕剧情（Blood Raven → Tristram）", "Act 1 story (Blood Raven → Tristram)") + '</td><td>' + bi("跟任务走，拿 Cain 免费鉴定；优先点核心技能。", "Follow the quests, get Cain's free identify, and prioritise your core skill.") + '</td></tr>' \
           '<tr><td>15–25</td><td>The Cold Plains / Stony Field / Underground Passage</td><td>' + bi("刷精英与经验，攒宝石与符文。", "Farm elites and XP, stockpile gems and runes.") + '</td></tr>' \
           '<tr><td>25–40</td><td>Tombs（A2）、Maggot Lair、Arcane Sanctuary</td><td>' + bi("法师用 Teleport 效率拉满；Countess 刷符文（Tal-Thul-Io 等）。", "Sorceress maxes efficiency with Teleport; farm the Countess for runes (Tal-Thul-Io, etc.).") + '</td></tr>' \
           '<tr><td>40–60</td><td>Chaos Sanctuary（A4）、Pits（A1）、Ancient Tunnels（A2）</td><td>' + bi("Chaos 是高经验密度经典点；Pits 无冰免适合冰法。", "Chaos is a classic high-XP spot; the Pits have no cold immunes, great for cold Sorcs.") + '</td></tr>' \
           '<tr><td>60–80</td><td>Terror Zones, Cows ' + bi("（牛场）", "(Cow Level)") + ', Baal ' + bi("跑步", "runs") + '</td><td>' + bi("恐怖地带经验爆表；牛场密度高适合 AoE。", "Terror Zones are XP gold; the Cow level is dense and great for AoE.") + '</td></tr>' \
           '<tr><td>80–99</td><td>Terror Zones ' + bi("（高密度）", "(high density)") + ', Pits, Chaos, Ubers ' + bi("刷符文", "for runes") + '</td><td>' + bi("配合 Sunder Charm 与 MF 装；组队高 PP 经验更高。", "With Sunder Charms and MF gear; higher player count in a party means more XP.") + '</td></tr>' \
           '</tbody></table>\n</div>\n' \
           '<h2 class="section-id" id="tips">' + bi("开荒要点", "Progression Tips") + '</h2>\n<div class="card"><ul class="clean">' \
           '<li><b>' + bi("选对起手：", "Pick the right starter:") + '</b>' + bi("法师（传送）、召唤流死灵（安全）、祝福之锤圣骑士（全能）最适合开荒。", "Sorceress (Teleport), summon Necromancer (safe) or Hammerdin (all-round) suit progression best.") + '</li>' \
           '<li><b>' + bi("女伯爵刷符文：", "The Countess for runes:") + '</b>' + bi("A1 监狱塔的女伯爵必掉符文，是精神 / 潜行等低符文来源。", "The Countess in the A1 prison tower always drops runes — your source for low runes like Spirit / Stealth.") + '</li>' \
           '<li><b>' + bi("免费鉴定：", "Free identify:") + '</b>' + bi("救出凯恩后回城可免费鉴定全部物品。", "Rescue Cain, then identify everything for free in town.") + '</li>' \
           '<li><b>' + bi("Terror Zones 轮换：", "Terror Zone rotation:") + '</b>' + bi("每小时换区，重开游戏即可刷新查看当前恐怖地带。", "It shifts hourly; restart the game to refresh and see the current zone.") + '</li>' \
           '<li><b>' + bi("MF 与效率的平衡：", "Balance MF and speed:") + '</b>' + bi("MF 不是越高越好，优先保证击杀速度与存活。", "More MF is not always better — prioritise kill speed and survival.") + '</li>' \
           '<li><b>' + bi("共享仓库与符文：", "Shared stash and runes:") + '</b>' + bi("同账号角色共享仓库，用小号养大号符文。", "Characters on one account share a stash, so feed runes from alts to your main.") + '</li>' \
           '</ul></div>\n' \
           '<h2 class="section-id" id="patch33">' + bi("Patch 3.3 练级装改动", "Patch 3.3 Leveling Gear Changes") + '</h2>\n<div class="card">\n' \
           '<p>' + bi("本季最大的好处是一批冷门低级暗金被救活了，开荒期「捡到就能穿」的选择明显变多（<b>改动仅在天梯模式生效</b>）：",
                      "The biggest win this season is a batch of overlooked low-level uniques being brought back to life, giving you far more \"wear whatever drops\" choices while leveling (<b>the changes apply in Ladder only</b>):") + '</p>\n' \
           '<table><thead><tr><th>' + bi("装备", "Item") + '</th><th>' + bi("改动", "Change") + '</th><th>' + bi("谁受益", "Who Benefits") + '</th></tr></thead><tbody>' \
           '<tr><td><b>' + bi("天使之袍（套装）", "Angelic Raiment (set)") + '</b></td><td>' + bi("三件时 Sickle +6 伤害、Mantle 对不死 +100% 伤害；<b>全套额外 +1 全技能</b>", "At 3 pieces the Sickle gains +6 damage and the Mantle +100% damage to undead; <b>the full set adds +1 to all skills</b>") + '</td><td>' + bi("全职业练级，法系收益最高", "Everyone leveling, casters most") + '</td></tr>' \
           '<tr><td><b>' + bi("放血者", "Bloodletter") + '</b></td><td>' + bi("新增 +20% 跑步/行走速度", "Gains +20% faster run/walk") + '</td><td>' + bi("旋风野蛮人（可双持）", "Whirlwind Barbarian (dual-wield)") + '</td></tr>' \
           '<tr><td><b>' + bi("战枝", "The Battlebranch") + '</b></td><td>' + bi("物品等级 34→30，需求等级 <b>25→17</b>", "Item level 34→30, required level <b>25→17</b>") + '</td><td>' + bi("近战在极早期就有可用武器", "Melee gets a usable weapon very early") + '</td></tr>' \
           '<tr><td><b>' + bi("灰烬灾星", "Bane Ash") + '</b></td><td>' + bi("移除攻速与增强伤害，改为 <b>+20% 施法速度</b>", "Loses IAS and enhanced damage, gains <b>+20% faster cast rate</b>") + '</td><td>' + bi("早期法系练级", "Early caster leveling") + '</td></tr>' \
           '<tr><td><b>' + bi("闪蝠之形", "Blinkbat's Form") + '</b></td><td>' + bi("跑速 10%→<b>30%</b>，并新增击杀回复 +1 法力", "Run speed 10%→<b>30%</b>, plus +1 mana after each kill") + '</td><td>' + bi("所有需要跑图的角色", "Every character that has to walk anywhere") + '</td></tr>' \
           '<tr><td><b>' + bi("孤坟之脊", "Gravenspine") + '</b></td><td>' + bi("新增 +10% 施法速度", "Gains +10% faster cast rate") + '</td><td>' + bi("法系练级", "Caster leveling") + '</td></tr>' \
           '<tr><td><b>' + bi("守望之盾", "The Ward") + '</b></td><td>' + bi("生成时自带 <b>1 个孔</b>", "Now comes with <b>1 socket</b>") + '</td><td>' + bi("早期镶符文/宝石", "Early rune or gem socketing") + '</td></tr>' \
           '<tr><td><b>' + bi("玛那德之愈", "Manald Heal") + '</b></td><td>' + bi("新增 +10% 施法速度", "Gains +10% faster cast rate") + '</td><td>' + bi("法系与近战通用的练级戒指", "A leveling ring for both casters and melee") + '</td></tr>' \
           '<tr><td><b>' + bi("啄目弓", "Pluckeye") + '</b></td><td>' + bi("新增 +25% 攻击速度", "Gains +25% increased attack speed") + '</td><td>' + bi("亚马逊早期", "Early Amazon") + '</td></tr>' \
           '<tr><td><b>' + bi("罗格之弓", "Rogue's Bow") + '</b></td><td>' + bi("新增 +1~3 冰箭或火箭（限亚马逊）", "Gains +1-3 to Cold Arrow or Fire Arrow (Amazon only)") + '</td><td>' + bi("亚马逊弓系起步", "Starting bow Amazon") + '</td></tr>' \
           '</tbody></table>\n</div>\n' \
           '<div class="callout warn"><b>' + bi("墨菲斯托不再能卡角：", "Mephisto can no longer be corner-trapped:") + '</b>' \
           + bi("3.3 补丁修复了 Boss AI（含经典的柱子卡位打法），也修正了作为 Herald 出现的议会成员不掉战利品的问题。<b>后果</b>：开荒头几天靠刷劳模攒军帽、蛇皮这类日用品的速度会明显变慢，请预留更长的攒装周期，或改从恐怖地带 / Herald 入手。",
                "Patch 3.3 fixed boss AI (including the classic pillar-trap trick) and fixed Council Members appearing as Heralds failing to drop loot. <b>Impact:</b> stockpiling staples like Harlequin Crest and Skin of Vipermagi off Mephisto in the first few days will be noticeably slower — budget a longer gearing window, or start from Terror Zones / Heralds instead.") + '</div>\n' \
           '<div class="pager"><a href="runewords.html"><small>' + bi("上一攻略", "Prev Guide") + '</small>' + bi("符文之语图鉴", "Runewords") + '</a><a href="terror-zones.html"><small>' + bi("下一攻略", "Next Guide") + '</small>' + bi("恐怖地带 & Sunder", "Terror Zones & Sunder") + '</a></div>'
    return _guide_page("练级与开荒", "g:leveling", body)

def g_terror():
    body = '<h1><span class="zt"><span class="zc">恐怖地带 </span><span class="ec" lang="en">Terror Zones</span></span> &amp; <span class="zt"><span class="zc">破免护符 </span><span class="ec" lang="en">Sunder Charms</span></span></h1>\n' \
           '<p>' + bi("2.5+ 版本的两大核心机制，彻底改变了 D2R 的 farm 与流派多样性。",
                      "Two core mechanics from patch 2.5+ that completely changed D2R farming and build diversity.") + '</p>\n' \
           '<h2 class="section-id" id="tz">' + bi("Terror Zones 恐怖地带", "Terror Zones") + '</h2>\n<div class="card"><ul class="clean">' \
           '<li><b>' + bi("解锁条件：", "Unlock:") + '</b>' + bi("在该难度击败 Baal 后解锁对应难度的恐怖地带。", "Defeating Baal on a difficulty unlocks that difficulty's Terror Zones.") + '</li>' \
           '<li><b>' + bi("每小时轮换：", "Hourly rotation:") + '</b>' + bi("恐怖地带每 60 分钟切换一个区域，重开游戏即可刷新查看当前所在地。", "The zone switches every 60 minutes; restart the game to refresh and view the current one.") + '</li>' \
           '<li><b>' + bi("等级缩放：", "Level scaling:") + '</b>' + bi("怪物等级随你的等级提升（至少高于你 2 级，地狱上限 96），经验与掉落显著更好。", "Monster level rises with yours (at least 2 above, capped at 96 in Hell), giving far better XP and drops.") + '</li>' \
           '<li><b>' + bi("识别方式：", "How to spot it:") + '</b>' + bi("怪物名旁特殊图标、屏幕提示、专属音效、环境变暗、紫色传送点名。", "A special icon by monster names, an on-screen notice, unique SFX, a darker environment and a purple waypoint name.") + '</li>' \
           '<li><b>' + bi("覆盖全图：", "Map-wide:") + '</b>' + bi("从 Blood Moor 到 Worldstone Chamber，大部分区域都可能成为恐怖地带。", "From the Blood Moor to the Worldstone Chamber, most areas can become a Terror Zone.") + '</li>' \
           '</ul></div>\n' \
           '<h2 class="section-id" id="sunder">' + bi("Sunder Charms 破免护符", "Sunder Charms") + '</h2>\n<div class="card">' \
           '<p>' + bi("六系独特的 <b>大型护符（Grand Charm）</b>，装备在背包即可打破对应元素/类型的怪物免疫（将免疫怪抗性降至 95%），让更多流派能 farm 全图。代价是自身对该元素的抗性下降。",
                      "Six unique Grand Charms — socketed in your inventory they break the matching element/type immunity (dropping an immune's resist to 95%), letting more builds farm the whole map. The cost is lowered resist to that element yourself.") + '</p>\n' \
           '<table><thead><tr><th>' + bi("护符", "Charm") + '</th><th>' + bi("破免类型", "Breaks") + '</th><th>' + bi("副作用", "Side Effect") + '</th><th>' + bi("大致掉率", "Drop Rate") + '</th></tr></thead><tbody>' \
           '<tr><td>The Flame Rift</td><td>' + bi("火免", "Fire") + '</td><td>' + bi("火抗 -70~90%", "Fire Res -70~90%") + '</td><td>' + bi("约 1/80", "≈1/80") + '</td></tr>' \
           '<tr><td>The Cold Rupture</td><td>' + bi("冰免", "Cold") + '</td><td>' + bi("冰抗 -70~90%", "Cold Res -70~90%") + '</td><td>' + bi("约 1/80", "≈1/80") + '</td></tr>' \
           '<tr><td>The Crack of the Heavens</td><td>' + bi("电免", "Lightning") + '</td><td>' + bi("电抗 -70~90%", "Light Res -70~90%") + '</td><td>' + bi("约 1/120", "≈1/120") + '</td></tr>' \
           '<tr><td>The Rotting Fissure</td><td>' + bi("毒免", "Poison") + '</td><td>' + bi("毒抗 -70~90%", "Poison Res -70~90%") + '</td><td>' + bi("约 1/200", "≈1/200") + '</td></tr>' \
           '<tr><td>The Bone Break</td><td>' + bi("物理免", "Physical") + '</td><td>' + bi("物理受伤 +10~20%", "Physical Dmg Taken +10~20%") + '</td><td>' + bi("约 1/400", "≈1/400") + '</td></tr>' \
           '<tr><td>The Black Cleft</td><td>' + bi("魔法免", "Magic") + '</td><td>' + bi("魔法抗 -45~65%", "Magic Res -45~65%") + '</td><td>' + bi("约 1/800", "≈1/800") + '</td></tr>' \
           '</tbody></table>\n' \
           '<div class="callout warn"><b>' + bi("掉落：", "Drop:") + '</b>' + bi("Sunder Charm 仅从恐怖地带中的 <b>冠军 / 独特 / 超级独特 / Boss</b> 难度怪物掉落。物理与魔法破免最稀有，优先级视你的流派而定（电/冰/火最常见）。",
                "Sunder Charms drop only from Champion / Unique / Super Unique / Boss monsters inside a Terror Zone. Physical and Magic Sunder are the rarest; prioritise by your build (lightning/cold/fire are most common).") + '</div>\n</div>\n' \
           '<h2 class="section-id" id="p33">' + bi("Patch 3.3 改动（第 15 赛季）", "Patch 3.3 Changes (Season 15)") + '</h2>\n<div class="card">\n' \
           '<p>' + bi("3.3 补丁把破免的获取从「<b>堆 MF 被动刷</b>」推向「<b>主动打 Herald</b>」，是本季最影响刷图习惯的改动：",
                      "Patch 3.3 moves Sunder acquisition away from <b>passively stacking MF</b> and toward <b>actively farming Heralds</b> — the change that most affects how you farm this season:") + '</p>\n' \
           '<table><thead><tr><th>' + bi("改动项", "Change") + '</th><th>' + bi("变更前 → 变更后", "Before → After") + '</th><th>' + bi("实际影响", "What It Means") + '</th></tr></thead><tbody>' \
           '<tr><td><b>' + bi("潜伏破免最低掉落等级", "Latent Sunder min drop level") + '</b></td><td>69 → 75</td><td>' + bi("角色等级不够时刷不出，需要往地狱更深处推进。", "You must push deeper into Hell before they can drop at all.") + '</td></tr>' \
           '<tr><td><b>' + bi("MF 刷取破免", "Sunders via Magic Find") + '</b></td><td>' + bi("全难度 → 仅地狱", "All difficulties → Hell only") + '</td><td>' + bi("堵上了第 14 赛季在噩梦刷潜伏破免的捷径。", "Closes the Season 14 shortcut of farming Latent Sunders in Nightmare.") + '</td></tr>' \
           '<tr><td><b>' + bi("MF 刷取掉率", "Magic Find drop rate") + '</b></td><td>' + bi("下调", "Reduced") + '</td><td>' + bi("Herald 掉率不受影响，纯堆 MF 收益变差。", "Herald rates are unaffected, so pure MF stacking pays off less.") + '</td></tr>' \
           '<tr><td><b>' + bi("Herald of Terror 3 层以上", "Herald of Terror tier 3+") + '</b></td><td>' + bi("稀有及以上掉率提高", "Higher Rare-or-better rate") + '</td><td>' + bi("高层先驱成为终局装备的主要来源。", "High-tier Heralds become the main source of endgame gear.") + '</td></tr>' \
           '<tr><td><b>' + bi("Worldstone Shard（世界之石碎片）", "Worldstone Shard") + '</b></td><td>' + bi("掉率降低，但额外多掉 1 件装备", "Lower rate, +1 extra item") + '</td><td>' + bi("单次收益变好，单位时间收益变差。", "Better per drop, worse per unit of time.") + '</td></tr>' \
           '<tr><td><b>' + bi("Ancient Statue（古代雕像）", "Ancient Statue") + '</b></td><td>' + bi("掉率降低", "Lower rate") + '</td><td>' + bi("制作材料变得更稀缺。", "Crafting materials become scarcer.") + '</td></tr>' \
           '</tbody></table>\n</div>\n' \
           '<div class="callout tip"><b>' + bi("应对思路：", "How to adapt:") + '</b>' \
           + bi("不要再指望「堆到 500 MF 就能刷出破免」。本季更合理的路线是：先把等级推到 75 以上并站稳地狱，再用<b>能快速清高密度场景的流派</b>冲 Herald 层数和恐怖地带；MF 装仍有用，但优先级排在清场速度与生存之后。",
                "Don't count on 'stack 500 MF and Sunders will come'. The stronger route this season: push past level 75 and get stable in Hell, then take a <b>build that clears dense zones fast</b> and push Herald tiers and Terror Zones. MF gear still helps, but it ranks below clear speed and survivability.") + '</div>\n' \
           '<div class="pager"><a href="leveling.html"><small>' + bi("上一攻略", "Prev Guide") + '</small>' + bi("练级与开荒", "Leveling") + '</a><a href="uber.html"><small>' + bi("下一攻略", "Next Guide") + '</small>' + bi("Uber 终局", "Uber Endgame") + '</a></div>'
    return _guide_page("恐怖地带 & Sunder", "g:terror-zones", body)

def g_uber():
    body = '<h1><span class="zt"><span class="zc">Uber 终局内容 </span><span class="ec" lang="en">Uber Endgame</span></span></h1>\n' \
           '<p>' + bi("D2R 的顶级 PvM 挑战：超级 boss 掉落毁灭（Annihilus）与小护身符（Torch），是终局玩家的标配。",
                      "The top PvM challenge in D2R: super bosses drop the Annihilus and Hellfire Torch — staples for every endgame player.") + '</p>\n' \
           '<h2 class="section-id" id="clone">' + bi("Diablo Clone 克隆", "Diablo Clone") + '</h2>\n<div class="card"><ul class="clean">' \
           '<li>' + bi("游戏中会出现「<b>Diablo 在我们中间行走…</b>」世界消息，击杀掉落的 <b>Token of Absolution（赦罪令牌）</b> 可在工坊合成重置技能/属性书。",
                       "A 'Diablo Walks the Earth…' world message appears; killing it drops the Token of Absolution, which you cube into a skill/stat reset book.") + '</li>' \
           '<li>' + bi("高概率掉 <b>Annihilus（毁灭小符）</b>：+1 全技能、+属性、+抗、+经验，全职业必刷。",
                       "High chance to drop the Annihilus charm: +1 all skills, +stats, +resists, +XP — a must-farm for every class.") + '</li>' \
           '</ul></div>\n' \
           '<h2 class="section-id" id="trist">' + bi("Uber Tristram 超级崔斯特姆", "Uber Tristram") + '</h2>\n<div class="card"><ul class="clean">' \
           '<li>' + bi("用三把钥匙（恐怖/仇恨/毁灭，由 Nihlathak 等掉落）在工坊合成组织，进入红色崔斯特姆。",
                       "Cube the three keys (Terror/Hatred/Destruction, dropped by Nihlathak and others) into an organ, then enter red Tristram.") + '</li>' \
           '<li>' + bi("对手：Uber Mephisto、Uber Diablo、Uber Baal（均超高血量与免疫）。",
                       "Foes: Uber Mephisto, Uber Diablo and Uber Baal (all with huge HP and immunities).") + '</li>' \
           '<li>' + bi("掉 <b>Hellfire Torch（地狱火火炬）</b>：+3 职业技能、+属性、+抗，角色专属。",
                       "Drops the Hellfire Torch: +3 class skills, +stats, +resists, character-specific.") + '</li>' \
           '<li><b>' + bi("推荐打法：", "Recommended:") + '</b>' + bi("Smiter 圣骑士（Grief + 暗金圣盾 + 击回 + Decrepify 佣兵）最稳；Mosaic 刺客也可用。",
                       "A Smiter Paladin (Grief + unique paladin shield + life tap + Decrepify merc) is safest; a Mosaic Assassin also works.") + '</li>' \
           '</ul></div>\n' \
           '<h2 class="section-id" id="mini">' + bi("Uber Andariel & Uber Duriel", "Uber Andariel & Uber Duriel") + '</h2>\n<div class="card"><ul class="clean">' \
           '<li>' + bi("2.6+ 新增的超级安达利尔与超级都瑞尔，掉落专属材料用于升级暗金（如将部分暗金升级为精英底材）。",
                       "Added in 2.6+: Uber Andariel and Uber Duriel drop exclusive materials used to upgrade uniques (e.g. upgrade some uniques to elite bases).") + '</li>' \
           '<li>' + bi("机制类似，需要对应破免与高生存，组队更轻松。",
                       "Similar mechanics — needs the right Sunder and high survivability; easier in a group.") + '</li>' \
           '</ul></div>\n' \
           '<div class="callout tip"><b>' + bi("钥匙获取：", "Key farming:") + '</b>' + bi("在噩梦/地狱击杀 Nihlathak（A5）、Summoner（A2）、Smith（A1 监狱）等有几率掉三种钥匙，攒齐后挑战 Uber。",
                "In Nightmare/Hell, Nihlathak (A5), the Summoner (A2) and the Smith (A1 prison) can drop the three keys; collect a set, then challenge the Ubers.") + '</div>\n' \
           '<div class="pager"><a href="terror-zones.html"><small>' + bi("上一攻略", "Prev Guide") + '</small>' + bi("恐怖地带 & Sunder", "Terror Zones & Sunder") + '</a><a href="tips.html"><small>' + bi("下一攻略", "Next Guide") + '</small>' + bi("综合技巧", "Tips") + '</a></div>'
    return _guide_page("Uber 终局", "g:uber", body)

def g_tips():
    body = '<h1><span class="zt"><span class="zc">综合技巧 </span><span class="ec" lang="en">Tips</span></span></h1>\n' \
           '<p>' + bi("零散但关键的高手细节，覆盖重置、配方、交易与生存。",
                      "Scattered but crucial expert details covering respecs, recipes, trading and survival.") + '</p>\n' \
           '<div class="card"><h3>' + bi("① 重置与洗点", "1 · Respec & Resets") + '</h3><ul class="clean">' \
           '<li><b>' + bi("Token of Absolution（赦罪令牌）：", "Token of Absolution:") + '</b>' + bi("集齐 4 种精华（每种 boss 掉），在工坊合成，可重置技能与属性。D2R 可多次洗点。",
                       "Collect the 4 essences (one per boss type), cube them to reset skills and stats. D2R allows repeated respecs.") + '</li>' \
           '<li><b>' + bi("活动代币：", "Event tokens:") + '</b>' + bi("部分活动/任务给的一次性洗点。", "Some events/quests grant a one-time respec.") + '</li></ul></div>\n' \
           '<div class="card"><h3>' + bi("② 实用赫拉迪克方块配方", "2 · Useful Cube Recipes") + '</h3><ul class="clean">' \
           '<li>' + bi("3 同色碎宝石 → 1 高一级宝石；3 完美宝石 + 装备 → 修复（部分）。",
                      "3 flaw gems of one color → 1 gem of the next tier; 3 perfect gems + item → repair (some).") + '</li>' \
           '<li>' + bi("符文升级：3 个同符文 → 1 个高一级（如 3 Lem → 1 Pul），用于冲高符文。",
                      "Rune upgrade: 3 of the same rune → 1 of the next tier (e.g. 3 Lem → 1 Pul) to climb toward high runes.") + '</li>' \
           '<li>' + bi("Ral + 普通箭/十字弓弹 → 无限箭袋（省箭）。", "Ral + normal arrows/bolts → infinite quiver (saves arrows).") + '</li>' \
           '<li>' + bi("宝石 + 装备可升级部分暗金底材品质。", "Gem + item can upgrade some unique base quality.") + '</li></ul></div>\n' \
           '<div class="card"><h3>' + bi("③ 生存与效率", "3 · Survival & Efficiency") + '</h3><ul class="clean">' \
           '<li><b>' + bi("抗性优先：", "Resists first:") + '</b>' + bi("地狱难度前堆满 75% 四抗（火/冰/电/毒），否则秒躺。",
                       "Hit 75% on all four (fire/cold/lightning/poison) before Hell, or you get one-shot.") + '</li>' \
           '<li><b>' + bi("FHR / FCR 档位：", "FHR / FCR breakpoints:") + '</b>' + bi("被打恢复与施法速度有档位，堆到关键阈值手感质变。",
                       "Hit recovery and cast speed have breakpoints — hitting a key threshold feels dramatically better.") + '</li>' \
           '<li><b>' + bi("Teleport 卡位：", "Teleport clustering:") + '</b>' + bi("法师用传送把怪聚堆再 AoE，效率翻倍。",
                       "The Sorceress teleports to bunch monsters, then AoE — double the efficiency.") + '</li>' \
           '<li><b>' + bi("Pet 与 Merc：", "Pet & Merc:") + '</b>' + bi("佣兵带 Insight（回蓝光环）、Infinity（降抗）、Fortitude（防御）是主流。",
                       "Mercenaries with Insight (mana aura), Infinity (resist reduction) and Fortitude (defence) are mainstream.") + '</li>' \
           '<li><b>' + bi("不能冰冻：", "Cannot be frozen:") + '</b>' + bi("用 Raven Frost / 靴子词缀 / 橡木等确保不被冻住断节奏。",
                       "Use Raven Frost / boot affixes / Oak to avoid being frozen and losing your rhythm.") + '</li></ul></div>\n' \
           '<div class="card"><h3>' + bi("④ 交易与经济", "4 · Trading & Economy") + '</h3><ul class="clean">' \
           '<li>' + bi("高符文（Vex/Jah/Ber 等）是硬通货，谨慎使用。", "High runes (Vex/Jah/Ber, etc.) are hard currency — spend them carefully.") + '</li>' \
           '<li>' + bi("带职业技能的普通品质装备也可能很值钱（如 +3 陷阱爪、+3 锤头环）。", "Plain-quality gear with class skills can also be valuable (e.g. +3 trap claws, +3 hammer circlet).") + '</li>' \
           '<li>' + bi("Runeword 底材注意孔数与类型（如 4 孔君主盾做 Spirit）。", "For runeword bases, watch socket count and type (e.g. a 4-socket Monarch for Spirit).") + '</li></ul></div>\n' \
           '<div class="pager"><a href="uber.html"><small>' + bi("上一攻略", "Prev Guide") + '</small>' + bi("Uber 终局", "Uber Endgame") + '</a><a href="../index.html"><small>' + bi("返回", "Back") + '</small>' + bi("首页", "Home") + '</a></div>'
    return _guide_page("综合技巧", "g:tips", body)

def g_farming():
    # 速刷场景排行（来自项目 MF.md）
    scene_rows = [
        (bi("地狱 A1 地穴 Tamoe Highland", "Hell A1 — The Pit (Tamoe Highland)"), "85", bi("无冰免，怪物密度高", "No cold immunes, high monster density"), bi("纯冰法最稳的 85 场景，通关后首选", "The safest 85-area for a pure cold Sorc; first pick after clearing")),
        (bi("地狱 A2 远古通道 Lost City", "Hell A2 — Lost City (Ancient Tunnels)"), "85", bi("怪少皮薄、无冰免", "Few, thin enemies, no cold immunes"), bi("传送清图极快，适合暴风雪速刷", "Teleport clears the map fast — great for Blizzard farming")),
        (bi("地狱 A3 墨菲斯托 Mephisto", "Hell A3 — Mephisto"), "78", bi("路程短、掉率池大", "Short path, large drop pool"), bi("经典速刷点，但 <b>3.3 补丁已修复卡角打法</b>，效率不如从前，需改为正面对抗", "A classic spot, but <b>patch 3.3 removed the corner-trap method</b> — less efficient than before, you now fight it head-on")),
        (bi("地狱 A5 暴躁外皮 Pindle", "Hell A5 — Pindleskin"), "85", bi("路程极短", "Extremely short path"), bi("单人 1PP 效率怪，顺路清场", "Great for solo 1PP, clear on the way")),
        (bi("地狱 A5 地狱议会 Trav", "Hell A5 — Travincal"), "85", bi("金币+装备双收", "Gold + gear together"), bi("可顺带攒符文与底材", "Also farm runes and bases on the side")),
    ]
    sr = "".join("<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in scene_rows)
    # 纯冰法高 MF 装备模板（来自项目 MF.md）
    gear_rows = [
        (bi("武器", "Weapon"), bi("眼球（50%MF）或 死亡深度 → 镶 24# IST", "The Oculus (50% MF) or Death's Breath → socket 24# Ist")),
        (bi("盾牌", "Shield"), bi("精神（Tal+Thul+Ort+Amn）→ 35%FCR 档", "Spirit (Tal+Thul+Ort+Amn) → 35% FCR breakpoint")),
        (bi("头盔", "Helm"), bi("诗寇蒂的愤怒 IRE 镶完美黄宝石（最高 100%MF）", "Harlequin Crest with a perfect topaz (up to 100% MF)")),
        (bi("衣服", "Armor"), bi("财富（Lem+Ko+Tir）300%MF", "Wealth (Lem+Ko+Tir) 300% MF")),
        (bi("腰带", "Belt"), bi("金色包袱 30%MF", "Goldwrap 30% MF")),
        (bi("手套", "Gloves"), bi("法师之拳 或 运气守护 40%MF", "Magefist or Chance Guards 40% MF")),
        (bi("鞋子", "Boots"), bi("战争旅者 50%MF", "War Traveler 50% MF")),
        (bi("项链", "Amulet"), bi("蓝色 +3 冰技 / 35%MF 或 塔拉夏项链", "Blue +3 cold skills / 35% MF, or Tal Rasha's Amulet")),
        (bi("戒指", "Rings"), bi("双拿格 30%MF×2 或 1×乔丹 + 1×蓝色 25%MF", "Twin Nagelring 30% MF ×2, or 1× Stone of Jordan + 1× blue 25% MF")),
        (bi("副手", "Swap"), bi("阿里巴巴（2 孔镶 IST）+ 韵律盾（IST）→ BOSS 最后一击换副手，MF 450–550 仍维持 105%FCR", "Ali Baba (2 sockets, Ist) + Rhyme shield (Ist) → switch on the boss's last hit; reach 450–550 MF while keeping 105% FCR")),
    ]
    gr = "".join("<tr><td><b>%s</b></td><td>%s</td></tr>" % (k, v) for k, v in gear_rows)
    # 佣兵 MF 配置（来自项目 MF.md）
    merc_rows = [
        (bi("武器", "Weapon"), bi("无限（Ber+Mal+Ber+Ist）→ 破多数冰免且减抗", "Infinity (Ber+Mal+Ber+Ist) → breaks most cold immunes and reduces resist")),
        (bi("衣服", "Armor"), bi("刚毅（El+Sol+Dol+Lo）", "Fortitude (El+Sol+Dol+Lo)")),
        (bi("头盔", "Helm"), bi("安达利尔的面容（安头）镶 IST", "Andariel's Visage socketed with Ist")),
        (bi("定位", "Role"), bi("佣兵捅冰免怪，法师专心暴风雪清场", "Merc pokes cold immunes while the Sorc focuses Blizzard on the pack")),
    ]
    mr = "".join("<tr><td><b>%s</b></td><td>%s</td></tr>" % (k, v) for k, v in merc_rows)
    # 卓古拉之握速刷目标（来自项目 卓古拉之握.md）
    drac_targets = [
        (bi("地狱 墨菲斯托", "Hell Mephisto"), bi("场景 78", "Area 78"), bi("路程短、传统速刷主力（<b>3.3 补丁后卡角已封</b>，需正面打）；日用品掉率池大，卓古拉属“常出”档；300+ MF 即可", "Short path and the traditional farming mainstay (<b>patch 3.3 closed the corner-trap</b>, fight head-on); large rare pool, Dracul's is 'common'; 300+ MF is enough")),
        (bi("地狱 安达利尔（恐怖地带）", "Hell Andariel (Terror Zone)"), bi("≥85 时", "At ≥85"), bi("恐怖地带刷新后掉落池升级到 85，精英暗金掉率更高；比劳模更省路程", "A Terror Zone upgrades the drop pool to 85, higher elite-unique rate; less walking than Meph")),
        (bi("地狱 迪亚波罗（混沌避难所）", "Hell Diablo (Chaos Sanctuary)"), "85", bi("85 场景=最高掉落池，所有精英暗金都能掉；清场慢但顺带刷符文", "An 85 area = top drop pool, every elite unique can drop; slow clear but farms runes too")),
    ]
    dt = "".join("<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>" % (a, b, c) for a, b, c in drac_targets)
    drac_alt = [
        (bi("聚气“偷取生命”杖", "Charge staff of 'Life Tap'"), bi("普通难度 A2 卓格南商店刷一根“生命偷取”聚气杖，进场先手动放诅咒再换盾击", "In Normal A2, farm a 'Life Tap' charge staff from Drognan's shop; cast the curse manually on entry, then swap to Smite")),
        (bi("合成 CB 手套", "Craft CB gloves"), bi("Blood 手套配方：4 号 + 完美红宝石 + 任意珠宝 + 重手套，可出 10% CB + 吸血/力量，成本极低、CB 值高", "Blood glove recipe: Amn (#4) + perfect ruby + any jewel + heavy gloves can roll 10% CB + life steal/strength at very low cost with high CB value")),
    ]
    da = "".join("<li><b>%s：</b>%s</li>" % (k, v) for k, v in drac_alt)
    body = '<h1><span class="zt"><span class="zc">速刷与 MF 指南 </span><span class="ec" lang="en">Farming</span></span></h1>\n' \
           '<p>' + bi("本页内容整理自项目内文档（MF.md / 卓古拉之握.md），聚焦<strong>通关后纯冰法速刷</strong>与<strong>暗金（卓古拉之握）速刷路线</strong>，是实战向的刷宝手册。MF（Magic Find，魔法寻获）越高，亮金/套装/符文掉率越高，但会牺牲部分生存与输出，需平衡。",
                      "This page is compiled from the project docs (MF.md / Dracul's Grasp.md), focusing on <strong>post-game pure-cold-Sorc farming</strong> and <strong>the unique (Dracul's Grasp) farming route</strong> — a practical loot guide. Higher MF (Magic Find) raises rare/set/rune drop rates, but trades away some survivability and damage, so balance it.") + '</p>\n' \
           '<div class="callout info"><b>' + bi("核心思路：", "Core idea:") + '</b>' + bi("练一个纯冰法师（暴风雪/冰封球）→ 力量刚好穿装备、其余全血、格挡 75%、MF 300+。先用冰免怪少的 85 场景起量，再用 Infinity 佣兵破冰免，最后靠 Sunder/副手换装把 MF 顶到 450–550。<b>3.3 补丁提醒：</b>破免在非地狱难度不再随 MF 掉落，且 Herald 掉率完全不吃 MF，本季要把<b>清场速度与 Herald 层数</b>排在 MF 数字前面。",
                "Level a pure cold Sorc (Blizzard/Frozen Orb) → just enough Strength for gear, rest Vitality, 75% block, MF 300+. Start with 85 areas that have few cold immunes to build volume, then break cold immunes with an Infinity mercenary, and finally push MF to 450–550 via Sunder/swap gear. <b>Patch 3.3 caveat:</b> Sunders no longer drop from Magic Find outside Hell and Herald rates ignore MF entirely, so this season prioritise clear speed and Herald tiers over raw MF numbers.") + '</div>\n' \
           '<h2 class="section-id" id="scenes">' + bi("一、单人效率速刷场景", "1 · Efficient Solo Farming Spots") + '</h2>\n' \
           '<div class="card"><table><thead><tr><th>' + bi("场景", "Spot") + '</th><th>' + bi("等级", "Lvl") + '</th><th>' + bi("特点", "Feature") + '</th><th>' + bi("备注", "Note") + '</th></tr></thead><tbody>' + sr + '</tbody></table></div>\n' \
           '<h2 class="section-id" id="mftpl">' + bi("二、纯冰法高 MF 装备模板", "2 · High-MF Gear Template (Cold Sorc)") + '</h2>\n' \
           '<div class="card"><table><thead><tr><th>' + bi("部位", "Slot") + '</th><th>' + bi("推荐", "Recommended") + '</th></tr></thead><tbody>' + gr + '</tbody></table></div>\n' \
           '<div class="callout tip"><b>' + bi("换装技巧：", "Swap trick:") + '</b>' + bi("BOSS 最后一击前切到“阿里巴巴 + 韵律盾”副手（双镶 IST），MF 值可达 450–550，同时仍维持 105% FCR 档位，手感不掉。",
                "Before the boss's last hit, swap to the 'Ali Baba + Rhyme shield' setup (both socketed with Ist) to hit 450–550 MF while still keeping the 105% FCR breakpoint — no loss in feel.") + '</div>\n' \
           '<h2 class="section-id" id="merc">' + bi("三、佣兵 MF 阶段配置", "3 · Mercenary MF Setup") + '</h2>\n' \
           '<div class="card"><table><thead><tr><th>' + bi("部位", "Slot") + '</th><th>' + bi("推荐", "Recommended") + '</th></tr></thead><tbody>' + mr + '</tbody></table></div>\n' \
           '<div class="callout tip"><b>' + bi("破冰免关键：", "Breaking cold immunes:") + '</b>' + bi("佣兵拿 <code>无限（Ber+Mal+Ber+Ist）</code> 提供 Conviction 光环降抗，捅冰免怪，法师专心暴风雪清场。",
                "Your mercenary wields Infinity (Ber+Mal+Ber+Ist) for the Conviction aura that lowers resist, poking cold immunes while the Sorc focuses Blizzard on the pack.") + '</div>\n' \
           '<h2 class="section-id" id="loop">' + bi("四、刷宝循环示例", "4 · Sample Farming Loop") + '</h2>\n' \
           '<div class="card"><ol class="clean">\n' \
           '<li>' + bi("开局城镇 → 传送 <b>远古通道</b> → 暴风雪清图 → 捡亮金/套装/符文 → 回城",
                       "Start in town → teleport to the <b>Ancient Tunnels</b> → Blizzard the map → grab rares/sets/runes → return to town") + '</li>\n' \
           '<li>' + bi("换场：<b>地穴</b> → <b>暴躁外皮</b> → <b>墨菲斯托</b>",
                       "Switch maps: the <b>Pits</b> → <b>Pindleskin</b> → <b>Mephisto</b>") + '</li>\n' \
           '<li>' + bi("每 15–20 分钟一轮，效率约 50–80 场/小时",
                       "One loop every 15–20 minutes, roughly 50–80 runs per hour") + '</li>\n</ol></div>\n' \
           '<h2 class="section-id" id="dracul">' + bi("五、暗金速刷：卓古拉之握 Dracul's Grasp", "5 · Unique Farming: Dracul's Grasp") + '</h2>\n' \
           '<p>' + bi("“卓古拉之握”属精英级暗金吸血鬼骸骨手套，无固定唯一掉源，<strong>任何地狱难度怪物/Boss/箱子都有可能掉</strong>。下面是一份效率高、相对省时的路线（来自项目文档）。",
                      "Dracul's Grasp is an elite unique vampire bone gloves with no fixed unique source — <strong>any Hell monster/Boss/chest can drop it</strong>. Below is an efficient, relatively quick route (from the project docs).") + '</p>\n' \
           '<div class="card"><table><thead><tr><th>' + bi("目标", "Target") + '</th><th>' + bi("场景", "Spot") + '</th><th>' + bi("推荐原因", "Why") + '</th></tr></thead><tbody>' + dt + '</tbody></table></div>\n' \
           '<div class="callout info"><b>' + bi("备选 85 场景：", "Alternative 85 areas:") + '</b>' + bi("古代通道（冰法最爱）、世界之石大殿 1–3 层 + 巴尔王座、奶牛关——这些 85 场景所有精英暗金都能掉，可顺带刷符文/底材。",
                "The Ancient Tunnels (cold Sorc's favourite), the Worldstone Keep 1–3 + Throne of Destruction, and the Secret Cow Level — all 85 areas can drop every elite unique, and farm runes/bases on the side.") + '</div>\n' \
           '<h3 class="section-id" style="margin-top:14px">' + bi("懒人速刷方案", "Lazy Farming Plan") + '</h3>\n' \
           '<div class="card"><ol class="clean">\n' \
           '<li>' + bi("练个冰法（暴风雪/冰封球）→ 力量够穿装备，其余全血，格挡 75%，MF 300+",
                       "Level a cold Sorc (Blizzard/Frozen Orb) → enough Strength for gear, rest Vitality, 75% block, MF 300+") + '</li>\n' \
           '<li>' + bi("每天上线 10 分钟：先看<strong>恐怖地带</strong>是否刷在 A1/A2（恐怖安姐 2 分钟一把）；不在则 <strong>劳模</strong>（卡角已封，约 1 分钟一把），刷 20 轮收工",
                       "10 minutes a day: check if a Terror Zone is in A1/A2 (Terror Andariel ~2 min a run); if not, run Mephisto (~1 min a run now that the corner-trap is gone), 20 runs and done") + '</li>\n' \
           '<li>' + bi("周末有空：去<strong>古代通道</strong>或<strong>混沌避难所</strong>深度刷，顺带刷符文/底材",
                       "On weekends: farm the <strong>Ancient Tunnels</strong> or <strong>Chaos Sanctuary</strong> in depth, also grabbing runes/bases") + '</li>\n</ol></div>\n' \
           '<div class="callout warn"><b>' + bi("掉率真相：", "Drop-rate truth:") + '</b>' + bi("卓古拉之握掉率约 1:几千～1:几万（跟军帽、乌鸦同量级），属“日用品”但不算常见；劳模/安姐/85 场景轮着刷，平均 1–3 天可见一双（300+ MF 前提下）。",
                "Dracul's Grasp drops around 1:several-thousand to 1:several-tens-of-thousand (same tier as Harlequin Crest or Raven Frost) — a 'common' unique but not frequent; rotate Meph/Andariel/85-areas and you'll see a pair every 1–3 days (at 300+ MF).") + '</div>\n' \
           '<h3 class="section-id" style="margin-top:14px">' + bi("实在刷不到的替代", "Alternatives If You Can't Drop It") + '</h3>\n' \
           '<div class="card"><ul class="clean">' + da + '</ul></div>\n' \
           '<div class="pager"><a href="../index.html"><small>' + bi("返回", "Back") + '</small>' + bi("首页", "Home") + '</a><a href="tips.html"><small>' + bi("上一攻略", "Prev Guide") + '</small>' + bi("综合技巧", "Tips") + '</a></div>'
    return _guide_page("速刷与 MF 指南", "g:farming", body)

# ---------------------------------------------------------------------------
# 收藏编年史：符文之语 / 套装 / 独特道具打勾清单
# 打勾状态存浏览器 localStorage，纯本地不上传。
# ---------------------------------------------------------------------------
def rune_need_table():
    """符文需求统计：集齐全部符文之语每种符文要几个。

    随上方打勾实时变化 —— JS 用 data-runes 里的符文序列重算剩余量。
    孔数分栏让玩家能按「先凑 4 孔」这类实际目标拆解。
    """
    tiers = [t["sockets"] for t in RUNE_TIERS]
    ths = "".join('<th data-sk="%d">%s</th>' % (s, bi("%d 孔" % s, "%d-soc" % s)) for s in tiers)
    rows = []
    for r in RUNE_NEED:
        tds = "".join('<td data-sk="%d">%d</td>' % (tiers[i], n)
                      for i, n in enumerate(r["by_tier"]))
        rows.append(
            '<tr data-rune="%s">'
            '<td><b><code class="rn">#%d %s</code></b></td>'
            '<td class="num tot">%d</td>'
            '<td class="num left">%d</td>'
            '%s'
            '<td class="col-bar"><span class="ch-bar tiny"><i style="width:%d%%"></i></span></td>'
            "</tr>"
            % (r["name"], r["idx"], r["name"], r["total"], r["total"], tds,
               round(r["total"] / 20.0 * 100))
        )
    return (
        '<div class="card rune-need-card" id="runeNeedCard">'
        '<button type="button" class="fold-toggle" id="runeNeedToggle" aria-expanded="true" aria-controls="runeNeedBody">'
        '<span class="fold-arrow" aria-hidden="true"></span>'
        '<span class="fold-title">' + bi("集齐全部所需符文统计", "Rune budget for every runeword") + '</span>'
        '<span class="fold-hint" id="runeNeedHint"></span>'
        '</button>'
        '<div class="fold-body" id="runeNeedBody">'
        '<p>' + bi(
            "这是「把所有符文之语都做一遍」的总账：每种符文需要几个（重复使用同一条里的符文会按出现次数累加，"
            "比如 Last Wish 要3 个 Jah）。右侧按孔数拆分，可以先定个小目标——"
            "比如「先把全部 4 孔凑齐」，只买那几档用得上的符文，不被高阶的 Zod 逼着肝。",
            "This is the full bill for crafting every runeword: how many of each rune you need, counting repeats "
            "within a single word (Last Wish alone needs three #31 Jah). The columns break it down by socket count, "
            "so you can aim at a smaller goal first — e.g. complete every 4-socket word and skip the #33 Zod runs "
            "entirely.") + '</p>'
        '<div class="tier-sum" id="rwTierSum"></div>'
        '<div class="table-scroll"><table class="rune-need"><thead><tr>'
        '<th>' + bi("符文", "Rune") + '</th>'
        '<th>' + bi("合计", "Total") + '</th>'
        '<th>' + bi("还缺", "Left") + '</th>'
        '<th class="tier-head">' + bi("按孔数拆分", "By sockets") + '</th>'
        '<th></th>'
        '</tr><tr class="tier-subhead"><th></th><th></th><th></th>' + ths + "<th></th></tr>"
        '</thead><tbody>' + "".join(rows) + '</tbody></table></div>'
        '<div class="callout tip"><b>' + bi("提示：", "Tip:") + '</b>'
        + bi("#33 Zod 只要 3 个、#32 Cham 6 个，压轴的 #31 Jah / #30 Ber 反而要 12 / 9 个 —— "
             "真正卡进度的是低阶符文（#13 Shael 要 20 个），先把女伯爵刷起来。",
             "Only three #33 Zod and six #32 Cham are needed, while #31 Jah and #30 Ber want 12 and 9 — "
             "the real bottleneck is the cheap runes (#13 Shael needs 20). Farm the Countess first.") +
        '</div></div></div>'
    )

def _esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def _ch_attr(s):
    """把文本塞进 HTML 属性前先清掉引号/尖括号，避免破坏结构。

    防回归：属性值必须是不含 '<' 的纯文本。bi() 的输出带 span，
    塞进属性会破坏 HTML（曾导致 placeholder 里出现 <span ...）。
    """
    out = _esc(s).replace('"', "&quot;").strip()
    if "<" in out or ">" in out:
        raise ValueError("属性值不能包含标签：%r" % (s,))
    return out

def _ch_name(zh, en):
    """条目名：中文为主 + 英文小字。

    两段都用 data-zh-is-name 保护 —— 译名由数据层给定，术语表不应再改写，
    否则「Enigma」会被再包一层，渲染成「谜团 谜团 Enigma」。
    """
    small = ' style="opacity:.55;font-size:.86em;font-weight:400"'
    if zh == en:
        return '<span data-zh-is-name="1">%s</span>' % _esc(en)
    return ('<span data-zh-is-name="1">%s</span> <span%s data-zh-is-name="1">%s</span>'
            % (_esc(zh), small, _esc(en)))

def _ch_props_html(props, limit=5):
    if not props:
        return ""
    return '<div class="ch-props">%s</div>' % "".join(
        '<span>%s</span>' % _esc(p) for p in props[:limit])

def _ch_base(en, zh):
    """底材：中文为主 + 英文小字。"""
    if not en:
        return _esc(zh) if zh else ""
    if not zh or zh == en:
        return _esc(en)
    return ('<span data-zh-is-name="1">%s</span> <span style="opacity:.7;font-weight:400">%s</span>'
            % (_esc(zh), _esc(en)))

def _ch_item(cid, cat, name_html, sub_html, props=None, req=0, search="", runes=None):
    return ('<div class="ch-item" role="checkbox" tabindex="0" aria-checked="false"'
            ' data-id="%s" data-cat="%s" data-search="%s" data-sockets="%s" data-runes="%s">'
            '<span class="ch-box"><span>✓</span></span>'
            '<div class="ch-main"><div class="ch-name">%s</div>%s%s</div>%s</div>'
            % (_ch_attr(cid), cat, _ch_attr(search),
               runes and str(len(runes.split(","))) or "", _ch_attr(runes or ""),
               name_html, sub_html,
               _ch_props_html(props or []),
               ('<span class="ch-req">%s</span>' % bi("需等级 %d" % req, "Lvl %d" % req)) if req else ""))

def _ch_section(sec_id, title_zh, title_en, cat, count, inner):
    return ('<section class="ch-sec" data-sec="%s">'
            '<header><h2>%s</h2><span class="cnt" data-catnum="%s">0 / %d</span>'
            '<span class="ch-bar grow"><i data-catbar="%s" style="width:0%%"></i></span></header>'
            '%s</section>' % (sec_id, bi(title_zh, title_en), cat, count, cat, inner))

def chronicle():
    # ---------------- 符文之语 ----------------
    rw_items = []
    for r in sorted(RUNEWORDS, key=lambda x: (-x["sockets"], x["en"])):
        rune_html = '<code class="rw">%s</code>' % " + ".join(r["runes"])
        ladder = ('<span class="ch-ladder">%s</span>' % bi("天梯专属", "Ladder")) if r["ladder_only"] else ""
        sub = ('<div class="ch-sub">%s %s · %s %s</div>'
               % (bi("符文顺序", "Runes"), rune_html, bi("底材", "Base"), _esc(r["base"]))
               + ("<div>%s</div>" % ladder if ladder else ""))
        search = " ".join([r["zh"], r["en"], r["base"]] + r["runes"] + r["effects"])
        rw_items.append(_ch_item(r["id"], "rw", _ch_name(r["zh"], r["en"]), sub,
                                 r["effects"], req=r.get("req", 0), search=search,
                                 runes=",".join(r["runes"])))

    # ---------------- 套装 ----------------
    set_items = []
    for s in SETS:
        piece_rows = []
        for p in s["pieces"]:
            piece_rows.append(_ch_item(
                "piece:" + p["en"], "set", _ch_name(p["zh"], p["en"]),
                '<div class="ch-sub">%s · %s</div>' % (_esc(p["group_zh"]), _ch_base(p["base"], p.get("base_zh", ""))),
                p["props"], req=p.get("req", 0),
                search=" ".join([s["zh"], s["en"], p["zh"], p["en"], p["base"], p.get("base_zh", "")])))
        bits = []
        if s["bonus2"]:
            bits.append(bi("2 件：", "2 pc: ") + "、".join(_esc(x) for x in s["bonus2"]))
        for b in s["bonus"]:
            bits.append("%d %s：%s" % (b["pieces"], bi("件", "pc"), _esc(b["text"])))
        bonus = ('<div class="ch-bonus">%s</div>' % "　·　".join(bits)) if bits else ""
        cnt_zh = "%d 件套" % s["count"]
        cnt_en = "%d-piece set" % s["count"]
        # 套装头部可点：一次勾/取消该套装全部部件（data-role=set-all，不计入总进度）
        head = ('<div class="ch-item ch-set-head" role="checkbox" tabindex="0" aria-checked="false"'
                ' data-id="__set__%s" data-cat="set" data-role="set-all" data-search="%s">'
                '<span class="ch-box"><span>✓</span></span>'
                '<div class="ch-main"><div class="ch-name"><b>%s</b></div>'
                '<div class="ch-sub">%s</div>%s</div>'
                '<span class="ch-req">%s</span></div>'
                % (_ch_attr(s["id"]), _ch_attr(" ".join([s["zh"], s["en"]])),
                   _ch_name(s["zh"], s["en"]),
                   bi(cnt_zh, cnt_en),
                   bonus,
                   bi("需等级 %d" % s["req"], "Lvl %d" % s["req"]) if s["req"] else ""))
        set_items.append('<div class="ch-subwrap">' + head
                         + '<div class="ch-grid ch-pieces">%s</div></div>' % "".join(piece_rows))

    # ---------------- 独特道具（按部位分组） ----------------
    GROUP_ORDER = [
        ("helms", "头盔", "Helms"), ("armor", "盔甲", "Body Armor"), ("shields", "盾牌", "Shields"),
        ("gloves", "手套", "Gloves"), ("boots", "靴子", "Boots"), ("belts", "腰带", "Belts"),
        ("amulets", "项链", "Amulets"), ("rings", "戒指", "Rings"), ("charms", "护符", "Charms"),
        ("jewels", "珠宝", "Jewels"), ("orbs", "宝珠", "Orbs"), ("wands", "魔杖", "Wands"),
        ("staves", "法杖", "Staves"), ("tomes", "典籍", "Tomes"), ("bows", "弓", "Bows"),
        ("crossbows", "弩", "Crossbows"), ("javelins", "标枪", "Javelins"),
        ("claws", "爪", "Claws"), ("polearms", "长柄武器", "Polearms"),
        ("spears", "长矛", "Spears"), ("scepters", "权杖", "Scepters"), ("swords", "剑", "Swords"),
        ("daggers", "匕首", "Daggers"), ("axes", "斧", "Axes"), ("melee", "钝器", "Blunt Weapons"),
        ("misc", "其他", "Other"),
    ]
    by_group = {}
    for u in UNIQUES:
        by_group.setdefault(u["group"], []).append(u)
    uni_blocks = []
    for gkey, gzh, gen in GROUP_ORDER:
        arr = by_group.get(gkey)
        if not arr:
            continue
        rows = []
        for u in arr:
            tags = ('<span class="ch-eth">%s</span>' % bi("无形", "Ethereal")) if u["eth"] else ""
            sub = '<div class="ch-sub">%s%s</div>' % (_ch_base(u["base"], u.get("base_zh", "")), tags)
            search = " ".join([u["zh"], u["en"], u["base"], u.get("base_zh", ""),
                               u["group_zh"]] + u["props"])
            rows.append(_ch_item(u["id"], "uni", _ch_name(u["zh"], u["en"]), sub,
                                 u["props"], req=u.get("req", 0), search=search))
        uni_blocks.append('<div class="ch-subwrap"><div class="ch-subgrp">%s · %d</div>'
                          '<div class="ch-grid">%s</div></div>'
                          % (bi(gzh, gen), len(arr), "".join(rows)))

    n_rw, n_set, n_uni = len(RUNEWORDS), len(SETS), len(UNIQUES)
    n_pieces = sum(len(s["pieces"]) for s in SETS)
    # 可勾选项 = 符文之语 + 套装部件 + 独特道具（套装头是批量开关，不计入）
    n_total = n_rw + n_pieces + n_uni

    body = (
      '<div class="breadcrumb"><a href="index.html">' + bi("首页", "Home") + '</a> / '
      + bi("收藏", "Collection") + ' / ' + bi("编年史", "Chronicle") + '</div>\n'
      '<div class="ch-hero"><div class="wrap">'
      '<h1><span class="zt"><span class="zc">收藏编年史 </span><span class="ec" lang="en">Collection Chronicle</span></span></h1>'
      '<p class="sub">' + bi(
          "暗黑 II 值得收集的东西就那么些：符文之语、套装、独特道具。这里把它们全列出来，你打勾记录自己收集了多少，"
          "进度条实时统计完成度。",
          "There are only so many things worth collecting in Diablo II: runewords, sets and unique items. "
          "Everything is listed here — tick off what you have and watch the progress bars fill up.") + '</p>'
      '<div class="ch-total">'
        '<div><div class="num"><span id="chTotal">0</span> <small id="chTotalOf">/ %d</small></div>'
        '<div class="meta"><b>%s</b><span id="chPct">0%%</span></div></div>'
        '<div class="ch-bar"><i id="chBar" style="width:0%%"></i></div>'
      '</div></div></div>\n'
      '<div class="ch-toolbar">'
        # placeholder / aria-label 是纯文本属性，不能用 bi()（会塞 span 破坏 HTML）
        '<input type="search" id="chSearch" placeholder="搜索中文名 / 英文名 / 属性…" aria-label="搜索收藏条目">'
        '<button class="ch-tab on" data-filter="all">%s</button>'
        '<button class="ch-tab" data-filter="rw">%s</button>'
        '<button class="ch-tab" data-filter="set">%s</button>'
        '<button class="ch-tab" data-filter="uni">%s</button>'
        '<button class="ch-reset" id="chReset" data-label="reset" data-confirm="reset-confirm">%s</button>'
        # 导出图片用于分享；导出 JSON 是可再导入的完整备份；导入用 label 包隐藏的 file input
        '<span class="ch-io">'
          '<button type="button" class="ch-btn" id="chShare">%s</button>'
          '<button type="button" class="ch-btn" id="chExport">%s</button>'
          '<label class="ch-btn" id="chImportLabel">%s'
            '<input type="file" id="chImport" accept=".json,application/json" hidden></label>'
        '</span>'
      '</div>\n'
      # 导入前先摆确认条：合并 / 覆盖 / 取消。文案由 JS 按语言现场写。
      '<div class="ch-io-bar" id="chIoBar" hidden><span class="ch-io-msg" id="chIoMsg"></span>'
      '<span class="ch-io-acts">'
        '<button type="button" class="ch-btn primary" id="chIoMerge"></button>'
        '<button type="button" class="ch-btn" id="chIoReplace"></button>'
        '<button type="button" class="ch-btn ghost" id="chIoCancel"></button>'
      '</span></div>\n'
      '<div class="callout info"><b>%s</b>%s</div>\n'
      % (n_total,
         bi("已收集", "Collected"),
         bi("全部", "All"), bi("符文之语", "Runewords"), bi("套装", "Sets"), bi("独特道具", "Uniques"),
         bi("清空打勾", "Reset"),
         bi("导出图片", "Export image"),
         bi("导出 JSON", "Export JSON"),
         bi("导入", "Import"),
         bi("数据只存在你自己的浏览器里：", "Everything stays in your browser: "),
         bi("打勾状态写在本地 <code>localStorage</code>，不会上传到任何服务器。想分享进度就点「导出图片」生成一张成绩卡；"
            "换浏览器、换设备之前点「导出 JSON」存一份备份，在新浏览器里「导入」即可恢复打勾记录。",
            "Ticks are saved to localStorage in this browser only — nothing is uploaded. Use Export image to get a "
            "shareable progress card; before switching browser or device, hit Export JSON to save a backup, then "
            "Import it in the new browser to restore your ticks."))
      + '<div data-chronicle>\n'
      + _ch_section("rw", "符文之语", "Runewords", "rw", n_rw,
                    rune_need_table()
                    + '<div class="ch-grid">%s</div>' % "".join(rw_items))
      + _ch_section("set", "套装", "Sets", "set", n_pieces, "".join(set_items))
      + _ch_section("uni", "独特道具", "Unique Items", "uni", n_uni, "".join(uni_blocks))
      + '</div>\n'
      '<div class="pager"><a href="index.html"><small>' + bi("返回", "Back") + '</small>'
      + bi("首页", "Home") + '</a><a href="guides/runewords.html"><small>'
      + bi("查看图鉴", "See Codex") + '</small>' + bi("符文之语图鉴", "Runewords") + '</a></div>'
    )
    # depth=0：chronicle.html 在站点根目录，和 index.html 同级。
    # 传1 会让 CSS/JS/内链全部指向 ../（跑到站点外层），页面就没样式了。
    return page("收藏编年史 · 暗黑破坏神 II 攻略站", 0, body, "chronicle", True,
                desc=CHRONICLE_DESC, en_t="Collection Chronicle | Diablo II: Resurrected Guide",
                keywords=CHRONICLE_KW)

FAVICON_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#0c0a09"/><polygon points="32,7 40,25 59,25 44,37 50,57 32,45 14,57 20,37 5,25 24,25" fill="none" stroke="#c8a24a" stroke-width="3"/><circle cx="32" cy="32" r="5.5" fill="#a3302e"/></svg>
'''

def seo_files():
    """robots.txt 与 sitemap.xml（每个页面单独一条 URL）。"""
    today = datetime.date.today().isoformat()
    entries = [("", "1.0", "weekly"), ("chronicle.html", "0.9", "weekly")]
    for cid, cn, en in CLASS_LIST:
        entries.append(("classes/" + cid + ".html", "0.8", "monthly"))
    for gid, name, en in GUIDE_LIST:
        entries.append(("guides/" + gid + ".html", "0.8", "monthly"))
    locs = ["  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n"
            "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
            % (SITE_URL, rel, today, freq, prio) for rel, prio, freq in entries]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(locs) + "\n</urlset>\n")
    robots = ("User-agent: *\nAllow: /\n\n"
              "# 私人笔记库与构建脚本不出现在搜索结果中\n"
              "Disallow: /diablo2.logseq/\nDisallow: /build_site.py\n\n"
              "Sitemap: " + SITE_URL + "sitemap.xml\n")
    return sitemap, robots

# ---------------------------------------------------------------------------
# Write all files
# ---------------------------------------------------------------------------
def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

write(os.path.join(OUT, "index.html"), home())
write(os.path.join(OUT, "favicon.svg"), FAVICON_SVG)
write(os.path.join(OUT, "robots.txt"), seo_files()[1])
write(os.path.join(OUT, "sitemap.xml"), seo_files()[0])
write(os.path.join(OUT, "css", "style.css"), CSS)
write(os.path.join(OUT, "js", "main.js"), JS)
write(os.path.join(OUT, "classes", "amazon.html"), amazon())
write(os.path.join(OUT, "classes", "sorceress.html"), sorceress())
write(os.path.join(OUT, "classes", "necromancer.html"), necromancer())
write(os.path.join(OUT, "classes", "paladin.html"), paladin())
write(os.path.join(OUT, "classes", "barbarian.html"), barbarian())
write(os.path.join(OUT, "classes", "druid.html"), druid())
write(os.path.join(OUT, "classes", "warlock.html"), warlock())
write(os.path.join(OUT, "classes", "assassin.html"), assassin())
write(os.path.join(OUT, "guides", "runewords.html"), g_runewords())
write(os.path.join(OUT, "guides", "leveling.html"), g_leveling())
write(os.path.join(OUT, "guides", "terror-zones.html"), g_terror())
write(os.path.join(OUT, "guides", "uber.html"), g_uber())
write(os.path.join(OUT, "guides", "tips.html"), g_tips())
write(os.path.join(OUT, "guides", "farming.html"), g_farming())
write(os.path.join(OUT, "chronicle.html"), chronicle())

# ---------------------------------------------------------------------------
# 自检：本地资源引用必须存在、且不能指向站点外层
# （曾因 chronicle.html 传错 depth 导致 CSS/JS 引用 ../，整页裸奔无样式）
# ---------------------------------------------------------------------------
import re as _re

_pages = ["index.html", "chronicle.html"] \
    + ["classes/%s.html" % c for c, _, _ in CLASS_LIST] \
    + ["guides/%s.html" % g for g, _, _ in GUIDE_LIST]
_errs = []
for _rel in _pages:
    _p = os.path.join(OUT, _rel)
    if not os.path.exists(_p):
        _errs.append("%s 未生成" % _rel)
        continue
    _h = open(_p, encoding="utf-8").read()
    _d = os.path.dirname(_p)
    for _m in _re.finditer(r'(?:href|src)="([^"]+\.(?:css|js|png|svg|ico))"', _h):
        _u = _m.group(1)
        if _u.startswith(("http://", "https://", "//")):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(_d, _u))):
            _errs.append("%s → 资源不存在: %s" % (_rel, _u))
    # 内部链接（不含锚点/外链）也查一遍
    for _m in _re.finditer(r'href="([^"#?:]+\.html)"', _h):
        _u = _m.group(1)
        if not os.path.exists(os.path.normpath(os.path.join(_d, _u))):
            _errs.append("%s → 链接不存在: %s" % (_rel, _u))
if _errs:
    print("!! 自检发现 %d 个引用问题：" % len(_errs))
    for _e in _errs[:20]:
        print("   -", _e)
    raise SystemExit(1)

print("Site generated.")
print("Self-check passed: %d pages, all local assets & links resolved." % len(_pages))
print("Total HTML files:", 1 + 8 + 6)
