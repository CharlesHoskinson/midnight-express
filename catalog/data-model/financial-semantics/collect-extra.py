from scrapling.fetchers import Fetcher
from pathlib import Path
import hashlib,json,datetime
base=Path(__file__).parent
mf=json.loads((base/'manifest.json').read_text())
items=[('cdm-model-common-correct','https://raw.githubusercontent.com/finos/common-domain-model/master/rosetta-source/src/main/rosetta/product-common-type.rosetta'),('cdm-model-math','https://raw.githubusercontent.com/finos/common-domain-model/master/rosetta-source/src/main/rosetta/base-math-type.rosetta'),('fix-quoterequest','https://fiximate.fixtrading.org/legacy/en/FIX.4.2/body_505482.html?find=Side'),('fix-quote','https://fiximate.fixtrading.org/legacy/en/FIX.4.4/body_505583.html'),('fix-introduction','https://www.fixtrading.org/online-specification/introduction/'),('fpml-pretrade-legacy','https://www.fpml.org/spec/fpml-4-4-12-rec-1/html/fpml-4-4-intro.html'),('cdm-commit','https://api.github.com/repos/finos/common-domain-model/commits/master')]
for name,url in items:
 row={'id':name,'url':url,'requested_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fetcher':'Scrapling Fetcher.get(url, timeout=25)'}
 try:
  r=Fetcher.get(url,timeout=25); data=r.get_all_text().encode(); (base/(name+'.txt')).write_bytes(data)
  row.update(status=r.status,text_path=name+'.txt',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),usable=(r.status==200 and len(data)>100))
 except Exception as e: row.update(usable=False,error=str(e))
 mf['sources'].append(row); print(name,row.get('status'),row.get('bytes'),row.get('error',''))
(base/'manifest.json').write_text(json.dumps(mf,indent=2)+'\n')
