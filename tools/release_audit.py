#!/usr/bin/env python3
"""Additional release-focused static security, portability and policy checks."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json,re
root=Path(__file__).resolve().parents[1]
docs=root/'docs'
class Page(HTMLParser):
    def __init__(self):super().__init__();self.tags=[];self.urls=[];self.external_assets=[];self.h1=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs);self.tags.append((tag,d))
        if tag=='h1':self.h1+=1
        for k in ('href','src'):
            if k in d:self.urls.append((tag,k,d[k]))
        if tag in ('script','iframe','form','object','embed') and tag!='script':self.external_assets.append(tag)
        if any(k.startswith('on') for k in d):self.external_assets.append(('inline-handler',tag))
errors=[]
pages=list(docs.rglob('*.html'))
for page in pages:
    rel=page.relative_to(docs)
    s=page.read_text(encoding='utf8')
    parser=Page();parser.feed(s)
    if '<html lang="zh-CN">' not in s: errors.append((rel,'missing lang'))
    if '<meta name="viewport"' not in s: errors.append((rel,'missing responsive viewport'))
    if parser.h1!=1:errors.append((rel,'h1 count',parser.h1))
    if parser.external_assets:errors.append((rel,'risky element',parser.external_assets))
    for tag,attr,url in parser.urls:
        if url.startswith(('javascript:','data:text/html','//','http://')):errors.append((rel,'unsafe reference',url))
        if tag in ('link','script') and url.startswith('https://'):errors.append((rel,'external runtime dependency',url))
        if url.startswith(('/assets/','/book/','/deep/')):errors.append((rel,'absolute path breaks Pages project URL',url))
    if rel.as_posix()=='index.html' and ('id="query"' not in s or 'aria-live' not in s):errors.append((rel,'search accessibility missing'))
for path in root.rglob('*'):
    if path.is_file() and path.suffix in {'.md','.py','.js','.html','.json','.yml','.yaml','.txt','.css','.csv'}:
        try:path.read_text(encoding='utf-8')
        except UnicodeDecodeError: errors.append((path.relative_to(root),'not UTF-8'))
for must in ('README.md','COPYRIGHT.md','CONTRIBUTING.md','SECURITY.md','PUBLISHING.md','RELEASE_CHECKLIST.md','docs/.nojekyll','docs/campus-policies.html','.github/workflows/verify.yml'):
    if not (root/must).exists():errors.append((must,'missing release document'))
for resource in ('docs/assets/site.css','docs/assets/site.js','docs/assets/search-core.js'):
    if not (root/resource).exists():errors.append((resource,'missing bundled asset'))
if errors:
    for e in errors:print('FAIL',e)
    raise SystemExit(1)
print('PASS release audit:',len(pages),'pages; UTF-8; one H1/page; portable asset paths; no third-party runtime scripts; no inline event handlers')
