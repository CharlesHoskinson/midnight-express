const pw=require('/home/hoskinson/.local/share/mise/installs/npm-playwright/1.63.0/node_modules/playwright');
const out='/tmp/mpe-subscription-design-council/claude-best-patterns/';
(async()=>{const b=await pw.chromium.launch({executablePath:'/home/hoskinson/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'});
const r={};
for(const [name,vp] of [['desktop',{width:1440,height:900}],['mobile',{width:390,height:844}]]){
 const p=await b.newPage({viewport:vp});const reqs=[];p.on('request',q=>reqs.push(q.url()));
 await p.goto('http://127.0.0.1:8876/subscriptions.html');await p.locator('#streams .stream').first().waitFor();
 const m=await p.evaluate(()=>{const f=document.querySelector('#streams .stream');const rect=f.getBoundingClientRect();
  const focusables=[...document.querySelectorAll('a,button,input,select,summary')].filter(e=>!e.disabled&&e.offsetParent!==null);
  const idx=focusables.indexOf(f.querySelector('button'));
  const ann=document.getElementById('announcement');const ar=ann.getBoundingClientRect();
  return {firstFeedTop:Math.round(rect.top+scrollY),viewportH:innerHeight,docH:document.documentElement.scrollHeight,buttons:document.querySelectorAll('button').length,streamButtons:document.querySelectorAll('#streams button').length,tabStopsBeforeFirstFeedAction:idx,h1Px:getComputedStyle(document.querySelector('h1')).fontSize,announcementEmptyVisible:ann.textContent===''&&ar.height>0,announcementH:Math.round(ar.height),localStorageKeys:Object.keys(localStorage),sessionStorageKeys:Object.keys(sessionStorage),urlParamsUsed:location.search+location.hash,headings:[...document.querySelectorAll('h1,h2')].map(h=>h.textContent),searchHasRoleCount:!!document.querySelector('[aria-live] , #streams[aria-live]'),resultCountShown:/result/i.test(document.querySelector('#streams').parentElement.textContent)};});
 await p.screenshot({path:out+name+'-initial.png'});
 // subscribe to payments and tick a few
 await p.getByRole('button',{name:'Subscribe to payments',exact:true}).first().click();
 await p.getByRole('button',{name:'Subscribe to quotes',exact:true}).first().click();
 for(let i=0;i<3;i++)await p.locator('#tick').click();
 await p.locator('#search').fill('payment');
 const after=await p.evaluate(()=>({subsText:document.getElementById('subscriptions').innerText.slice(0,900),inboxItems:document.querySelectorAll('.inbox-item').length,inboxText:document.getElementById('inbox').innerText.slice(0,600),streamsShown:document.querySelectorAll('#streams .stream').length,subsTop:Math.round(document.getElementById('subscriptions').getBoundingClientRect().top+scrollY),inboxTop:Math.round(document.getElementById('inbox').getBoundingClientRect().top+scrollY),announcement:document.getElementById('announcement').textContent,overflow:document.documentElement.scrollWidth>innerWidth}));
 await p.locator('#subscriptions').scrollIntoViewIfNeeded();await p.screenshot({path:out+name+'-subscribed.png'});
 // search no results
 await p.locator('#search').fill('zzz-no-match');const noRes=await p.evaluate(()=>({streamsShown:document.querySelectorAll('#streams .stream').length,streamsText:document.getElementById('streams').innerText}));
 // search for profile / mpe terms
 await p.locator('#search').fill('invoice');const invoiceRes=await p.evaluate(()=>document.querySelectorAll('#streams .stream').length);
 await p.locator('#search').fill('urn:mpe:source');const srcRes=await p.evaluate(()=>document.querySelectorAll('#streams .stream').length);
 await p.reload();await p.locator('#streams .stream').first().waitFor();
 const reload=await p.evaluate(()=>({subsText:document.getElementById('subscriptions').innerText,inbox:document.getElementById('inbox').innerText,search:document.getElementById('search').value}));
 r[name]={initial:m,after,noRes,invoiceRes,srcRes,reload,requestsAfterLoad:reqs.map(u=>new URL(u).pathname)};
 await p.close();}
console.log(JSON.stringify(r,null,1));await b.close();})();
