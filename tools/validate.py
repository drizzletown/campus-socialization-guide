#!/usr/bin/env python3
"""Check chapter completeness, exported pages, and relative links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlparse
import json,re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
# Long-form chapters have editorial headings chosen individually
root=Path(__file__).resolve().parents[1];docs=root/'docs'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,tag,attrs):
  props=dict(attrs)
  for key in ('href','src'):
   if key in props:self.urls.append(props[key])

files=list(docs.rglob('*.html'))
assert len(files)==206,(len(files),'expected 103 zh + 103 en HTML pages')
assert len(list((docs/'en/book').glob('ch*.html')))==50
assert len(list((root/'content/en').glob('part*/ch*.md')))==50
assert len(list((docs/'en/deep').glob('*.html')))==8
assert len(list((docs/'en/tools').glob('tool*.html')))==12
assert len(list((docs/'en/cases').glob('case*.html')))==12
assert len(json.loads((docs/'en/search-index.json').read_text(encoding='utf8')))==50
assert len(list((root/'content').glob('part*/ch*.md')))==50
assert len(list((root/'content/tools').glob('tool*.md')))==12
assert len(list((root/'content/cases').glob('case*.md')))==12
assert len(json.loads((docs/'search-index.json').read_text(encoding='utf8')))==50
assert len(json.loads((docs/'search-guides.json').read_text(encoding='utf8')))==21
routes=json.loads((docs/'search-guides.json').read_text(encoding='utf8'))
for route in routes:
 for field in ('primary','secondary'):
  assert (docs/route[field]).is_file(),(route['id'],field,route[field])
assert len(json.loads((root/'content/evaluation/role-trials.json').read_text(encoding='utf8')))==21
assert (docs/'practice.html').exists() and (docs/'practice.html').read_text(encoding='utf8').count('class="trial-card"')==21
assert (docs/'en/practice.html').read_text(encoding='utf8').count('class="trial-card"')==21
for t in json.loads((root/'content/evaluation/role-trials.json').read_text(encoding='utf8')):
 assert all(t.get(k) for k in ('scene','diagnosis','action','owner','boundary')) and t['route'] in {x['id'] for x in routes},t.get('id')
assert (docs/'campus-policies.html').exists()
assert (docs/'decision-lab.html').exists()
assert len(list((root/'content/deep').glob('*.md')))==7
assert len(list((docs/'deep').glob('*.html')))==8
assert (root/'content/guides/decision-lab.md').exists()
lab=(docs/'decision-lab.html').read_text(encoding='utf8')
assert lab.count('<details>')==24, '12 cases must each have two contrasting branches'
assert '情境分流' in (docs/'index.html').read_text(encoding='utf8')
assert 'lang="en"' in (docs/'en/index.html').read_text(encoding='utf8')
assert 'hreflang="en"' in (docs/'index.html').read_text(encoding='utf8')
assert 'hreflang="zh-CN"' in (docs/'en/index.html').read_text(encoding='utf8')
bad=[]
for file in files:
 data=file.read_text(encoding='utf8');p=Links();p.feed(data)
 if '<main id="main">' not in data:bad.append((str(file),'missing main'))
 for u in p.urls:
  if u.startswith(('http:','https:','mailto:','tel:','javascript:','#','data:')):continue
  pathpart=unquote(urlparse(u).path)
  if not pathpart:continue
  target=(file.parent/pathpart).resolve()
  if not target.exists():bad.append((str(file.relative_to(docs)),u))
assert not bad, 'Broken/missing page references:\n'+'\n'.join(map(str,bad[:30]))
whole=(root/'BOOK_FULL.md').read_text(encoding='utf8')
assert len(whole)>45000
for i in range(1,51):assert f'# 第{i:02d}章 ' in whole
for i in range(1,51):
 s=(root/f'content/part{(i-1)//5+1:02d}/ch{i:02d}.md').read_text(encoding='utf8')
 assert len(__import__('re').findall(r'^## ',s,__import__('re').M))==2,(i,'expected two original thematic sections')
 assert len(s)>=1700,(i,'too brief',len(s))
 assert '## 从眼前的事情说起' not in s and '## 不同条件下怎样判断' not in s and '## 从判断走向行动' not in s
for p in range(1,11):
 assert (docs/'volumes'/f'part{p:02d}.html').is_file()
 assert (docs/'en/volumes'/f'part{p:02d}.html').is_file()
print(f'PASS: {len(files)} HTML files, 50 long-form chapters, 10 bilingual volume introductions, 12 worksheets, 12 cases, all local links resolved, full book length {len(whole):,} chars')
