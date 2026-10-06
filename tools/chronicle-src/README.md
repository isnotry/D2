# 收藏编年史 · 数据管线

生成 `../d2_chronicle_data.py`（被 `build_site.py` import）。

## 用法

```bash
cd tools/chronicle-src
python3 build_chronicle.py            # 打印统计
python3 -c "import build_chronicle as b; b.emit('../../d2_chronicle_data.py')"
cd ../.. && python3 build_site.py     # 重新生成站点
```

## 数据源

| 来源 | 用途 | 位置 |
|---|---|---|
| `blizzhackers/d2data` | 官方属性数据（patch 3.3） | 外部，1.2G 不入库；放本目录或 `/tmp`，或用 `D2DATA_DIR` 指定 |
| `DozenTwelve/diablo2-tacker` | 繁体译名（opencc 转简体） | 外部；同理用 `D2TRACKER_DIR` |
| `ref/d2rworld_*.json` | **d2r.world 官方简中译名（权威）** | 随仓库提交 |

`ref/` 是从 d2r.world 抓取的存档，优先级最高：

- `d2rworld_base_zh_s.json` — 底材 492 条
- `d2rworld_uniques_zh_s.json` — 独特道具 402 条
- `d2rworld_setparts_zh_s.json` — 套装部件 135 条
- `d2rworld_sets_zh_s.json` — 套装 34 条

## 几个必须知道的坑

1. **d2data 用的是游戏内部名**，与官方显示名不同，必须过 `MANUAL_ALIAS` / `SET_ALIAS` / `PART_ALIAS`
   （如内部名 `McAuley's Folly` 实为官方 `Sander's Folly` 山德的愚行；
   `War Bonnet` 属性与官方 `Biggin's Bonnet` 完全一致，是同一件的老名字）。
2. **`disableChronicle=1` 的条目要过滤**：游戏内标记「不计入图鉴」，实际不可获取。
   Warlord's Glory 整套 5 件都是，不能进收藏清单。
3. **任务物品要排除**：`lvl=0` 且 `lvl req=0` 的（赫拉迪克杖三件、可汗之锤两件、地狱熔炉锤），
   只在任务流程里临时存在。
4. 符文顺序读 `Rune1..Rune7`，**别解析 `*RunesUsed` 字符串**（Last Wish 的 Jah×3 会丢）。
5. 天梯专属判定：有 `firstLadderSeason` 且**无** `lastLadderSeason`。

## 分享卡片的视觉回归

「导出图片」的功能是 canvas 手绘的，坐标全硬编码在 `build_site.py` 的 `drawShareCard()` 里。
jsdom 只能断言「画了哪些文字」，**看不出排版错位**，所以另配一个真渲染脚本：

```bash
npm i jsdom canvas          # 仅本地验证用，站点本身零依赖
NODE_PATH=<node_modules> node tools/chronicle-src/render-card.js /tmp/cardout
```

会输出 4 张图供肉眼核对：`card-empty / card-mid / card-full / card-full-en`。

⚠️ 卡片高度 H=800 是画布硬边界，各区块 y 值是算好的（页脚分隔线在 y=716、文字在 y=754）。
改版式务必重跑这个脚本看图，否则内容会和页脚叠在一起。
