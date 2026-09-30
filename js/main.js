
// 中英文切换：默认中文，点击切英文并记住选择
(function(){
  var bar=document.querySelector("nav.topbar .wrap");
  if(bar){
    var btn=document.createElement("button");
    btn.id="langToggle";btn.className="lang-toggle";
    btn.setAttribute("aria-label","切换中英文");
    bar.appendChild(btn);
    var en=localStorage.getItem("lang")==="en";
    var origTitle=document.title;
    function set(v){document.documentElement.classList.toggle("en",v);localStorage.setItem("lang",v?"en":"");btn.textContent=v?"中文":"EN";document.title=v?(document.documentElement.getAttribute("data-en-title")||origTitle):origTitle;}
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
