"""Archive primary safety evidence with Scrapling, including PDF full text."""
from scrapling.fetchers import Fetcher
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime, hashlib, json, subprocess

ROOT = Path(__file__).parent
SOURCES = [
    ('langsec-report', 'https://langsec.org/papers/langsec-tr.pdf'),
    ('saltzer-basic', 'https://web.mit.edu/Saltzer/www/publications/protection/Basic.html'),
    ('saltzer-descriptors', 'https://web.mit.edu/Saltzer/www/publications/protection/Descriptors.html'),
    ('hardy-deputy', 'https://cap-lore.com/CapTheory/ConfusedDeputy.html'),
    ('rfc8785', 'https://www.rfc-editor.org/rfc/rfc8785.txt'),
    ('rfc8725', 'https://www.rfc-editor.org/rfc/rfc8725.txt'),
    ('rfc7493', 'https://www.rfc-editor.org/rfc/rfc7493.txt'),
    ('schema-core', 'https://json-schema.org/draft/2020-12/json-schema-core'),
    ('schema-validation', 'https://json-schema.org/draft/2020-12/json-schema-validation'),
    ('camel-paper', 'https://arxiv.org/pdf/2503.18813v1'),
]

def fetch(item):
    name, url = item
    record = {'id': name, 'url': url, 'fetcher': 'Scrapling Fetcher.get(timeout=25)'}
    try:
        # Research-only public PDF mirror has an incomplete certificate chain.
        # Record this reduced provenance; never apply it to runtime authority.
        if name == 'langsec-report':
            response = Fetcher.get(url, timeout=25, verify=False)
            record['tls_verification'] = False
            record['provenance_caveat'] = 'Incomplete public-site TLS chain; PDF fetched without certificate verification.'
        else:
            response = Fetcher.get(url, timeout=25)
            record['tls_verification'] = True
        body = bytes(response.body)
        suffix = '.pdf' if body.startswith(b'%PDF') else '.raw'
        raw_path = ROOT / (name + suffix)
        raw_path.write_bytes(body)
        text_path = ROOT / (name + '.txt')
        if suffix == '.pdf':
            subprocess.run(['pdftotext', '-layout', str(raw_path), str(text_path)], check=True)
            text = text_path.read_text()
            extraction = 'pdftotext -layout, complete PDF'
        elif url.endswith('.txt'):
            text = body.decode('utf-8')
            text_path.write_text(text)
            extraction = 'complete UTF-8 response'
        else:
            text = response.get_all_text()
            text_path.write_text(text)
            extraction = 'Scrapling get_all_text, complete HTML'
        record.update(status=response.status, resolved_url=str(response.url),
            retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            raw_path=raw_path.name, text_path=text_path.name, extraction=extraction,
            raw_sha256=hashlib.sha256(body).hexdigest(),
            text_sha256=hashlib.sha256(text.encode()).hexdigest(), text_chars=len(text))
    except Exception as exc:
        record['error'] = str(exc)
    return record

with ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(fetch, SOURCES))
(ROOT / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
for record in records:
    print(record['id'], record.get('status'), record.get('text_chars'), record.get('error', ''))
