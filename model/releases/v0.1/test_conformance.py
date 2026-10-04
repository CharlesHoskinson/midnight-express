"""Run checked-in raw JSON corpus and meaningful reference state/context counterexamples."""
import copy
import json
from pathlib import Path
from validator import ROOT, Harness, Invalid, raw_json, proposal_digest, load_profile

def main():
    context=raw_json((ROOT/'conformance/trusted-context.json').read_bytes())
    count=0
    def checked(raw, expected, harness=None):
        nonlocal count
        try:
            actual=(harness or Harness(copy.deepcopy(context))).check(raw, eid='opaque-test-eid')
        except Invalid as err:
            assert expected=='reject', (expected, str(err))
        else:
            assert actual['status']==expected, (expected,actual)
            assert actual['executes'] is False
        count+=1
    def encoded(e): return json.dumps(e,separators=(',',':'))
    for case in json.loads((ROOT/'conformance/cases.json').read_bytes()):
        checked((ROOT/case['file']).read_bytes(),case['expect'])
    a=raw_json((ROOT/'examples/agent.json').read_bytes())
    h=Harness(copy.deepcopy(context))
    checked(encoded(a),'sandbox-candidate-only',h)
    checked(encoded(a),'duplicate-event',h)
    replay=copy.deepcopy(a); replay['id']='event:new-delivery'
    # A new opaque EID and occurrence identity never renew the logical action.
    checked(encoded(replay),'duplicate-action',h)
    conflict=copy.deepcopy(replay); conflict['id']='event:changed-intent'
    conflict['data']['validFrom']='2026-10-04T11:30:00.000Z'
    checked(encoded(conflict),'reject',h)
    changed=copy.deepcopy(a); changed['data']['proposal']['target']='sandbox:reports/other'
    changed['data']['proposalDigest']=proposal_digest(changed['data']['proposal'],changed['mpecontract'])
    checked(encoded(changed),'reject') # Valid hash cannot substitute for exact trusted proposal.
    changed=copy.deepcopy(a); changed['data']['policyDigest']='sha256:'+'4'*64
    checked(encoded(changed),'reject')
    for change in ('no-trust','no-proposal','revoked','low-budget','unknown-target','no-role','wrong-principal'):
        c=copy.deepcopy(context)
        if change=='no-trust': c.pop('fixtureTrust')
        if change=='no-proposal': c['proposals']={}
        if change=='revoked': c['revokedActions']=['action:demo']
        if change=='low-budget': c['maxSteps']=4
        if change=='unknown-target': c['sandboxTargets']=[]
        if change=='no-role': c['sources']={}
        if change=='wrong-principal': c['sources']['urn:mpe:source:human']['principal']='human:bob'
        checked(encoded(a),'reject',Harness(c))
    rfq=raw_json((ROOT/'examples/rfq.json').read_bytes())
    h=Harness(copy.deepcopy(context)); checked(encoded(rfq),'offchain-quote-valid',h)
    changed=copy.deepcopy(rfq); changed['data']['quoteId']='quote:conflicting'
    checked(encoded(changed),'reject',h)
    # Cash overflow with individually bounded quantity/price coefficients.
    changed=copy.deepcopy(rfq); changed['data']['quantity']['coefficient']='999999999999999999'
    c=copy.deepcopy(context); c['rfqs']['rfq:demo']['quantity']=changed['data']['quantity']
    checked(encoded(changed),'reject',Harness(c))
    # Both opposite requester perspectives are valid when the exact trusted RFQ agrees.
    changed=copy.deepcopy(rfq); changed['data'].update(requesterSide='SellAsset',buyer='party:dealer',seller='party:buyer')
    c=copy.deepcopy(context); c['rfqs']['rfq:demo']['requesterSide']='SellAsset'
    checked(encoded(changed),'offchain-quote-valid',Harness(c))
    # Profile integrity verified before parsing business data; schema resources have no refs.
    for name in ('rfq.v0.1','invoice.v0.1','agent.v0.1'):
        m,_=load_profile(name)
        from jsonschema import Draft202012Validator
        schema=raw_json((ROOT/m['schema']).read_bytes())
        Draft202012Validator.check_schema(schema)
        assert '$ref' not in json.dumps(schema)
    sizes={p.name:len(p.read_bytes()) for p in (ROOT/'examples').glob('*.json')}
    assert max(sizes.values())<=3926,sizes
    print(f'PASS {count} checks; 3 schema self-checks; pinned local resources verified')
    print('Unsigned JSON example byte sizes: '+json.dumps(sizes,sort_keys=True))
    print('No cryptography, finality, durable commit, execution, or sealed-wire conformance tested.')
if __name__=='__main__': main()
