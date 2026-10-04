"""Maintainer-only deterministic artifact builder; runtime never invokes this or installs profiles."""
from pathlib import Path
import copy
import json
import hashlib
import rfc8785
ROOT = Path(__file__).resolve().parent

def put(path, value):
    (ROOT/path).write_text(json.dumps(value, indent=2, ensure_ascii=True)+'\n')
def digest(obj):
    return 'sha256:'+hashlib.sha256(rfc8785.dumps(obj)).hexdigest()
def object_(properties):
    return {'type':'object','properties':properties,'required':list(properties),'additionalProperties':False}
def enum(*items): return {'enum':list(items)}
def const(value): return {'const':value}
def ident(scope): return {'type':'string','pattern':f'^{scope}:[a-z0-9][a-z0-9._/-]{{0,63}}(?![\\s\\S])','maxLength':80}
def decimal(scale,unit=None):
    fields={'coefficient':{'type':'string','pattern':'^[1-9][0-9]{0,17}(?![\\s\\S])'},'scale':const(scale)}
    if unit: fields['unit']=const(unit)
    return object_(fields)
TIME={'type':'string','pattern':'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.000Z(?![\\s\\S])'}
HASH={'type':'string','pattern':'^sha256:[0-9a-f]{64}(?![\\s\\S])'}
party=ident('party')
proposal=object_({'environment':const('Sandbox'),'operation':const('WriteReport'),'target':ident('sandbox'),
 'inputDigest':HASH,'budget':decimal(0,'Step'),'expires':TIME})
bodies={
 'rfq.v0.2':object_({'rfqId':ident('rfq'),'quoteId':ident('quote'),'requester':party,'dealer':party,
 'requesterSide':enum('BuyAsset','SellAsset'),'buyer':party,'seller':party,'asset':ident('asset'),
 'quantity':decimal(0,'Share'),'currency':const('iso4217:USD'),
 'price':object_({'kind':const('AbsolutePerUnit'),'value':decimal(2),'currency':const('iso4217:USD'),
                 'assetRef':ident('asset'),'unit':const('Share'),'baseQuantity':const('1'),'fees':const('None')}),
 'cash':decimal(2),'quoteKind':const('Firm'),'validFrom':TIME,'validUntil':TIME,'settlement':const('OffchainCoordinationOnly')}),
 'invoice.v0.2':object_({'invoiceId':ident('invoice'),'supplier':party,'customer':party,'documentDigest':HASH,
 'currency':const('iso4217:USD'),'payable':decimal(2),'paymentId':ident('payment'),
 'amount':decimal(2),'status':enum('Pending','Final','Reversed'),'observedAt':TIME,'effectiveAt':TIME,
 'rail':const('fixture-bank-v1')}),
 'agent.v0.2':object_({'authorityDomain':const('urn:mpe:sandbox:local'),'executionScope':ident('scope'),'budgetWindow':const('window:fixture'),'actionId':ident('action'),'proposal':proposal,'proposalDigest':HASH,
                    'policyDigest':HASH,'human':ident('human'),'validFrom':TIME,'validUntil':TIME,'maxEffects':const(1)})}
