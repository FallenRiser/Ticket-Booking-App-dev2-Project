if(!self.define){let e,s={};const i=(i,n)=>(i=new URL(i+".js",n).href,s[i]||new Promise((s=>{if("document"in self){const e=document.createElement("script");e.src=i,e.onload=s,document.head.appendChild(e)}else e=i,importScripts(i),s()})).then((()=>{let e=s[i];if(!e)throw new Error(`Module ${i} didn’t register its module`);return e})));self.define=(n,o)=>{const r=e||("document"in self?document.currentScript.src:"")||location.href;if(s[r])return;let l={};const t=e=>i(e,r),u={module:{uri:r},exports:l,require:t};s[r]=Promise.all(n.map((e=>u[e]||t(e)))).then((e=>(o(...e),l)))}}define(["./workbox-5b385ed2"],(function(e){"use strict";e.setCacheNameDetails({prefix:"ticketshow"}),self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"/css/app.5641b8ba.css",revision:null},{url:"/css/chunk-vendors.3b0641a8.css",revision:null},{url:"/fonts/Bluto.2726f441.otf",revision:null},{url:"/fonts/PlayfairDisplay-SemiBold.b6d1d3d2.ttf",revision:null},{url:"/fonts/Showtime.fca2bffc.ttf",revision:null},{url:"/index.html",revision:"75b4458a359740a3725c0f70259fe086"},{url:"/js/app.05e27678.js",revision:null},{url:"/js/chunk-vendors.7b08e1d3.js",revision:null},{url:"/manifest.json",revision:"dd4d161c062e5aee622fdea65769bd07"},{url:"/robots.txt",revision:"b6216d61c03e6ce0c9aea6ca7808f7ca"}],{})}));
//# sourceMappingURL=service-worker.js.map