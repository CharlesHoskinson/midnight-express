"""Stateful, language-neutral scenarios, including current-context changes."""
import copy
from mutations import rehash


def collect_sequences(cases):
    fixture = {label: (e, c) for label, e, _, c in cases if label.startswith('fixture_')}
    result = []
    for label in ('rfq', 'invoice-final', 'agent'):
        base, context = fixture['fixture_' + label]
        e, c = copy.deepcopy(base), copy.deepcopy(context)
        steps = []
        def add(name, event=e, ctx=c):
            steps.append({'label': name, 'event': copy.deepcopy(event), 'context': copy.deepcopy(ctx)})
        add('fresh'); add('same-occurrence-retry')
        e['id'] = 'event:new-' + label; add('same-action-new-occurrence' if label == 'agent' else 'fresh-new-occurrence')
        if label == 'agent':
            e['id'] = base['id']; e['time'] = '2026-10-04T11:00:01.000Z'; e['data']['validFrom'] = e['time']
            add('same-occurrence-changed-metadata')
            e, c = copy.deepcopy(base), copy.deepcopy(context)
            e['id'] = 'event:expiry-change'; e['data']['proposal']['expires'] = '2026-10-04T14:00:00.000Z'
            e['data']['validUntil'] = e['data']['proposal']['expires']; rehash(e, c)
            add('changed-expiry-current-context', e, c)
            e, c = copy.deepcopy(base), copy.deepcopy(context)
            e['id'] = 'event:target-change'; e['data']['proposal']['target'] = 'sandbox:reports/other'
            c['sandboxTargets'].append(e['data']['proposal']['target']); rehash(e, c)
            add('changed-target-current-context', e, c)
            c = copy.deepcopy(context); c['now'] = base['data']['validUntil']; add('expired-retry', base, c)
            c = copy.deepcopy(context); c['revokedActions'] = [base['data']['actionId']]; add('revoked-retry', base, c)
            c = copy.deepcopy(context); c['policyDigest'] = 'sha256:' + '4' * 64; add('policy-rotation-stale-retry', base, c)
            e = copy.deepcopy(base); e['id'] = 'event:policy-change'; e['data']['policyDigest'] = c['policyDigest']
            add('policy-rotation-current-event', e, c)
        expected = ['offchain-quote-valid' if label == 'rfq' else 'final-payment-evidence-only' if label == 'invoice-final' else 'sandbox-candidate-only', 'duplicate-event', 'duplicate-action' if label == 'agent' else 'offchain-quote-valid' if label == 'rfq' else 'final-payment-evidence-only']
        if label == 'agent': expected += ['reject'] * 7
        for step, verdict in zip(steps, expected):
            step['expectedVerdict'] = verdict
            if step['label'] in ('same-occurrence-changed-metadata', 'changed-expiry-current-context', 'changed-target-current-context', 'policy-rotation-current-event'):
                step['freshExpectedVerdict'] = 'sandbox-candidate-only'
        result.append({'label': label, 'steps': steps})
    return result
