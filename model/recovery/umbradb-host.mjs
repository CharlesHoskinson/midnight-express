/** One fixture-authorized sandbox operation. Public Umbra API only; no nested transactions.
 * This host is not a production authentication service or financial executor.
 */
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const library=process.env.UMBRA_DIST;
if(!library)throw Error('Set UMBRA_DIST to the built, reviewed Umbra checkout dist directory');
const U=await import(pathToFileURL(library+'/index.js').href);
export class SandboxHost {
 constructor(sql,schema){this.sql=sql;this.schema=schema;this.tx=new U.PgTransactionLeaseLayer(sql);this.kv=new U.PgTemporalKV(sql,schema);this.checkpoints=new U.PgCheckpointStore(sql,this.tx,schema);this.watermarks=new U.PgWatermarks(sql,schema);}
 async commit(event,authorize,{phase,scope=event.data.executionScope,cursor='1'}={}){
  event=structuredClone(event);
  if(scope!==event.data.executionScope)throw Error('execution scope mismatch');
  if(!/^(0|[1-9][0-9]*)$/.test(cursor))throw Error('cursor grammar');
  if(typeof authorize!=='function')throw Error('A trusted host authorization callback is mandatory');
  const domain=event.data.authorityDomain,action=event.data.actionId;
  if(event.data.proposal.environment!=='Sandbox'||event.data.proposal.operation!=='WriteReport')throw Error('Unsupported operation');
  const key=domain+'|'+action;const occurrence=event.source+'|'+event.id;
  const canonical=(v)=>v&&typeof v==='object'?(Array.isArray(v)?'['+v.map(canonical).join(',')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}'):JSON.stringify(v);
  const eventHash='sha256:'+createHash('sha256').update(canonical(event)).digest('hex');
  const verify=async()=>{const r=await authorize(event);if(r.status!=='sandbox-candidate-only'||r.executes!==false||r.fixtureTrust!=='trusted-test-fixture-only')throw Error('No current fixture capability');const expected='sha256:'+createHash('sha256').update(canonical({domain:'mpe.model.intent.v0.2',source:event.source,type:event.type,profile:event.mpeprofile,contract:event.mpecontract,data:event.data})).digest('hex');if(r.businessDigest!==expected)throw Error('capability intent mismatch');return r;};
  await verify();let result;
  // Bounded retries re-enter the complete policy/transaction boundary after a CAS conflict.
  for(let attempt=0;attempt<3;attempt++){
   try{result=await this.tx.withTransaction(async(tx)=>{
    const capability=await verify(),intent=capability.businessDigest;
    const oldOccurrence=await this.kv.get('mpe-inbox',scope,occurrence,{tx});
    if(oldOccurrence&&oldOccurrence.value.eventHash!==eventHash)throw Error('event-identity-conflict');
    const old=await this.kv.get('mpe-actions',scope,key,{tx});
    if(old&&old.value.intent!==intent)throw Error('action-identity-conflict');
    if(!oldOccurrence)await this.kv.put('mpe-inbox',scope,occurrence,{eventHash,action:key,contract:event.mpecontract},{tx,expectedVersion:0n});
    if(old){const before=await this.watermarks.get('mpe-cursor',scope,{tx});if(!before||BigInt(cursor)>BigInt(before.cursor))await this.watermarks.set('mpe-cursor',scope,{cursor,action:key,contract:event.mpecontract},{tx});return {status:oldOccurrence?'duplicate-event':'duplicate-action',executes:false,action:key};}
    const budgetKey=domain+'|'+event.data.human+'|'+event.data.budgetWindow;
    const previous=await this.kv.get('mpe-budgets',scope,budgetKey,{tx});const spent=previous?.value.spent||0;
    const reserve=Number(event.data.proposal.budget.coefficient);
    if(!Number.isSafeInteger(reserve)||reserve<1||spent+reserve>capability.maxSteps)throw Error('aggregate budget reservation refused');
    // Step = one atomic report-row write. Declared maximum is reserved; unused capacity released.
    await this.kv.put('mpe-reports',scope,key,{target:event.data.proposal.target,inputDigest:event.data.proposal.inputDigest,operation:'WriteReport'},{tx,expectedVersion:0n});
    if(phase==='afterEffect')process.kill(process.pid,'SIGKILL');
    await this.kv.put('mpe-budgets',scope,budgetKey,{spent:spent+1,chargedSteps:1,reservation:reserve,unusedReleased:reserve-1},{tx,expectedVersion:previous?.version||0n});
    await this.kv.put('mpe-actions',scope,key,{intent,contract:event.mpecontract,target:event.data.proposal.target,state:'Succeeded',chargedSteps:1},{tx,expectedVersion:0n});
    await this.kv.put('mpe-outbox',scope,key,{state:'Ready',requestDigest:intent,idempotencyKey:key},{tx,expectedVersion:0n});
    await this.checkpoints.save(scope,'mpe-fixture',Buffer.from(JSON.stringify({action:key,contract:event.mpecontract,intent})),{tx});
    await this.watermarks.set('mpe-cursor',scope,{cursor,action:key,contract:event.mpecontract},{tx});
    if(phase==='beforeCommit')process.kill(process.pid,'SIGKILL');
    return {status:'sandbox-report-committed',executes:true,action:key,chargedSteps:1,authority:'fixture-only'};
   });break;}catch(e){if(e.code!=='VERSION_CONFLICT'||attempt===2)throw e;}
  }
  if(phase==='afterCommit')process.kill(process.pid,'SIGKILL');
  return result;
 }
 async stageDispatch(scope,key){return this.tx.withTransaction(async(tx)=>{
  const o=await this.kv.get('mpe-outbox',scope,key,{tx});if(!o||o.value.state!=='Ready')throw Error('Dispatch needs Ready; unknown outcome requires reconciliation');
  return this.kv.put('mpe-outbox',scope,key,{...o.value,state:'Dispatching',attemptId:key+'|attempt:1'},{tx,expectedVersion:o.version});
 });}
 async markUnknown(scope,key){return this.tx.withTransaction(async(tx)=>{const o=await this.kv.get('mpe-outbox',scope,key,{tx});if(!o||!['Dispatching','OutcomeUnknown'].includes(o.value.state))throw Error('unknown transition');return this.kv.put('mpe-outbox',scope,key,{...o.value,state:'OutcomeUnknown'},{tx,expectedVersion:o.version});});}
 async reconcile(scope,key,destinationEvidence){return this.tx.withTransaction(async(tx)=>{const o=await this.kv.get('mpe-outbox',scope,key,{tx});if(!o||!['Dispatching','OutcomeUnknown'].includes(o.value.state))throw Error('reconcile state');if(!destinationEvidence)return {status:'OutcomeUnknown',executes:false};if(destinationEvidence.idempotencyKey!==key||destinationEvidence.requestDigest!==o.value.requestDigest)throw Error('destination evidence mismatch');await this.kv.put('mpe-outbox',scope,key,{...o.value,state:'Succeeded',resultDigest:destinationEvidence.resultDigest},{tx,expectedVersion:o.version});return {status:'reconciled',executes:false};});}
}
export async function connect(schema){const sql=U.createClient({connectionString:process.env.MPE_TEST_DATABASE_URL||'postgres://postgres@127.0.0.1:55437/postgres',schema,maxConnections:4});await U.runMigrations(sql,{schema});return {sql,host:new SandboxHost(sql,schema)};}
