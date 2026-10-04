from scrapling.fetchers import Fetcher
from pathlib import Path
import hashlib,json,datetime
out=Path(__file__).parent
sources=[('shacl','https://www.w3.org/TR/shacl/'),('jsonld11','https://www.w3.org/TR/json-ld11/'),('jsonld11-api','https://www.w3.org/TR/json-ld11-api/'),('owl2-primer','https://www.w3.org/TR/owl2-primer/'),('ucum','https://ucum.org/ucum'),('qudt-schema','https://www.qudt.org/doc/2025/01/DOC_SCHEMA-QUDT.html'),('json-schema-validation','https://json-schema.org/draft/2020-12/json-schema-validation')]
manifest=[]
for name,url in sources:
 try:
  r=Fetcher.get(url,timeout=25)
  raw=r.body
  if isinstance(raw,str): raw=raw.encode()
  txt=r.get_all_text(separator='\n',strip=True)
  (out/(name+'.html')).write_bytes(raw)
  (out/(name+'.txt')).write_text(txt)
  entry={'id':name,'url':url,'status':r.status,'fetched_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'html':name+'.html','text':name+'.txt','html_sha256':hashlib.sha256(raw).hexdigest(),'text_sha256':hashlib.sha256(txt.encode()).hexdigest(),'text_chars':len(txt)}
 except Exception as e:entry={'id':name,'url':url,'error':str(e)}
 manifest.append(entry);print(json.dumps(entry),flush=True)
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
