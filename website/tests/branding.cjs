'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs/promises'),path=require('node:path');
let chromium;try{({chromium}=require('playwright'));}catch{({chromium}=require('/home/hoskinson/.local/share/mise/installs/npm-playwright/1.63.0/node_modules/playwright'));}
(async()=>{
 const root=path.resolve(__dirname,'../../reviews/midnight-branding');await fs.mkdir(root,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:'/home/hoskinson/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'}),context=await browser.newContext(),page=await context.newPage(),errors=[],failures=[],results=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)failures.push({url:r.url(),status:r.status()});});
 try{
  for(const name of ['index','data-model','subscriptions','specification','implementation']){
   for(const width of [1440,390]){
    await page.setViewportSize({width,height:1050});await page.goto(`http://127.0.0.1:8876/${name}.html`,{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);
    if(name==='subscriptions')await page.locator('#result-count').filter({hasText:'603 feeds'}).waitFor();
    for(const image of await page.locator('img').all()){await image.scrollIntoViewIfNeeded();await image.evaluate(i=>i.complete?Promise.resolve():new Promise((resolve,reject)=>{i.addEventListener('load',resolve,{once:true});i.addEventListener('error',reject,{once:true});}));}
    await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));await page.waitForFunction(()=>scrollY===0);
    const metrics=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,background:getComputedStyle(document.body).backgroundColor,font:getComputedStyle(document.body).fontFamily,eyebrows:document.querySelectorAll('.eyebrow,.detail-label,.edition,.problem-index').length,loadedFonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family),brandBounds:document.querySelector('.brand').getBoundingClientRect().toJSON(),images:[...document.images].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0,alt:!!i.alt}))}));
    assert.equal(metrics.background,'rgb(10, 10, 10)');assert.match(metrics.font,/Outfit/);assert.deepEqual(metrics.loadedFonts,['Outfit']);assert.ok(metrics.brandBounds.top>=0);assert.equal(metrics.eyebrows,0);assert.ok(metrics.scroll<=width+1,`${name} at ${width} overflow`);assert.ok(metrics.images.every(i=>i.loaded&&i.alt));results.push({name,...metrics});
    if(process.env.MPE_CAPTURE_VISUALS==='1')await page.screenshot({path:path.join(root,`${name}-${width}.png`),fullPage:true});
   }
   await page.setViewportSize({width:320,height:1000});await page.evaluate(()=>document.documentElement.style.fontSize='200%');const wide=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));if(wide.scroll>wide.width+1)console.log('Overflow geometry',name,wide,await page.evaluate(()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),a=[];let n;while(n=w.nextNode()){if(!n.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(n);if(r.getBoundingClientRect().right>innerWidth+1)a.push({parent:n.parentElement.tagName,class:n.parentElement.className,text:n.textContent.slice(0,50),right:r.getBoundingClientRect().right});}return a.slice(0,20);}));assert.ok(wide.scroll<=wide.width+1,`${name} at 320 / 200% text overflow: ${JSON.stringify(await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>({tag:e.tagName,class:e.className,right:e.getBoundingClientRect().right,text:e.textContent.slice(0,70)})).slice(0,15)))}`);results.push({name,text:'200%',...wide});
  }
  await page.setViewportSize({width:1440,height:1050});await page.goto('http://127.0.0.1:8876/index.html',{waitUntil:'networkidle'});await page.locator('#architecture').evaluate(e=>e.scrollIntoView({block:'start',behavior:'instant'}));
  if(process.env.MPE_CAPTURE_VISUALS==='1')await page.screenshot({path:path.join(root,'architecture-desktop.png')});
  await page.locator('[data-component=gossip]').click();await page.locator('#component-detail').filter({hasText:'GossipSub'}).waitFor();
  await page.locator('[data-workflow=invoices]').click();await page.locator('#workflow-panel').filter({hasText:/invoice/i}).waitFor();
  assert.deepEqual(errors,[]);assert.deepEqual(failures,[]);
  await fs.writeFile(path.join(root,'site-evidence.json'),JSON.stringify({browser:await browser.version(),results,errors,failures},null,2)+'\n');console.log('PASS Midnight palette, Outfit font, generated assets, no eyebrow labels, navigation/workflow/stack controls and all-page mobile/enlarged-text reflow');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
