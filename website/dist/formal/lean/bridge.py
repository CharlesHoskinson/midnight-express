"""Strict, finite trusted fixture translator; no verified parser/hash claim.

Each node stores decoded typed values in its wire reconstruction. Object codecs
consume every key, reinsert constructor-fixed tags, and check exact round trips.
Canonical coefficients intentionally have no 18-digit bound: Nat negatives for
semantic bounds (including real overflowing cash products) must remain testable.
"""
import datetime as dt
import json
import re
from dataclasses import dataclass


@dataclass
class Node:
    code: str
    wire: object


def text(value):
    if not isinstance(value, str):
        raise ValueError('expected string')
    # Lean supports \xHH for controls, whereas JSON's \b and \f are invalid.
    escaped = ''.join('\\x%02x' % ord(ch) if ord(ch) < 32 or ord(ch) == 127
                      else '\\\\' if ch == '\\' else '\\"' if ch == '"' else ch
                      for ch in value)
    value.encode('utf-8', errors='strict')
    return Node('"' + escaped + '"', value)


def natural(value):
    if type(value) is not int or value < 0:
        raise ValueError('expected Nat')
    return Node(str(value), int(value))


def coefficient(value):
    if not isinstance(value, str) or not re.fullmatch(r'0|[1-9][0-9]*', value):
        raise ValueError('noncanonical coefficient')
    n = int(value)
    return Node(str(n), str(n))


def instant(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.000Z', value):
        raise ValueError('noncanonical instant')
    date = dt.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=dt.timezone.utc)
    epoch = int((date - dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)).total_seconds())
    restored = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(seconds=epoch)
    wire = f'{restored.year:04d}-{restored.month:02d}-{restored.day:02d}T{restored.hour:02d}:{restored.minute:02d}:{restored.second:02d}.000Z'
    return Node(str(epoch) if epoch >= 0 else '(' + str(epoch) + ')', wire)


def enum(value, choices):
    if value not in choices:
        raise ValueError('unsupported fixed/enum tag: ' + repr(value))
    code = choices[value]
    return Node(code, next(k for k, v in choices.items() if v == code))


def obj(value, fields, fixed=None):
    """Fields are (Lean name, wire key(s), codec); tuple keys flatten a record."""
    fixed = fixed or {}
    consumed = set(fixed)
    for _, key, _ in fields:
        consumed.update(key if isinstance(key, tuple) else (key,))
    if not isinstance(value, dict) or set(value) != consumed:
        raise ValueError(f'unconsumed/missing object keys: expected {sorted(consumed)}, got {sorted(value) if isinstance(value, dict) else type(value)}')
    if any(value[k] != v for k, v in fixed.items()):
        raise ValueError('unsupported constructor-fixed tag')
    wire, rendered = dict(fixed), []
    for lean, key, codec in fields:
        node = codec({k: value[k] for k in key} if isinstance(key, tuple) else value[key])
        rendered.append(f'{lean} := {node.code}')
        if isinstance(key, tuple): wire.update(node.wire)
        else: wire[key] = node.wire
    node = Node('{ ' + ', '.join(rendered) + ' }', wire)
    if node.wire != value:
        raise ValueError('typed object reconstruction differs from input')
    return node


UNIT = {'Share': '.share', 'Step': '.step'}
RFQ_KEYS = ('requester', 'dealer', 'requesterSide', 'asset', 'quantity', 'currency')
INVOICE_KEYS = ('supplier', 'customer', 'documentDigest', 'currency', 'payable')
ENVELOPE_KEYS = ('specversion', 'id', 'source', 'type', 'time', 'datacontenttype', 'dataschema', 'mpeprofile', 'mpecontract')


def decimal(d):
    return obj(d, [('coefficient', 'coefficient', coefficient), ('scale', 'scale', natural)])


def quantity(d):
    return obj(d, [('value', ('coefficient', 'scale'), decimal), ('unit', 'unit', lambda v: enum(v, UNIT))])


def proposal(d):
    return obj(d, [('environment', 'environment', lambda v: enum(v, {'Sandbox': '.sandbox'})),
                   ('operation', 'operation', lambda v: enum(v, {'WriteReport': '.writeReport'})),
                   ('target', 'target', text), ('inputDigest', 'inputDigest', text),
                   ('budget', 'budget', quantity), ('expires', 'expires', instant)])


def rfq_terms(d):
    return obj(d, [('requester', 'requester', text), ('dealer', 'dealer', text),
                   ('requesterSide', 'requesterSide', lambda v: enum(v, {'BuyAsset': '.buy', 'SellAsset': '.sell'})),
                   ('asset', 'asset', text), ('quantity', 'quantity', quantity),
                   ('currency', 'currency', lambda v: enum(v, {'iso4217:USD': '.usd'}))])


def invoice_terms(d):
    return obj(d, [(k, k, text) for k in ('supplier', 'customer', 'documentDigest')] +
               [('currency', 'currency', lambda v: enum(v, {'iso4217:USD': '.usd'})), ('payable', 'payable', decimal)])


