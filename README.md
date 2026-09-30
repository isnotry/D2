# 暗黑破坏神 II：复活攻略站 · D2R Guide

**简体中文** | [English](README.en.md)

![零依赖](https://img.shields.io/badge/dependencies-0-brightgreen)
![零构建](https://img.shields.io/badge/build-none-blue)
![纯静态](https://img.shields.io/badge/web-15%20pages-lightgrey)
![内容版本](https://img.shields.io/badge/content-Patch%203.3%20%2F%20S15-orange)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)

> Diablo II: Resurrected 全职业加点与流派攻略的中英双语静态站，零依赖零构建，打开即用。

![界面截图](https://cdn.jsdelivr.net/gh/isnotry/d2@main/docs/screenshot.png)

**[在线使用](https://isnotry.github.io/d2/)**

---

## 它是什么

一个面向 D2R 玩家的静态攻略站：八大职业的技能树加点、主流流派 Build、装备思路与开荒 / 终局技巧，外加符文之语图鉴、恐怖地带、Uber 终局等 6 个攻略专题。

纯 HTML + CSS + 原生 JS，无框架、无后端、无任何第三方库；全部页面由一个 Python 脚本 `build_site.py` 生成，内容已同步到 Patch 3.3 / 天梯第 15 赛季。

## 特性

- **八大职业全覆盖** —— 亚马逊、法师、亡灵法师、圣骑士、野蛮人、德鲁伊、刺客、术士，每页含技能树加点、流派 Build 卡与实战要点
- **六个攻略专题** —— 符文之语图鉴、练级与开荒、恐怖地带与破免、Uber 终局、综合技巧、速刷与 MF
- **中英双语一键切换** —— 右上角 `EN / 中文` 按钮，选择存 localStorage，刷新不丢
- **跟随赛季更新** —— 内容基于 Patch 3.3 / 第 15 赛季 meta（破免获取收紧、练级暗金重做、术士 Sigil: Death 上位等）
- **纯静态零依赖** —— 不用任何框架与构建工具，clone 下来双击 `index.html` 就能看
- **一处数据源** —— 所有页面由 `build_site.py` 单文件生成，改文案重跑一次即可
- **暗金主题视觉** —— 自绘 CSS 主题，图标全部为 Unicode 字符，不引用任何游戏美术素材

## 快速开始

### 在线使用

点击 **[在线使用](https://isnotry.github.io/d2/)** 即可打开，无需安装、不用注册。

### 本地使用

```bash
git clone git@github.com:isnotry/d2.git
cd d2
python3 -m http.server 8000
# 打开 http://localhost:8000
```

也可以直接用浏览器打开 `index.html`，效果相同。

## 页面清单

| 页面 | 路径 | 内容 |
|---|---|---|
| 首页 | `index.html` | 本季核心机制、职业总览、攻略入口 |
| 职业页 ×8 | `classes/*.html` | 技能树加点、流派 Build、装备与实战要点 |
| 符文之语图鉴 | `guides/runewords.html` | 常用符文之语配方表与天梯轮转说明 |
| 练级与开荒 | `guides/leveling.html` | 1-85 级路线、本季练级装改动 |
| 恐怖地带与破免 | `guides/terror-zones.html` | 恐怖地带机制、破免护符获取与 Patch 3.3 改动 |
| Uber 终局 | `guides/uber.html` | 超级 Boss 触发方式与打法要点 |
| 综合技巧 | `guides/tips.html` | 通用机制、名词表、常见误区 |
| 速刷与 MF | `guides/farming.html` | 高效刷宝场景与 MF 阈值 |

## 界面说明

| 位置 | 元素 | 作用 |
|---|---|---|
| 顶栏左侧 | 站名 | 点击回到首页 |
| 顶栏中部 | Home / Classes / Guides | 三组页面的导航 |
| 顶栏右侧 | `EN / 中文` 按钮 | 中英切换，选择记忆在 localStorage |
| 正文 | 流派卡 / 数据表 | 每个流派的定位、加点与装备一览 |
| 页脚 | 免责声明 + 仓库链接 | 非官方声明与本仓库入口 |

## 重新生成站点

所有页面都由 `build_site.py` 生成，改完脚本重跑一次即可覆盖输出：

```bash
python3 build_site.py
```

产物：`index.html`、`classes/*.html`、`guides/*.html`、`css/style.css`、`js/main.js`。

双语机制：正文用 `bi(中文, 英文)` 产出 `.zc` / `.ec` 两个 `span`，CSS 按 `<html class="en">` 切换显示；游戏术语另有一张中英对照表 `ZH_PAIRS`，正文里的术语会被自动替换成双语。

## 数据与隐私

本站不收集任何数据、不发送任何请求（无统计、无广告、无 CDN 字体以外的外链）。

| 存储 key | 内容 |
|---|---|
| `lang` | 语言选择（`en` 或空），仅存本机浏览器 |

## 目录结构

```text
d2/
├── build_site.py               # 站点生成脚本（唯一数据源）
├── index.html                  # 首页（生成产物）
├── classes/                    # 8 个职业页（生成产物）
├── guides/                     # 6 个攻略专题页（生成产物）
├── css/style.css               # 全站样式（生成产物）
├── js/main.js                  # 语言切换等少量 JS（生成产物）
├── docs/                       # README 截图
└── README.md
```

## 开发说明

- 改内容只动 `build_site.py`，不要手改 HTML —— 重新生成会覆盖
- 新增文案用 `bi(中文, 英文)`；游戏专名写进 `ZH_PAIRS` 术语表即可自动双语
- `.zt` 双语结构别手拆：`html.en` 下的显隐全靠 `.zc` / `.ec` 两个类名

## 版权与商标声明

**本站为非官方粉丝作品，与 Blizzard Entertainment, Inc. 无任何隶属、授权或背书关系。**

- `Diablo`、`Diablo II`、`Diablo II: Resurrected` 及游戏内专有名词为 Blizzard Entertainment, Inc. 的商标，本站仅在描述与指示意义上引用
- 游戏内的美术、音效、截图等素材版权归 Blizzard Entertainment, Inc. 所有，**本仓库不包含任何此类素材**；站内所有图标均为 Unicode 字符或自绘 SVG
- 游戏数值、配方、术语等事实性信息的整理与表述为本站原创编写

## 浏览器支持

现代 Chrome / Edge / Firefox / Safari 均可，无 IE 兼容；CSS 用了 `grid` 与 `:not()` 选择器，布局在窄屏下自动降级为单列。

## 许可

- **代码**（`build_site.py`、`css/`、`js/` 及生成的 HTML 结构）：[MIT](LICENSE)
- **攻略文本内容**：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) —— 署名、非商业、相同方式共享

[MIT](LICENSE) © 2026 isnotry
