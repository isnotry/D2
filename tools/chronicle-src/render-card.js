#!/usr/bin/env node
/**
 * 分享卡片视觉回归 —— 把「导出图片」实际会生成的 PNG 渲染出来看。
 *
 * 为什么需要它：卡片是 canvas 手绘的，坐标全硬编码在 build_site.py 的
 * drawShareCard() 里。jsdom 能断言「画了哪些文字」，但**看不出排版错位**
 * （曾经差点让符文摘要盒压到页脚上）。这个脚本真渲染成图，用眼睛核对。
 *
 * 依赖（仅本地验证用，站点本身零依赖；D2 项目没有 package.json）：
 *   npm i jsdom canvas
 *
 * 用法：
 *   NODE_PATH=<node_modules 路径> node tools/chronicle-src/render-card.js [输出目录]
 * 输出：
 *   <输出目录>/card-empty.png     0 / 622
 *   <输出目录>/card-mid.png       约 1/3 进度
 *   <输出目录>/card-full.png      622 / 622
 *   <输出目录>/card-full-en.png   622 / 622 + 英文模式
 *   默认输出到系统临时目录。
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { JSDOM } = require('jsdom');
const { createCanvas } = require('canvas');

const ROOT = path.resolve(__dirname, '..', '..');
const OUT = process.argv[2] || os.tmpdir();
fs.mkdirSync(OUT, { recursive: true });
const S = 2;                                     // 超采样，与页面一致
const W = 1200, H = 800;                         // 必须与 build_site.py 的 CARD 一致

const html = fs.readFileSync(path.join(ROOT, 'chronicle.html'), 'utf8');
const js = fs.readFileSync(path.join(ROOT, 'js/main.js'), 'utf8');
// 站点 JS 分两段：SiteStore 在前，编年史模块在后，必须都加载
const storePart = js.slice(0, js.indexOf('// 中英文切换'));
const chronPart = js.slice(js.indexOf('// 收藏编年史'));

function newPage() {
  const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'https://x.test/' + Math.random() });
  const w = dom.window;
  w.eval(storePart);
  w.eval(chronPart);
  return w;
}

function shot(w, file) {
  const IO = w.__chronicleIO;
  const cv = createCanvas(W * S, H * S);
  const ctx = cv.getContext('2d');
  ctx.scale(S, S);
  ctx.textBaseline = 'alphabetic';
  IO.drawShareCard(ctx, IO.fullStats(), IO.runeSummary());
  fs.writeFileSync(file, cv.toBuffer('image/png'));
  const st = IO.fullStats();
  console.log('%s  %d / %d  %s%%', file, st.done, st.total, st.pct);
}

const tick = (w, pred) => [...w.document.querySelectorAll('.ch-item')]
  .forEach((e, i) => { if (e.getAttribute('data-role') !== 'set-all' && pred(e, i)) e.click(); });

let w = newPage();
shot(w, path.join(OUT, 'card-empty.png'));

w = newPage();
tick(w, () => true);
shot(w, path.join(OUT, 'card-full.png'));

w.document.documentElement.classList.add('en');
shot(w, path.join(OUT, 'card-full-en.png'));

w = newPage();
tick(w, (e, i) => i % 3 === 0);
shot(w, path.join(OUT, 'card-mid.png'));
