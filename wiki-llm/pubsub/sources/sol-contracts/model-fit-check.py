import sys,json,copy,hashlib,datetime
from pathlib import Path
repo=Path('/home/hoskinson/Projects/midnight-express');sys.path.insert(0,str(repo/'model'))
from validator import Harness,Invalid,raw_json
ctxbytes=(repo/'model/conformance/trusted-context.json').read_bytes();ctx=raw_json(ctxbytes);rows=[]
def check(name,e,c=None,h=None,selector='all'):
 raw=e if isinstance(e,bytes) else json.dumps(e,separators=(',',':')).encode()
 try:
  result=(h or Harness(copy.deepcopy(c or ctx))).check(raw,eid='opaque-local-demo-eid')
  matched=selector=='all' or selector=='payment-final' and raw_json(raw)['data']['status']=='Final' or selector=='approval-report' and raw_json(raw)['data']['proposal']['operation']=='WriteReport'
  rows.append({'case':name,'validation':'accepted','result':result,'selector':selector,'localMatch':bool(matched),'inputSha256':hashlib.sha256(raw).hexdigest()})
 except Invalid as e:rows.append({'case':name,'validation':'rejected','reason':str(e),'selector':selector,'localMatch':False,'inputSha256':hashlib.sha256(raw).hexdigest()})
def fixture(name):return (repo/'model/examples'/name).read_bytes()
check('quote-exact-fixed-context',fixture('rfq.json'))
check('approval-exact-fixed-context',fixture('agent.json'),selector='approval-report')
for status in ['pending','final','reversed']:
 check('payment-'+status+'-base-context',fixture('invoice-'+status+'.json'),selector='payment-final')
 c=copy.deepcopy(ctx);e=raw_json(fixture('invoice-'+status+'.json'));c['paymentEvidence'][e['data']['paymentId']]=copy.deepcopy(e['data'])
 check('payment-'+status+'-supplied-matching-evidence',e,c,selector='payment-final')
h=Harness(copy.deepcopy(ctx));a=raw_json(fixture('agent.json'));check('approval-initial-ledger',a,h=h);check('approval-duplicate-occurrence',a,h=h);a['id']='event:replay';check('approval-new-occurrence-same-action',a,h=h);a['id']='event:conflict';a['data']['validFrom']='2026-10-04T11:30:00.000Z';check('approval-same-action-changed-content',a,h=h)
c=copy.deepcopy(ctx);c['revokedActions']=['action:demo'];check('approval-revoked',fixture('agent.json'),c)
c=copy.deepcopy(ctx);c['now']='2026-10-05T12:00:00.000Z';check('quote-expired-current-day',fixture('rfq.json'),c);check('approval-expired-current-day',fixture('agent.json'),c)
c=copy.deepcopy(ctx);c['sources']={};check('quote-no-source-authority',fixture('rfq.json'),c)
c=copy.deepcopy(ctx);c['paymentEvidence']={};check('payment-no-evidence',fixture('invoice-final.json'),c)
e=raw_json(fixture('rfq.json'));e['type']='mpe.contract.renewed.v0.2';check('new-contract-type-under-rfq-profile',e)
e=raw_json(fixture('rfq.json'));e['subscriptionId']='subscription:quotes';check('subscription-field-in-business-envelope',e)
report={'kind':'OfflineModelFitReport','generatedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'actual model.validator Harness.check; local selector evaluated only after success','trustedContext':'model/conformance/trusted-context.json','trustedContextSha256':hashlib.sha256(ctxbytes).hexdigest(),'trustedNow':ctx['now'],'sourceTrust':'supplied trusted-test-fixture-only; unsigned; no production authentication','paymentContextNote':'Matching-evidence cases explicitly replace paymentEvidence with complete event data as supplied fixture evidence; this is not deriving trusted evidence from a live sender. Base-context outcomes remain separately visible.','cases':rows,'allAcceptedExecutesFalse':all(r['result']['executes'] is False for r in rows if r['validation']=='accepted'),'limits':['No subscription runtime or wire validation','No browser validator','No live authority or payment execution','Selector matches never imply execution permission']}
(repo/'wiki-llm/pubsub/data-model-fit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'cases':len(rows),'accepted':sum(r['validation']=='accepted' for r in rows),'allAcceptedExecutesFalse':report['allAcceptedExecutesFalse'],'outcomes':[(r['case'],r['validation'],r.get('result',{}).get('status',r.get('reason'))) for r in rows]},indent=2))
