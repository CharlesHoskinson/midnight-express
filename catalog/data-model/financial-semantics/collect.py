from scrapling.fetchers import Fetcher
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,datetime
base=Path(__file__).parent
sources=[
('cdm-product','https://cdm.finos.org/docs/product-model/'),
('cdm-pretrade','https://cdm.finos.org/docs/pre-trade-processing/'),
('cdm-namespace','https://cdm.finos.org/docs/namespace/'),
('cdm-readme','https://raw.githubusercontent.com/finos/common-domain-model/master/README.md'),
('cdm-license','https://raw.githubusercontent.com/finos/common-domain-model/master/LICENSE.md'),
('cdm-model-common','https://raw.githubusercontent.com/finos/common-domain-model/master/rosetta-source/src/main/rosetta/product-common.rosetta'),
('fpml-standard','https://www.fpml.org/the_standard/'),
('fpml-expiry','https://www.fpml.org/spec/fpml-5-12-4-rec-1/html/pretrade/schemaDocumentation/schemas/fpml-asset-5-12_xsd/groups/QuotationCharacteristics.model/expiryTime.html'),
('fpml-pretrade','https://www.fpml.org/spec/fpml-5-13-5-rec-2/html/pretrade/fpml-5-13-intro-2.html'),
('fix-implementation','https://dev.fixtrading.org/implementation-guide/'),
('fix-sbe-encoding','https://raw.githubusercontent.com/FIXTradingCommunity/fix-simple-binary-encoding/master/v2-0-RC1/doc/02FieldEncoding.md'),
('iso-business-model','https://www.iso20022.org/iso20022-repository/business-model'),
('iso-dictionary','https://www.iso20022.org/understanding-data-dictionary'),
('ubl-invoice','https://docs.oasis-open.org/ubl/os-UBL-2.3/mod/summary/reports/UBL-Invoice-2.3.html'),
]
def fetch(item):
 name,url=item
 row=dict(id=name,url=url,requested_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),fetcher='Scrapling Fetcher.get(url, timeout=25)')
 try:
  r=Fetcher.get(url,timeout=25)
  text=r.get_all_text(); data=text.encode()
  (base/(name+'.txt')).write_bytes(data)
  row.update(status=r.status,text_path=name+'.txt',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),usable=(r.status==200 and len(data)>100))
 except Exception as e: row.update(usable=False,error=str(e))
 return row
with ThreadPoolExecutor(max_workers=5) as pool: rows=list(pool.map(fetch,sources))
(base/'manifest.json').write_text(json.dumps({'collected_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':rows},indent=2)+'\n')
for r in rows: print(r['id'],r.get('status'),r.get('bytes'),r.get('error',''))
