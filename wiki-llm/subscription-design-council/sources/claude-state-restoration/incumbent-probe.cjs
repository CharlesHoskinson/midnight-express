const pw=require('/home/hoskinson/.local/share/mise/installs/npm-playwright/1.63.0/node_modules/playwright');
(async()=>{const b=await pw.chromium.launch({headless:true,executablePath:'/home/hoskinson/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'});
const ctx=await b.newContext({viewport:{width:1440,height:900}});const p=await ctx.newPage();const out={};
await p.goto('http://127.0.0.1:8876/subscriptions.html');await p.locator('#streams .stream').first().waitFor();
out.streamCount=await p.locator('#streams .stream').count();
out.subscribeButtons=await p.locator('#streams button').evaluateAll(bs=>bs.map(b=>b.textContent).filter(t=>t.startsWith('Subscribe')));
out.domNodes=await p.evaluate(()=>document.querySelectorAll('*').length);
out.docHeight1440=await p.evaluate(()=>document.documentElement.scrollHeight);
out.streamsTopY=await p.evaluate(()=>document.getElementById('streams').getBoundingClientRect().top+scrollY);
out.subsTopY=await p.evaluate(()=>document.getElementById('subscriptions').getBoundingClientRect().top+scrollY);
out.inboxTopY=await p.evaluate(()=>document.getElementById('inbox').getBoundingClientRect().top+scrollY);
// build state
await p.fill('#search','payment');out.searchHits=await p.locator('#streams .stream').count();
out.urlAfterSearch=p.url();
await p.selectOption('#consumer','dapp');
await p.getByRole('button',{name:'Subscribe to payments',exact:true}).first().click();
await p.locator('#tick').click();await p.locator('#tick').click();await p.locator('#process').click();
out.beforeReload={subs:await p.locator('.subscription').count(),inbox:await p.locator('.inbox-item').count(),search:await p.inputValue('#search'),consumer:await p.inputValue('#consumer')};
out.storage=await p.evaluate(async()=>({local:Object.keys(localStorage),session:Object.keys(sessionStorage),idb:indexedDB.databases?(await indexedDB.databases()).map(d=>d.name):'n/a',estimate:navigator.storage?await navigator.storage.estimate():null,persisted:navigator.storage&&navigator.storage.persisted?await navigator.storage.persisted():null}));
// read/unread: inbox item activation changes?
const itemTextBefore=await p.locator('.inbox-item button').first().textContent();await p.locator('.inbox-item button').first().click();out.inboxItemAfterOpen=await p.locator('.inbox-item button').first().textContent();out.itemTextBefore=itemTextBefore;out.detailOpen=await p.evaluate(()=>document.querySelector('details').open);
out.announcement=await p.textContent('#announcement');
await p.reload();await p.locator('#streams .stream').first().waitFor();
out.afterReload={subs:await p.locator('.subscription').count(),inbox:await p.locator('.inbox-item').count(),search:await p.inputValue('#search'),consumer:await p.inputValue('#consumer'),subsText:await p.textContent('#subscriptions')};
// second tab independence
const p2=await ctx.newPage();await p2.goto('http://127.0.0.1:8876/subscriptions.html');await p2.locator('#streams .stream').first().waitFor();
await p.getByRole('button',{name:'Subscribe to quotes',exact:true}).first().click();await p2.waitForTimeout(300);out.secondTabSubs=await p2.locator('.subscription').count();
// keyboard: tab stops before first stream subscribe
await p.reload();await p.locator('#streams .stream').first().waitFor();
out.tabStopsBeforeSubscriptionsPanel=await p.evaluate(()=>{const f=[...document.querySelectorAll('a,button,input,select,summary,[tabindex]')].filter(e=>!e.disabled&&e.tabIndex>=0);const target=document.getElementById('tick');return f.indexOf(target);});
out.sticky=await p.evaluate(()=>{const a=document.getElementById('announcement');const r=a.getBoundingClientRect();return {h:r.height,pos:getComputedStyle(a).position,bg:getComputedStyle(a).backgroundColor,empty:a.textContent===''};});
await p.screenshot({path:'incumbent-desktop-1440.png'});
const m=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:1});const pm=await m.newPage();await pm.goto('http://127.0.0.1:8876/subscriptions.html');await pm.locator('#streams .stream').first().waitFor();
out.docHeight390=await pm.evaluate(()=>document.documentElement.scrollHeight);out.streamsTopY390=await pm.evaluate(()=>document.getElementById('streams').getBoundingClientRect().top+scrollY);out.inboxTopY390=await pm.evaluate(()=>document.getElementById('inbox').getBoundingClientRect().top+scrollY);
await pm.evaluate(()=>document.getElementById('streams').scrollIntoView());await pm.screenshot({path:'incumbent-mobile-390-streams.png'});
console.log(JSON.stringify(out,null,1));await b.close();})().catch(e=>{console.error(e);process.exit(1)});
