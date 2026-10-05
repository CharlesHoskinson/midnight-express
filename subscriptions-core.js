/* Synthetic consumer model. No transport, authentication or execution. */
(function (root) {
  'use strict';
  const MAX_JOURNAL = 1024, MAX_RECEIPTS = 4096;
  function catalog(records) {
    const result = [];
    for (const category of ['quotes', 'payments', 'approvals']) {
      const examples = records.filter(r => r.category === category && r.validation === 'offline-reference-accepted');
      if (!examples.length) continue;
      const event = examples[0].event;
      result.push({id: category, name: {quotes:'Dealer quotes', payments:'Supplier payment observations', approvals:'Human approval observations'}[category], description: 'Historical business examples checked offline. Source identity and current authority are not verified here.', category, evidence:'Offline reference', source:event.source, publisher:'Reference fixture', profile:event.mpeprofile, contract:event.mpecontract, allowedRecords:records.filter(r=>r.category===category), examples});
    }
    for (const category of ['contracts', 'credentials', 'ops']) {
      for (let i = 1; i <= 200; i++) {
        const suffix = String(i).padStart(3, '0'), source = `urn:mpe:source:demo-${category}-${suffix}`;
        result.push({id:`${category}-${suffix}`, name:`${{contracts:'Contract renewals',credentials:'Credential notices',ops:'Service health'}[category]} · ${suffix}`, description:{contracts:'Synthetic renewal notices from one independently scoped contract service.',credentials:'Synthetic credential status notices from one independently scoped issuer.',ops:'Synthetic service health notices from one independently scoped monitor.'}[category], category, evidence:'Synthetic', source, publisher:`Demo ${category} source ${suffix}`, profile:'mock.local.v1', contract:'mock-only', examples:[]});
      }
    }
    return result.sort((a,b) => a.name.localeCompare(b.name));
  }
  const initial = () => ({watches:{}, receipts:{}, journal:{}, folders:{}, views:{}, meta:{runtime:{cursor:0, sequence:0, schema:1}, presentation:{view:'directory',query:'',category:'all',evidence:'all',following:'all',folder:'all',page:0,selected:null,inboxQuery:''}}});
  const copy = x => structuredClone(x);
  function intent(w, f) {
    return {kind:'LocalSubscriptionIntent',version:1,subscriptionId:`subscription:${w.id}`,revision:w.revision,owner:'principal:demo',shardHandle:'shard:demo-private',selector:{category:f.category,profile:f.profile,contract:f.contract,sourceEquals:[f.source],predicate:w.predicate},start:w.start,expiresAt:'2026-10-04T13:00:00.000Z',sink:{handle:'sink:local-inbox',maxInFlight:2,maxQueuedEvents:4,maxQueuedBytes:16384},requestedState:w.requested==='closed'?'unsubscribed':w.requested};
  }
  function follow(s, f, predicate='all', folder='') {
    if (s.watches[f.id] && s.watches[f.id].requested !== 'closed') return;
    if (!['all','payment-final'].includes(predicate) || (predicate === 'payment-final' && f.category !== 'payments')) throw Error('Unsupported predicate.');
    const old = s.watches[f.id];
    const w = {id:f.id,revision:(old?.revision || 0)+1,requested:'active',predicate,folder,pinned:false,coverage:'continuous',generationBoundary:s.meta.runtime.cursor,scheduled:s.meta.runtime.cursor,delivered:s.meta.runtime.cursor,processed:s.meta.runtime.cursor,queue:[],inFlight:[],seen:{},decided:[],start:{mode:'latest',cursor:''},history:old?.history || []};
    w.history.push(intent(w,f)); s.watches[f.id] = w;
  }
  function revise(s,f,requested) {
    const w=s.watches[f.id]; if (!w || w.requested==='closed') throw Error('Feed is not followed.');
    w.requested=requested; w.revision++; w.history.push(intent(w,f));
    if(requested==='closed') {
      for(const r of Object.values(s.receipts)) if(r.feedId===w.id && ['awaiting-review','awaiting-local-review','content-conflict'].includes(r.disposition)) r.disposition='historical-closed';
      w.queue=[]; w.inFlight=[];
    }
  }
  const matches = (w,f,entry) => entry.source === f.source && entry.category === f.category && (w.predicate !== 'payment-final' || entry.record.event?.data?.status === 'Final');
  function dispatch(s,w) {
    if(w.requested!=='active') return;
    while(w.queue.length && w.inFlight.length<2) {
      const cursor=w.queue.shift(), entry=s.journal[cursor];
      const id=`${w.id}:${cursor}`, valid=entry.record.validation !== 'offline-reference-rejected';
      const occurrence=entry.record.event ? `${entry.source}|${entry.record.event.id}` : entry.occurrence;
      const content=JSON.stringify(entry.record.event || entry.record.mock);
      let disposition=valid?(entry.record.event?'awaiting-review':'awaiting-local-review'):'quarantined';
      if(valid && w.seen[occurrence]) disposition=w.seen[occurrence]===content?'duplicate':'content-conflict';
      if(valid && !w.seen[occurrence]) w.seen[occurrence]=content;
      s.receipts[id]={id,feedId:w.id,cursor,revision:w.revision,disposition,read:false,saved:false,record:entry.record};
      w.delivered=Math.max(w.delivered,cursor);
      if(['awaiting-review','awaiting-local-review','content-conflict'].includes(disposition)) w.inFlight.push(cursor);
      else w.decided.push(cursor);
    }
  }
  function checkpoint(s,w,f) {
    let cursor=w.processed;
    while(cursor<w.scheduled) {
      const next=cursor+1, e=s.journal[next];
      if(!e || (matches(w,f,e) && !w.decided.includes(next))) break;
      cursor=next;
    }
    w.processed=cursor;
  }
  function pump(s,feeds) {
    const map=new Map(feeds.map(f=>[f.id,f]));
    for(const w of Object.values(s.watches)) {
      if(w.requested==='closed' || w.coverage==='lost') continue;
      const f=map.get(w.id); dispatch(s,w);
      for(let c=w.scheduled+1;c<=s.meta.runtime.cursor;c++) {
        const e=s.journal[c]; if(!e) {w.coverage='lost'; break;}
        if(matches(w,f,e)) {
          const bytes=w.queue.reduce((n,k)=>n+s.journal[k].bytes,0);
          if(w.queue.length>=4 || bytes+e.bytes>16384) {w.coverage='behind'; break;}
          w.queue.push(c);
        }
        w.scheduled=c; dispatch(s,w);
      }
      if(w.scheduled===s.meta.runtime.cursor) w.coverage='continuous';
      checkpoint(s,w,f);
    }
  }
  function append(s,entry) {
    if(Object.keys(s.journal).length>=MAX_JOURNAL || Object.keys(s.receipts).length + Object.keys(s.watches).length >= MAX_RECEIPTS) throw Error('Demo storage budget reached. Preserve or clear history before further intake.');
    entry.bytes=new TextEncoder().encode(JSON.stringify(entry.record)).length;
    s.journal[++s.meta.runtime.cursor]=entry;
  }
  function intake(s,feeds,selected) {
    s.meta.runtime.sequence++;
    const f=feeds.find(f=>f.id===selected) || feeds.find(f=>f.category==='ops');
    const record=f.examples.length ? copy(f.examples[(s.meta.runtime.sequence-1)%f.examples.length]) : {category:f.category,title:`${f.name}: notice ${s.meta.runtime.sequence}`,mode:'synthetic-local',validation:'mock-only',mock:{source:f.source,notice:s.meta.runtime.sequence,message:f.description}};
    append(s,{category:f.category,source:f.source,occurrence:`${f.source}|notice:${s.meta.runtime.sequence}`,record});
  }
  function decide(s,feeds,id,disposition) {
    const r=s.receipts[id],w=r && s.watches[r.feedId];
    if(!w || w.requested==='closed' || !['awaiting-review','awaiting-local-review','content-conflict'].includes(r.disposition)) throw Error('This receipt has no pending processing decision.');
    if(!['reviewed','quarantined'].includes(disposition)) throw Error('Unsupported decision.');
    r.disposition=disposition; w.inFlight=w.inFlight.filter(c=>c!==r.cursor); w.decided.push(r.cursor); pump(s,feeds);
  }
  function acceptStart(s,f) {
    const w=s.watches[f.id]; if(w.coverage!=='lost' || w.queue.length || w.inFlight.length) throw Error('Resolve outstanding work before accepting an unavailable interval.');
    w.start={mode:'after',cursor:`cursor:demo/${s.meta.runtime.cursor}`} ; w.revision++; w.history.push(intent(w,f));
    w.scheduled=w.delivered=w.processed=s.meta.runtime.cursor; w.coverage='continuous';
  }
  function validate(s,feeds) {
    const ids=new Set(feeds.map(f=>f.id)), byId=new Map(feeds.map(f=>[f.id,f]));
    for(const table of ['watches','receipts','journal','folders','views','meta']) if(!s[table] || typeof s[table]!=='object' || Array.isArray(s[table])) throw Error('Saved demo has an invalid table.');
    if(s.meta.runtime?.schema!==1) throw Error('Saved schema version is unsupported.');
    if(!Number.isSafeInteger(s.meta.runtime?.cursor) || s.meta.runtime.cursor<0 || s.meta.runtime.cursor>MAX_JOURNAL || !Number.isSafeInteger(s.meta.runtime.sequence)) throw Error('Saved journal is invalid.');
    if(Object.keys(s.journal).length!==s.meta.runtime.cursor || Object.keys(s.receipts).length>MAX_RECEIPTS || Object.keys(s.watches).length>feeds.length || Object.keys(s.folders).length>100 || Object.keys(s.views).length>100) throw Error('Saved demo exceeds its bounds.');
    for(let c=1;c<=s.meta.runtime.cursor;c++) if(!s.journal[c] || !Number.isInteger(s.journal[c].bytes) || s.journal[c].bytes<0 || s.journal[c].bytes>65536 || typeof s.journal[c].source!=='string') throw Error('Saved journal continuity is invalid.');
    for(const e of Object.values(s.journal)) {
      const f=feeds.find(f=>f.source===e.source && f.category===e.category);
      if(!f || !e.record || e.bytes!==new TextEncoder().encode(JSON.stringify(e.record)).length) throw Error('Saved record binding or size is invalid.');
      if(f.evidence==='Offline reference') {
        if(!f.allowedRecords.some(r=>JSON.stringify(r)===JSON.stringify(e.record))) throw Error('Saved offline record differs from its immutable reference.');
      } else if(e.record.event || e.record.wire || e.record.receipt || e.record.validation!=='mock-only' || e.record.mock?.source!==f.source || e.record.mode!=='synthetic-local' || typeof e.occurrence!=='string' || !e.occurrence.startsWith(f.source+'|notice:')) throw Error('Saved mock record is invalid.');
    }
    const p=s.meta.presentation;
    if(!p || !['all','quotes','payments','approvals','contracts','credentials','ops'].includes(p.category) || !['all','Synthetic','Offline reference'].includes(p.evidence) || !['all','yes','no','pinned'].includes(p.following) || !['directory','mine','inbox','tools'].includes(p.view) || typeof p.query!=='string' || p.query.length>1000 || typeof p.inboxQuery!=='string' || p.inboxQuery.length>1000 || !Number.isInteger(p.page) || p.page<0 || (p.selected!==null && !ids.has(p.selected))) throw Error('Saved view is invalid.');
    for(const v of [...Object.values(s.folders),...Object.values(s.views)]) if(typeof v.name!=='string' || !v.name.trim() || v.name.length>60) throw Error('Saved organization is invalid.');
    for(const [id,w] of Object.entries(s.watches)) {
      if(!ids.has(id) || w.id!==id || !['active','paused','closed'].includes(w.requested) || !['continuous','behind','lost'].includes(w.coverage) || !Number.isInteger(w.revision) || w.revision<1 || !['all','payment-final'].includes(w.predicate) || (w.predicate==='payment-final' && id!=='payments')) throw Error('Saved intent is invalid.');
      for(const key of ['scheduled','delivered','processed']) if(!Number.isInteger(w[key]) || w[key]<0 || w[key]>s.meta.runtime.cursor) throw Error('Saved position is invalid.');
      if(!Array.isArray(w.queue) || w.queue.length>4 || !Array.isArray(w.inFlight) || w.inFlight.length>2 || !Array.isArray(w.decided) || !Array.isArray(w.history) || !w.seen || typeof w.seen!=='object') throw Error('Saved watch limits are invalid.');
      if(w.history.length>2048 || typeof w.folder!=='string' || typeof w.pinned!=='boolean' || w.queue.reduce((n,c)=>n+(s.journal[c]?.bytes || 0),0)>16384 || w.processed>w.scheduled || w.delivered>w.scheduled) throw Error('Saved watch bounds are invalid.');
      for(const h of w.history) if(h.subscriptionId!==`subscription:${id}` || h.selector?.sourceEquals?.length!==1 || h.selector.sourceEquals[0]!==byId.get(id).source || h.owner!=='principal:demo' || h.shardHandle!=='shard:demo-private' || h.selector.category!==byId.get(id).category || h.selector.profile!==byId.get(id).profile || h.selector.contract!==byId.get(id).contract) throw Error('Saved binding no longer matches its descriptor.');
      if(!Number.isInteger(w.generationBoundary) || w.generationBoundary<0 || w.generationBoundary>s.meta.runtime.cursor) throw Error('Saved watch generation is invalid.');
      if(new Set([...w.queue,...w.inFlight]).size!==w.queue.length+w.inFlight.length) throw Error('Saved work contains duplicate positions.');
      for(const c of [...w.queue,...w.inFlight]) if(c<=w.processed || c>w.scheduled || !matches(w,byId.get(id),s.journal[c])) throw Error('Saved pending work is inconsistent.');
      for(const c of w.inFlight) if(!['awaiting-review','awaiting-local-review','content-conflict'].includes(s.receipts[`${id}:${c}`]?.disposition)) throw Error('Saved pending disclosure is missing.');
      for(const c of [...w.queue,...w.inFlight,...w.decided]) if(!s.journal[c]) throw Error('Saved work references missing history.');
    }
    for(const [id,r] of Object.entries(s.receipts)) if(r.id!==id || !s.watches[r.feedId] || !s.journal[r.cursor] || !['awaiting-review','awaiting-local-review','content-conflict','reviewed','quarantined','duplicate','historical-closed'].includes(r.disposition) || !r.record || typeof r.read!=='boolean' || typeof r.saved!=='boolean') throw Error('Saved receipt is invalid.');
    for(const r of Object.values(s.receipts)) if(!Number.isInteger(r.revision) || r.revision<1 || r.revision>s.watches[r.feedId].revision || JSON.stringify(r.record)!==JSON.stringify(s.journal[r.cursor].record) || s.journal[r.cursor].source!==byId.get(r.feedId).source || s.journal[r.cursor].category!==byId.get(r.feedId).category) throw Error('Saved disclosure does not match its bound journal record.');
    return s;
  }
  const api={catalog,initial,copy,intent,follow,revise,pump,intake,append,decide,acceptStart,validate,MAX_JOURNAL,MAX_RECEIPTS};
  root.ExpressDemo=api; if(typeof module!=='undefined') module.exports=api;
})(globalThis);
