#!/usr/bin/env python3
"""Finite Python/Lean conformance on real JSON fixtures and semantic mutations.

Generates kernel-checked `by decide` examples; never calls native_decide.
This bridge is a trusted test translator, not a verified parser or refinement.
Run with the Python environment containing model/requirements.lock.txt packages.
"""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / 'model'))
from validator import Harness, Invalid, raw_json, proposal_digest


from bridge import text, proposal, event, context as render_context
from mutations import MUT, decimal_probes
from conditions import conditions
from sequences import collect_sequences
import time

VERDICTS = {"offchain-quote-valid": ".quote", "sandbox-candidate-only": ".candidate",
    "final-payment-evidence-only": ".paymentFinal", "payment-evidence-pending-or-reversed": ".paymentOther",
    "duplicate-event": ".duplicateEvent", "duplicate-action": ".duplicateAction"}
EXEMPTIONS = {"c.sourceKnown": "Absent source necessarily also fails sourceRole and sourcePrincipal.",
    "q.priceCurrency": "Currency has only the usd constructor; unequal currencies are unrepresentable."}

def python_outcome(e, ctx, harness=None):
    h = harness or Harness(copy.deepcopy(ctx))
    h.context = copy.deepcopy(ctx)
    try:
        return h.check(json.dumps(e, separators=(",", ":")))["status"], None
    except Invalid as error:
        return "reject", str(error)

def python_verdict(e, ctx, harness=None):
    return python_outcome(e, ctx, harness)[0]

def lean_result(status):
    return "none" if status == "reject" else "some (observation " + VERDICTS[status] + ")"


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
    add('cash_product_mismatch_at_max_quantity', changed, 'reject', ctx)
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
    for label, profile, mutation in MUT:
        e = copy.deepcopy(examples['invoice-final' if profile == 'invoice' else profile])
        ctx = copy.deepcopy(c)
        mutation(e, ctx)
        add('isolating_' + label, e, 'reject', ctx)
    cases.extend(decimal_probes(examples, c))
    return cases


def commitment_table(cases, sequences):
    entries = {}
    pairs = [(e, c) for _, e, _, c in cases] + [(step['event'], step['context']) for seq in sequences for step in seq['steps']]
    for e, c in pairs:
        for p in list(c['proposals'].values()) + ([e['data']['proposal']] if 'proposal' in e['data'] else []):
            key = (json.dumps(p, sort_keys=True), e['mpecontract'])
            entries[key] = (p, e['mpecontract'], proposal_digest(p, e['mpecontract']))
    return list(entries.values())


