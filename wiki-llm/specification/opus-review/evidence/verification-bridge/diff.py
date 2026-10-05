"""Scratch differential harness for the Python validator and Lean `validate`/`check`.
Reuses check.py's translator unchanged. Writes only into this scratch directory."""
import copy, json, random, sys
from pathlib import Path
ROOT = Path('/home/hoskinson/Projects/midnight-express')
sys.path.insert(0, str(ROOT / 'formal/lean'))
import check
from validator import Harness, Invalid, raw_json, proposal_digest, digest, business_digest

OUT = Path('/tmp/mpe-lean-opus-review/verification-bridge')
CTX = raw_json((ROOT / 'model/conformance/trusted-context.json').read_bytes())
BASE = {n: raw_json((ROOT / f'model/examples/{n}.json').read_bytes())
        for n in ('rfq', 'agent', 'invoice-final', 'invoice-pending', 'invoice-reversed')}
T = lambda hhmmss: f'2026-10-04T{hhmmss}.000Z'

def rehash(e, c):
    d = e['data']
    if 'proposal' in d:
        d['proposalDigest'] = proposal_digest(d['proposal'], e['mpecontract'])
        c['proposals'][d['actionId']] = copy.deepcopy(d['proposal'])

def sync_evidence(e, c):
    c['paymentEvidence'][e['data']['paymentId']] = copy.deepcopy(e['data'])

def sync_rfq(e, c):
    ref = c['rfqs'][e['data']['rfqId']]
    for k in ('requester', 'dealer', 'requesterSide', 'asset', 'quantity', 'currency'):
        ref[k] = copy.deepcopy(e['data'][k])

# Each mutation: (name, profile, function(e, c)) intended to falsify one Lean conjunct.
def m(fn):
    return fn
MUT = []
def mut(name, profile):
    def wrap(fn): MUT.append((name, profile, fn)); return fn
    return wrap

@mut('q_not_yet_valid', 'rfq')
def _(e, c): e['data']['validFrom'] = T('12:30:00')
@mut('q_occurred_after_validFrom', 'rfq')
def _(e, c): e['time'] = T('11:00:01')
@mut('q_buyer_equals_seller', 'rfq')
def _(e, c):
    d = e['data']; d['requester'] = d['dealer']; d['buyer'] = d['dealer']; d['seller'] = d['dealer']; sync_rfq(e, c)
@mut('q_price_scale_3', 'rfq')
def _(e, c): e['data']['price']['value']['scale'] = 3
@mut('q_cash_product_above_bound', 'rfq')
def _(e, c):
    d = e['data']; d['price']['value']['coefficient'] = '999999999999999999'
    d['cash']['coefficient'] = str(int(d['quantity']['coefficient']) * 999999999999999999)
@mut('q_base_quantity_2', 'rfq')
def _(e, c): e['data']['price']['baseQuantity'] = 2
@mut('q_quantity_zero', 'rfq')
def _(e, c): e['data']['quantity']['coefficient'] = '0'; e['data']['cash']['coefficient'] = '0'; sync_rfq(e, c)
@mut('q_quantity_unit_step', 'rfq')
def _(e, c):
    e['data']['quantity']['unit'] = 'Step'; e['data']['price']['unit'] = 'Step'; sync_rfq(e, c)
@mut('env_dataschema', 'rfq')
def _(e, c): e['dataschema'] = 'urn:mpe:model:invoice.v0.2'
@mut('env_type', 'rfq')
def _(e, c): e['type'] = 'mpe.agent.approval.v0.2'
@mut('env_specversion', 'rfq')
def _(e, c): e['specversion'] = '1.1'
@mut('env_contenttype', 'rfq')
def _(e, c): e['datacontenttype'] = 'text/plain'
@mut('env_contract_alone', 'rfq')
def _(e, c): e['mpecontract'] = 'sha256:' + '7' * 64
@mut('src_wrong_role_right_principal', 'rfq')
def _(e, c): c['sources'][e['source']]['role'] = 'human-approver'
@mut('i_terms_mismatch', 'invoice')
def _(e, c): e['data']['documentDigest'] = 'sha256:' + '2' * 64; sync_evidence(e, c)
@mut('i_effective_after_observed', 'invoice')
def _(e, c): e['data']['effectiveAt'] = T('11:00:01'); e['data']['observedAt'] = T('11:00:00'); sync_evidence(e, c)
@mut('i_amount_zero', 'invoice')
def _(e, c): e['data']['amount']['coefficient'] = '0'; sync_evidence(e, c)
@mut('i_other_rail', 'invoice')
def _(e, c):
    e['data']['rail'] = 'other-bank-v1'; sync_evidence(e, c); c['sources'][e['source']]['principal'] = 'other-bank-v1'
