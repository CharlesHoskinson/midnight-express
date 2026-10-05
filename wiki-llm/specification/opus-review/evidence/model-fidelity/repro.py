import copy, json, sys
from pathlib import Path
ROOT = Path('/home/hoskinson/Projects/midnight-express')
sys.path.insert(0, str(ROOT/'model')); sys.path.insert(0, str(ROOT/'formal/lean'))
from validator import Harness, Invalid, raw_json, proposal_digest
def load(p): return raw_json((ROOT/p).read_bytes())
c = load('model/conformance/trusted-context.json')
def run(h, e):
    try: return h.check(json.dumps(e, separators=(',',':')))['status']
    except Invalid as err: return 'reject:'+str(err)
q = load('model/examples/rfq.json'); a = load('model/examples/agent.json'); inv = load('model/examples/invoice-final.json')
# 1 same quoteId, two different firm prices, both accepted in one harness
h = Harness(copy.deepcopy(c)); q2 = copy.deepcopy(q); q2['id']='event:rfq-2'
q2['data']['price']['value']['coefficient']='12000'; q2['data']['cash']['coefficient']='1200000'
print('quoteId-conflict', run(h,q), run(h,q2))
# 2 same Final payment observed twice under new event ids
h = Harness(copy.deepcopy(c)); i2 = copy.deepcopy(inv); i2['id']='event:invoice-final-2'
print('payment-double', run(h,inv), run(h,i2))
# 3 cumulative overpayment across paymentIds (25000 + 30000 > 50000 payable)
ctx = copy.deepcopy(c); ev = copy.deepcopy(ctx['paymentEvidence']['payment:demo'])
ev['paymentId']='payment:demo2'; ev['amount']['coefficient']='30000'; ctx['paymentEvidence']['payment:demo2']=ev
h = Harness(ctx); i3 = copy.deepcopy(inv); i3['id']='event:invoice-final-3'; i3['data']=copy.deepcopy(ev)
print('cumulative-overpay', run(h,inv), run(h,i3))
# 4 Final then Reversed for the same paymentId across context refresh: both accepted, no transition rule
ctx2 = copy.deepcopy(c); r = copy.deepcopy(ctx2['paymentEvidence']['payment:demo']); r['status']='Reversed'
ctx2['paymentEvidence']['payment:demo']=r
h = Harness(copy.deepcopy(c)); out1 = run(h,inv); h.context = ctx2
i4 = copy.deepcopy(inv); i4['id']='event:invoice-reversed-demo'; i4['data']=copy.deepcopy(r)
print('final-then-reversed', out1, run(h,i4))
# 5 budget window: two distinct actions in window:fixture each 5 Steps, maxSteps 10 -> 10 total; then third -> 15
ctx = copy.deepcopy(c); h = Harness(ctx); outs=[]
for n in range(3):
    aid = f'action:demo{n}'; ctx['proposals'][aid]=copy.deepcopy(c['proposals']['action:demo'])
    e = copy.deepcopy(a); e['id']=f'event:agent-{n}'; e['data']['actionId']=aid
    outs.append(run(h,e))
print('budget-window', outs)
# 6 reissued proposal under same action key (Python hashes intent itself)
h = Harness(copy.deepcopy(c)); first = run(h,a)
ctx = copy.deepcopy(c); p = copy.deepcopy(a['data']['proposal']); p['target']='sandbox:reports/other'
ctx['proposals']['action:demo']=p; ctx['sandboxTargets'].append(p['target']); h.context=ctx
a2 = copy.deepcopy(a); a2['id']='event:agent-2'; a2['data']['proposal']=p
a2['data']['proposalDigest']=proposal_digest(p, a2['mpecontract'])
print('reissued-same-key', first, run(h,a2))
# 7 Examples.lean freshness without building
import check
print('examples-current', check.generate(check.collect()) == (ROOT/'formal/lean/MidnightExpress/Examples.lean').read_text())
