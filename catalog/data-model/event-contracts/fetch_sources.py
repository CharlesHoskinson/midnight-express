"""Re-fetch primary specifications with Scrapling and retain bytes, text, hashes."""
from scrapling.fetchers import Fetcher
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,datetime
ROOT=Path(__file__).parent
SOURCES=[
('cloudevents-core','https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/cloudevents/spec.md'),
('cloudevents-json','https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/cloudevents/formats/json-format.md'),
('json-schema-core','https://json-schema.org/draft/2020-12/json-schema-core'),
('json-schema-validation','https://json-schema.org/draft/2020-12/json-schema-validation'),
('avro-specification','https://avro.apache.org/docs/1.12.0/specification/'),
('protobuf-evolution','https://protobuf.dev/programming-guides/proto3/'),
('protobuf-json','https://protobuf.dev/programming-guides/json/'),
('protobuf-noncanonical','https://protobuf.dev/programming-guides/serialization-not-canonical/'),
('rfc8785-jcs','https://www.rfc-editor.org/rfc/rfc8785.txt'),
('rfc7493-ijson','https://www.rfc-editor.org/rfc/rfc7493.txt'),
('rfc3339-time','https://www.rfc-editor.org/rfc/rfc3339.txt'),
('asyncapi-3','https://raw.githubusercontent.com/asyncapi/spec/v3.0.0/spec/asyncapi.md'),
]
def fetch(item):
 name,url=item
 try:
  r=Fetcher.get(url,timeout=25)
  body=bytes(r.body)
  txt=r.get_all_text()
  (ROOT/(name+'.raw')).write_bytes(body)
  (ROOT/(name+'.txt')).write_text(txt)
  m={'id':name,'url':url,'resolved_url':str(r.url),'status':r.status,'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fetcher':'Scrapling Fetcher.get(timeout=25)','raw_path':name+'.raw','text_path':name+'.txt','raw_sha256':hashlib.sha256(body).hexdigest(),'text_sha256':hashlib.sha256(txt.encode()).hexdigest(),'text_chars':len(txt)}
 except Exception as e: m={'id':name,'url':url,'error':str(e)}
 (ROOT/(name+'.metadata.json')).write_text(json.dumps(m,indent=2)+'\n')
 return m
with ThreadPoolExecutor(max_workers=4) as pool: records=list(pool.map(fetch,SOURCES))
(ROOT/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
for r in records: print(r['id'],r.get('status'),r.get('text_chars'),r.get('error',''))