def generate(cases):
    sequences = collect_sequences(cases)
    commitments = commitment_table(cases, sequences)
    lines = ['import MidnightExpress.Replay', 'import MidnightExpress.Bridge', '',
        '/- Generated finite evidence: trusted strict translator and external SHA-256; no refinement theorem. -/',
        'set_option maxRecDepth 10000', 'set_option maxHeartbeats 2000000', '', 'namespace MidnightExpress.Examples', '',
        'def fixtureCommitments : List ((Proposal × String) × String) := [' + ', '.join(
            '((' + proposal(p).code + ', ' + text(contract).code + '), ' + text(digest).code + ')' for p, contract, digest in commitments) + ']',
        'def fixtureCommitment (p : Proposal) (contract : String) : String :=',
        '  (lookup (p, contract) fixtureCommitments).getD ""', '']
    escape_probe = ''.join(chr(n) for n in range(32)) + chr(127) + '\\' + '"' + '😀'
    lines += ['example : (' + text(escape_probe).code + '.toList.map Char.toNat) = [' + ', '.join(str(ord(ch)) for ch in escape_probe) + '] := by decide', '']
    vectors, isolation, names = [], {}, set()
    for index, (label, e, expected, ctx) in enumerate(cases):
        actual, reason = python_outcome(e, ctx)
        assert actual == expected, (label, expected, actual)
        checks = conditions(ctx, e); names.update(checks)
        failures = [name for name, passes in checks.items() if not passes]
        if len(failures) == 1: isolation.setdefault(failures[0], []).append(label)
        vectors.append({'label': label, 'event': e, 'context': ctx, 'expectedVerdict': expected, 'pythonReason': reason, 'failingConditions': failures})
        lines += [f'-- {label}: {expected}', f'def event{index} : Event := {event(e)}',
            f'def context{index} : Context := {render_context(ctx, "fixtureCommitment")}',
            f'example : validate context{index} event{index} = {lean_result(expected)} := by decide',
            f'example : Bridge.failingConditions context{index} event{index} = [' + ', '.join(text(x).code for x in failures) + '] := by decide', '']
    assert names - isolation.keys() == EXEMPTIONS.keys(), ('uncovered gates', names - isolation.keys())
    for seq_index, seq in enumerate(sequences):
        h = Harness(copy.deepcopy(seq['steps'][0]['context']))
        refs = []
        for i, step in enumerate(seq['steps']):
            if 'freshExpectedVerdict' in step:
                fresh = python_verdict(step['event'], step['context'])
                assert fresh == step['freshExpectedVerdict'], (step['label'], 'fresh classification', fresh)
            expected, reason = python_outcome(step['event'], step['context'], h)
            step['pythonReason'] = reason
            assert step['expectedVerdict'] == expected, (seq['label'], step['label'], step['expectedVerdict'], expected)
            ref = f'seq{seq_index}step{i}'
            lines += [f'-- {seq["label"]}/{step["label"]}: {expected}',
                f'def {ref}event : Event := {event(step["event"])}',
                f'def {ref}context : Context := {render_context(step["context"], "fixtureCommitment")}']
            refs.append(f'({ref}context, {ref}event)')
        lines += [f'def seq{seq_index} := run {{}} [' + ', '.join(refs) + ']',
            f'example : seq{seq_index}.1.map Prod.snd = [' + ', '.join(lean_result(step['expectedVerdict']) for step in seq['steps']) + '] := by decide',
            f'example : seq{seq_index}.2.events.length = {len(h.events)} := by decide',
            f'example : seq{seq_index}.2.actions.length = {len(h.actions)} := by decide', '']
        seq['expectedJournalCounts'] = {'events': len(h.events), 'actions': len(h.actions)}
    lines += ['end MidnightExpress.Examples', '']
    coverage = {'decimalFacetCases': [label for label, _, _, _ in cases if label.startswith('decimal_')], 'format': 'mpe.semantic-condition-coverage.v1', 'conditions': sorted(names),
        'isolatingCases': dict(sorted(isolation.items())), 'exemptions': EXEMPTIONS,
        'evidence': 'Each listed failingConditions list is independently checked in Lean by decide.'}
    data = {'format': 'mpe.semantic-vectors.v1', 'boundary': 'Already decoded typed values; bounded trusted fixture context; sequential replay; no execution.',
        'commitments': [{'proposal': p, 'contract': c, 'digest': d} for p, c, d in commitments],
        'cases': vectors, 'sequences': sequences}
    return '\n'.join(lines), json.dumps(data, indent=2, ensure_ascii=False) + '\n', json.dumps(coverage, indent=2, ensure_ascii=False) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true', help='refresh Examples and vectors before strict proof gate')
    args = parser.parse_args()
    started = time.monotonic()
    cases = collect()
    artifacts = zip((HERE / 'MidnightExpress/Examples.lean', HERE / 'vectors.json', HERE / 'coverage.json'), generate(cases))
    for path, generated in artifacts:
        if args.update: path.write_text(generated)
        elif not path.exists() or path.read_text() != generated:
            raise SystemExit(f'{path.name} is stale: inspect fixture changes and run check.py --update')
    subprocess.run([sys.executable, '-m', 'unittest', 'test_bridge'], cwd=HERE, check=True, timeout=30)
    # Toolchain verification, --wfail compilation, whole-namespace audit, timeout.
    from proof_gate import run_proof_gate
    metadata = run_proof_gate(HERE)
    print(f'PASS {len(cases)} Python/Lean typed cases; 54 gate atoms, 52 isolated, 2 justified exemptions; 3 structural sequences')
    print(f'Proof gate: {metadata}; total wall seconds: {time.monotonic() - started:.2f}; heartbeat bound per declaration: 2000000')
    print('Evidence: by decide is kernel-checked. Translator, wire parsing and SHA-256 remain outside the proof boundary.')


if __name__ == '__main__':
    main()
