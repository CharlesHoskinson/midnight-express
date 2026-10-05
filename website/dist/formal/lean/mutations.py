"""Deterministic mutations of representable semantic gate conditions."""
import copy
from validator import proposal_digest

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
def _(e, c): e['data']['price']['baseQuantity'] = '2'
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



def decimal_probes(examples, context):
    """Probe each representable Decimal facet, including deliberately invalid Nats."""
    cases = []
    paths = [('rfq', 'quantity'), ('rfq', 'price'), ('rfq', 'cash'),
             ('invoice-final', 'amount'), ('invoice-final', 'payable'), ('agent', 'budget')]
    for profile, field in paths:
        for facet, value in [('zero', '0'), ('above-bound', '1000000000000000000'), ('wrong-scale', None)]:
            e, c = copy.deepcopy(examples[profile]), copy.deepcopy(context)
            d = e['data']
            target = d['price']['value'] if field == 'price' else d['proposal']['budget'] if field == 'budget' else d[field]
            if facet == 'wrong-scale': target['scale'] = 1 if field in ('quantity', 'budget') else 3
            else: target['coefficient'] = value
            if profile == 'rfq':
                if field in ('quantity', 'price'):
                    d['cash']['coefficient'] = str(int(d['quantity']['coefficient']) * int(d['price']['value']['coefficient']))
                sync_rfq(e, c)
            elif profile == 'invoice-final':
                c['invoices'][d['invoiceId']]['payable'] = copy.deepcopy(d['payable']); sync_evidence(e, c)
            else:
                c['maxSteps'] = max(c['maxSteps'], int(target['coefficient'])); rehash(e, c)
            cases.append((f'decimal_{field}_{facet}', e, 'reject', c))
    for profile in ('rfq', 'invoice-final', 'agent'):
        e, c = copy.deepcopy(examples[profile]), copy.deepcopy(context); d = e['data']
        if profile == 'rfq':
            d['quantity']['coefficient'] = '1'; d['price']['value']['coefficient'] = '999999999999999999'
            d['cash']['coefficient'] = '999999999999999999'; sync_rfq(e, c)
            expected = 'offchain-quote-valid'
        elif profile == 'invoice-final':
            d['amount']['coefficient'] = d['payable']['coefficient'] = '999999999999999999'
            c['invoices'][d['invoiceId']]['payable'] = copy.deepcopy(d['payable']); sync_evidence(e, c)
            expected = 'final-payment-evidence-only'
        else:
            d['proposal']['budget']['coefficient'] = '999999999999999999'; c['maxSteps'] = 999999999999999999; rehash(e, c)
            expected = 'sandbox-candidate-only'
        cases.append((f'decimal_{profile}_at-bound', e, expected, c))
    return cases