def invoice(d):
    return obj(d, [('invoiceId', 'invoiceId', text), ('terms', INVOICE_KEYS, invoice_terms),
                   ('paymentId', 'paymentId', text), ('amount', 'amount', decimal),
                   ('status', 'status', lambda v: enum(v, {'Final': '.final', 'Pending': '.pending', 'Reversed': '.reversed'})),
                   ('observedAt', 'observedAt', instant), ('effectiveAt', 'effectiveAt', instant), ('rail', 'rail', text)])


def price(d):
    return obj(d, [('value', 'value', decimal), ('currency', 'currency', lambda v: enum(v, {'iso4217:USD': '.usd'})),
                   ('assetRef', 'assetRef', text), ('unit', 'unit', lambda v: enum(v, UNIT)),
                   ('baseQuantity', 'baseQuantity', coefficient), ('fees', 'fees', lambda v: enum(v, {'None': '.none'}))],
               {'kind': 'AbsolutePerUnit'})


def payload(d):
    if 'rfqId' in d:
        n = obj(d, [('rfqId', 'rfqId', text), ('quoteId', 'quoteId', text), ('terms', RFQ_KEYS, rfq_terms),
                    ('buyer', 'buyer', text), ('seller', 'seller', text), ('price', 'price', price),
                    ('cash', 'cash', decimal), ('validFrom', 'validFrom', instant), ('validUntil', 'validUntil', instant)],
                {'quoteKind': 'Firm', 'settlement': 'OffchainCoordinationOnly'})
        return Node('.rfq ' + n.code, n.wire)
    if 'invoiceId' in d:
        n = invoice(d)
        return Node('.invoice ' + n.code, n.wire)
    n = obj(d, [(k, k, text) for k in ('authorityDomain', 'executionScope', 'budgetWindow', 'actionId', 'proposalDigest', 'policyDigest', 'human')] +
            [('proposal', 'proposal', proposal), ('validFrom', 'validFrom', instant), ('validUntil', 'validUntil', instant), ('maxEffects', 'maxEffects', natural)])
    return Node('.agent ' + n.code, n.wire)


def envelope(d):
    return obj(d, [(lean, wire, instant if wire == 'time' else text) for lean, wire in
                   zip(('specversion', 'id', 'source', 'eventType', 'occurred', 'contentType', 'dataSchema', 'profile', 'contract'), ENVELOPE_KEYS)])


def event(e):
    return obj(e, [('envelope', ENVELOPE_KEYS, envelope), ('payload', 'data', payload)]).code


def table(items, codec):
    if not isinstance(items, dict): raise ValueError('expected table object')
    decoded = [(text(k), codec(v)) for k, v in items.items()]
    return Node('[' + ', '.join(f'({k.code}, {v.code})' for k, v in decoded) + ']', {k.wire: v.wire for k, v in decoded})


def strings(values):
    if not isinstance(values, list): raise ValueError('expected string list')
    nodes = [text(v) for v in values]
    return Node('[' + ', '.join(v.code for v in nodes) + ']', [v.wire for v in nodes])


def authority(a):
    return obj(a, [('role', 'role', lambda v: enum(v, {'dealer': '.dealer', 'payment-adapter': '.paymentAdapter', 'human-approver': '.humanApprover'})),
                   ('principal', 'principal', text)])


def rfq_entry(q):
    if set(q) != set(RFQ_KEYS) | {'state'}: raise ValueError('unread RFQ context key')
    terms = rfq_terms({k: q[k] for k in RFQ_KEYS})
    state = enum(q['state'], {'open': 'true', 'closed': 'false'})
    return Node(f'({state.code}, {terms.code})', dict(terms.wire, state=state.wire))


def context(c, commitments):
    keys = {'now', 'sources', 'rfqs', 'invoices', 'paymentEvidence', 'authorityDomain', 'executionScope', 'budgetWindow', 'proposals', 'policyDigest', 'humans', 'revokedActions', 'sandboxTargets', 'maxSteps'}
    if set(c) not in (keys, keys | {'fixtureTrust'}): raise ValueError('unconsumed/missing context keys')
    if 'fixtureTrust' in c and c['fixtureTrust'] != 'trusted-test-fixture-only': raise ValueError('unknown trust tag')
    fields = {'trusted': Node(str('fixtureTrust' in c).lower(), c.get('fixtureTrust')),
              'now': instant(c['now']), 'sources': table(c['sources'], authority),
              'rfqs': table(c['rfqs'], rfq_entry), 'invoices': table(c['invoices'], invoice_terms),
              'paymentEvidence': table(c['paymentEvidence'], invoice), 'proposals': table(c['proposals'], proposal)}
    fields.update({k: text(c[k]) for k in ('authorityDomain', 'executionScope', 'budgetWindow', 'policyDigest')})
    fields.update({k: strings(c[k]) for k in ('humans', 'revokedActions', 'sandboxTargets')})
    fields['maxSteps'] = natural(c['maxSteps'])
    reconstructed = {k: v.wire for k, v in fields.items() if k != 'trusted'}
    if fields['trusted'].wire is not None: reconstructed['fixtureTrust'] = fields['trusted'].wire
    if reconstructed != c: raise ValueError('context typed reconstruction differs')
    return '{ ' + ', '.join(f'{k} := {v.code}' for k, v in fields.items()) + ', proposalDigest := ' + commitments + ' }'
