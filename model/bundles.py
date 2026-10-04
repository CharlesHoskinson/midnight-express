"""Immutable offline semantic bundles. Local installed allowlist is trusted fixture policy.
Release attestations live separately; no sender URL is fetched and no bundle is auto-installed.
"""
from pathlib import Path
import hashlib,json,os,re
import rfc8785
from jsonschema import Draft202012Validator

def decode(raw):
    if len(raw)>131072:raise ValueError('bundle metadata size')
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('duplicate bundle key')
            out[k]=v
        return out
    def bad(token):raise ValueError('bundle numeric token')
    return json.loads(raw,object_pairs_hook=pairs,parse_float=bad,parse_constant=bad)

def digest(value):return 'sha256:'+hashlib.sha256(rfc8785.dumps(value)).hexdigest()
def encode(value):return (json.dumps(value,indent=2,ensure_ascii=True)+'\n').encode()
def filehash(raw):return 'sha256:'+hashlib.sha256(raw).hexdigest()
def no_refs(value):
    if isinstance(value,dict):
        if any(k in value for k in ('$ref','$dynamicRef','$recursiveRef')):raise ValueError('offline schema must be standalone')
        for v in value.values():no_refs(v)
    elif isinstance(value,list):
        for v in value:no_refs(v)

def publish_bundle(r,profile,schema,core,normative):
    no_refs(schema);Draft202012Validator.check_schema(schema)
    resources={'schema.json':encode(schema),'core.json':encode(core),'rules.json':encode(normative)}
    m={'bundleVersion':1,'profile':profile,'version':'0.2','status':'experimental-model-only','role':normative['role'],
       'schema':'schema.json','resources':{k:filehash(v) for k,v in resources.items()},'signatures':'unsigned-fixture-only'}
    contract=digest(m);folder=r/'bundles'/contract.split(':')[1];folder.mkdir(parents=True,exist_ok=True)
    for name,raw in {**resources,'manifest.json':encode(m)}.items():
        p=folder/name
        if p.exists() and p.read_bytes()!=raw:raise ValueError('immutable bundle overwrite')
        if not p.exists():p.write_bytes(raw)
    p=r/'profiles/installed.json';installed=json.loads(p.read_text()) if p.exists() else {}
    installed[contract]={'profile':profile,'directory':folder.relative_to(r).as_posix(),'mode':'conformance'}
    p.write_bytes(encode(installed));(r/'profiles'/f'{profile}.json').write_bytes(encode(m))
    return contract

def register_legacy(r):
    p=r/'profiles/installed.json';installed=json.loads(p.read_text())
    for profile,contract in json.loads((r/'releases/v0.1/profiles/lock.json').read_text()).items():
        installed[contract]={'profile':profile,'directory':'releases/v0.1','mode':'historical-read-only'}
    p.write_bytes(encode(installed))

def load_bundle(r,profile,contract=None):
    if not isinstance(profile,str):raise ValueError('invalid profile')
    if contract is None:contract=decode((r/'profiles/lock.json').read_bytes()).get(profile)
    if not isinstance(contract,str) or not re.fullmatch('sha256:[0-9a-f]{64}',contract):raise ValueError('invalid contract')
    installed=decode((r/'profiles/installed.json').read_bytes())
    entry=installed.get(contract)
    if not isinstance(entry,dict) or set(entry)!={'profile','directory','mode'} or entry['profile']!=profile:raise ValueError('contract not installed')
    if entry['mode']!='conformance':raise ValueError('historical-read-only: use archived interpreter; cannot dispatch')
    folder=(r/entry['directory']).resolve()
    if not folder.is_relative_to(r.resolve()) or (r/entry['directory']).is_symlink():raise ValueError('bundle path escape')
    mraw=(folder/'manifest.json').read_bytes();m=decode(mraw)
    if set(m)!={'bundleVersion','profile','version','status','role','schema','resources','signatures'} or digest(m)!=contract or m['profile']!=profile or m['bundleVersion']!=1 or m['version']!='0.2' or m['status']!='experimental-model-only' or m['signatures']!='unsigned-fixture-only':
        raise ValueError('invalid manifest')
    if set(m['resources'])!={'schema.json','core.json','rules.json'} or m['schema']!='schema.json':raise ValueError('invalid closure')
    # Read once, verify those exact bytes, and validate from the same snapshot.
    captured={}
    for name,expected in m['resources'].items():
        p=folder/name
        if p.is_symlink() or not p.resolve().is_relative_to(folder):raise ValueError('resource escape')
        raw=p.read_bytes()
        if filehash(raw)!=expected:raise ValueError('resource integrity')
        captured[name]=decode(raw)
    schema=captured['schema.json'];no_refs(schema);Draft202012Validator.check_schema(schema)
    normative=captured['rules.json'];core=captured['core.json']
    if schema['properties']['mpeprofile']['const']!=profile or schema['$id']!=f'urn:mpe:model:{profile}' or normative['profile']!=profile or normative['role']!=m['role'] or core['version']!='0.2':raise ValueError('bundle metadata mismatch')
    return {**m,'schemaObject':schema,'normative':normative,'coreObject':core},contract

def negotiate(local,remote):
    """Pure exact intersection; callers authenticate private capabilities. No downgrade/fetch."""
    if len(local)>32 or len(remote)>32:raise ValueError('capability bound')
    for value in [*local,*remote]:
        if not isinstance(value,str) or not re.fullmatch('sha256:[0-9a-f]{64}',value):raise ValueError('invalid capability')
    return sorted(set(local)&set(remote))