types={'rfq.v0.2':'mpe.rfq.quote.v0.2','invoice.v0.2':'mpe.invoice.payment-observed.v0.2','agent.v0.2':'mpe.agent.approval.v0.2'}
roles={'rfq.v0.2':'dealer','invoice.v0.2':'payment-adapter','agent.v0.2':'human-approver'}
rules={
 'version':'0.2','status':'experimental-model-only',
 'identity':{'event':'(source,id), immutable complete event','action':'(authorityDomain,executionScope,actionId); target and contract changes conflict; reference candidates only',
             'eid':'opaque transport identifier supplied separately; never computed or used for business replay'},
 'canonicalization':{'algorithm':'RFC8785/JCS UTF-8 then SHA-256','intentDomain':'mpe.model.intent.v0.2',
  'intentFields':['source','type','profile','contract','data'],'proposalDomain':'mpe.model.proposal.v0.2',
  'proposalFields':['contract','proposal'],'manifest':'JCS of entire manifest; lock.json pins it; manifests never include their own hash'},
 'primitives':{'ids':'bounded ASCII scoped identifiers; no normalization','jsonNumbers':'lexical nonnegative integer tokens only, <=9007199254740991; no floating/exponent tokens or negative zero',
 'timestamp':'real UTC calendar YYYY-MM-DDTHH:mm:ss.000Z; no leap seconds; seconds precision only',
 'decimal':'positive canonical coefficient (1..18 digits), value coefficient * 10^-scale; fixed per-field scale, no leading zeros, exponents, sign, zero, floats, coercion or rounding',
 'currency':'only iso4217:USD; pilot asset/unit from trusted RFQ fixture, only whole Share quantities',
 'limits':{'rawBodyBytes':3926,'maxDepth':12,'maxStringCharacters':512,'maxArrayItems':16}},
 'rfq':['open trusted RFQ; requester/dealer/side/asset/quantity/currency exact match',
 'buyer/seller determined by requester side and distinct','absolute USD per exactly one Share, assetRef and unit match; fees None only',
 'occurred <= validFrom <= trusted now < validUntil (exclusive)',
 'cash coefficient equals whole Share coefficient * USD cents price coefficient; 18-digit bound',
 'Firm is fixture business description only; no acceptance, trade execution or settlement'],
 'invoice':['trusted invoice identity, parties, currency, payable and document digest match',
 'payment source must match trusted complete paymentEvidence entry; effectiveAt <= observedAt <= trusted now',
 'Pending/Reversed remain evidence and never imply payment completion',
 'all statuses require amount <= payable; effectiveAt <= observedAt <= event time <= trusted now; event time is observation-record creation',
 'Final remains source assertion only; partial allowed; no posting, allocation, tax or payment execution'],
 'agent':['exact trusted proposal and policy; JCS proposal hash binds complete proposal and profile contract',
 'human locally allowlisted, action not revoked, target locally allowlisted, Step budget within maxSteps',
 'occurred <= validFrom <= now < validUntil <= proposal.expires; maxEffects exactly 1',
 'new event id or EID cannot refresh same action; same action different intent is conflict',
 'Step means one atomic sandbox report-row write; full declared budget reserved at effect boundary then actual one Step charged; fixture authority only',
 'successful check produces sandbox candidate only; no actual execution or authenticated approval'],
 'context':'Explicit trusted test fixture only; missing, stale or insufficient evidence rejects. Production source authentication, policy, clocks, durable atomic replay and finality remain pending.',
 'unsupported':['all unknown fields and enum values','all uninstalled or mismatched schemas/profiles','all remote fetching and RDF reasoning','all LLM repairs and default insertion'],
 'sources':[
 {'concept':'private structured context / occurrence identity','url':'https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md'},
 {'concept':'closed structural validation','url':'https://json-schema.org/draft/2020-12/json-schema-core'},
 {'concept':'canonical business intent','url':'https://www.rfc-editor.org/rfc/rfc8785'},
 {'concept':'quantity units, denominator, buyer/seller; original narrow adaptation','url':'https://cdm.finos.org/docs/product-model/'},
 {'concept':'invoice parties, payable and payment distinction; original narrow adaptation','url':'https://docs.oasis-open.org/ubl/os-UBL-2.3/mod/summary/reports/UBL-Invoice-2.3.html'}]}
# Normative commitments do not depend on implementation source bytes.
from bundles import publish_bundle
core={"version":"0.2","eventFields":["specversion","id","source","type","time","datacontenttype","dataschema","mpeprofile","mpecontract","data"],
      "canonicalization":rules["canonicalization"],"primitives":{k:v for k,v in rules["primitives"].items() if k!="currency"},"unsupported":rules["unsupported"]}
