const pw=require('/home/hoskinson/.local/share/mise/installs/npm-playwright/1.63.0/node_modules/playwright');
const out='/tmp/mpe-subscription-design-council/claude-operability/';
(async()=>{
 const b=await pw.chromium.launch({executablePath:'/home/hoskinson/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'});
 const p=await b.newPage({viewport:{width:1280,height:900}});const log=(...a)=>console.log(...a);
 await p.goto('http://127.0.0.1:8876/subscriptions.html');await p.locator('#streams .stream').first().waitFor();
 const ae=()=>p.evaluate(()=>{const a=document.activeElement;return a===document.body?'BODY':`${a.tagName}#${a.id}:${(a.textContent||'').slice(0,40)}`});
 // tab stops until first stream subscribe button
 let n=0;for(;n<80;n++){await p.keyboard.press('Tab');const t=await ae();if(t.includes('Subscribe to quotes'))break;}
 log('tab presses to first Subscribe:',n+1);
 await p.keyboard.press('Enter');log('focus after Enter on Subscribe:',await ae());
 log('announcement:',await p.locator('#announcement').textContent());
 // count total tab stops
 const stops=await p.evaluate(()=>document.querySelectorAll('a,button,input,select,summary').length);log('focusable elems:',stops);
 log('first viewport y of #streams, #subscriptions, #inbox:',await p.evaluate(()=>['streams','subscriptions','inbox'].map(i=>Math.round(document.getElementById(i).getBoundingClientRect().top+scrollY))));
 // keyboard: activate tick via focus + Enter
 await p.locator('#tick').focus();await p.keyboard.press('Enter');log('after tick focus:',await ae());
 await p.locator('#tick').focus();await p.keyboard.press('Enter');
 log('inbox:',await p.locator('#inbox').innerText());
 // inbox item button focus & enter
 await p.locator('#inbox button').first().focus();await p.keyboard.press('Enter');log('after inbox Enter focus:',await ae(),'detail open:',await p.evaluate(()=>document.querySelector('details').open));
 log('detail head:',(await p.locator('#detail').textContent()).slice(0,300));
 // pause via keyboard
 await p.locator('.subscription').getByRole('button',{name:'Pause'}).focus();await p.keyboard.press('Enter');log('after Pause focus:',await ae());
 // revoke then pause message
 await p.locator('#revoke').click();await p.locator('.subscription').getByRole('button',{name:/Pause|Resume/}).click();log('revoked+pause/resume msg:',await p.locator('#announcement').textContent());
 log('sub text revoked:',await p.locator('#subscriptions').innerText());
 // unsubscribed rendering
 await p.locator('#reset').click();await p.getByRole('button',{name:'Subscribe to payments',exact:true}).first().click();
 log('payments subscribe buttons:',await p.getByRole('button',{name:'Subscribe to payments',exact:true}).count());
 await p.getByRole('button',{name:'Subscribe to payments',exact:true}).nth(2).click();log('dup subscribe msg:',await p.locator('#announcement').textContent());
 await p.locator('#tick').click();await p.locator('#duplicate').click();log('inbox after dup:',await p.locator('#inbox').innerText());
 log('sub after dup:',await p.locator('#subscriptions').innerText());
 await p.locator('.subscription').getByRole('button',{name:'Unsubscribe'}).click();
 log('unsub row:',await p.locator('#subscriptions').innerText());
 log('unsub row buttons:',await p.locator('.subscription button').allTextContents());
 // backpressure gap labeling
 await p.locator('#reset').click();await p.getByRole('button',{name:'Subscribe to contracts',exact:true}).click();for(let i=0;i<7;i++)await p.locator('#tick').click();
 log('backpressure sub text:',await p.locator('#subscriptions').innerText());log('ann:',await p.locator('#announcement').textContent());
 await p.screenshot({path:out+'desktop-backpressure.png',fullPage:false});
 await p.locator('#subscriptions').scrollIntoViewIfNeeded();await p.screenshot({path:out+'desktop-subs.png'});
 // reload
 await p.reload();await p.locator('#streams .stream').first().waitFor();log('after reload subs:',await p.locator('#subscriptions').innerText(),'| inbox:',await p.locator('#inbox').innerText());
 // search for "invoice" / "bank"
 await p.fill('#search','bank');log('search bank results:',await p.locator('.stream').count());await p.fill('#search','invoice');log('search invoice:',await p.locator('.stream').count());await p.fill('#search','');
 // mobile
 const m=await b.newPage({viewport:{width:390,height:844}});await m.goto('http://127.0.0.1:8876/subscriptions.html');await m.locator('#streams .stream').first().waitFor();
 await m.screenshot({path:out+'mobile-first.png'});log('mobile #streams y:',await m.evaluate(()=>Math.round(document.getElementById('streams').getBoundingClientRect().top)),'inbox y',await m.evaluate(()=>Math.round(document.getElementById('inbox').getBoundingClientRect().top)), 'doc h',await m.evaluate(()=>document.documentElement.scrollHeight));
 await b.close();
})();
