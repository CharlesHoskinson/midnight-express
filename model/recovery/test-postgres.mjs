import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';import {readFileSync,writeFileSync,mkdtempSync,rmSync} from 'node:fs';import {tmpdir} from 'node:os';import {resolve} from 'node:path';import {spawnSync} from 'node:child_process';import {connect} from './umbradb-host.mjs';
const root=resolve('model'),python=process.env.MPE_PYTHON||'/tmp/mpe-data-model-validation-env/bin/python';
const event=JSON.parse(readFileSync(root+'/examples/agent.json')),context=JSON.parse(readFileSync(root+'/conformance/trusted-context.json'));
function authorization(c){return async(e)=>{let dir=mkdtempSync(tmpdir()+'/mpe-authority-');try{writeFileSync(dir+'/event.json',JSON.stringify(e));writeFileSync(dir+'/context.json',JSON.stringify(c));let p=spawnSync(python,[root+'/validator.py',dir+'/event.json','--context',dir+'/context.json'],{encoding:'utf8'});if(p.status!==0)throw Error('reference authorization refused');return {...JSON.parse(p.stdout),fixtureTrust:c.fixtureTrust,maxSteps:c.maxSteps};}finally{rmSync(dir,{recursive:true,force:true})}};}
const scoped=(scope,e=event,c=context)=>{let input=structuredClone(e),authority=structuredClone(c);input.data.executionScope='scope:'+scope.toLowerCase();authority.executionScope=input.data.executionScope;return {input,authorize:authorization(authority),scope:input.data.executionScope};};
const schema=process.env.MPE_TEST_SCHEMA||'mpe_format_'+process.pid;
const {sql,host}=await connect(schema);
if(process.argv[2]==='worker'){
 const q=scoped(process.argv[3]);await host.commit(q.input,q.authorize,{scope:q.scope,phase:process.argv[4]});await sql.end();process.exit(0);
}
if(process.argv[2]==='remote-worker'){
 const q=scoped(process.argv[3]),key=event.data.authorityDomain+'|'+event.data.actionId;
 await host.stageDispatch(q.scope,key);
 const remote={idempotencyKey:key,requestDigest:(await host.kv.get('mpe-actions',q.scope,key)).value.intent,resultDigest:'sha256:'+'4'.repeat(64)};
 await host.tx.withTransaction(tx=>host.kv.put('mpe-destination-fixture',q.scope,key,remote,{tx,expectedVersion:0n}));
 process.kill(process.pid,'SIGKILL');
}
let checks=0;const check=x=>{assert.ok(x);checks++};
try{
 const key=event.data.authorityDomain+'|'+event.data.actionId;
 for(const phase of ['afterEffect','beforeCommit','afterCommit']){
  const label='crash-'+phase;const q=scoped(label);const scope=q.scope;
  const child=spawnSync(process.execPath,[import.meta.filename,'worker',label,phase],{env:{...process.env,MPE_TEST_SCHEMA:schema},encoding:'utf8',timeout:30000});assert.equal(child.signal,'SIGKILL',child.stderr);checks++;
  const committed=phase==='afterCommit';
  for(const ns of ['mpe-inbox','mpe-actions','mpe-reports','mpe-outbox']){
   const k=ns==='mpe-inbox'?q.input.source+'|'+q.input.id:key;check(Boolean(await host.kv.get(ns,scope,k))===committed);
  }
  check(Boolean(await host.watermarks.get('mpe-cursor',scope))===committed);
  check(Boolean(await host.kv.get('mpe-budgets',scope,event.data.authorityDomain+'|'+event.data.human+'|'+event.data.budgetWindow))===committed);
  if(committed)check(Boolean(await host.checkpoints.load(scope,'mpe-fixture')));else{await assert.rejects(()=>host.checkpoints.load(scope,'mpe-fixture'));checks++;}
  const retried=await host.commit(q.input,q.authorize,{scope});check(retried.status===(committed?'duplicate-event':'sandbox-report-committed'));
  const action=await host.kv.get('mpe-actions',scope,key);check(action.version===1n);
  const budget=await host.kv.get('mpe-budgets',scope,event.data.authorityDomain+'|'+event.data.human+'|'+event.data.budgetWindow);check(budget.value.spent===1);
 }
 let q=scoped('replay'),scope=q.scope;check((await host.commit(q.input,q.authorize,{scope})).executes===true);
 const replay=structuredClone(q.input);replay.id='event:second-occurrence';check((await host.commit(replay,q.authorize,{scope,cursor:'2'})).status==='duplicate-action');check((await host.watermarks.get('mpe-cursor',scope)).cursor==='2');check((await host.commit(replay,q.authorize,{scope})).status==='duplicate-event');replay.time='2026-10-04T10:59:59.000Z';await assert.rejects(()=>host.commit(replay,q.authorize,{scope}),/event-identity-conflict/);checks++;
 const revoked=structuredClone(context);revoked.revokedActions=['action:demo'];await assert.rejects(()=>host.commit(scoped('revoked',event,revoked).input,scoped('revoked',event,revoked).authorize,{scope:'scope:revoked'}));checks++;
 let called=0;const boundary=scoped('revoked-at-boundary');const fresh=boundary.authorize,deny=scoped('revoked-at-boundary',event,revoked).authorize;await assert.rejects(()=>host.commit(boundary.input,async e=>(++called===1?fresh(e):deny(e)),{scope:boundary.scope}));checks++;check(await host.kv.get('mpe-reports',boundary.scope,key)===null);
 const low=structuredClone(context);low.maxSteps=4;await assert.rejects(()=>host.commit(scoped('budget-denied',event,low).input,scoped('budget-denied',event,low).authorize,{scope:'scope:budget-denied'}));checks++;
 // Two actual workers race the same action; winner is a single version and Step.
 const r=scoped('race');const race=await Promise.all([host.commit(r.input,r.authorize,{scope:r.scope}),host.commit(r.input,r.authorize,{scope:r.scope})]);check(race.filter(x=>x.executes).length===1);check((await host.kv.get('mpe-actions','scope:race',key)).version===1n);
 const aggregate=scoped('aggregate');const cap=structuredClone(context);cap.executionScope=aggregate.scope;cap.maxSteps=5;
 await host.commit(aggregate.input,authorization(cap),{scope:aggregate.scope});
 const second=structuredClone(aggregate.input);second.id='event:second-action';second.data.actionId='action:second';cap.proposals['action:second']=structuredClone(second.data.proposal);
 await assert.rejects(()=>host.commit(second,authorization(cap),{scope:aggregate.scope}),/aggregate budget/);checks++;
 check(await host.kv.get('mpe-actions',aggregate.scope,event.data.authorityDomain+'|action:second')===null);
 check((await host.watermarks.get('mpe-cursor',aggregate.scope)).cursor==='1');
 const retarget=structuredClone(q.input),targetContext=structuredClone(context);targetContext.executionScope=q.scope;retarget.id='event:retarget';retarget.data.proposal.target='sandbox:reports/other';targetContext.proposals['action:demo']=retarget.data.proposal;targetContext.sandboxTargets.push(retarget.data.proposal.target);
 const canon=v=>v&&typeof v==='object'?'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canon(v[k])).join(',')+'}':JSON.stringify(v);
 retarget.data.proposalDigest='sha256:'+createHash('sha256').update(canon({domain:'mpe.model.proposal.v0.2',contract:retarget.mpecontract,proposal:retarget.data.proposal})).digest('hex');
 await assert.rejects(()=>host.commit(retarget,authorization(targetContext),{scope:q.scope}),/action-identity-conflict/);checks++;
 const wrongScope=scoped('scope-mismatch');await assert.rejects(()=>host.commit(wrongScope.input,wrongScope.authorize,{scope:'scope:other'}),/scope mismatch/);checks++;
 // Destination fixture commits on a separate transaction; worker dies before local acknowledgement.
 q=scoped('remote-crash');scope=q.scope;await host.commit(q.input,q.authorize,{scope});
 const killed=spawnSync(process.execPath,[import.meta.filename,'remote-worker','remote-crash'],{env:{...process.env,MPE_TEST_SCHEMA:schema},encoding:'utf8',timeout:30000});assert.equal(killed.signal,'SIGKILL',killed.stderr);checks++;
 check((await host.kv.get('mpe-outbox',scope,key)).value.state==='Dispatching');
 // Recovery exposes uncertainty and reconciles the original destination key.

 const remote={idempotencyKey:key,requestDigest:(await host.kv.get('mpe-actions',scope,key)).value.intent,resultDigest:'sha256:'+'4'.repeat(64)};
 await host.markUnknown(scope,key);await assert.rejects(()=>host.stageDispatch(scope,key),/unknown outcome/);checks++;
 check((await host.reconcile(scope,key,null)).status==='OutcomeUnknown');check((await host.reconcile(scope,key,(await host.kv.get('mpe-destination-fixture',scope,key)).value)).status==='reconciled');check((await host.kv.get('mpe-destination-fixture',scope,key)).version===1n);
 const state=await host.checkpoints.load('scope:crash-aftercommit','mpe-fixture');check(Boolean(state));
 const version=await sql`select version() as version`;const report={status:'real-postgres-fixture-sandbox',checks,postgres:version[0].version,umbraCheckout:process.env.UMBRA_COMMIT||'record externally',processKills:4,publicTransactionComposition:true,productionAuthentication:false,remoteService:'separate-transaction-fixture',effects:'database-report-rows-only'};writeFileSync(root+'/evidence/recovery-results.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
}finally{await sql.end();}
