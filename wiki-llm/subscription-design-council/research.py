#!/usr/bin/env python3
"""Public-source Scrapling retrieval and PixelRAG visual grounding with per-source provenance."""
import argparse,datetime,hashlib,json,os,re,subprocess,sys
from pathlib import Path
from scrapling.fetchers import Fetcher
ROOT=Path(__file__).resolve().parent
PIXELSHOT='/home/hoskinson/.local/share/scrapling-venv/bin/pixelshot'
p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('--slug',required=True);p.add_argument('--group',required=True);p.add_argument('--visual',action='store_true');a=p.parse_args()
if not re.fullmatch(r'[a-z0-9-]+',a.slug) or not re.fullmatch(r'[a-z0-9-]+',a.group):sys.exit('invalid archive slug/group')
out=ROOT/'sources'/a.group;out.mkdir(parents=True,exist_ok=True)
m={'url':a.url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tool':'Scrapling','visual_tool':'PixelRAG pixelshot 0.4.0' if a.visual else None}
try:
 r=Fetcher.get(a.url,timeout=35);raw=bytes(r.body);text=r.get_all_text(separator='\n')
 (out/(a.slug+'.raw')).write_bytes(raw);(out/(a.slug+'.txt')).write_text(text)
 m.update(status=r.status,raw_sha256=hashlib.sha256(raw).hexdigest(),text_sha256=hashlib.sha256(text.encode()).hexdigest(),bytes=len(raw),text_bytes=len(text.encode()),final_url=str(r.url))
 m['accepted_source']=r.status==200 and len(text)>120
except Exception as e:m.update(accepted_source=False,error=str(e))
if a.visual:
 env=dict(os.environ,CHROME_PATH='/home/hoskinson/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome')
 try:
  tiles=out/(a.slug+'-tiles');before=set(tiles.rglob('*.jpg')) if tiles.exists() else set()
  r=subprocess.run([PIXELSHOT,a.url,'--output',str(tiles),'--backend','cdp','--workers','1','--tile-height','1568','--wait-network-idle'],env=env,capture_output=True,text=True,timeout=110)
  files=list(tiles.rglob('*.jpg'));m['visual']={'exit_code':r.returncode,'tiles':[{'path':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files],'stderr':r.stderr[-2500:],'verified_capture':r.returncode==0 and bool(files)}
 except Exception as e:m['visual']={'verified_capture':False,'error':str(e)}
(out/(a.slug+'.json')).write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(m))
sys.exit(0 if m.get('accepted_source') else 1)
