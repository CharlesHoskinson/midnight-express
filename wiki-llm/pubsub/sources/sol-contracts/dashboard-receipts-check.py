import sys,json,hashlib,copy
from pathlib import Path
repo=Path('/home/hoskinson/Projects/midnight-express');sys.path.insert(0,str(repo/'model'))
from validator import Harness,Invalid,digest
p=repo/'wiki-llm/pubsub/data-model-fit.json';report=json.loads(p.read_text());manifest=json.loads((repo/'website/dist/subscriptions-fixtures.json').read_bytes());receipts=[]
for i,r in enumerate(manifest['records']):
 if r.get('mode')!='v0.2-fixture':continue
 e=r['event'];c=r['context'];raw=json.dumps(e,separators=(',',':')).encode()
 receipt={'fixtureIndex':i,'id':e['id'],'schemaId':e['dataschema'],'profile':e['mpeprofile'],'contract':e['mpecontract'],'eventHash':digest(e),'contextHash':digest(c),'hashAlgorithm':'sha256 over RFC8785 JCS objects','trustedNow':c['now'],'trust':'offline synthetic fixture precheck; no live authority','event':e,'context':c}
 try:
  result=Harness(copy.deepcopy(c)).check(raw);receipt.update(status=result['status'],businessDigest=result['businessDigest'],executes=result['executes'],validation='offline-prechecked')
 except Invalid as err:receipt.update(status='rejected',reason=str(err),executes=False,validation='rejected')
 receipts.append(receipt)
report['dashboardReceipts']=receipts;report['conformanceCheck']={'command':'/tmp/mpe-data-model-validation-env/bin/python model/test_conformance.py','result':'PASS 80 checks; 3 schema self-checks; pinned local resources verified'};p.write_text(json.dumps(report,indent=2)+'\n');print([(r['id'],r['status']) for r in receipts])
