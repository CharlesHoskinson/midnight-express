"""Isolated negative build tests; never edit canonical Lean or public sources.

Expected current behavior: plain build accepts sorry; --wfail rejects it.
An unaudited project axiom passes --wfail and the current selective Audit.lean.
These are review evidence, not acceptable behaviors for a future proof gate.
"""
from pathlib import Path
import tempfile,shutil,subprocess,json
ROOT=Path(__file__).resolve().parents[4]
source=ROOT/'formal/lean'
version=(source/'lean-toolchain').read_text().strip().replace(':','---').replace('/','--')
lake=Path.home()/'.elan/toolchains'/version/'bin/lake'
if not lake.exists():
 found=shutil.which('lake')
 if not found:raise SystemExit('Install pinned Lean toolchain before running this review evidence')
 lake=Path(found)
with tempfile.TemporaryDirectory(prefix='mpe-lean-review-') as temporary:
 scratch=Path(temporary)/'lean'
 shutil.copytree(source,scratch,ignore=shutil.ignore_patterns('.lake'))
 original=(source/'MidnightExpress.lean').read_text()
 results=[]
 def run(label,args,expected):
  p=subprocess.run([str(lake),*args],cwd=scratch,capture_output=True,text=True,timeout=120)
  results.append({'case':label,'arguments':args,'exit_code':p.returncode})
  if (p.returncode==0)!=expected:
   raise AssertionError((label,p.returncode,p.stdout,p.stderr))
 (scratch/'MidnightExpress.lean').write_text(original+'\ntheorem reviewCanary : False := by sorry\n')
 run('placeholder_ordinary_build',['build'],True)
 run('placeholder_warnings_fail',['--wfail','build'],False)
 (scratch/'MidnightExpress.lean').write_text(original+'\naxiom reviewOracle : False\ntheorem reviewOracleLeak : False := reviewOracle\n')
 run('unaudited_axiom_warnings_fail',['--wfail','build'],True)
 run('unaudited_axiom_selective_print_audit',['env','lean','Audit.lean'],True)
 print(json.dumps(results,indent=2))
