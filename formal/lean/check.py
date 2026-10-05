#!/usr/bin/env python3
"""Finite Python/Lean conformance on real JSON fixtures and semantic mutations.

Generates kernel-checked `by decide` examples; never calls native_decide.
This bridge is a trusted test translator, not a verified parser or refinement.
Run with the Python environment containing model/requirements.lock.txt packages.
"""
import argparse
import copy
import datetime
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / 'model'))
from validator import Harness, Invalid, raw_json, proposal_digest


def string(value):
    return json.dumps(value, ensure_ascii=False)


def record(fields):
    return '{ ' + ', '.join(f'{key} := {value}' for key, value in fields.items()) + ' }'


def instant(value):
    return str(int(datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.000Z').replace(
        tzinfo=datetime.timezone.utc).timestamp()))


def decimal(d):
    return record({'coefficient': str(int(d['coefficient'])), 'scale': str(d['scale'])})


def quantity(d):
    return record({'value': decimal(d), 'unit': {'Share': '.share', 'Step': '.step'}[d['unit']]})


def proposal(d):
    assert d['environment'] == 'Sandbox' and d['operation'] == 'WriteReport'
    return record({'environment': '.sandbox', 'operation': '.writeReport',
        'target': string(d['target']), 'inputDigest': string(d['inputDigest']),
        'budget': quantity(d['budget']), 'expires': instant(d['expires'])})


def rfq_terms(d):
    assert d['currency'] == 'iso4217:USD'
    return record({'requester': string(d['requester']), 'dealer': string(d['dealer']),
        'requesterSide': {'BuyAsset': '.buy', 'SellAsset': '.sell'}[d['requesterSide']],
        'asset': string(d['asset']), 'quantity': quantity(d['quantity']), 'currency': '.usd'})


def invoice_terms(d):
    assert d['currency'] == 'iso4217:USD'
    return record({**{k: string(d[k]) for k in ('supplier', 'customer', 'documentDigest')},
        'currency': '.usd', 'payable': decimal(d['payable'])})


def invoice(d):
    return record({'invoiceId': string(d['invoiceId']), 'terms': invoice_terms(d),
        'paymentId': string(d['paymentId']), 'amount': decimal(d['amount']),
        'status': {'Final': '.final', 'Pending': '.pending', 'Reversed': '.reversed'}[d['status']],
        'observedAt': instant(d['observedAt']), 'effectiveAt': instant(d['effectiveAt']),
        'rail': string(d['rail'])})


def event(e):
    env = record({**{k: string(e[k]) for k in ('specversion', 'id', 'source')},
        'eventType': string(e['type']), 'occurred': instant(e['time']),
        'contentType': string(e['datacontenttype']), 'dataSchema': string(e['dataschema']),
        'profile': string(e['mpeprofile']), 'contract': string(e['mpecontract'])})
    d = e['data']
    if 'rfqId' in d:
        p = d['price']
        assert p['currency'] == 'iso4217:USD' and p['kind'] == 'AbsolutePerUnit' and p['fees'] == 'None'
        assert d['quoteKind'] == 'Firm' and d['settlement'] == 'OffchainCoordinationOnly'
        payload = '.rfq ' + record({'rfqId': string(d['rfqId']), 'quoteId': string(d['quoteId']),
            'terms': rfq_terms(d), 'buyer': string(d['buyer']), 'seller': string(d['seller']),
            'price': record({'value': decimal(p['value']), 'currency': '.usd',
                'assetRef': string(p['assetRef']), 'unit': {'Share': '.share', 'Step': '.step'}[p['unit']],
                'baseQuantity': str(int(p['baseQuantity'])), 'fees': '.none'}),
            'cash': decimal(d['cash']), 'validFrom': instant(d['validFrom']),
            'validUntil': instant(d['validUntil'])})
    elif 'invoiceId' in d:
        payload = '.invoice ' + invoice(d)
    else:
        payload = '.agent ' + record({**{k: string(d[k]) for k in ('authorityDomain',
            'executionScope', 'budgetWindow', 'actionId', 'proposalDigest', 'policyDigest', 'human')},
            'proposal': proposal(d['proposal']), 'validFrom': instant(d['validFrom']),
            'validUntil': instant(d['validUntil']), 'maxEffects': str(d['maxEffects'])})
    return record({'envelope': env, 'payload': payload})


def table(items, convert):
    return '[' + ', '.join(f'({string(k)}, {convert(v)})' for k, v in items.items()) + ']'


