'use strict';
const fs=require('node:fs');
const {chromium}=require('/home/hoskinson/.local/share/mise/installs/npm-playwright/1.63.0/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/home/hoskinson/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'});
 const page=await browser.newPage({viewport:{width:1440,height:900}});
 await page.goto('http://127.0.0.1:8876/subscriptions.html');
 await page.locator('#streams .stream').first().waitFor();
 const initial=await page.evaluate(()=>({rows:document.querySelectorAll('.stream').length,dom:document.querySelectorAll('*').length,searchY:document.querySelector('#search').getBoundingClientRect().top,bodyHeight:document.body.scrollHeight}));
 const timing=await page.evaluate(async()=>{
  const input=document.querySelector('#search'),sync=[],paint=[];
  for(let i=0;i<30;i++){
   input.value=i%2?'':'payment';const start=performance.now();
   input.dispatchEvent(new Event('input',{bubbles:true}));sync.push(performance.now()-start);
   await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));paint.push(performance.now()-start);
  }
  const stats=a=>({min:Math.min(...a),median:[...a].sort((a,b)=>a-b)[Math.floor(a.length/2)],p95:[...a].sort((a,b)=>a-b)[Math.ceil(a.length*.95)-1],max:Math.max(...a)});
  return {samples:30,handler_ms:stats(sync),input_to_second_raf_ms:stats(paint),note:'Local 9-record incumbent only; second rAF proxy is not INP or production latency.'};
 });
 await page.locator('#search').fill('unlikely-no-results-query');
 const empty=await page.locator('#streams').textContent();
 await page.locator('#search').fill('');
 const button=page.getByRole('button',{name:'Subscribe to payments',exact:true}).first();await button.focus();await page.keyboard.press('Enter');
 const focusAfterFollow=await page.evaluate(()=>({tag:document.activeElement.tagName,id:document.activeElement.id,text:document.activeElement===document.body?'BODY':document.activeElement.textContent.slice(0,60)}));
 const identity=await page.locator('#subscriptions').textContent();
 await page.reload();await page.locator('#streams .stream').first().waitFor();const reload=await page.locator('#subscriptions').textContent();
 const widths=[];for(const width of [320,390]){await page.setViewportSize({width,height:844});await page.addStyleTag({content:'html{font-size:200%}'});widths.push(await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,searchY:document.querySelector('#search').getBoundingClientRect().top,bodyHeight:document.body.scrollHeight})));}
 const output={retrieved_utc:new Date().toISOString(),browser:await browser.version(),method:'Playwright local-only behavior verification; no external retrieval',viewport:{width:1440,height:900},initial,timing,emptyResultsText:empty,focusAfterFollow,followSubscriptionText:identity,reloadSubscriptionText:reload,mobileFont200:widths};
 fs.writeFileSync('/home/hoskinson/Projects/midnight-express/wiki-llm/subscription-design-council/sources/gpt-usability-verification/local-verification.json',JSON.stringify(output,null,2)+'\n');console.log(JSON.stringify(output,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1;});
