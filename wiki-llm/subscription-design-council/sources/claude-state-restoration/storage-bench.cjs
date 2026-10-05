const pw=require('/home/hoskinson/.local/share/mise/installs/npm-playwright/1.63.0/node_modules/playwright');
(async()=>{const b=await pw.chromium.launch({headless:true,executablePath:'/home/hoskinson/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'});
const ctx=await b.newContext();const p=await ctx.newPage();await p.goto('http://127.0.0.1:8876/subscriptions.html');
const r=await p.evaluate(async()=>{
 const req=(r)=>new Promise((ok,no)=>{r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error);});
 const done=t=>new Promise((ok,no)=>{t.oncomplete=ok;t.onerror=()=>no(t.error);t.onabort=()=>no(t.error);});
 const open=()=>new Promise((ok,no)=>{const o=indexedDB.open('bench-mpe-ui',1);o.onupgradeneeded=()=>{const d=o.result;d.createObjectStore('meta');d.createObjectStore('follows',{keyPath:'feedKey'});const rm=d.createObjectStore('readMarks',{keyPath:['feedKey','occurrenceKey']});rm.createIndex('byFeed','feedKey');d.createObjectStore('folders',{keyPath:'id'});};o.onsuccess=()=>ok(o.result);o.onerror=()=>no(o.error);});
 let db=await open();const out={};
 // write 600 follows, 40 folders, 20000 read marks
 let t0=performance.now();let tx=db.transaction(['follows','folders','readMarks','meta'],'readwrite',{durability:'relaxed'});
 for(let i=0;i<600;i++)tx.objectStore('follows').put({feedKey:`demo:${['quotes','payments','approvals','contracts','credentials','ops'][i%6]}:${String(i).padStart(4,'0')}`,folderId:`f${i%40}`,muted:i%17===0,followedAt:'2026-10-04T12:00:00.000Z',labelOverride:null});
 for(let i=0;i<40;i++)tx.objectStore('folders').put({id:`f${i}`,name:`Folder ${i}`,order:i});
 for(let i=0;i<20000;i++)tx.objectStore('readMarks').put({feedKey:`demo:quotes:${String(i%600).padStart(4,'0')}`,occurrenceKey:`occ:${i}`,state:'read',at:'2026-10-04T12:00:00.000Z'});
 tx.objectStore('meta').put({schemaVersion:1,writtenAt:1},'header');await done(tx);out.writeAllMs=+(performance.now()-t0).toFixed(1);
 db.close();
 t0=performance.now();db=await open();out.openMs=+(performance.now()-t0).toFixed(1);
 t0=performance.now();tx=db.transaction(['follows','folders','meta'],'readonly');const [f,fo,m]=await Promise.all([req(tx.objectStore('follows').getAll()),req(tx.objectStore('folders').getAll()),req(tx.objectStore('meta').get('header'))]);out.restoreFollowsFoldersMs=+(performance.now()-t0).toFixed(1);out.follows=f.length;
 t0=performance.now();tx=db.transaction('readMarks','readonly');const cnt=await req(tx.objectStore('readMarks').index('byFeed').count(IDBKeyRange.only('demo:quotes:0007')));out.readCountOneFeedMs=+(performance.now()-t0).toFixed(1);out.cnt=cnt;
 t0=performance.now();tx=db.transaction('readMarks','readonly');const all=await req(tx.objectStore('readMarks').getAllKeys());out.allReadKeysMs=+(performance.now()-t0).toFixed(1);out.allKeys=all.length;
 // single toggle write latency
 t0=performance.now();tx=db.transaction('readMarks','readwrite',{durability:'relaxed'});tx.objectStore('readMarks').put({feedKey:'demo:quotes:0001',occurrenceKey:'occ:x',state:'read',at:'x'});await done(tx);out.singleMarkWriteMs=+(performance.now()-t0).toFixed(1);
 // search 600 titles in memory
 const titles=f.map(x=>x.feedKey+' synthetic quote payment approval feed description words');t0=performance.now();for(let k=0;k<100;k++)titles.filter(s=>s.includes('0420')||s.includes('approv'));out.search600x100Ms=+(performance.now()-t0).toFixed(1);
 // localStorage quota probe
 const blob='x'.repeat(1024*1024);let n=0;try{for(;n<12;n++)localStorage.setItem('bench'+n,blob);}catch(e){out.lsError=e.name;}out.lsMiBBeforeError=n;for(let k=0;k<12;k++)localStorage.removeItem('bench'+k);
 db.close();await new Promise(ok=>{const d=indexedDB.deleteDatabase('bench-mpe-ui');d.onsuccess=d.onerror=d.onblocked=ok;});
 out.locks='locks' in navigator;out.bc=typeof BroadcastChannel;out.persistedApi=typeof navigator.storage.persist;
 return out;});
// render 600 rows DOM cost
const rr=await p.evaluate(()=>{const host=document.createElement('div');document.body.append(host);const t0=performance.now();const frag=document.createDocumentFragment();for(let i=0;i<600;i++){const a=document.createElement('article');a.innerHTML=`<h3>Feed ${i}</h3><p>desc</p><button>Follow</button><button>Inspect</button>`;frag.append(a);}host.append(frag);void host.offsetHeight;return {render600Ms:+(performance.now()-t0).toFixed(1),nodes:document.querySelectorAll('*').length};});
console.log(JSON.stringify({...r,...rr,ua:await p.evaluate(()=>navigator.userAgent)}));await b.close();})().catch(e=>{console.error(e);process.exit(1)});