def context(c, e):
    roles = {'dealer': '.dealer', 'payment-adapter': '.paymentAdapter', 'human-approver': '.humanApprover'}
    def authority(a):
        return record({'role': roles[a['role']], 'principal': string(a['principal'])})
    commitments = 'fun _ _ => ""'
    if 'proposal' in e['data']:
        p = e['data']['proposal']
        commitments = ('fun p contract => if p = ' + proposal(p) + ' ∧ contract = ' +
            string(e['mpecontract']) + ' then ' + string(proposal_digest(p, e['mpecontract'])) + ' else ""')
    return record({'trusted': str(c.get('fixtureTrust') == 'trusted-test-fixture-only').lower(),
        'now': instant(c['now']), 'sources': table(c['sources'], authority),
        'rfqs': table(c['rfqs'], lambda q: '(' + str(q['state'] == 'open').lower() + ', ' + rfq_terms(q) + ')'),
        'invoices': table(c['invoices'], invoice_terms), 'paymentEvidence': table(c['paymentEvidence'], invoice),
        **{k: string(c.get(k, '')) for k in ('authorityDomain', 'executionScope', 'budgetWindow', 'policyDigest')},
        'proposals': table(c['proposals'], proposal),
        **{k: '[' + ', '.join(map(string, c[k])) + ']' for k in ('humans', 'revokedActions', 'sandboxTargets')},
        'maxSteps': str(c['maxSteps']), 'proposalDigest': commitments})


def collect():
    c = raw_json((ROOT / 'model/conformance/trusted-context.json').read_bytes())
    cases = []
    def add(label, e, expected, ctx=None):
        cases.append((label, copy.deepcopy(e), expected, copy.deepcopy(c if ctx is None else ctx)))
    examples = {}
    for label, expected in [('rfq', 'offchain-quote-valid'), ('agent', 'sandbox-candidate-only'),
        ('invoice-final', 'final-payment-evidence-only'), ('invoice-pending', 'payment-evidence-pending-or-reversed'),
        ('invoice-reversed', 'payment-evidence-pending-or-reversed')]:
        examples[label] = raw_json((ROOT / f'model/examples/{label}.json').read_bytes())
        add('fixture_' + label, examples[label], expected)
    # This slice deliberately omits lexical/schema-only failures that typed decoding cannot represent.
    for name in ('side', 'cash', 'expired', 'expired-approval', 'price-asset',
        'payment-final-invention', 'missing-payment-evidence', 'unauthorized-human',
        'changed-target', 'changed-input', 'profile-hash', 'unknown-profile'):
        add('corpus_' + name, raw_json((ROOT / f'model/conformance/{name}.json').read_bytes()), 'reject')
    a, q, inv = examples['agent'], examples['rfq'], examples['invoice-final']
    for label in ('no-trust', 'revoked', 'low-budget', 'no-role', 'wrong-principal', 'no-proposal', 'unknown-target', 'wrong-policy'):
        changed = copy.deepcopy(c)
        if label == 'no-trust': changed.pop('fixtureTrust')
        if label == 'revoked': changed['revokedActions'] = [a['data']['actionId']]
        if label == 'low-budget': changed['maxSteps'] = 4
        if label == 'no-role': changed['sources'] = {}
        if label == 'wrong-principal': changed['sources'][a['source']]['principal'] = 'human:bob'
        if label == 'no-proposal': changed['proposals'] = {}
        if label == 'unknown-target': changed['sandboxTargets'] = []
        if label == 'wrong-policy': changed['policyDigest'] = 'sha256:' + '4' * 64
        add('context_' + label, a, 'reject', changed)
    for label, base in [('quote', q), ('approval', a)]:
        for bound, expected in [('validFrom', 'offchain-quote-valid' if label == 'quote' else 'sandbox-candidate-only'),
                                ('validUntil', 'reject')]:
            changed = copy.deepcopy(c); changed['now'] = base['data'][bound]
            add(label + '_at_' + bound, base, expected, changed)
    changed = copy.deepcopy(q); changed['data']['requesterSide'] = 'SellAsset'
    changed['data']['buyer'], changed['data']['seller'] = changed['data']['seller'], changed['data']['buyer']
    ctx = copy.deepcopy(c); ctx['rfqs'][q['data']['rfqId']]['requesterSide'] = 'SellAsset'
    add('sell_side', changed, 'offchain-quote-valid', ctx)
    changed = copy.deepcopy(q); changed['data']['quantity']['coefficient'] = '999999999999999999'
    ctx = copy.deepcopy(c); ctx['rfqs'][q['data']['rfqId']]['quantity'] = changed['data']['quantity']
    add('cash_overflow', changed, 'reject', ctx)
    changed = copy.deepcopy(a); changed['data']['proposal']['target'] = 'sandbox:reports/other'
    changed['data']['proposalDigest'] = proposal_digest(changed['data']['proposal'], changed['mpecontract'])
    add('rehashed_changed_proposal', changed, 'reject')
    changed = copy.deepcopy(inv); changed['time'] = '2026-10-04T10:00:00.000Z'
    add('observation_after_occurrence', changed, 'reject')
    changed = copy.deepcopy(inv); changed['data']['amount']['coefficient'] = '50001'
    ctx = copy.deepcopy(c); ctx['paymentEvidence'][changed['data']['paymentId']] = changed['data']
    add('complete_evidence_overpayment', changed, 'reject', ctx)
    changed = copy.deepcopy(q); changed['time'] = '2026-10-04T12:00:01.000Z'
    add('future_occurrence', changed, 'reject')
    ctx = copy.deepcopy(c); ctx['rfqs'][q['data']['rfqId']]['state'] = 'closed'
    add('closed_rfq', q, 'reject', ctx)
    return cases


