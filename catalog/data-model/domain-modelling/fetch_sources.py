from scrapling.fetchers import Fetcher
from pathlib import Path
import hashlib,json,datetime,subprocess,concurrent.futures,zipfile,io
ROOT=Path(__file__).parent
SOURCES=[
('ddd-reference-page','https://www.domainlanguage.com/ddd/reference/'),
('ddd-reference','https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf'),
('canonical-data-model','https://www.enterpriseintegrationpatterns.com/patterns/messaging/CanonicalDataModel.html'),
('format-indicator','https://www.enterpriseintegrationpatterns.com/patterns/messaging/FormatIndicator.html'),
('ubl-customization','https://docs.oasis-open.org/ubl/guidelines/UBL2-Customization1.0cs01.html'),
('ubl-2.4','https://docs.oasis-open.org/ubl/UBL-2.4.html'),
('ccts-2.01','https://unece.org/fileadmin/DAM/cefact/codesfortrade/CCTS/CCTS_V2-01_Final.pdf'),
('iso20022-business-model','https://www.iso20022.org/iso20022-repository/business-model'),
('iso20022-dictionary','https://www.iso20022.org/understanding-data-dictionary'),
('iso20022-faq','https://www.iso20022.org/faq'),
('iso20022-terms','https://www.iso20022.org/terms-use'),
('iso20022-about','https://www.iso20022.org/about-iso-20022'),
('iso20022-ipr','https://www.iso20022.org/intellectual-property-rights'),
('oasis-business-document-ndr','https://docs.oasis-open.org/ubl/Business-Document-NDR/v1.0/os/Business-Document-NDR-v1.0-os.html'),
('ccts-oasis-mirror','https://www.oasis-open.org/committees/download.php/6232/CEFACT-CCTS-Version-2pt01.zip'),
]
def fetch(item):
 name,url=item
 try:
  r=Fetcher.get(url,timeout=25)
  raw=bytes(r.body)
  pdf=raw.startswith(b'%PDF')
  suffix='.pdf' if pdf else ('.zip' if raw.startswith(b'PK') else '.html')
  file=ROOT/(name+suffix);file.write_bytes(raw)
  txt=ROOT/(name+'.txt')
  if pdf:
   subprocess.run(['pdftotext','-layout',str(file),str(txt)],check=True)
  elif suffix=='.zip':
   z=zipfile.ZipFile(io.BytesIO(raw));parts=[]
   for n in z.namelist():
    if n.lower().endswith('.pdf'):
     child=ROOT/(name+'-'+Path(n).name);child.write_bytes(z.read(n))
     childtext=child.with_suffix('.txt')
     subprocess.run(['pdftotext','-layout',str(child),str(childtext)],check=True)
     parts.append(childtext.read_text())
   txt.write_text('\n'.join(parts))
  else: txt.write_text(r.get_all_text(separator='\n'),encoding='utf-8')
  return dict(id=name,url=url,status=r.status,fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),raw_file=file.name,raw_sha256=hashlib.sha256(raw).hexdigest(),text_file=txt.name,text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest(),text_bytes=txt.stat().st_size)
 except Exception as e:return dict(id=name,url=url,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,SOURCES))
(ROOT/'manifest.json').write_text(json.dumps(results,indent=2)+'\n')
for r in results: print(r['id'],r.get('status'),r.get('text_bytes'),r.get('error',''))
