const pw=require('/home/hoskinson/.local/share/mise/installs/npm-playwright/1.63.0/node_modules/playwright');
(async()=>{const b=await pw.chromium.launch({executablePath:'/home/hoskinson/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'});
for(const [w,h,zoom] of [[390,844,'200%'],[1280,900,'100%']]){
const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('http://127.0.0.1:8876/subscriptions.html');await p.locator('#streams .stream').first().waitFor();
await p.addStyleTag({content:`html{font-size:${zoom}}`});
await p.getByRole('button',{name:'Subscribe to quotes',exact:true}).click();await p.locator('#tick').click();
await p.evaluate(()=>scrollTo(0,0));let hidden=0,partial=0,total=0,bodyLoss=0;
for(let i=0;i<70;i++){await p.keyboard.press('Tab');const r=await p.evaluate(()=>{const a=document.activeElement;if(a===document.body)return 'body';const e=a.getBoundingClientRect(),n=document.getElementById('announcement').getBoundingClientRect();const ov=Math.max(0,Math.min(e.bottom,n.bottom)-Math.max(e.top,n.top));return ov<=0?'clear':ov>=e.height-1?'hidden:'+a.textContent.slice(0,30):'partial'});total++;if(r==='body')bodyLoss++;else if(r.startsWith('hidden')){hidden++;}else if(r==='partial')partial++;}
const annH=await p.evaluate(()=>Math.round(document.getElementById('announcement').getBoundingClientRect().height));
console.log(w,zoom,'tabs',total,'entirely-hidden-by-announcement',hidden,'partial',partial,'announcement height px',annH);
// Process via global button when two subs have work
await p.close();}
const p=await b.newPage();await p.goto('http://127.0.0.1:8876/subscriptions.html');await p.locator('#streams .stream').first().waitFor();
await p.getByRole('button',{name:'Subscribe to quotes',exact:true}).click();await p.getByRole('button',{name:'Subscribe to ops',exact:true}).click();
await p.getByRole('button',{name:'Subscribe to ops',exact:true}).click();console.log('second subscribe ops ann:',await p.locator('#announcement').textContent());
await p.locator('#tick').click();await p.locator('#tick').click();console.log('inbox',JSON.stringify(await p.locator('#inbox').innerText()));
// expire then try recovering: only Reset
await p.locator('#stale').click();console.log('expired buttons:',await p.locator('.subscription button').allTextContents());
await p.locator('.subscription').first().getByRole('button',{name:'Unsubscribe'}).click();console.log('unsub while expired ann:',await p.locator('#announcement').textContent(),'|',await p.locator('.subscription h3').allTextContents());
await b.close();})();
