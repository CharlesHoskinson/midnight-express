'use strict';
const assert=require('node:assert/strict'),C=require('../dist/subscriptions-core.js'),fixtures=require('../dist/subscriptions-fixtures.json').records;
const feeds=C.catalog(fixtures),find=id=>feeds.find(f=>f.id===id);
assert.equal(feeds.length,603);assert.equal(new Set(feeds.map(f=>f.source)).size,603);
let s=C.initial();C.intake(s,feeds,'ops-001');assert.equal(s.meta.runtime.cursor,1,'intake independent of followers');
C.follow(s,find('ops-001'));C.follow(s,find('ops-002'));C.intake(s,feeds,'ops-001');C.pump(s,feeds);
assert.equal(s.watches['ops-001'].inFlight.length,1);assert.equal(s.watches['ops-002'].inFlight.length,0);
const first=Object.values(s.receipts)[0],processed=s.watches['ops-001'].processed;first.read=true;assert.equal(s.watches['ops-001'].processed,processed);
for(let i=0;i<8;i++)C.intake(s,feeds,'ops-001');C.pump(s,feeds);assert.equal(s.watches['ops-001'].coverage,'behind');assert.equal(s.watches['ops-001'].queue.length,4);assert.equal(s.watches['ops-001'].inFlight.length,2);
let pending=Object.values(s.receipts).filter(r=>r.disposition==='awaiting-local-review');C.decide(s,feeds,pending[1].id,'reviewed');assert.equal(s.watches['ops-001'].processed,processed,'out-of-order decision cannot advance across first pending');
C.revise(s,find('ops-001'),'paused');C.pump(s,feeds);assert.equal(s.watches['ops-001'].requested,'paused');
C.decide(s,feeds,first.id,'quarantined');assert.equal(s.watches['ops-001'].inFlight.length,1,'processing paused history does not dispatch');
C.revise(s,find('ops-001'),'active');C.pump(s,feeds);
while(s.watches['ops-001'].inFlight.length)C.decide(s,feeds,`ops-001:${s.watches['ops-001'].inFlight[0]}`,'reviewed');
assert.equal(s.watches['ops-001'].coverage,'continuous');assert.equal(s.watches['ops-001'].processed,s.meta.runtime.cursor);
C.append(s,C.copy(s.journal[s.meta.runtime.cursor]));C.pump(s,feeds);assert.equal(Object.values(s.receipts).at(-1).disposition,'duplicate');
C.revise(s,find('ops-001'),'paused');s.watches['ops-001'].coverage='lost';C.acceptStart(s,find('ops-001'));assert.equal(s.watches['ops-001'].requested,'paused');C.validate(s,feeds);
let q=C.initial();C.follow(q,find('quotes'));const bad=fixtures.find(r=>r.validation==='offline-reference-rejected'),good=find('quotes').examples[0];
for(const record of [bad,good]){C.append(q,{category:'quotes',source:record.event.source,occurrence:record.event.id,record});C.pump(q,feeds);}
assert.deepEqual(Object.values(q.receipts).map(r=>r.disposition),['quarantined','awaiting-review']);C.validate(q,feeds);
C.revise(q,find('quotes'),'closed');assert.equal(Object.values(q.receipts)[1].disposition,'historical-closed');
let big=C.initial();const mocks=feeds.filter(f=>f.evidence==='Synthetic');for(const f of mocks)C.follow(big,f);for(const f of mocks)C.intake(big,feeds,f.id);C.pump(big,feeds);C.validate(big,feeds);
assert.equal(Object.keys(big.receipts).length,600);assert.ok(Object.values(big.watches).every(w=>w.inFlight.length===1));for(const w of Object.values(big.watches)){const e=big.journal[w.inFlight[0]];assert.equal(e.source,find(w.id).source);}
const corrupt=C.copy(big);corrupt.watches['ops-001'].history[0].selector.sourceEquals=['urn:wrong'];assert.throws(()=>C.validate(corrupt,feeds),/binding/);


const wrong=C.copy(big);wrong.meta.runtime.schema=99;assert.throws(()=>C.validate(wrong,feeds),/schema/);
const badReceipt=C.copy(q);const altered=Object.values(badReceipt.receipts)[0].record;altered.title='X'+altered.title.slice(1);assert.throws(()=>C.validate(badReceipt,feeds),/immutable reference/);
const budget=C.initial();for(let i=0;i<C.MAX_JOURNAL;i++)C.intake(budget,feeds,'ops-001');assert.throws(()=>C.intake(budget,feeds,'ops-001'),/storage budget/);assert.equal(budget.meta.runtime.cursor,C.MAX_JOURNAL);

console.log('PASS: 603 independent scopes, 600 live mock watches, bounded backpressure, replay, rejected-before-dedup, receipt decisions, pause-preserving recovery and restore validation.');
