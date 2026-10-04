from pathlib import Path
import copy,json,tempfile
from chains.observations import ethereum,solana,Journal,TOKEN,TRANSFER,b58encode
from validator import ROOT

def main():
 count=0
 def check(x):
  nonlocal count
  assert x;count+=1
 def rejects(f):
  nonlocal count
  try:f()
  except (ValueError,KeyError):count+=1;return
  raise AssertionError('expected refusal')
 ec={'fixtureTrust':'trusted-test-fixture-only','chainId':'0x1','genesis':'0x'+'01'*32,'contract':'0x'+'11'*20,'blockHash':'0x'+'02'*32}
 log={'address':ec['contract'],'blockHash':ec['blockHash'],'transactionHash':'0x'+'03'*32,'logIndex':'0x0','removed':False,'topics':[TRANSFER,'0x'+'00'*12+'22'*20,'0x'+'00'*12+'33'*20],'data':'0x'+'00'*31+'05'}
 er={'status':'0x1','blockHash':ec['blockHash'],'transactionHash':log['transactionHash'],'blockNumber':'0x64','logs':[log]}
 ef=ethereum(er,ec);check(len(ef)==1 and ef[0]['rawAmount']=='5')
 for n in (0,2**256-1):
  e=copy.deepcopy(er);e['logs'][0]['data']='0x'+n.to_bytes(32,'big').hex();check(ethereum(e,ec)[0]['rawAmount']==str(n))
 e=copy.deepcopy(er);e['status']='0x0';check(ethereum(e,ec)==[])
 e=copy.deepcopy(er);e['logs'][0]['topics'].append('0x'+'00'*32);rejects(lambda:ethereum(e,ec))
 e=copy.deepcopy(er);e['logs'][0]['removed']=True;rejects(lambda:ethereum(e,ec))
 c=copy.deepcopy(ec);c['blockHash']='0x'+'04'*32;rejects(lambda:ethereum(er,c))
 key=lambda n:b58encode(bytes([n])*32)
 sc={'fixtureTrust':'trusted-test-fixture-only','genesis':key(1),'branchHash':key(2),'instructionOutcomeSource':'fixture-program-trace-v1','instructionOutcomes':{'outer:0/inner:0':'Succeeded','outer:0/inner:1':'Succeeded'}}
 ins={'programIdIndex':0,'accounts':[1,2,3,4],'data':b58encode(b'\x0c'+(5).to_bytes(8,'little')+b'\x06')}
 sr={'version':'legacy','slot':100,'transaction':{'signatures':[b58encode(b'\x03'*64)],'message':{'accountKeys':[TOKEN,key(4),key(5),key(6),key(7)],'instructions':[ins]}},'meta':{'err':None,'innerInstructions':[{'index':0,'instructions':[copy.deepcopy(ins),copy.deepcopy(ins)]}],'preTokenBalances':[{'accountIndex':1,'mint':key(5),'uiTokenAmount':{'decimals':6,'amount':'100'}}]}}
 sf=solana(sr,sc);check(len(sf)==3 and len({f['factId'] for f in sf})==3)
 for n in (0,2**64-1):
  s=copy.deepcopy(sr);s['transaction']['message']['instructions'][0]['data']=b58encode(b'\x0c'+n.to_bytes(8,'little')+b'\x06');check(solana(s,sc)[0]['rawAmount']==str(n))
 s=copy.deepcopy(sr);s['meta']['err']={'InstructionError':[0,'Custom']};check(solana(s,sc)==[])
 c=copy.deepcopy(sc);c['instructionOutcomes']['outer:0/inner:0']='Failed';check(len(solana(sr,c))==2)
 c=copy.deepcopy(sc);c.pop('instructionOutcomes');rejects(lambda:solana(sr,c))
 s=copy.deepcopy(sr);s['version']=0;rejects(lambda:solana(s,sc))
 s=copy.deepcopy(sr);s['meta']['preTokenBalances']=[];rejects(lambda:solana(s,sc))
 with tempfile.TemporaryDirectory() as d:
  path=Path(d)/'facts.sqlite';j=Journal(path);f=ef[0];t0='2026-10-04T11:00:00.000Z';t1='2026-10-04T11:01:00.000Z';t2='2026-10-04T11:02:00.000Z'
  for delivery in ['poll','subscription','backfill']:j.append(delivery,t0,'fact',f['factId'],f)
  check(j.append('poll',t0,'fact',f['factId'],f)=='duplicate-delivery')
  j.append('finality',t0,'finality',f['factId'],{'commitment':'ethereum:finalized','source':'fixture-node'})
  before=j.totals(t0,'ethereum:finalized');check(list(before['rawTotals'].values())==['5'])
  j.append('removed',t1,'invalidate',f['factId'],{'reason':'reorg','source':'fixture-ancestry'})
  check(j.totals(t1,'ethereum:finalized')['rawTotals']=={});check(j.totals(t0,'ethereum:finalized')==before)
  e=copy.deepcopy(er);e['blockHash']=e['logs'][0]['blockHash']='0x'+'08'*32;c=copy.deepcopy(ec);c['blockHash']=e['blockHash'];new=ethereum(e,c)[0];check(new['factId']!=f['factId']);j.append('reinclude',t2,'fact',new['factId'],new);j.append('finality-new',t2,'finality',new['factId'],{'commitment':'ethereum:finalized','source':'fixture-node'});check(list(j.totals(t2,'ethereum:finalized')['rawTotals'].values())==['5'])
  expected=j.totals(t2,'ethereum:finalized');j.close();j=Journal(path);check(j.totals(t2,'ethereum:finalized')==expected)
  rejects(lambda:j.append('poll',t1,'fact',f['factId'],f));rejects(lambda:j.append('bad-finality',t2,'finality',f['factId'],{'commitment':'confirmed'}))
  j.append('other-provider',t2,'finality',new['factId'],{'commitment':'ethereum:safe','source':'fixture-other-node'});check(j.totals(t2,'ethereum:finalized')['rawTotals']=={});check(any(g['missing']=='contradictory-native-commitment' for g in j.totals(t2,'ethereum:finalized')['gaps']))
  rejects(lambda:j.append('clock-regression',t0,'gap','coverage:old',{'scope':'old','missing':'late'}))
  j.append('gap',t2,'gap','coverage:range',{'scope':'fixture-range','missing':'history-pruned'});check(len(j.totals(t2,'ethereum:finalized')['gaps'])==2);j.close()
 fixtures={'status':'synthetic-read-only','ethereum':{'receipt':er,'context':ec},'solana':{'transaction':sr,'context':sc}}
 (ROOT/'chains/fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n');report={'checks':count,'status':'synthetic-read-only-projections','liveRPC':False,'finalityVerified':False,'effectAuthority':False};(ROOT/'evidence/chain-results.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
if __name__=='__main__':main()
