"""Implementation/dependency evidence; separate from immutable semantic commitments."""
from pathlib import Path
import hashlib,json,sys,subprocess,importlib.metadata
ROOT=Path(__file__).parent
files=[p for p in ROOT.rglob('*') if p.is_file() and 'target' not in p.parts and 'node_modules' not in p.parts and 'releases' not in p.parts and p.suffix in ('.py','.mts','.mjs','.lock','.toml')]
files+=[ROOT/'requirements.lock.txt',ROOT/'interpreters/package-lock.json']
report={'release':'0.2.0-conformance-prototype','semanticContracts':json.loads((ROOT/'profiles/lock.json').read_text()),'sourceHashes':{str(p.relative_to(ROOT)):'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))},'python':sys.version,'node':subprocess.check_output(['node','--version'],text=True).strip(),'rust':subprocess.check_output(['rustc','--version'],text=True).strip(),'cargo':subprocess.check_output(['cargo','--version'],text=True).strip(),'pythonPackages':{n:importlib.metadata.version(n) for n in ['jsonschema','rfc8785','attrs','referencing','rpds-py','jsonschema-specifications']},'authentication':'unsigned-local-release-evidence','productionAssurance':False}
(ROOT/'evidence/implementation-release.json').write_text(json.dumps(report,indent=2)+'\n')
print('Wrote separate implementation release evidence')