@mut('i_payable_scale_3', 'invoice')
def _(e, c):
    e['data']['payable']['scale'] = 3; sync_evidence(e, c); c['invoices'][e['data']['invoiceId']]['payable']['scale'] = 3
@mut('a_execution_scope', 'agent')
def _(e, c): e['data']['executionScope'] = 'scope:other'
@mut('a_occurred_after_validFrom', 'agent')
def _(e, c): e['time'] = T('11:00:01')
@mut('a_not_yet_valid', 'agent')
def _(e, c): e['data']['validFrom'] = T('12:30:00')
@mut('a_validUntil_after_expires', 'agent')
def _(e, c): e['data']['validUntil'] = T('13:00:01')
@mut('a_wrong_digest_same_proposal', 'agent')
def _(e, c): e['data']['proposalDigest'] = 'sha256:' + '5' * 64
@mut('a_human_not_listed', 'agent')
def _(e, c): c['humans'] = []
@mut('a_ctx_window', 'agent')
def _(e, c): c['budgetWindow'] = 'window:other'
@mut('a_ctx_domain', 'agent')
def _(e, c): c['authorityDomain'] = 'urn:mpe:sandbox:other'
@mut('a_max_effects_2', 'agent')
def _(e, c): e['data']['maxEffects'] = 2
@mut('a_budget_zero', 'agent')
def _(e, c): e['data']['proposal']['budget']['coefficient'] = '0'; rehash(e, c)
@mut('a_budget_unit_share', 'agent')
def _(e, c): e['data']['proposal']['budget']['unit'] = 'Share'; rehash(e, c)
@mut('a_domain_literal_both', 'agent')
def _(e, c): e['data']['authorityDomain'] = 'urn:mpe:sandbox:other'; c['authorityDomain'] = 'urn:mpe:sandbox:other'
@mut('a_window_literal_both', 'agent')
def _(e, c): e['data']['budgetWindow'] = 'window:other'; c['budgetWindow'] = 'window:other'

@mut('q_quantity_scale_1', 'rfq')
def _(e, c): e['data']['quantity']['scale'] = 1; sync_rfq(e, c)
@mut('q_buyer_only_wrong', 'rfq')
def _(e, c): e['data']['buyer'] = 'party:third'
@mut('q_seller_only_wrong', 'rfq')
def _(e, c): e['data']['seller'] = 'party:third'
@mut('q_price_unit_step', 'rfq')
def _(e, c): e['data']['price']['unit'] = 'Step'
@mut('i_future_occurrence', 'invoice')
def _(e, c): e['time'] = T('12:00:01')

def base_for(profile, rng=None):
    if profile == 'invoice':
        return BASE[rng.choice(['invoice-final', 'invoice-pending', 'invoice-reversed']) if rng else 'invoice-final']
    return BASE[profile]

def python_verdict(e, c, harness=None):
    try:
        return (harness or Harness(copy.deepcopy(c))).check(json.dumps(e, separators=(',', ':')))['status']
    except Invalid:
        return 'reject'

LEAN = {'reject': 'none', 'offchain-quote-valid': 'some (observation .quote)',
        'sandbox-candidate-only': 'some (observation .candidate)',
        'final-payment-evidence-only': 'some (observation .paymentFinal)',
        'payment-evidence-pending-or-reversed': 'some (observation .paymentOther)'}
