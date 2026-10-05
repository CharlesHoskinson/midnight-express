import copy, json, sys
from pathlib import Path
sys.path.insert(0,'/home/hoskinson/Projects/midnight-express/model')
import validator, bundles
R = Path('/tmp/mpe-lean-opus-review/model-fidelity/mcopy'); validator.ROOT = R
m, old = bundles.load_bundle(R, 'rfq.v0.2')
rules = copy.deepcopy(m['normative']); rules['note'] = 'second reviewed conformance bundle'
new = bundles.publish_bundle(R, 'rfq.v0.2', m['schemaObject'], m['coreObject'], rules)
print('lock still', json.loads((R/'profiles/lock.json').read_text())['rfq.v0.2'] == old, 'new', new != old)
c = validator.raw_json((R/'conformance/trusted-context.json').read_bytes())
q = validator.raw_json((R/'examples/rfq.json').read_bytes())
for contract in (old, new):
    e = copy.deepcopy(q); e['mpecontract'] = contract; e['id'] = 'event:' + contract[7:15]
    try: print(contract[:15], validator.Harness(copy.deepcopy(c)).check(json.dumps(e))['status'])
    except validator.Invalid as err: print(contract[:15], 'reject', err)