put('profiles/rules.json',rules)
lock={}
for name,body in bodies.items():
    schema=object_({'specversion':const('1.0'),'id':ident('event'),
     'source':{'type':'string','pattern':'^urn:mpe:source:[a-z0-9][a-z0-9-]{0,31}(?![\\s\\S])'},
     'type':const(types[name]),'time':TIME,'datacontenttype':const('application/json'),
     'dataschema':const('urn:mpe:model:'+name),'mpeprofile':const(name),'mpecontract':HASH,'data':body})
    schema['$schema']='https://json-schema.org/draft/2020-12/schema'
    schema['$id']='urn:mpe:model:'+name
    put(f'schemas/{name}.json',schema)
    normative={"profile":name,"rules":rules[name.split('.')[0]],"role":roles[name],"context":rules['context']}
    lock[name]=publish_bundle(r=ROOT,profile=name,schema=schema,core=core,normative=normative)
put('profiles/lock.json',lock)
now='2026-10-04T12:00:00.000Z'; end='2026-10-04T13:00:00.000Z'; start='2026-10-04T11:00:00.000Z'
rfq={'rfqId':'rfq:demo','quoteId':'quote:demo','requester':'party:buyer','dealer':'party:dealer','requesterSide':'BuyAsset',
 'buyer':'party:buyer','seller':'party:dealer','asset':'asset:pilot-share-42','quantity':{'coefficient':'100','scale':0,'unit':'Share'},
 'currency':'iso4217:USD','price':{'kind':'AbsolutePerUnit','value':{'coefficient':'12345','scale':2},'currency':'iso4217:USD',
 'assetRef':'asset:pilot-share-42','unit':'Share','baseQuantity':'1','fees':'None'},'cash':{'coefficient':'1234500','scale':2},
 'quoteKind':'Firm','validFrom':start,'validUntil':end,'settlement':'OffchainCoordinationOnly'}
invoice={'invoiceId':'invoice:supplier/demo','supplier':'party:supplier','customer':'party:customer','documentDigest':'sha256:'+'1'*64,
 'currency':'iso4217:USD','payable':{'coefficient':'50000','scale':2},'paymentId':'payment:demo',
 'amount':{'coefficient':'25000','scale':2},'status':'Final','observedAt':start,'effectiveAt':start,'rail':'fixture-bank-v1'}
prop={'environment':'Sandbox','operation':'WriteReport','target':'sandbox:reports/demo','inputDigest':'sha256:'+'2'*64,
      'budget':{'coefficient':'5','scale':0,'unit':'Step'},'expires':end}
agent={'authorityDomain':'urn:mpe:sandbox:local','executionScope':'scope:fixture','budgetWindow':'window:fixture','actionId':'action:demo','proposal':prop,'proposalDigest':digest({'domain':'mpe.model.proposal.v0.2','contract':lock['agent.v0.2'],'proposal':prop}),
 'policyDigest':'sha256:'+'3'*64,'human':'human:alice','validFrom':start,'validUntil':end,'maxEffects':1}
context={'authorityDomain':'urn:mpe:sandbox:local','executionScope':'scope:fixture','budgetWindow':'window:fixture','fixtureTrust':'trusted-test-fixture-only','now':now,
 'sources':{'urn:mpe:source:dealer':{'role':'dealer','principal':'party:dealer'},
 'urn:mpe:source:bank':{'role':'payment-adapter','principal':'fixture-bank-v1'},
 'urn:mpe:source:human':{'role':'human-approver','principal':'human:alice'}},
 'rfqs':{'rfq:demo':{**{k:rfq[k] for k in ('requester','dealer','requesterSide','asset','quantity','currency')},'state':'open'}},
 'invoices':{'invoice:supplier/demo':{k:invoice[k] for k in ('supplier','customer','currency','payable','documentDigest')}},
 'paymentEvidence':{'payment:demo':invoice},'proposals':{'action:demo':prop},'policyDigest':agent['policyDigest'],
 'humans':['human:alice'],'revokedActions':[],'sandboxTargets':['sandbox:reports/demo'],'maxSteps':10}
