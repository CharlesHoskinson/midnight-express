import json
from pathlib import Path
p=Path('target/criterion/recognition_32_keys_class2/new/estimates.json')
r=json.loads(p.read_text())
cores=r['mean']['point_estimate']*100/1e9
print(f'32-key class-2 recognition at 100 events/s: mean wall-time duty-cycle upper bound {cores:.6f} cores')
assert cores <= .5, f'recognition budget exceeded: {cores}'
