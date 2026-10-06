
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
