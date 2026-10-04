"""Bounded v0.1 reference MODEL validator. Never executes, authenticates, or fetches."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import rfc8785
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
MAX_BODY = 3926
class Invalid(ValueError):
    pass

def raw_json(raw):
    if isinstance(raw, bytes):
        raw = raw.decode('utf-8', errors='strict')
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise Invalid('duplicate-json-key')
            out[key] = value
        return out
    def bad(value):
        raise Invalid('non-json-number')
    value = json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    def bounded(node, depth=0):
        if depth > 12:
            raise Invalid('depth')
        if isinstance(node, str):
            node.encode('utf-8', errors='strict')
            if len(node) > 512:
                raise Invalid('string-bound')
        elif isinstance(node, dict):
            for k, v in node.items():
                bounded(k, depth+1); bounded(v, depth+1)
        elif isinstance(node, list):
            if len(node) > 16:
                raise Invalid('array-bound')
            for v in node:
                bounded(v, depth+1)
    bounded(value)
    return value

def digest(obj):
    return 'sha256:' + hashlib.sha256(rfc8785.dumps(obj)).hexdigest()

def file_digest(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()

def instant(text):
    if not isinstance(text, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.000Z', text):
        raise Invalid('utc-format')
    try:
        return dt.datetime.strptime(text, '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=dt.timezone.utc)
    except ValueError as e:
        raise Invalid('utc-calendar') from e

def proposal_digest(proposal, contract):
    return digest({'domain':'mpe.model.proposal.v0.1', 'contract':contract, 'proposal':proposal})

def business_digest(event):
    # Deliberately excludes occurrence id/time and all outer envelope bytes/EID.
    return digest({'domain':'mpe.model.intent.v0.1', 'source':event['source'],
                   'type':event['type'], 'profile':event['mpeprofile'],
                   'contract':event['mpecontract'], 'data':event['data']})

def load_profile(name):
    lock = raw_json((ROOT/'profiles/lock.json').read_bytes())
    if name not in lock:
        raise Invalid('unknown-profile')
    manifest = raw_json((ROOT/'profiles'/f'{name}.json').read_bytes())
    if digest(manifest) != lock[name]:
        raise Invalid('local-manifest-integrity')
    for path, expected in manifest['resources'].items():
        local = ROOT/path
        if not local.is_relative_to(ROOT) or file_digest(local) != expected:
            raise Invalid('local-resource-integrity')
    return manifest, lock[name]

class Harness:
    """In-memory trusted TEST FIXTURE state. No durable/atomic authorization guarantee."""
    def __init__(self, context):
        self.context = context
        self.events = {}
        self.actions = {}
    def check(self, raw, eid=None):
        try:
            if len(raw.encode('utf-8') if isinstance(raw,str) else raw) > MAX_BODY:
                raise Invalid('body-bound')
            e = raw_json(raw)
            if not isinstance(e, dict):
                raise Invalid('event-object')
            m, contract = load_profile(e.get('mpeprofile'))
            if e.get('mpecontract') != contract:
                raise Invalid('profile-hash')
            schema = raw_json((ROOT/m['schema']).read_bytes())
            Draft202012Validator(schema).validate(e)
            c = self.context
            if c.get('fixtureTrust') != 'trusted-test-fixture-only':
                raise Invalid('insufficient-trusted-context')
            now = instant(c['now'])
            occurred = instant(e['time'])
            if occurred > now:
                raise Invalid('future-occurrence')
            d = e['data']
            # An authentic role is simulated only by explicit locally trusted fixture entries.
            authority = c['sources'].get(e['source'])
            if not isinstance(authority, dict) or authority.get('role') != m['role']:
                raise Invalid('source-role')
            subject = d['dealer'] if e['mpeprofile']=='rfq.v0.1' else d['human'] if e['mpeprofile']=='agent.v0.1' else d['rail']
            if authority.get('principal') != subject:
                raise Invalid('source-principal')
            result = self._semantic(e, now)
            identity = (e['source'], e['id'])
            eventhash = digest(e)
            intent = business_digest(e)
            if identity in self.events:
                if self.events[identity] != eventhash:
                    raise Invalid('event-identity-conflict')
                return {'status':'duplicate-event', 'businessDigest':intent, 'executes':False}
            if e['mpeprofile'] == 'agent.v0.1':
                key = (d['proposal']['target'], d['actionId'])
                if key in self.actions:
                    if self.actions[key] != intent:
                        raise Invalid('action-identity-conflict')
                    return {'status':'duplicate-action', 'businessDigest':intent, 'executes':False}
                self.actions[key] = intent
            self.events[identity] = eventhash
            return {'status':result, 'businessDigest':intent, 'executes':False}
        except Invalid:
            raise
        except (ValueError, TypeError, KeyError, UnicodeError, OSError) as err:
            raise Invalid('invalid-or-insufficient-input') from err
        except Exception as err:
            # Includes jsonschema validation failures; never repair or dispatch partial input.
            raise Invalid('schema-or-validation-failure') from err
    def _semantic(self, e, now):
        d = e['data']; p = e['mpeprofile']; c = self.context
        if p == 'rfq.v0.1':
            ref = c['rfqs'].get(d['rfqId'])
            if ref is None or ref['state'] != 'open':
                raise Invalid('unknown-or-closed-rfq')
            for field in ('requester','dealer','requesterSide','asset','quantity','currency'):
                if d[field] != ref[field]:
                    raise Invalid('rfq-terms-mismatch')
            buyer, seller = (d['requester'],d['dealer']) if d['requesterSide']=='BuyAsset' else (d['dealer'],d['requester'])
            if buyer == seller or (d['buyer'],d['seller']) != (buyer,seller):
                raise Invalid('side-mismatch')
            if d['price']['assetRef'] != d['asset'] or d['price']['unit'] != d['quantity']['unit'] or d['price']['currency'] != d['currency']:
                raise Invalid('price-basis-mismatch')
            if not instant(e['time']) <= instant(d['validFrom']) <= now < instant(d['validUntil']):
                raise Invalid('quote-validity')
            # Integer cents; no silent rounding or floating point conversion.
            cash = int(d['quantity']['coefficient']) * int(d['price']['value']['coefficient'])
            if cash > 999999999999999999 or int(d['cash']['coefficient']) != cash:
                raise Invalid('cash-obligation-mismatch')
            return 'offchain-quote-valid'
        if p == 'invoice.v0.1':
            inv = c['invoices'].get(d['invoiceId'])
            if inv is None or any(d[k] != inv[k] for k in ('supplier','customer','currency','payable','documentDigest')):
                raise Invalid('invoice-mismatch')
            if instant(d['observedAt']) > now or instant(d['effectiveAt']) > instant(d['observedAt']):
                raise Invalid('evidence-time')
            record = c['paymentEvidence'].get(d['paymentId'])
            if record != d:
                raise Invalid('insufficient-payment-evidence')
            if d['status'] != 'Final':
                return 'payment-evidence-pending-or-reversed'
            if int(d['amount']['coefficient']) > int(d['payable']['coefficient']):
                raise Invalid('overpayment-outside-profile')
            return 'final-payment-evidence-only'
        if p == 'agent.v0.1':
            prop = d['proposal']
            if d['proposalDigest'] != proposal_digest(prop, e['mpecontract']):
                raise Invalid('proposal-hash')
            expected = c['proposals'].get(d['actionId'])
            if expected != prop or d['policyDigest'] != c['policyDigest']:
                raise Invalid('proposal-or-policy-mismatch')
            if d['human'] not in c['humans'] or d['actionId'] in c['revokedActions']:
                raise Invalid('human-or-revocation')
            if not instant(e['time']) <= instant(d['validFrom']) <= now < instant(d['validUntil']) <= instant(prop['expires']):
                raise Invalid('approval-validity')
            if prop['target'] not in c['sandboxTargets'] or int(prop['budget']['coefficient']) > c['maxSteps']:
                raise Invalid('sandbox-capability')
            return 'sandbox-candidate-only'
        raise Invalid('unsupported-profile')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('event', type=Path)
    parser.add_argument('--context', type=Path, required=True, help='explicit trusted TEST fixture; never sender evidence')
    args = parser.parse_args()
    try:
        print(json.dumps(Harness(raw_json(args.context.read_bytes())).check(args.event.read_bytes()), sort_keys=True))
    except Invalid as err:
        parser.exit(1, str(err)+'\n')
