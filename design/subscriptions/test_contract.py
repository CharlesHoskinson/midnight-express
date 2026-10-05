"""Finite structural checks for the proposed LOCAL contract, no runtime authority."""
import datetime
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((Path(__file__).parent / 'local-subscription-intent.schema.json').read_text())
Draft202012Validator.check_schema(SCHEMA)
FORMATS = FormatChecker()
@FORMATS.checks('date-time', raises=ValueError)
def real_instant(value):
    if not isinstance(value, str):
        return True  # schema type check handles nonstrings
    datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.000Z')
    return True
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FORMATS)

def example(category='quotes'):
    files = {'quotes':'rfq.json','payments':'invoice-final.json','approvals':'agent.json'}
    if category in files:
        event = json.loads((ROOT/'model/examples'/files[category]).read_text())
        profile, contract = event['mpeprofile'], event['mpecontract']
    else:
        profile, contract = 'mock.local.v1', 'mock-only'
    return {'kind':'LocalSubscriptionIntent','version':1,'subscriptionId':'subscription:demo',
            'revision':1,'owner':'principal:demo','shardHandle':'shard:demo-private',
            'selector':{'category':category,'profile':profile,'contract':contract,
                        'sourceEquals':[],'predicate':'all'},
            'start':{'mode':'latest','cursor':''},'expiresAt':'2026-10-04T13:00:00.000Z',
            'sink':{'handle':'sink:local-inbox','maxInFlight':2,'maxQueuedEvents':4,'maxQueuedBytes':16384},
            'requestedState':'active'}

def main():
    count = 0
    def check(record, valid):
        nonlocal count
        errors = list(VALIDATOR.iter_errors(record))
        assert bool(errors) != valid, [e.message for e in errors]
        count += 1
    for category in ['quotes','payments','approvals','contracts','credentials','ops']:
        check(example(category), True)
    for category, predicate in [('payments','payment-final'),('approvals','approval-report')]:
        r=example(category);r['selector']['predicate']=predicate;check(r, True)
    for mode in ['earliest','latest','after']:
        r=example();r['start']={'mode':mode,'cursor':'cursor:demo/000001' if mode=='after' else ''};check(r,True)
    for state in ['paused','unsubscribed']:
        r=example();r['requestedState']=state;r['revision']=2;check(r,True)
    # Every nested object is closed; selectors must stay out of network metadata.
    for path, field, value in [((), 'topic','quotes'),(('selector',),'expression','data.amount > 0'),
                               (('sink',),'url','https://attacker.example/collect'),
                               (('start',),'eventTime','2026-10-04T12:00:00.000Z')]:
        r=example();target=r
        for key in path:target=target[key]
        target[field]=value;check(r,False)
    for field, value in [('owner','https://example.com'),('shardHandle','shard:demo\n'),
                         ('subscriptionId','subscription:demo '),('revision',0),('revision',9007199254740992),
                         ('requestedState','revoked'),('expiresAt','2026-02-30T12:00:00.000Z'),
                         ('expiresAt','0000-01-01T00:00:00.000Z'),('expiresAt','2026-10-04T13:00:00Z')]:
        r=example();r[field]=value;check(r,False)
    for field, value in [('maxInFlight',0),('maxInFlight',65),('maxQueuedEvents',1025),('maxQueuedBytes',4194305),('handle','https://example.com')]:
        r=example();r['sink'][field]=value;check(r,False)
    for field, value in [('contract','sha256:'+'0'*64),('category','credentials'),('predicate','payment-final'),
                         ('sourceEquals',['urn:mpe:source:dealer\n']),('sourceEquals',['urn:mpe:source:dealer']*2)]:
        r=example();r['selector'][field]=value;check(r,False)
    for mode,cursor in [('after',''),('latest','cursor:demo/1'),('earliest','cursor:demo/1')]:
        r=example();r['start']={'mode':mode,'cursor':cursor};check(r,False)
    for key in example():
        r=example();del r[key];check(r,False)
    print(f'PASS {count} finite structural/closure/privacy-boundary checks; schema self-check passed')
    print('No shard authority, cursor ownership, runtime revision enforcement, wire sealing or production privacy tested.')

if __name__ == '__main__':
    main()
