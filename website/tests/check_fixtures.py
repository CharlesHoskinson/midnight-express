"""Revalidate public synthetic fixture receipts without changing evidence files."""
import copy
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'model'))
from validator import Harness, Invalid, digest

manifest = json.loads((ROOT / 'website/dist/subscriptions-fixtures.json').read_text())
for record in manifest['records']:
    if record['mode'] != 'v0.2-fixture':
        assert record['event'] is None and record['context'] is None and record['wire'] is None
        continue
    event, context, receipt = record['event'], record['context'], record['offlineReceipt']
    assert record['wire'] is None, 'Do not fabricate sealed wire from JSON fixtures'
    assert receipt['eventHash'] == digest(event)
    assert receipt['contextHash'] == digest(context)
    assert receipt['trustedNow'] == context['now']
    assert receipt['executes'] is False
    try:
        result = Harness(copy.deepcopy(context)).check(json.dumps(event, separators=(',', ':')).encode())
    except Invalid as error:
        assert receipt['status'] == 'rejected'
        assert receipt['reason'] == str(error)
        assert record['validation'] == 'offline-reference-rejected'
    else:
        assert record['validation'] == 'offline-reference-accepted'
        for key in ('status', 'businessDigest', 'executes'):
            assert receipt[key] == result[key]
    print('PASS', record['title'])
print('Public synthetic receipts match actual fixed-context validator results; no live authority established.')