def generate(cases):
    verdicts = {'offchain-quote-valid': '.quote', 'sandbox-candidate-only': '.candidate',
        'final-payment-evidence-only': '.paymentFinal', 'payment-evidence-pending-or-reversed': '.paymentOther'}
    lines = ['import MidnightExpress.Validation', '', '/- Generated by check.py from actual JSON fixtures and semantic mutations.',
        '   Kernel-checked finite examples, not a verified JSON decoder or Python refinement. -/',
        'set_option maxRecDepth 100000', 'set_option maxHeartbeats 0', '', 'namespace MidnightExpress.Examples', '']
    for index, (label, e, expected, ctx) in enumerate(cases):
        try:
            actual = Harness(copy.deepcopy(ctx)).check(json.dumps(e, separators=(',', ':')))['status']
        except Invalid:
            actual = 'reject'
        assert actual == expected, (label, expected, actual)
        lines += [f'-- {label}: {expected}', f'def event{index} : Event := {event(e)}',
            f'def context{index} : Context := {context(ctx, e)}']
        result = 'none' if expected == 'reject' else 'some (observation ' + verdicts[expected] + ')'
        lines += [f'example : validate context{index} event{index} = {result} := by decide', '']
    lines += ['-- Occurrence and action identities are independent. Digests below are abstract tokens.',
        'def remembered : ReplayState := { events := [(("source", "event1"), "whole1")], actions := [(("domain", "scope", "action"), "intent")] }',
        'example : replay remembered ("source", "event1") "whole1" none "intent" .candidate =',
        '  some (observation .duplicateEvent, remembered) := by decide',
        'example : replay remembered ("source", "event1") "changed" none "intent" .candidate = none := by decide',
        'example : (replay remembered ("source", "event2") "whole2"',
        '  (some ("domain", "scope", "action")) "intent" .candidate).map (fun x => x.1.verdict) =',
        '  some .duplicateAction := by decide',
        'example : replay remembered ("source", "event2") "whole2"',
        '  (some ("domain", "scope", "action")) "changed" .candidate = none := by decide',
        '', 'end MidnightExpress.Examples', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true', help='refresh checked-in Examples.lean before checking')
    args = parser.parse_args()
    cases = collect()
    generated = generate(cases)
    path = HERE / 'MidnightExpress/Examples.lean'
    if args.update:
        path.write_text(generated)
    elif not path.exists() or path.read_text() != generated:
        raise SystemExit('Examples.lean is stale: inspect fixture changes and run check.py --update')
    lake = shutil.which('lake')
    if not lake:
        version = (HERE / 'lean-toolchain').read_text().strip().replace(':', '---').replace('/', '--')
        candidate = Path.home() / '.elan/toolchains' / version / 'bin/lake'
        if candidate.exists(): lake = str(candidate)
    if not lake: raise SystemExit('lake not found; install the pinned Lean toolchain or add it to PATH')
    subprocess.run([lake, 'build'], cwd=HERE, check=True)
    print(f'PASS {len(cases)} Python/Lean semantic cases and 4 kernel-checked replay examples')
    print('Boundary: trusted Python translator + external commitment calculation; no parser/hash/runtime refinement proof.')


if __name__ == '__main__':
    main()
