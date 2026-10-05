(function(){
  'use strict';
  const C=ExpressDemo, $=id=>document.getElementById(id);
  let state=C.initial(), feeds=[], fixtures=[], store=null, revision=0, authority='unknown', busy=false, undo=null, ready=false;
  const selected=new Set(), rowNodes=new Map(), channel=typeof BroadcastChannel==='function'?new BroadcastChannel('midnight-express-demo'):null;
  const node=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
  const button=(text,run)=>{const b=node('button',text);b.type='button';b.onclick=run;return b;};
  const announce=text=>{$('announcement').textContent=text;};
  const presentation=()=>state.meta.presentation;
  const active=w=>w && w.requested!=='closed';
  const requireAuthority=()=>{if(authority!=='granted')throw Error('Check the simulation before delivery or processing. This does not check production authority.');};
  async function change(action,message,regions='all',needsAuthority=false){
    if(!ready || busy){announce(busy?'Wait for the saved operation to finish.':'Saved state is unavailable. Open Manage data to reload; unreadable storage can be removed through browser site-data controls.');return false;}
    busy=true;
    const focused=document.activeElement, previewFocused=focused?.closest('#preview'), receiptId=focused?.closest('[data-receipt-id]')?.dataset.receiptId, actionIndex=receiptId?[...focused.parentElement.children].indexOf(focused):-1;
    try{
      const after=C.copy(state);action(after);C.validate(after,feeds);
      const next=await store.commit(state,after,revision,()=>{if(needsAuthority)requireAuthority();});state=after;revision=next;
      channel?.postMessage({revision});render(regions);if(receiptId){const row=[...document.querySelectorAll('[data-receipt-id]')].find(n=>n.dataset.receiptId===receiptId);const controls=row?.querySelector('.controls');(controls?.children[Math.min(actionIndex,controls.children.length-1)])?.focus({preventScroll:true});}if(previewFocused&&!document.contains(focused))$('preview-heading')?.focus({preventScroll:true});if(message)announce(message);return true;
    }catch(error){announce(`${error.message} No new progress was committed.`);return false;}finally{busy=false;}
  }
  async function restore(){
    ready=false;authority='unknown';clearTimeout(queryTimer);
    try{
      if(!store)store=await ExpressStore.open(message=>{ready=false;$('storage-status').textContent=message;});
      const saved=await store.read();state=saved.state?C.validate(saved.state,feeds):C.initial();revision=saved.revision;
      ready=true;selected.clear();rowNodes.clear();$('feeds').replaceChildren();undo=null;
      $('storage-status').textContent=saved.state?'Saved synthetic demo restored. Check the simulation before resuming delivery.':'Synthetic changes are saved on this browser. Delivery starts unchecked.';
      syncInputs();render();
    }catch(error){$('storage-status').textContent=`Saved demo unavailable: ${error.message} Writes are blocked. Browser site-data controls can remove an unreadable database; that also removes saved history.`;announce('Saved data could not be trusted. No delivery resumed.');}
  }
  function syncInputs(){const p=presentation();for(const id of ['search','category','evidence','following','folder','inbox-search'])$(id).value=p[{search:'query','inbox-search':'inboxQuery'}[id]||id]??'all';}
  function filtered(){
    const p=presentation(),tokens=p.query.toLowerCase().trim().split(/\s+/).filter(Boolean);
    return feeds.filter(f=>{const w=state.watches[f.id];return (p.view!=='mine'||active(w)) && (p.category==='all'||p.category===f.category) && (p.evidence==='all'||p.evidence===f.evidence) && (p.following==='all'||(p.following==='yes'&&active(w))||(p.following==='no'&&!active(w))||(p.following==='pinned'&&active(w)&&w.pinned)) && (p.view!=='mine'||p.folder==='all'||w?.folder===p.folder) && tokens.every(t=>`${f.name} ${f.description} ${f.source} ${f.publisher} ${f.category} ${f.profile}`.toLowerCase().includes(t));});
  }
  function view(name){change(s=>{s.meta.presentation.view=name;s.meta.presentation.page=0;},null,'all');}
  function render(regions='all'){
    const p=presentation();
    for(const b of document.querySelectorAll('[data-view]')){if(b.dataset.view===p.view)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');}
    $('catalog-pane').hidden=!['directory','mine'].includes(p.view);$('inbox-pane').hidden=p.view!=='inbox';$('tools-pane').hidden=p.view!=='tools';
    $('view-heading').textContent=p.view==='mine'?'My feeds':'Directory';
    if(regions==='all'||regions==='catalog'){renderCatalog();renderPreview();renderFolders();}
    if(regions==='results')renderCatalog();
    if(regions==='all'||regions==='inbox')renderInbox();
    if(regions==='all'||regions==='tools')renderTools();
    $('permission').textContent=`Current simulation authority: ${authority}. No current wallet or production grant is inferred.`;
  }
  function renderCatalog(){
    const results=filtered(),p=presentation(),max=Math.max(0,Math.ceil(results.length/50)-1),page=Math.min(max,p.page||0),start=page*50,visible=results.slice(start,start+50),ids=new Set(visible.map(f=>f.id));
    for(const id of selected)if(!ids.has(id))selected.delete(id);
    for(const [id,n] of rowNodes)if(!ids.has(id)){n.remove();rowNodes.delete(id);}
    for(const f of visible){
      let row=rowNodes.get(f.id);
      if(!row){
        row=node('li',undefined,'feed-row');row.dataset.feedId=f.id;
        const select=node('input');select.type='checkbox';select.setAttribute('aria-label',`Select ${f.name} for organization`);select.onchange=()=>{select.checked?selected.add(f.id):selected.delete(f.id);};
        const text=node('div'),open=button(f.name,()=>openPreview(f.id));open.className='feed-open';text.append(open,node('p',f.description),node('p',f.source,'source'),node('p',`${f.category} · ${f.evidence}`));
        const follow=button('Follow',()=>quickFollow(f));follow.className='follow';row.append(select,text,follow);rowNodes.set(f.id,row);
      }
      const w=state.watches[f.id],follow=row.querySelector('.follow');follow.textContent=active(w)?(w.requested==='paused'?'Paused · configure':'Following · configure'):'Follow';
      follow.onclick=()=>active(w)?openPreview(f.id):quickFollow(f);
      const checkbox=row.querySelector('input');checkbox.checked=selected.has(f.id);checkbox.disabled=!active(w);
      // Append only if its current position differs; preserve focus for changed rows.
      const position=visible.indexOf(f);
      if($('feeds').children[position]!==row)$('feeds').insertBefore(row,$('feeds').children[position]||null);
    }
    $('result-count').textContent=`${results.length} feeds · ${selected.size} selected on this page`;
    $('page-range').textContent=results.length?`${start+1}–${start+visible.length} of ${results.length}`:'No results';
    $('previous').disabled=page===0;$('next').disabled=page===max;$('batch').hidden=p.view!=='mine';
    $('select-page').checked=visible.length>0&&visible.every(f=>selected.has(f.id));$('undo').disabled=!undo;
  }
  function folderSelect(value,id){const select=node('select');if(id)select.id=id;select.append(new Option('Unfiled',''));for(const [key,f] of Object.entries(state.folders))select.append(new Option(f.name,key));select.value=value||'';return select;}
  async function quickFollow(f){await change(s=>C.follow(s,f),'Following saved locally. Use Delivery tools to check the simulation and generate an example.','catalog');}
  let returnScroll=0;
  function openPreview(id){returnScroll=scrollY;change(s=>{s.meta.presentation.selected=id;},null,'catalog').then(ok=>{if(ok&&matchMedia('(max-width:700px)').matches){$('preview').scrollIntoView();$('preview-heading').focus();}});}
  function renderPreview(){
    const p=presentation(),f=feeds.find(f=>f.id===p.selected),box=$('preview');box.hidden=!f||!['directory','mine'].includes(p.view);document.querySelector('.workspace').classList.toggle('preview-open',!box.hidden);
    if(box.hidden)return;
    box.replaceChildren();const back=button('Back to results',()=>change(s=>{s.meta.presentation.selected=null;},null,'catalog').then(()=>{rowNodes.get(f.id)?.querySelector('.feed-open').focus({preventScroll:true});scrollTo({top:returnScroll,behavior:'instant'});}));back.className='mobile-back';box.append(back);
    const heading=node('h2',f.name);heading.id='preview-heading';heading.tabIndex=-1;box.append(heading,node('p',f.description),node('h3','About this feed'),node('p',`Declared source: ${f.source}`),node('p',`Profile: ${f.profile}. Evidence: ${f.evidence}.`),node('p','Source labels describe the demo binding; they do not authenticate a publisher. Folder and feed names are local organization, never relay topics.'));
    const w=state.watches[f.id],controls=node('div',undefined,'controls'),folder=folderSelect(w?.folder,'preview-folder'),label=node('label','Folder');label.append(folder);controls.append(label);
    const predicate=node('select');predicate.id='preview-predicate';predicate.append(new Option('All matching events','all'));if(f.category==='payments')predicate.append(new Option('Source-asserted Final only','payment-final'));predicate.value=w?.predicate||'all';const pl=node('label','Local predicate');pl.append(predicate);controls.append(pl);
    if(!active(w)){
      controls.append(button('Follow in demo',()=>change(s=>{C.follow(s,f,predicate.value,folder.value);},'Follow saved. Delivery begins only after an explicit simulation check.','catalog')));
      box.append(node('p','Starts after the current demo journal position. Previously disclosed examples are not replayed as new work.'));
    }else{
      controls.append(button('Save scope and folder',()=>{
        if(predicate.value!==w.predicate){try{requireAuthority();}catch(e){announce(e.message);return;}if(w.inFlight.length||w.queue.length){announce('Resolve pending work before revising scope.');return;}}
        change(s=>{const watch=s.watches[f.id];watch.folder=folder.value;if(watch.predicate!==predicate.value){watch.predicate=predicate.value;watch.revision++;watch.start={mode:'after',cursor:`cursor:demo/${s.meta.runtime.cursor}`} ;watch.scheduled=watch.delivered=watch.processed=s.meta.runtime.cursor;watch.history.push(C.intent(watch,f));}},'Configuration saved.','catalog',predicate.value!==w.predicate);
      }));
      controls.append(button(w.requested==='paused'?'Resume delivery':'Pause delivery',()=>{
        if(w.requested==='paused'){try{requireAuthority();}catch(e){announce(e.message);return;}}
        change(s=>{C.revise(s,f,w.requested==='paused'?'active':'paused');if(authority==='granted')C.pump(s,feeds);},'Requested state saved.','all',w.requested==='paused');
      }),button(w.pinned?'Unpin':'Pin',()=>change(s=>{s.watches[f.id].pinned=!s.watches[f.id].pinned;},'Organization saved.','catalog')),button('Unfollow',()=>change(s=>C.revise(s,f,'closed'),'Feed closed. Outstanding disclosures remain historical.','all')),button('Open inbox',()=>view('inbox')));
      box.append(node('p',`Requested: ${w.requested}. Coverage: ${w.coverage}. Authority: ${authority}.`));
    }
    box.append(controls,node('h3','Examples'));
    if(f.examples.length){for(const r of f.examples){box.append(node('p',summary(r)));const d=node('details');d.append(node('summary','Original offline example'),node('pre',JSON.stringify(r,null,2)));box.append(d);}}
    else box.append(node('p',`${f.name} emits a synthetic notice with source ${f.source}. It has no business wire or validator receipt.`));
    if(w){const d=node('details');d.append(node('summary','Delivery details and intent revisions'),node('pre',JSON.stringify({intent:C.intent(w,f),history:w.history,delivered:w.delivered,processed:w.processed,scheduled:w.scheduled,queue:w.queue,inFlight:w.inFlight},null,2)));box.append(d);}
  }
  function summary(r){
    if(r.category==='payments')return r.event?.data?.status==='Final'?'Final asserted by the source. This observation proves neither invoice settlement nor an executed payment.':`Payment status observed: ${r.event?.data?.status || 'unknown'}. No payment is executed here.`;
    return r.title || r.mock?.message || 'Synthetic observation';
  }
  function renderInbox(){
    if(presentation().view!=='inbox')return;
    const box=$('inbox');box.replaceChildren();const tokens=presentation().inboxQuery.toLowerCase().split(/\s+/).filter(Boolean);
    const records=Object.values(state.receipts).filter(r=>tokens.every(t=>`${summary(r.record)} ${r.feedId}`.toLowerCase().includes(t))).sort((a,b)=>b.cursor-a.cursor).slice(0,100);
    if(!records.length)box.append(node('p','No disclosed items match. Follow a feed, check the simulation and simulate source intake in Delivery tools.'));
    else box.append(node('p',`Showing ${records.length} most recent matching receipts. Search covers disclosed summaries and feed identities.`));
    for(const r of records){const item=node('article',undefined,'receipt');item.dataset.receiptId=r.id;item.append(node('h3',summary(r.record)),node('p',`${r.feedId} · ${r.read?'Read':'Unread'} · ${r.saved?'Saved · ':''}${r.disposition} · historical synthetic disclosure`));
      const controls=node('div',undefined,'controls');controls.append(button(r.read?'Mark unread':'Mark read',()=>change(s=>{s.receipts[r.id].read=!s.receipts[r.id].read;},'Reading marker saved. Processing is unchanged.','inbox')),button(r.saved?'Unsave':'Save',()=>change(s=>{s.receipts[r.id].saved=!s.receipts[r.id].saved;},'Reading marker saved.','inbox')));
      if(['awaiting-review','awaiting-local-review','content-conflict'].includes(r.disposition))for(const [text,value] of [['Record review','reviewed'],['Quarantine','quarantined']])controls.append(button(text,()=>{try{requireAuthority();}catch(e){announce(e.message);return;}change(s=>C.decide(s,feeds,r.id,value),'Receipt-specific disposition saved with its contiguous processing position. No effect authorized.','all',true);}));
      item.append(controls);const d=node('details');d.append(node('summary','Receipt evidence and original record'),node('pre',JSON.stringify(r,null,2)));item.append(d);box.append(item);
    }
  }
  function renderTools(){
    if(presentation().view!=='tools')return;const box=$('delivery');box.replaceChildren();
    const watches=Object.values(state.watches);box.append(node('p',`Fixed simulation context clock: 2026-10-04T12:00:00.000Z. Offline quotes and approvals are historical and authorize no action. Whole journal: ${state.meta.runtime.cursor} positions. Aggregate demo bounds: ${C.MAX_JOURNAL} journal entries and ${C.MAX_RECEIPTS} receipts. Intake is independent of following.`));
    if(!watches.length)box.append(node('p','No followed feeds yet. Directory is available without a wallet.'));
    for(const w of watches){const f=feeds.find(f=>f.id===w.id),row=node('article',undefined,'delivery-row');row.append(node('h3',f.name),node('p',`Requested ${w.requested} · authority ${authority} · coverage ${w.coverage}`),node('p',`Delivered position ${w.delivered} · processed position ${w.processed} · ${w.inFlight.length} pending decisions · ${w.queue.length} queued`));
      if(w.coverage==='behind')row.append(node('p','Matching work is retained. Queue credits are full; record pending dispositions, then recover retained work.'),button('Recover retained work',()=>{try{requireAuthority();}catch(e){announce(e.message);return;}change(s=>C.pump(s,feeds),'Retained work checked. Requested pauses are preserved.','all',true);}));
      if(w.coverage==='lost')row.append(node('p','The simulated interval is unavailable. Accepting a new start is explicit and requires no undecided work.'),button('Accept a new start after unavailable interval',()=>{try{requireAuthority();}catch(e){announce(e.message);return;}change(s=>C.acceptStart(s,f),'New start revision recorded; requested pause preserved.','all',true);}));
      box.append(row);
    }
  }
  function renderFolders(){
    for(const id of ['folder','batch-folder']){const select=$(id),value=id==='folder'?presentation().folder:select.value;select.replaceChildren();if(id==='folder')select.append(new Option('All folders','all'));select.append(new Option('Unfiled',''));for(const [key,f] of Object.entries(state.folders))select.append(new Option(f.name,key));select.value=value;}
    const saved=$('saved-view'),value=saved.value;saved.replaceChildren(new Option('Choose a view',''));for(const [key,v] of Object.entries(state.views))saved.append(new Option(v.name,key));saved.value=value;
    const box=$('folder-list');box.replaceChildren();for(const [id,f] of Object.entries(state.folders)){const row=node('div',undefined,'folder-row'),input=node('input');input.value=f.name;input.maxLength=60;input.setAttribute('aria-label',`Rename folder ${f.name}`);row.append(input,button('Rename',()=>change(s=>{if(!input.value.trim())throw Error('A folder needs a name.');s.folders[id].name=input.value.trim();},'Folder renamed.','catalog')),button('Delete folder',()=>change(s=>{delete s.folders[id];for(const w of Object.values(s.watches))if(w.folder===id)w.folder='';if(s.meta.presentation.folder===id)s.meta.presentation.folder='all';},'Folder deleted. Feeds moved to Unfiled.','catalog')));box.append(row);}
  }
  for(const b of document.querySelectorAll('[data-view]'))b.onclick=()=>view(b.dataset.view);
  let queryTimer=null;
  for(const id of ['search','category','evidence','following','folder','inbox-search'])$(id).addEventListener(id.includes('search')?'input':'change',()=>{
    const key={search:'query','inbox-search':'inboxQuery'}[id]||id,value=$(id).value;
    const update=()=>{if(busy){queryTimer=setTimeout(update,30);return;}change(s=>{s.meta.presentation[key]=value;s.meta.presentation.page=0;},null,key==='inboxQuery'?'inbox':'results');};
    if(id.includes('search')){clearTimeout(queryTimer);queryTimer=setTimeout(update,120);}else update();
  });
  $('clear-search').onclick=()=>{clearTimeout(queryTimer);$('search').value='';change(s=>{s.meta.presentation.query='';s.meta.presentation.page=0;},null,'results');$('search').focus();};
  $('previous').onclick=()=>change(s=>{s.meta.presentation.page=Math.max(0,s.meta.presentation.page-1);},null,'catalog');
  $('next').onclick=()=>change(s=>{s.meta.presentation.page++;},null,'catalog');
  $('select-page').onchange=()=>{selected.clear();if($('select-page').checked)for(const [id] of rowNodes)if(active(state.watches[id]))selected.add(id);renderCatalog();};
  function organize(pinned){const ids=[...selected];if(!ids.length){announce('Select followed feeds on this page first.');return;}const old=ids.map(id=>({id,folder:state.watches[id].folder,pinned:state.watches[id].pinned}));change(s=>{for(const id of ids){if(pinned)s.watches[id].pinned=true;else s.watches[id].folder=$('batch-folder').value;}},`${ids.length} selected page feeds updated. Undo is available.`, 'catalog').then(ok=>{if(ok){undo=old;$('undo').disabled=false;}});}
  $('move').onclick=()=>organize(false);$('pin').onclick=()=>organize(true);$('undo').onclick=()=>{const old=undo;if(!old)return;change(s=>{for(const x of old)if(s.watches[x.id]){s.watches[x.id].folder=s.folders[x.folder]?x.folder:'';s.watches[x.id].pinned=x.pinned;}},'Organization restored.','catalog').then(ok=>{if(ok){undo=null;$('undo').disabled=true;}});};
  $('add-folder').onclick=()=>{const name=$('folder-name').value.trim();if(!name){announce('Enter a folder name.');return;}change(s=>{if(Object.keys(s.folders).length>=100)throw Error('Folder limit reached.');s.folders[crypto.randomUUID()]={name};},'Folder created.','catalog').then(ok=>{if(ok)$('folder-name').value='';});};
  $('save-view').onclick=()=>{const name=$('view-name').value.trim();if(!name){announce('Enter a saved view name.');return;}change(s=>{if(Object.keys(s.views).length>=100)throw Error('Saved view limit reached.');const {query,category,evidence,following,folder}=s.meta.presentation;s.views[crypto.randomUUID()]={name,query,category,evidence,following,folder};},'Saved view created. It changes no subscription.','catalog');};
  $('saved-view').onchange=()=>{const saved=state.views[$('saved-view').value];if(saved)change(s=>{Object.assign(s.meta.presentation,{...saved,page:0});},'Saved filters opened.','catalog').then(syncInputs);};
  $('check-simulation').onclick=()=>{authority='granted';change(s=>C.pump(s,feeds),'Fresh simulation check only. Requested pauses retained.','all',true).then(ok=>{if(!ok){authority='unknown';render('tools');}});};
  function simulate(action,message){try{requireAuthority();}catch(e){announce(e.message);return;}change(s=>{action(s);C.pump(s,feeds);},message,'all',true);}
  $('tick').onclick=()=>simulate(s=>C.intake(s,feeds,presentation().selected),'Whole-journal intake saved. Only matching local watches receive it.');
  $('duplicate').onclick=()=>simulate(s=>{const e=s.journal[s.meta.runtime.cursor];if(!e)throw Error('Simulate an occurrence first.');C.append(s,C.copy(e));},'Occurrence replay saved. Valid identical repeats are audit receipts, not new business information.');
  $('negative').onclick=()=>simulate(s=>{const r=fixtures.find(r=>r.validation==='offline-reference-rejected');if(!r)throw Error('No rejected reference available.');C.append(s,{category:r.category,source:r.event.source,occurrence:r.event.id,record:C.copy(r)});},'Offline rejected reference quarantined before identity checks.');
  $('gap').onclick=()=>simulate(s=>{for(const w of Object.values(s.watches))if(w.requested!=='closed')w.coverage='lost';},'Unavailable-interval simulation recorded. Queued work remains intact.');
  for(const [id,value] of [['stale','expired'],['revoke','revoked']])$(id).onclick=()=>{authority=value;render('tools');announce('Delivery and processing blocked until an explicit fresh simulation check. Historical reading remains available.');};
  $('reset').onclick=()=>change(s=>{const fresh=C.initial();s.watches=fresh.watches;s.receipts={};s.journal={};s.meta.runtime=fresh.meta.runtime;},'Simulation reset. Organization retained.').then(ok=>{if(ok){authority='unknown';render();}});
  $('clear-history').onclick=()=>change(s=>{s.receipts={};s.journal={};s.meta.runtime={cursor:0,sequence:0,schema:1};for(const w of Object.values(s.watches)){w.requested=w.requested==='closed'?'closed':'paused';w.revision++;w.queue=[];w.inFlight=[];w.seen={};w.decided=[];w.generationBoundary=0;w.scheduled=w.delivered=w.processed=0;w.coverage='continuous';w.start={mode:'latest',cursor:''};w.history.push(C.intent(w,feeds.find(f=>f.id===w.id)));}},'Saved synthetic history cleared. Open watches paused.').then(ok=>{if(ok){authority='unknown';render();}});
  $('forget').onclick=()=>change(s=>{s.folders={};s.views={};for(const w of Object.values(s.watches)){w.folder='';w.pinned=false;}s.meta.presentation.folder='all';},'Organization forgotten. Subscriptions retained.');
  $('reload-state').onclick=restore;
  $('export').onclick=()=>{const blob=new Blob([JSON.stringify({notice:'Synthetic historical demo only. No authenticated grant, wallet data or execution.',intents:Object.values(state.watches).map(w=>C.intent(w,feeds.find(f=>f.id===w.id))),state},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=node('a');a.href=url;a.download='midnight-express-synthetic-history.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
  channel && (channel.onmessage=event=>{if(event.data?.revision!==revision){authority='unknown';ready=false;$('storage-status').textContent='Another tab changed saved state. Open Manage data and reload saved state before editing or delivery.';render('tools');}});
  const wallet=MothReadOnlyConnector.create({networkId:'preprod'});
  $('origin-warning').textContent=`Origin: ${location.origin}. GitHub Pages projects on this origin share this grant boundary.`;
  $('wallet-ack').onchange=()=>{$('connect').disabled=!$('wallet-ack').checked;};
  $('discover').onclick=()=>{const found=wallet.discover();$('wallet-status').textContent=found.compatible?'Compatible Moth detected. Connect requires your explicit acknowledgment.':found.reason;};
  $('connect').onclick=()=>{if(!$('wallet-ack').checked)return;wallet.connect().catch(e=>{$('wallet-status').textContent=e.message;});};
  $('check-wallet').onclick=()=>wallet.checkStatus().catch(e=>{$('wallet-status').textContent=e.message;});
  $('disconnect').onclick=()=>wallet.disconnect();wallet.subscribe(s=>{$('wallet-status').textContent=`${s.status}${s.error?': '+s.error:''}. Local disconnect cannot revoke the origin grant; manage grants in Moth.`;});
  fetch('subscriptions-fixtures.json').then(r=>{if(!r.ok)throw Error('Reference fixtures could not be loaded.');return r.json();}).then(data=>{fixtures=data.records;feeds=C.catalog(fixtures);return restore();}).catch(e=>{announce(e.message);$('storage-status').textContent='Directory unavailable. Reload to retry.';});
})();
