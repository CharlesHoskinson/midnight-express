#!/usr/bin/env python3
"""Run the Inkwell pass on each revised file as soon as it appears in ../draft-r2. Exits when all files in FILES are done."""
import concurrent.futures as cf, time, sys
from pathlib import Path
import run_inkwell as R
SKIP = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else set()
started = set(SKIP)
ex = cf.ThreadPoolExecutor(6)
futs = []
while True:
    for f in R.FILES:
        if f in started or f.startswith("B"):
            continue
        if (R.IN2 / f).exists() and (R.IN2 / f).stat().st_size > 800:
            time.sleep(5)  # let the writer finish flushing
            started.add(f)
            futs.append(ex.submit(R.job, f))
            print("queued", f, flush=True)
    done = sum(1 for f in R.FILES if not f.startswith("B") and (R.OUT / f).exists())
    if len([f for f in R.FILES if not f.startswith("B")]) == done:
        break
    time.sleep(60)
for fu in futs:
    print(*fu.result(), flush=True)
