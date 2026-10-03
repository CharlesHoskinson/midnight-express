from pathlib import Path
import subprocess, time, json, concurrent.futures
root=Path.cwd(); evidence=root/'evidence/repair'; results=root/'results/repair'
evidence.mkdir(parents=True,exist_ok=True); results.mkdir(parents=True,exist_ok=True)
with (evidence/'build.txt').open('w') as log:
    status=subprocess.run(['cargo','build','--workspace','--release'],stdout=log,stderr=subprocess.STDOUT).returncode
if status: raise SystemExit(status)
summary=[]
def run(scenario,overlap=False):
    name='baseline' if scenario=='baseline-off' else scenario
    destination=root/'results/repair-idontwant' if scenario=='baseline-off' else results
    destination.mkdir(parents=True,exist_ok=True)
    cmd=['target/release/mpe-sim','run','--scenario',name,'--nodes','50','--seed','1','--duration-secs','60','--out',str(destination/(name+'.50.json'))]
    if scenario=='baseline-off': cmd += ['--idontwant','off']
    print('START',scenario,flush=True); t=time.monotonic()
    with (evidence/(scenario+'.log')).open('w') as log:
        try: status=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=300).returncode
        except subprocess.TimeoutExpired: status=124
    elapsed=time.monotonic()-t
    row={'scenario':scenario,'exit':status,'wall_secs':elapsed,'command':cmd,'overlapped':overlap}
    print('END',scenario,status,round(elapsed,2),flush=True)
    return row
for group in [['baseline'],['baseline-off'],['spam'],['malformed','replay'],['eclipse'],['backfill'],['leakage'],['fallback'],['churn','anchor']]:
    if len(group)==1: summary.append(run(group[0]))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            summary.extend(pool.map(lambda s:run(s,True),group))
    (evidence/'runs.json').write_text(json.dumps(summary,indent=2))