HEADER = ['import MidnightExpress.Validation', 'set_option maxRecDepth 100000', 'set_option maxHeartbeats 0',
          'open MidnightExpress', '']

def targeted():
    lines = list(HEADER); skipped = []
    for i, (name, profile, fn) in enumerate(MUT):
        e, c = copy.deepcopy(base_for(profile)), copy.deepcopy(CTX); fn(e, c)
        expected = python_verdict(e, c)
        try:
            ev, cx = check.event(e), check.context(c, e)
        except (KeyError, AssertionError) as err:
            skipped.append((name, repr(err))); continue
        lines += [f'-- {name}: python={expected}', f'def tev{i} : Event := {ev}', f'def tcx{i} : Context := {cx}',
                  f'example : validate tcx{i} tev{i} = {LEAN[expected]} := by decide', '']
        print(name, expected)
    (OUT / 'targeted.lean').write_text('\n'.join(lines))
    print('skipped (untranslatable):', skipped)

def fuzz(n, seed):
    rng = random.Random(seed); cases = []; untranslatable = 0
    by_profile = {}
    for name, profile, fn in MUT: by_profile.setdefault(profile, []).append((name, fn))
    shifts = {'rfq': [('data', 'validFrom'), ('data', 'validUntil'), (None, 'time')],
              'agent': [('data', 'validFrom'), ('data', 'validUntil'), (None, 'time')],
              'invoice': [('data', 'observedAt'), ('data', 'effectiveAt'), (None, 'time')]}
    import datetime
    while len(cases) < n:
        profile = rng.choice(['rfq', 'invoice', 'agent'])
        e, c = copy.deepcopy(base_for(profile, rng)), copy.deepcopy(CTX); applied = []
        for _ in range(rng.randint(0, 3)):
            kind = rng.random()
            if kind < 0.5:
                name, fn = rng.choice(by_profile[profile] + (by_profile['rfq'][8:14] if profile != 'rfq' else []))
                try: fn(e, c)
                except KeyError: continue
                applied.append(name)
            else:
                where, field = rng.choice(shifts[profile]); delta = rng.choice([-3600, -1, 1, 3600])
                target = e['data'] if where else e
                t = datetime.datetime.strptime(target[field], '%Y-%m-%dT%H:%M:%S.000Z') + datetime.timedelta(seconds=delta)
                target[field] = t.strftime('%Y-%m-%dT%H:%M:%S.000Z'); applied.append(f'{field}{delta:+d}')
                if profile == 'invoice' and rng.random() < 0.7: sync_evidence(e, c)
        expected = python_verdict(e, c)
        try: cases.append((applied, check.event(e), check.context(c, e), expected))
        except (KeyError, AssertionError): untranslatable += 1
    lines = list(HEADER)
    for i, (_, ev, cx, _) in enumerate(cases):
        lines += [f'def fev{i} : Event := {ev}', f'def fcx{i} : Context := {cx}']
    lines.append('def fuzzCases : List (Nat × Context × Event × Option Result) := [' + ', '.join(
        f'({i}, fcx{i}, fev{i}, {LEAN[x]})' for i, (_, _, _, x) in enumerate(cases)) + ']')
    lines += ['#eval do', '  let bad := fuzzCases.filter (fun (p : Nat × Context × Event × Option Result) => validate p.2.1 p.2.2.1 != p.2.2.2)',
              '  IO.println s!"FUZZ total={fuzzCases.length} mismatches={bad.map (fun (p : Nat × Context × Event × Option Result) => p.1)}"']
    (OUT / 'fuzz.lean').write_text('\n'.join(lines))
    from collections import Counter
    print('fuzz cases', len(cases), 'untranslatable skipped', untranslatable, Counter(x for *_, x in cases))
    json.dump([(i, a, x) for i, (a, _, _, x) in enumerate(cases)], open(OUT / 'fuzz-index.json', 'w'))

if __name__ == '__main__':
    if sys.argv[1] == 'targeted': targeted()
    else: fuzz(int(sys.argv[2]), int(sys.argv[3]))
