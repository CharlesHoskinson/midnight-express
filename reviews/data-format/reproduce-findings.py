"""Independent review counterexamples against the unchanged experimental model.
Reports observed behavior, not passing security acceptance. Never executes effects.
"""
from pathlib import Path
import copy,json,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'model'))
from validator import Harness,Invalid,raw_json
context=raw_json((ROOT/'model/conformance/trusted-context.json').read_bytes())
def sample(name):return raw_json((ROOT/f'model/examples/{name}.json').read_bytes())
def outcome(event,harness=None):
 try:return (harness or Harness(copy.deepcopy(context))).check(json.dumps(event))['status']
 except Invalid as e:return 'reject:'+str(e)
findings=[]
e=sample('rfq');e['id']+='\n'
findings.append({'finding':'terminal-newline-event-id','expected':'reject','observed':outcome(e)})
e=sample('rfq');e['data']['price']['value']['coefficient']+='\n'
findings.append({'finding':'terminal-newline-price-coefficient','expected':'reject','observed':outcome(e)})
e=sample('agent');h=Harness(copy.deepcopy(context));outcome(e,h);e['id']='event:second-occurrence';outcome(e,h);e['time']='2026-10-04T10:59:59.000Z'
findings.append({'finding':'duplicate-action-occurrence-conflict','expected':'reject:event-identity-conflict','observed':outcome(e,h)})
e=sample('agent');raw=json.dumps(e).replace('"maxEffects": 1','"maxEffects": 1.0000000000000001')
try:observed=Harness(copy.deepcopy(context)).check(raw)['status']
except Invalid as err:observed='reject:'+str(err)
findings.append({'finding':'fractional-max-effects-rounded-before-validation','expected':'reject','observed':observed})
report={'status':'review-counterexamples-not-runtime-acceptance','modelChanged':False,'executes':False,'findings':findings}
print(json.dumps(report,indent=2))
