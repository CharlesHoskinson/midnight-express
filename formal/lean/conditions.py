"""Independent Python mirror of diagnostic atoms, verified per vector in Lean."""
from validator import proposal_digest, load_profile
from bridge import instant

MAX = 999999999999999999


def stamp(t): return int(instant(t).code.strip('()'))
def valid(d, scale): return 0 < int(d['coefficient']) <= MAX and d['scale'] == scale


def conditions(c, e):
    d, profile = e['data'], e['mpeprofile']
    # Payload constructor, independently of envelope dispatch.
    p = 'rfq.v0.2' if 'rfqId' in d else 'invoice.v0.2' if 'invoiceId' in d else 'agent.v0.2'
    model, contract = load_profile(p)
    expected_type = {'rfq.v0.2': 'mpe.rfq.quote.v0.2', 'invoice.v0.2': 'mpe.invoice.payment-observed.v0.2', 'agent.v0.2': 'mpe.agent.approval.v0.2'}[p]
    principal = d['dealer'] if p == 'rfq.v0.2' else d['rail'] if p == 'invoice.v0.2' else d['human']
    source = c['sources'].get(e['source'])
    now, occurred = stamp(c['now']), stamp(e['time'])
    checks = {'c.trusted': c.get('fixtureTrust') == 'trusted-test-fixture-only',
              'c.profileDecodes': profile == p, 'c.specversion': e['specversion'] == '1.0',
              'c.contentType': e['datacontenttype'] == 'application/json', 'c.contract': e['mpecontract'] == contract,
              'c.eventType': e['type'] == expected_type, 'c.dataSchema': e['dataschema'] == 'urn:mpe:model:' + p,
              'c.notFuture': occurred <= now, 'c.sourceKnown': source is not None,
              'c.sourceRole': source is not None and source['role'] == model['role'],
              'c.sourcePrincipal': source is not None and source['principal'] == principal}
    if p == 'rfq.v0.2':
        ref = c['rfqs'].get(d['rfqId']); price, qty = d['price'], d['quantity']
        buyer, seller = (d['requester'], d['dealer']) if d['requesterSide'] == 'BuyAsset' else (d['dealer'], d['requester'])
        checks.update({'q.openTerms': ref is not None and ref['state'] == 'open' and all(ref[k] == d[k] for k in ('requester','dealer','requesterSide','asset','quantity','currency')),
            'q.buyer': d['buyer'] == buyer, 'q.seller': d['seller'] == seller, 'q.distinct': d['buyer'] != d['seller'],
            'q.assetRef': price['assetRef'] == d['asset'], 'q.priceUnit': price['unit'] == qty['unit'],
            'q.priceCurrency': price['currency'] == d['currency'], 'q.baseQuantity': int(price['baseQuantity']) == 1,
            'q.shareUnit': qty['unit'] == 'Share', 'q.qtyValid': valid(qty, 0), 'q.priceValid': valid(price['value'], 2),
            'q.cashValid': valid(d['cash'], 2), 'q.occ≤from': occurred <= stamp(d['validFrom']),
            'q.from≤now': stamp(d['validFrom']) <= now, 'q.now<until': now < stamp(d['validUntil']),
            'q.cashProduct': int(d['cash']['coefficient']) == int(qty['coefficient']) * int(price['value']['coefficient'])})
    elif p == 'invoice.v0.2':
        ref = c['invoices'].get(d['invoiceId'])
        checks.update({'i.terms': ref is not None and all(ref[k] == d[k] for k in ('supplier','customer','documentDigest','currency','payable')),
            'i.evidence': c['paymentEvidence'].get(d['paymentId']) == d,
            'i.eff≤obs': stamp(d['effectiveAt']) <= stamp(d['observedAt']), 'i.obs≤occ': stamp(d['observedAt']) <= occurred,
            'i.notOver': int(d['amount']['coefficient']) <= int(d['payable']['coefficient']),
            'i.amountValid': valid(d['amount'], 2), 'i.payableValid': valid(d['payable'], 2), 'i.rail': d['rail'] == 'fixture-bank-v1'})
    else:
        prop = d['proposal']
        checks.update({'a.domain': d['authorityDomain'] == c['authorityDomain'], 'a.scope': d['executionScope'] == c['executionScope'],
            'a.window': d['budgetWindow'] == c['budgetWindow'], 'a.digest': d['proposalDigest'] == proposal_digest(prop, e['mpecontract']),
            'a.proposal': c['proposals'].get(d['actionId']) == prop, 'a.policy': d['policyDigest'] == c['policyDigest'],
            'a.human': d['human'] in c['humans'], 'a.notRevoked': d['actionId'] not in c['revokedActions'],
            'a.occ≤from': occurred <= stamp(d['validFrom']), 'a.from≤now': stamp(d['validFrom']) <= now,
            'a.now<until': now < stamp(d['validUntil']), 'a.until≤expires': stamp(d['validUntil']) <= stamp(prop['expires']),
            'a.target': prop['target'] in c['sandboxTargets'], 'a.budget≤max': int(prop['budget']['coefficient']) <= c['maxSteps'],
            'a.budgetValid': valid(prop['budget'], 0), 'a.stepUnit': prop['budget']['unit'] == 'Step',
            'a.maxEffects': d['maxEffects'] == 1, 'a.domainLit': d['authorityDomain'] == 'urn:mpe:sandbox:local',
            'a.windowLit': d['budgetWindow'] == 'window:fixture'})
    return checks
