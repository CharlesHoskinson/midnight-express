"""Reproduce the runtime side of the independent Opus replay-token probe."""
import sys,json,copy,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'model'))
from validator import Harness,Invalid,raw_json,business_digest
c=raw_json((ROOT/'model/conformance/trusted-context.json').read_bytes())
e=raw_json((ROOT/'model/examples/agent.json').read_bytes())
h=Harness(c)
first=h.check(json.dumps(e))
altered=copy.deepcopy(e)
altered['id']='event:agent-2'
altered['data']['validUntil']=datetime.datetime.fromtimestamp(1791118000,datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
assert first['status']=='sandbox-candidate-only'
assert business_digest(e)!=business_digest(altered)
assert Harness(c).check(json.dumps(altered))['status']=='sandbox-candidate-only'
try:h.check(json.dumps(altered))
except Invalid as err:
 assert str(err)=='action-identity-conflict'
 print('PASS: fresh approval is valid, but altered business intent conflicts under the prior action key.')
else:raise AssertionError('Expected action-identity-conflict')
