"""Independent process agreement: Python diagnostic, Rust interpreter, TypeScript interpreter.
Golden corpus retains raw tokens. Synthetic context is explicit; no network/source authentication.
"""
from pathlib import Path
import copy,json,subprocess
from validator import ROOT,Harness,Invalid,raw_json,business_digest
import rfc8785
C=raw_json((ROOT/'conformance/trusted-context.json').read_bytes())
T=raw_json((ROOT/'examples/rfq.json').read_bytes())
commands=[['node',str(ROOT/'interpreters/typescript.mts'),str(ROOT)], [str(ROOT/'interpreters/rust/target/debug/mpe-rfq-conformance'),str(ROOT)]]
def run(command,requests):
 p=subprocess.run(command,input=''.join(json.dumps(x)+'\n' for x in requests),text=True,capture_output=True,check=True)
 lines=p.stdout.splitlines();assert len(lines)==len(requests),(p.stderr,p.stdout)
 return [json.loads(x) for x in lines]
def expected(raw,c):
 try:r=Harness(copy.deepcopy(c)).check(raw)
 except Invalid:return {'status':'reject','executes':False}
 e=raw_json(raw);intent={'domain':'mpe.model.intent.v0.2','source':e['source'],'type':e['type'],'profile':e['mpeprofile'],'contract':e['mpecontract'],'data':e['data']}
 return {**r,'canonicalEvent':rfc8785.dumps(e).decode(),'canonicalIntent':rfc8785.dumps(intent).decode()}
def main():
 requests=[];labels=[]
 for case in json.loads((ROOT/'conformance/cases.json').read_bytes()):
  raw=(ROOT/case['file']).read_text()
  if 'urn:mpe:source:dealer' in raw:requests.append({'raw':raw,'context':C});labels.append(case['file'])
 for label,mutate in [('newline-id',lambda e:e.update(id=e['id']+'\n')),('newline-coefficient',lambda e:e['data']['price']['value'].update(coefficient='12345\n')),('wrong-cash',lambda e:e['data']['cash'].update(coefficient='1234499')),('unknown-field',lambda e:e.update(extra='ignored?')),('leap-second',lambda e:e.update(time='2016-12-31T23:59:60.000Z')),('zero-year',lambda e:e.update(time='0000-01-01T00:00:00.000Z'))]:
  e=copy.deepcopy(T);mutate(e);requests.append({'raw':json.dumps(e),'context':C});labels.append(label)
 for token in ['2.0','2e0','2.0000000000000001','2e999','-0']:
  requests.append({'raw':json.dumps(T).replace('"scale": 2','"scale": '+token,1),'context':C});labels.append('raw-scale-'+token)
 for label,raw in [('duplicate-key',json.dumps(T).replace('"specversion": "1.0"','"specversion":"1.0","specversion":"1.0"')),('escaped-key',json.dumps(T).replace('"id": "event:rfq"','"id":"event:rfq","\\u0069d":"event:rfq"'))]:requests.append({'raw':raw,'context':C});labels.append(label)
 sell=copy.deepcopy(T);sell['data'].update(requesterSide='SellAsset',buyer='party:dealer',seller='party:buyer');c=copy.deepcopy(C);c['rfqs']['rfq:demo']['requesterSide']='SellAsset';requests.append({'raw':json.dumps(sell),'context':c});labels.append('opposite-perspective')
 for price in ('1','999999999999999999'):
  e=copy.deepcopy(T);e['data']['quantity']['coefficient']='1';e['data']['price']['value']['coefficient']=price;e['data']['cash']['coefficient']=price;c=copy.deepcopy(C);c['rfqs']['rfq:demo']['quantity']=copy.deepcopy(e['data']['quantity']);requests.append({'raw':json.dumps(e),'context':c});labels.append('exact-boundary-price-'+price)
 oracles=[expected(q['raw'],q['context']) for q in requests]
 for command in commands:
  actual=run(command,requests)
  for label,a,e in zip(labels,actual,oracles):assert a==e,(command[0],label,a,e)
 # Stateful occurrence disagreement must be caught independently too.
 replay=[{'kind':'process','raw':json.dumps(T),'context':C},{'kind':'process','raw':json.dumps(T),'context':C}]
 altered=copy.deepcopy(T);altered['time']='2026-10-04T10:59:59.000Z';replay.append({'kind':'process','raw':json.dumps(altered),'context':C})
 for command in commands:assert [x['status'] for x in run(command,replay)]==['offchain-quote-valid','duplicate-event','reject']
 # Two independently specified source formats and implementation-owned adapters.
 a={'format':'dealer-a.usd-share.v1','quantity':'100','unitPriceDollars':'123.45','currency':'USD','basisShares':'1','perspective':'RequesterBuy','fees':'None'}
 b={'format':'dealer-b.cents-lot.v1','quantity':'100','quotePriceMinor':'1234500','currency':'USD','basisShares':'100','perspective':'DealerSell','fees':'None'}
 source_cases=[]
 for label,base,cmd,kind in [('a',a,commands[0],'adapter-a'),('b',b,commands[1],'adapter-b')]:
  good=run(cmd,[{'kind':kind,'input':base,'template':T}])[0];assert good['event']==T,(label,good)
  for field,value in [('basisShares',''),('currency','EUR'),('perspective','Unknown'),('fees','Excluded'),('quantity','0')]:
   bad=copy.deepcopy(base);bad[field]=value;assert run(cmd,[{'kind':kind,'input':bad,'template':T}])[0]['status']=='reject'
  bad=copy.deepcopy(base);bad['unknownFee']='1';assert run(cmd,[{'kind':kind,'input':bad,'template':T}])[0]['status']=='reject'
  source_cases.append({'sourceFormat':base['format'],'rawSource':json.dumps(base,separators=(',',':')),'canonicalEvent':rfc8785.dumps(good['event']).decode(),'intentDigest':business_digest(good['event']),'loss':[],'transformations':['exact-price-basis','explicit-role-perspective'],'status':'unsigned-fixture-mapping'})
 bad=copy.deepcopy(b);bad['quotePriceMinor']='1234501';assert run(commands[1],[{'kind':'adapter-b','input':bad,'template':T}])[0]['status']=='reject'
 assert source_cases[0]['intentDigest']==source_cases[1]['intentDigest']
 cases=[{'caseId':label,'rawEvent':q['raw'],'context':q['context'],'expected':oracle} for label,q,oracle in zip(labels,requests,oracles)]
 report={'status':'synthetic-independent-conformance','implementations':['Python','Rust','TypeScript'],'cases':len(cases),'acceptedDisagreements':0,'safeRefusals':sum(e['status']=='reject' for e in oracles),'adapterCases':15,'replaySequenceCases':3,'sourceAuthentication':False,'executes':False}
 evidence=ROOT/'evidence';evidence.mkdir(exist_ok=True)
 (evidence/'rfq-golden-vectors.json').write_text(json.dumps(cases,indent=2)+'\n');(evidence/'adapter-receipts.json').write_text(json.dumps(source_cases,indent=2)+'\n');(evidence/'interoperability-results.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':main()
