#!/usr/bin/env python3
"""Refresh static product cards from the canonical register and editorial content."""
from pathlib import Path
from html import escape
import json,re
root=Path(__file__).resolve().parent
canonical=json.loads((root.parent/'docs/product-requirements/use-cases.json').read_text())
product=json.loads((root/'dist/product-content.js').read_text().removeprefix('window.MPE_PRODUCT = ').removesuffix(';\n'))
assert len(canonical)==10 and set(product['cases'])=={c['id'] for c in canonical}
cards=[]
for c in sorted(canonical,key=lambda c:c['rank']):
    e=product['cases'][c['id']]
    stage='Proposed pilot' if c['rank']<=3 else 'Candidate · '+c['delivery_stage'].lower()
    fields=[('Who is involved',e['who']),('What starts it',c['trigger']),('Illustrative scenario',e['example']),('Value to test',c['value_hypothesis']),('Initial scope',c['initial_delivery_scope']),('How we would measure it',c['pilot_success_measure']),('Scope boundary',e['boundary']),('What must be proven',c['remaining_gate']),('Integration dependencies',c['stack_dependencies'])]
    fields_html=''.join(f'<h4>{escape(label)}</h4><p>{escape(value)}</p>' for label,value in fields)
    cards.append((c['rank'],f'<details class="case" id="{c["id"].lower()}"><summary><div><span class="case-stage">{escape(stage)}</span><h3>{escape(e["title"])}</h3><p>{escape(e["summary"])}</p></div></summary><div class="case-body">{fields_html}<p class="case-reference">Requirement identity: {escape(c["id"])} · {escape(c["recommended_title"])}</p></div></details>'))
p=root/'dist/index.html';html=p.read_text()
for marker,ranks in [('pilot-grid',range(1,4)),('case-grid',range(4,11))]:
    content='\n'.join(card for rank,card in cards if rank in ranks)
    # Markers allow content regeneration without touching the rest of the page.
    start=f'<!-- {marker}:start -->';end=f'<!-- {marker}:end -->'
    replacement=start+'\n'+content+'\n'+end
    if start in html:
        html=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:replacement,html,flags=re.S)
    else:
        pattern=rf'(<div id="{marker}" class="[^"]+">)\s*(</div>)'
        html,count=re.subn(pattern,lambda m:m[1]+'\n'+replacement+'\n'+m[2],html)
        assert count==1,marker
p.write_text(html.rstrip()+"\n")
(root/'dist/use-cases.js').write_text('window.MPE_USE_CASES = '+json.dumps(sorted(canonical,key=lambda c:c['rank']),ensure_ascii=False)+';\n')
print('Refreshed ten static cards; canonical IDs, ranks, scopes and gates preserved.')
