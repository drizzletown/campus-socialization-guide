#!/usr/bin/env python3
"""Check chapter completeness, exported pages, and relative links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlparse
import json,re
root=Path(__file__).resolve().parents[1];docs=root/'docs'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,tag,attrs):
  props=dict(attrs)
  for key in ('href','src'):
   if key in props:self.urls.append(props[key])

files=list(docs.rglob('*.html'))
assert len(files)==93,(len(files),'expected 93 HTML pages including seven deep-reading topics')
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
assert (docs/'reader-lab.html').exists() and (docs/'reader-lab.html').read_text(encoding='utf8').count('class="trial-card"')==21
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
 for token in ('## 一个可能遇到的现场','## 把问题看清楚','## 继续往深处想','## 用 SSCM 五维辨认当前条件','## 可以实行的四步','## 需要守住的边界'):
  assert token in s,(i,token)
 assert all(f'{x}：' in s for x in 'CNRVA')
 assert '### 深入推演：' in s or '### 情境对照：' in s, (i,'missing scenario reasoning')
print(f'PASS: {len(files)} HTML files, 50 chapters, 12 worksheets, 12 cases, all local links resolved, full book length {len(whole):,} chars')
