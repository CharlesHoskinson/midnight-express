'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs/promises'),os=require('node:os'),path=require('node:path');
const {chromium}=require('/home/hoskinson/.local/share/mise/installs/npm-playwright/1.63.0/node_modules/playwright');
(async()=>{
 const dir=await fs.mkdtemp(path.join(os.tmpdir(),'mpe-zoom-')),extension=path.join(dir,'extension');await fs.mkdir(extension);
 await fs.writeFile(path.join(extension,'manifest.json'),JSON.stringify({manifest_version:3,name:'Local zoom audit',version:'1.0',permissions:['tabs'],background:{service_worker:'worker.js'}}));await fs.writeFile(path.join(extension,'worker.js'),'chrome.runtime.onInstalled.addListener(()=>{});');
 const context=await chromium.launchPersistentContext(path.join(dir,'profile'),{headless:true,viewport:null,executablePath:'/home/hoskinson/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome',ignoreDefaultArgs:['--disable-extensions'],args:[`--disable-extensions-except=${extension}`,`--load-extension=${extension}`,'--window-size=1440,1000']});
 try{
  const worker=context.serviceWorkers()[0]||await context.waitForEvent('serviceworker'),page=await context.newPage();await page.goto('http://127.0.0.1:8876/subscriptions.html');await page.locator('#result-count').filter({hasText:'603 feeds'}).waitFor();
  const baseline=await page.evaluate(()=>innerWidth);
  const zoom=await worker.evaluate(()=>new Promise(resolve=>chrome.tabs.query({url:'http://127.0.0.1:8876/subscriptions.html'},tabs=>chrome.tabs.setZoom(tabs[0].id,2,()=>chrome.tabs.getZoom(tabs[0].id,resolve)))));
  await page.waitForTimeout(100);assert.equal(zoom,2);const geometry=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));assert.ok(geometry.width<baseline);assert.ok(geometry.scroll<=geometry.width+1);
  await page.locator('#search').fill('urn:mpe:source:demo-ops-002');await page.locator('#result-count').filter({hasText:'1 feeds'}).waitFor();await page.locator('.follow').click();await page.locator('.follow').filter({hasText:'Following'}).waitFor();
  const rgb=s=>s.match(/[\d.]+/g).slice(0,3).map(Number),lum=c=>c.map(n=>{n/=255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4;}).reduce((a,n,i)=>a+n*[.2126,.7152,.0722][i],0),ratio=(a,b)=>(Math.max(lum(a),lum(b))+.05)/(Math.min(lum(a),lum(b))+.05);
  const styles=await page.evaluate(()=>{const keys=['body','.notice','.feed-row p','button','input','header nav a'];return keys.map(key=>{const e=document.querySelector(key),c=getComputedStyle(e);let n=e,b=c.backgroundColor;while(b==='rgba(0, 0, 0, 0)'&&n.parentElement){n=n.parentElement;b=getComputedStyle(n).backgroundColor;}return {key,color:c.color,background:b,fontSize:c.fontSize};});});
  const contrast=styles.map(s=>({...s,ratio:ratio(rgb(s.color),rgb(s.background))}));assert.ok(contrast.every(s=>s.ratio>=4.5));
  await page.hover('.follow');const hover=await page.locator('.follow').evaluate(e=>({color:getComputedStyle(e).color,background:getComputedStyle(e).backgroundColor}));assert.ok(ratio(rgb(hover.color),rgb(hover.background))>=4.5);
  await fs.writeFile(path.resolve(__dirname,'../../reviews/subscription-workspace/zoom-contrast.json'),JSON.stringify({zoom,baseline,geometry,task:'Search and independently follow at actual Chrome tab zoom 200%',contrast,hover},null,2));console.log('PASS actual browser zoom 200%, search/follow task, representative computed contrast and button hover');
 }finally{await context.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