pending=copy.deepcopy(invoice); pending['status']='Pending'; pending['paymentId']='payment:pending'
context['paymentEvidence']['payment:pending']=pending
reversed_=copy.deepcopy(invoice); reversed_['status']='Reversed'; reversed_['paymentId']='payment:reversed'
context['paymentEvidence']['payment:reversed']=reversed_
put('conformance/trusted-context.json',context)
events={}
for label,name,source,data in [('rfq','rfq.v0.2','dealer',rfq),('invoice-final','invoice.v0.2','bank',invoice),
 ('invoice-pending','invoice.v0.2','bank',pending),('invoice-reversed','invoice.v0.2','bank',reversed_),('agent','agent.v0.2','human',agent)]:
    e={'specversion':'1.0','id':'event:'+label,'source':'urn:mpe:source:'+source,'type':types[name],
       'time':start,'datacontenttype':'application/json','dataschema':'urn:mpe:model:'+name,
       'mpeprofile':name,'mpecontract':lock[name],'data':data}
    events[label]=e; put(f'examples/{label}.json',e)
cases=[]
for label,status in [('rfq','offchain-quote-valid'),('invoice-final','final-payment-evidence-only'),
 ('invoice-pending','payment-evidence-pending-or-reversed'),('invoice-reversed','payment-evidence-pending-or-reversed'),('agent','sandbox-candidate-only')]:
    cases.append({'file':f'examples/{label}.json','expect':status})
def negative(label,base,field,value):
    e=copy.deepcopy(events[base]); target=e
    parts=field.split('.')
    for part in parts[:-1]: target=target[part]
    target[parts[-1]]=value
    path=f'conformance/{label}.json'; put(path,e); cases.append({'file':path,'expect':'reject'})
negative('price-asset','rfq','data.price.assetRef','asset:other')
negative('price-unit','rfq','data.price.unit','Token')
negative('side','rfq','data.requesterSide','SellAsset')
negative('precision','rfq','data.price.value.scale',3)
negative('currency','rfq','data.price.currency','iso4217:EUR')
negative('unknown-fee','rfq','data.price.handlingFee',{'coefficient':'100','scale':2})
negative('fee-enum','rfq','data.price.fees','Excluded')
negative('expired','rfq','data.validUntil',now)
negative('cash','rfq','data.cash.coefficient','1234499')
negative('unknown-profile','rfq','mpeprofile','rfq.v9')
negative('profile-hash','agent','mpecontract','sha256:'+'0'*64)
negative('schema','rfq','dataschema','https://evil.invalid/schema')
negative('calendar','rfq','time','2026-02-30T11:00:00.000Z')
negative('timestamp-offset','rfq','time','2026-10-04T11:00:00+00:00')
negative('non-ascii-id','rfq','id','event:démo')
negative('zero','rfq','data.quantity.coefficient','0')
negative('decimal-leading-zero','rfq','data.price.value.coefficient','012345')
negative('decimal-exponent','rfq','data.price.value.coefficient','1e3')
negative('decimal-overflow','rfq','data.price.value.coefficient','1000000000000000000')
negative('changed-target','agent','data.proposal.target','sandbox:reports/other')
negative('changed-input','agent','data.proposal.inputDigest','sha256:'+'4'*64)
negative('expired-approval','agent','data.validUntil',now)
negative('unauthorized-human','agent','data.human','human:mallory')
negative('unknown-operation','agent','data.proposal.operation','SendPayment')
negative('payment-final-invention','invoice-pending','data.status','Final')
negative('invoice-currency','invoice-final','data.currency','iso4217:EUR')
negative('missing-payment-evidence','invoice-final','data.paymentId','payment:unknown')
raw=json.dumps(events['agent'],separators=(',',':'))
(ROOT/'conformance/duplicate-key.json').write_text(raw.replace('"maxEffects":1','"maxEffects":1,"maxEffects":2'))
cases.append({'file':'conformance/duplicate-key.json','expect':'reject'})
(ROOT/'conformance/duplicate-escaped-key.json').write_text(raw.replace('"maxEffects":1','"maxEffects":1,"max\\u0045ffects":2'))
cases.append({'file':'conformance/duplicate-escaped-key.json','expect':'reject'})
put('conformance/cases.json',cases)
print(f'Built {len(bodies)} schemas, {len(lock)} pinned manifests, {len(events)} examples, {len(cases)} cases')

from bundles import register_legacy
register_legacy(ROOT)
