"""Validate every generated scope and lifecycle revision against the existing contract."""
import json
import subprocess
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / 'design/subscriptions/local-subscription-intent.schema.json').read_text())
js = """
const C=require('./website/dist/subscriptions-core.js');
const feeds=C.catalog(require('./website/dist/subscriptions-fixtures.json').records),s=C.initial();
for(const f of feeds){C.follow(s,f);C.revise(s,f,'paused');s.watches[f.id].coverage='lost';C.acceptStart(s,f);C.revise(s,f,'closed');}
console.log(JSON.stringify(Object.values(s.watches).flatMap(w=>w.history)));
"""
records = json.loads(subprocess.check_output(['node', '-e', js], cwd=ROOT))
validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
for record in records:
    validator.validate(record)
print(f'PASS {len(records)} generated intent revisions against the unchanged closed schema')
