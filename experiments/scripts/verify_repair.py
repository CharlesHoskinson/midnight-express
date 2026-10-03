from pathlib import Path
import subprocess,json,time
commands={
 'build':['cargo','build','--workspace','--release'],
 'fmt':['cargo','fmt','--all','--','--check'],
 'clippy':['cargo','clippy','--workspace','--all-targets','--','-D','warnings'],
 'tests':['cargo','test','--workspace']
}
summary={}
for name,cmd in commands.items():
 t=time.monotonic()
 with Path('evidence/repair/'+name+'.txt').open('w') as log:
  status=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
 summary[name]={'command':cmd,'exit':status,'wall_secs':time.monotonic()-t}
 print(name,status,flush=True)
 Path('evidence/repair/hygiene.json').write_text(json.dumps(summary,indent=2))
 if status: raise SystemExit(status)
