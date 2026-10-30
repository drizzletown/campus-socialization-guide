#!/usr/bin/env python3
"""Build parallel public Chinese/English reading pages and navigation.
Run AFTER build.py, extras.py, decision_lab.py and reader_lab.py.
Edit Chinese content/partXX/chXX.md and English content/en/partXX/chXX.md.
"""
from pathlib import Path
from html import escape as esc
import os,re,json,shutil
import mistune

ROOT=Path(__file__).parent; DOC=ROOT/'docs'; EN=DOC/'en'; CEN=ROOT/'content/en'
MD=mistune.create_markdown(plugins=['table','strikethrough'])
VOL=['Understanding Socialization','Courses and Learning','Life and Family','Friendship and Relationships','Organizations and Civic Life','Research and Practice','Digital Life and AI','Careers and Choices','Rights and Protection','Long-Term Development']
DEEP=[('01-learning','Academic Help and Fair Grades',[7,8,9]),('02-dorm','Shared Housing and Safety',[11,18]),('03-research','Entering Research Responsibly',[26,27,28,29,30]),('04-organizations','Student Clubs and Governance',[21,22,23,24,25,47]),('05-relationships','Friendship, Consent and Autonomy',[16,17,18,19,20,42]),('06-career','From Campus to Work',[30,36,37,38,39,40]),('07-rights','Appeals, Protection and Emergencies',[35,41,42,43,44,45])]

def load():
 ds=[]
 for i in range(1,51):
  p=(i-1)//5+1
  txt=(CEN/f'part{p:02d}'/f'ch{i:02d}.md').read_text(encoding='utf8')
  name=re.search(r'^# Chapter \d+\. (.*)',txt,re.M).group(1)
  ds.append({'id':i,'part':p,'title':name,'text':txt})
 return ds

def shell(title,body,path,desc='A practical student guide to university learning, relationships and informed choices.'):
 # path is relative to EN, e.g. book/ch01.html or index.html
 depth=len(Path(path).parts)-1
 base='../'*depth or './'; external='../'*(depth+1)
 zhpage=external+path
 nav=[('Home','index.html'),('Start Here','preface.html'),('Find a Topic','index.html#topics'),('Scenario Guide','decision-lab.html'),('Deep Reading','deep/index.html'),('Practice','practice.html'),('Cases','cases/index.html'),('Worksheets','tools/index.html'),('Policy Guide','campus-policies.html'),('About','about.html')]
 navhtml=''.join(f'<a href="{base}{url}">{esc(lbl)}</a>' for lbl,url in nav)
 relfont='<meta name="color-scheme" content="light dark">'
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{relfont}<meta name="referrer" content="strict-origin-when-cross-origin"><meta name="description" content="{esc(desc)}"><title>{esc(title)} · Entering University</title><link rel="stylesheet" href="{external}assets/site.css"><script defer src="{base}site-en.js"></script></head><body class="english-edition"><a class="skip" href="#main">Skip to content</a><header class="topbar"><a class="brand" href="{base}index.html"><span class="brandmark">U</span><span>Entering University<br><small>Learning to Live with the World</small></span></a><nav aria-label="Main navigation">{navhtml}<a class="lang-toggle" lang="zh-CN" hreflang="zh-CN" href="{zhpage}">中文</a></nav></header><main id="main">{body}</main><footer><p><strong>Entering University, Learning to Live with the World</strong> · Student Socialization Cognitive Model</p><p>Use current institutional rules and qualified support for individual decisions. In immediate danger, contact local emergency services.</p><p>The site does not ask for registration; worksheet entries are not submitted or automatically saved.</p><a href="{base}about.html">About, privacy and rights</a> · <a href="{base}campus-policies.html">Checking current policies</a></footer></body></html>'''

def write(path,title,body):
 target=EN/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(shell(title,body,path),encoding='utf8')

def chapters(ds):
 for d in ds:
  n=d['id'];p=d['part']
  sidenav=''.join(f'<a class="{"active" if x["id"]==n else ""}" href="ch{x["id"]:02d}.html">{x["id"]:02d}. {esc(x["title"])}</a>' for x in ds if x['part']==p)
  prev=f'<a href="ch{n-1:02d}.html" rel="prev">← Previous</a>' if n>1 else '<span></span>'
  nextp=f'<a href="ch{n+1:02d}.html" rel="next">Next →</a>' if n<50 else '<span></span>'
  deep=''.join(f'<a href="../deep/{slug}.html">{esc(title)} ↗</a> ' for slug,title,ids in DEEP if n in ids)
  more=f'<div class="info"><strong>Further reading:</strong> {deep}</div>' if deep else ''
  body=f'''<div class="read-layout"><aside class="bookside"><a href="../index.html#part{p}">← Part {p}: {esc(VOL[p-1])}</a><h3>In this part</h3>{sidenav}<a href="../tools/index.html">Worksheets ↗</a></aside><div class="reader"><div class="chapter-meta">Part {p} · {esc(VOL[p-1])}</div><div class="reading-actions"><span>Chapter {n} of 50</span><button type="button" data-complete="{n}">Mark as read</button><button type="button" data-print="true">Print</button></div><article class="bookarticle">{MD(d['text'])}</article>{more}<div class="chapter-nav">{prev}{nextp}</div></div></div>'''
  write(f'book/ch{n:02d}.html',d['title'],body)

def home(ds):
 parts=[]
 for p,vol in enumerate(VOL,1):
  entries=''.join(f'<a class="chlink" href="book/ch{x["id"]:02d}.html"><span>{x["id"]:02d}</span>{esc(x["title"])}<span aria-hidden="true">↗</span></a>' for x in ds if x['part']==p)
  parts.append(f'<section class="part-block" id="part{p}"><div><div class="eyebrow">PART {p:02d}</div><h3>{esc(vol)}</h3><p>Five practical chapters about real situations, responsibilities and choices.</p></div><div class="chapterlist">{entries}</div></section>')
 topics=[('Getting started with university',[1,2,5,6,11]),('Course questions and grades',[7,8,9,41]),('Roommates and shared living',[11,18,44]),('Friends and personal boundaries',[16,19,20,42]),('Research and project entry',[26,27,28]),('Student clubs and authority',[21,22,24,25]),('AI, online conduct and privacy',[10,31,34,35]),('Major and postgraduate choices',[36,37,48]),('Internships and jobs',[30,38,39]),('Harassment, rights and safety',[41,42,44,45]),('Money and part-time work',[13,43]),('Life after graduation',[46,49,50])]
 t=''.join(f'<div class="problem"><div>{esc(label)}</div><p>{" · ".join(f"<a href=\"book/ch{i:02d}.html\">{i:02d}</a>" for i in ids)}</p></div>' for label,ids in topics)
 body=f'''<section class="hero"><div class="eyebrow">STUDENT SOCIALIZATION COGNITIVE MODEL · SSCM</div><h1>Entering University,<em> Learning to Live with the World.</em></h1><p class="lead">A practical guide to learning, living, relationships, responsibility and informed choice. Explore 50 chapters in ten parts, seven detailed topic guides, worked cases and worksheets. There is no personality ranking or requirement to become more outgoing.</p><div class="hero-actions"><a class="primary" href="book/ch01.html">Read chapter one →</a><a class="secondary" href="decision-lab.html">I have a specific problem</a><a class="secondary" href="book-all.html">Read the complete book</a></div><div class="hero-points"><div><b>Observe</b><span>Find facts and distinguish assumptions</span></div><div><b>Understand</b><span>Identify skills, access, roles and rules</span></div><div><b>Act</b><span>Take a manageable, informed step</span></div><div><b>Revise</b><span>Adjust after receiving feedback</span></div></div></section>
<section id="search" class="search-area"><div class="eyebrow">SEARCH THE GUIDE</div><h2>Start with the question you have</h2><label for="query">Search a chapter title or describe a situation in English</label><input id="query" class="searchbox" type="search" placeholder="e.g., my roommate makes noise at night; I cannot get feedback on a grade" autocomplete="off"><p class="muted" id="count" aria-live="polite">Type a few words to find relevant chapters.</p><p class="muted">Search suggests reading routes; it does not determine whether an incident is dangerous. Seek urgent help for immediate threats.</p><div id="results" class="search-results" aria-live="polite"></div></section>
<section id="topics"><div class="eyebrow">FIND BY SITUATION</div><h2>You don't have to read in order</h2><p>Choose the issue closest to your situation, then check whether the facts really match.</p><div class="problem-grid">{t}</div></section>
<section class="search-area"><div class="eyebrow">GO DEEPER</div><h2>Some situations need more than a short answer</h2><p>Explore seven detailed guides on academic support, housing, research, organizations, relationships, careers and rights.</p><a class="primary" href="deep/index.html">Seven detailed topic guides →</a> <a class="secondary" href="practice.html">Scenario practice →</a></section>
<section id="read"><div class="eyebrow">TABLE OF CONTENTS</div><h2>Ten parts, fifty chapters</h2><p>Chapters are topics, not levels of maturity or a required progression.</p>{''.join(parts)}</section>
<section class="bottom-banner"><h2>Use a worksheet when your thoughts feel tangled.</h2><p>Write down facts, responsibilities, possible explanations and one manageable next step. You can print worksheets without creating an account.</p><a class="primary" href="tools/index.html">Open the worksheets →</a></section>'''
 write('index.html','Home',body)
 (EN/'search-index.json').write_text(json.dumps([{'id':d['id'],'title':d['title'],'part':d['part'],'text':d['text']} for d in ds],ensure_ascii=False),encoding='utf8')

def deep():
 cards=[]
 for slug,title,ids in DEEP:
  src=(CEN/'deep'/f'{slug}.md').read_text(encoding='utf8')
  back=f'<p><a href="index.html">← All topic guides</a></p>'
  refs=' · '.join(f'<a href="../book/ch{i:02d}.html">Chapter {i:02d}</a>' for i in ids)
  write(f'deep/{slug}.html',title,f'<div class="guide">{back}<article class="bookarticle">{MD(src)}</article><p class="muted">Related: {refs}</p></div>')
  cards.append(f'<a class="chlink" href="{slug}.html"><span>GUIDE</span>{esc(title)}<span aria-hidden="true">↗</span></a>')
 write('deep/index.html','Detailed Topic Guides','<div class="guide"><div class="eyebrow">DEEP READING</div><h1>Seven practical topic guides</h1><p>When a situation is complex, compare different causes, safe options and institutional responsibilities.</p><div class="chapterlist">'+''.join(cards)+'</div></div>')

def guides(ds):
 for name,title in [('preface','Start Here'),('model','The SSCM Framework'),('about','About This Guide'),('campus-policies','Checking University Policies')]:
  content=(CEN/'guides'/f'{name}.md').read_text(encoding='utf8')
  write(name+'.html',title,'<div class="guide"><article class="bookarticle">'+MD(content)+'</article><p><a href="index.html">← Back to home</a></p></div>')
 allbook='# Entering University, Learning to Live with the World\n\n'+(CEN/'guides/preface.md').read_text(encoding='utf8')+'\n\n---\n\n'+(CEN/'guides/model.md').read_text(encoding='utf8')+'\n\n---\n\n'+'\n\n---\n\n'.join(d['text'] for d in ds)
 (ROOT/'BOOK_EN.md').write_text(allbook,encoding='utf8')
 write('book-all.html','Complete Book','<div class="guide"><article class="bookarticle">'+MD('\n'.join(line if line.startswith('# Entering University') else ('#'+line if line.startswith('# ') else line) for line in allbook.splitlines()))+'</article></div>')

def tools():
 lines=(CEN/'data/tools.tsv').read_text(encoding='utf8').splitlines();assert len(lines)==12
 cards=[]
 for i,line in enumerate(lines,1):
  title,desc,fields=line.split('|');prompts=fields.split(';');assert len(prompts)==6
  blanks=''.join(f'<div class="tool-field"><label for="f{i}-{j}">{j}. {esc(p)}</label><div class="blank" id="f{i}-{j}" role="textbox" aria-multiline="true" contenteditable="true" spellcheck="false"></div><div class="hint">Only this page contains your writing. It is not automatically saved.</div></div>' for j,p in enumerate(prompts,1))
  content=f'<div class="guide"><div class="eyebrow">WORKSHEET {i:02d} / 12</div><h1>{esc(title)}</h1><p>{esc(desc)}</p><div class="info">Entries are not submitted or automatically saved. Avoid placing sensitive identifying details on shared devices.</div><div class="tool-actions"><button type="button" data-print="true">Print / Save as PDF</button></div><div class="tool-fields">{blanks}</div><p><a href="index.html">← All worksheets</a></p></div>'
  write(f'tools/tool{i:02d}.html',title,content)
  cards.append(f'<a class="tool-card" href="tool{i:02d}.html"><b>WORKSHEET {i:02d}</b><h3>{esc(title)}</h3><p>{esc(desc)}</p></a>')
 write('tools/index.html','Worksheets','<div class="guide"><div class="eyebrow">PRACTICAL WORKSHEETS</div><h1>Twelve worksheets for real decisions</h1><p>Complete them privately, print them or use the questions as a thinking framework. There are no scores.</p></div><div class="tool-grid">'+''.join(cards)+'</div>')

def cases():
 lines=(CEN/'data/cases.tsv').read_text(encoding='utf8').splitlines(); assert len(lines)==12
 cards=[]
 for i,line in enumerate(lines,1):
  title,event,explain,action,boundary=line.split('|')
  body=f'''<div class="guide"><div class="eyebrow">WORKED CASE {i:02d} / 12</div><h1>{esc(title)}</h1><article class="bookarticle"><h2>What happened</h2><p>{esc(event)}</p><h2>Understand the different causes</h2><p>{esc(explain)}</p><h2>What can be done</h2><p>{esc(action)}</p><h2>Safety and boundaries</h2><p>{esc(boundary)}</p></article><p><a href="index.html">← All cases</a></p></div>'''
  write(f'cases/case{i:02d}.html',title,body)
  cards.append(f'<a class="tool-card" href="case{i:02d}.html"><b>CASE {i:02d}</b><h3>{esc(title)}</h3><p>{esc(event)}</p></a>')
 write('cases/index.html','Worked Cases','<div class="guide"><div class="eyebrow">WORKED EXAMPLES</div><h1>Twelve cases in context</h1><p>These hypothetical situations illustrate how different facts lead to different choices.</p></div><div class="tool-grid">'+''.join(cards)+'</div>')

def practice(ds):
 tests=[('L01','I want to ask a professor but do not know what to say',7),('L02','My submitted assignment has a zero grade',8),('L03','A team member never received repository access',9),('D01','My roommate keeps me awake on late-night calls',11),('D02','My roommate threatens to reveal private information',42),('D03','Someone takes my belongings and excludes me',18),('R01','How can I approach a research supervisor?',26),('R02','My supervisor wants lab data on a personal drive',28),('R03','A senior student offers authorship without work',28),('C01','The club asks me to pay activity costs up front',24),('C02','Only friends of the officers receive recognition',41),('C03','A team outing is treated as compulsory',25),('P01','My partner demands my phone password',20),('P02','An ex waits outside my room after I said no',42),('P03','My former partner will not stop contacting me',19),('J01','I receive no answers to job applications',38),('J02','An interviewer requests a training deposit',38),('J03','My internship demands client data by personal email',30),('Q01','A scholarship award appears miscalculated',41),('Q02','I fear retaliation after reporting a teacher',42),('Q03','Someone collapses during a campus activity',45)]
 assert len(tests)==21
 sections=[]
 categories=[('Academic life','L'),('Shared housing','D'),('Research','R'),('Student organizations','C'),('Relationships','P'),('Jobs and internships','J'),('Rights and safety','Q')]
 for cat,prefix in categories:
  cards=[]
  for code,title,n in tests:
   if not code.startswith(prefix):continue
   d=ds[n-1];paras=re.findall(r'(?<=\n\n)[^#\n>][^\n]+',d['text']);scene=paras[0] if paras else title
   parts=re.split(r'^## ',d['text'],flags=re.M);overview=next((p.split('\n\n',1)[1].strip().split('\n\n')[0] for p in parts if p.startswith('Understand the situation')),title)
   action=next((p.split('\n\n',1)[1].strip().split('\n\n##')[0] for p in parts if p.startswith('Actions you can take')),'')
   safety=next((p.split('\n\n',1)[1].strip().split('\n\n')[0] for p in parts if p.startswith('Boundaries and safety')),'')
   cards.append(f'''<article class="trial-card"><h3>{esc(code)} · {esc(title)}</h3><p><strong>Situation:</strong> {esc(scene)}</p><p>Before opening the answer, consider what is known, what is assumed, who has authority, and what you could safely do.</p><details><summary>Show a possible response</summary><p><b>Possible explanation:</b> {esc(overview)}</p><p><b>Action:</b></p>{MD(action)}<p><b>Boundary:</b> {esc(safety)}</p><p><a href="book/ch{n:02d}.html">Read Chapter {n:02d} →</a></p></details></article>''')
  sections.append(f'<section class="trial-group"><h2>{esc(cat)}</h2><div class="trial-grid">{"".join(cards)}</div></section>')
 write('practice.html','Scenario Practice','<div class="guide"><div class="eyebrow">PRACTICE</div><h1>Try a situation before reading its discussion</h1><p>Twenty-one hypothetical student questions. Think about the facts, possible explanations, the first practical step and any safety boundary; then compare your reasoning with a suggested response. There is no score.</p></div>'+''.join(sections))


def decision(ds):
 nums=[7,9,11,13,19,22,26,28,30,35,38,41]
 cards=[]
 for n in nums:
  d=ds[n-1];txt=d['text']
  def sec(k):
   m=re.search(r'^## '+re.escape(k)+r'\n\n(.+?)(?=\n\n## |\Z)',txt,re.M|re.S)
   return m.group(1).strip() if m else ''
  cards.append(f'''<article class="lab-card"><div class="eyebrow">SITUATION {n:02d}</div><h2>{esc(d['title'])}</h2><p>{esc(sec('A situation you may recognize'))}</p><details><summary>Compare causes and options</summary><p>{esc(sec('When conditions differ'))}</p>{MD(sec('Actions you can take'))}<p><strong>Boundary:</strong> {esc(sec('Boundaries and safety'))}</p></details><a href="book/ch{n:02d}.html">Read Chapter {n:02d} →</a></article>''')
 write('decision-lab.html','Scenario Guide','<div class="guide"><div class="eyebrow">MAKE A SITUATED DECISION</div><h1>Similar problems can have different causes</h1><p>Choose a situation, consider alternative explanations and decide which action would be safe and within your authority.</p><p class="info">An immediate threat or medical emergency calls for local emergency help, not a routine discussion exercise.</p></div><div class="lab-grid">'+''.join(cards)+'</div>')

def client_script():
 code=r'''(()=>{'use strict';const key='sscm-read-en-1';document.querySelectorAll('[data-print]').forEach(b=>b.addEventListener('click',()=>window.print()));const b=document.querySelector('[data-complete]');if(b){const n=b.dataset.complete;let done=[];try{done=JSON.parse(localStorage.getItem(key)||'[]')}catch{}const paint=()=>{const y=done.includes(n);b.classList.toggle('is-done',y);b.textContent=y?'Read ✓ (undo)':'Mark as read'};b.addEventListener('click',()=>{done=done.includes(n)?done.filter(x=>x!==n):[...done,n];try{localStorage.setItem(key,JSON.stringify(done))}catch{}paint()});paint()}
const q=document.querySelector('#query'),out=document.querySelector('#results'),counter=document.querySelector('#count');if(!q||!out)return;let chapters=[];function show(){const words=q.value.toLowerCase().trim().split(/[^a-z0-9]+/).filter(x=>x.length>1);out.replaceChildren();if(!words.length){counter.textContent='Type a topic or a short question to start.';return}const scored=chapters.map(c=>{const title=c.title.toLowerCase(),body=c.text.toLowerCase();let n=0;words.forEach(w=>{if(title.includes(w))n+=8;if(body.includes(w))n+=1});return{c,n}}).filter(x=>x.n>0).sort((a,b)=>b.n-a.n||a.c.id-b.c.id).slice(0,12);counter.textContent=scored.length?`${scored.length} suggested chapters. Compare the facts before choosing an action.`:'No exact match; try a shorter phrase or explore the topic guides.';scored.forEach(({c})=>{const a=document.createElement('a');a.className='hit';a.href='book/ch'+String(c.id).padStart(2,'0')+'.html';a.textContent=`Chapter ${c.id}: ${c.title}`;out.append(a)});if(!scored.length){const a=document.createElement('a');a.className='hit';a.href='deep/index.html';a.textContent='Explore seven detailed topic guides';out.append(a)}}q.addEventListener('input',show);fetch('./search-index.json').then(r=>{if(!r.ok)throw Error('index');return r.json()}).then(data=>{chapters=data;show()}).catch(()=>{counter.textContent='The search index could not be loaded. Browse the table of contents below.'})})();'''
 (EN/'site-en.js').write_text(code,encoding='utf8')

def clean_zh():
 # Content sources are rebuilt in Chinese upstream. Keep only public-facing pages and no process reports.
 for f in [DOC/'pilot.html',DOC/'reader-lab.html']:
  f.unlink(missing_ok=True)
 # Keep the source generator's legal/case disclaimers while removing authoring-trial language from site presentation.
 replacements={
  '21个编辑构造的模拟问题':'21个情境练习',
  '模拟读者情境':'情境练习',
  '模拟试读':'情境练习',
  '读者试用':'',
  '内容审校及检索测试':'思考和判断',
  '展开编辑讨论路径':'查看参考分析',
  '编辑构造':'示例性',
  '编辑给出的讨论路径':'参考分析',
  '编辑构造的':'示例性',
  '编辑讨论':'参考讨论',
  '已于2026年10月30日对照期刊或出版社页面核查。正式学术发表时仍需依据目标期刊格式补全全部相关引文。':'',
 }
 for path in DOC.rglob('*.html'):
  if EN in path.parents:continue
  text=path.read_text(encoding='utf8')
  for a,b in replacements.items():text=text.replace(a,b)
  # The generated old navigation may still contain a link to pilot in unusual cases.
  text=re.sub(r'<a[^>]*href="[^"]*pilot\.html"[^>]*>.*?</a>','',text)
  text=text.replace('href="reader-lab.html"','href="practice.html"')
  path.write_text(text,encoding='utf8')
 # Existing Chinese example practice is generated by reader_lab.py as practice.html
 for path in DOC.rglob('*.html'):
  if EN in path.parents:continue
  rel=path.relative_to(DOC)
  target=EN/rel
  if not target.exists():target=EN/'index.html'
  href=os.path.relpath(target,path.parent).replace(os.sep,'/')
  text=path.read_text(encoding='utf8')
  link=f'<a class="lang-toggle" lang="en" hreflang="en" href="{href}">English</a>'
  if 'hreflang="en"' not in text: text=text.replace('</nav></header>',link+'</nav></header>',1)
  path.write_text(text,encoding='utf8')
 # Strip stale output; users can still use public practice page.
 (ROOT/'content/guides/reader-lab.md').unlink(missing_ok=True)


def main():
 ds=load();EN.mkdir(parents=True,exist_ok=True)
 chapters(ds);home(ds);deep();guides(ds);tools();cases();practice(ds);decision(ds);client_script();clean_zh()
 css=DOC/'assets/site.css';txt=css.read_text(encoding='utf8')
 extra='\n/* Bilingual public navigation and readable English typography */\n.topbar nav .lang-toggle{border:1px solid var(--accent);border-radius:18px;padding:3px 12px;color:var(--accent);font-weight:750;white-space:nowrap}.english-edition .bookarticle{font-family:Georgia,"Times New Roman",serif;line-height:1.85;letter-spacing:0}.english-edition .bookarticle h1,.english-edition .bookarticle h2,.english-edition .bookarticle h3{font-family:system-ui,-apple-system,sans-serif}.english-edition .hero h1{letter-spacing:-.035em}.english-edition .part-block{gap:30px}@media(max-width:560px){.topbar nav .lang-toggle{padding:2px 9px}}\n'
 if '/* Bilingual public navigation' not in txt:css.write_text(txt+extra,encoding='utf8')
 print('Bilingual complete: 50 English chapters + 7 guides + 12 cases + 12 tools + 21 exercises; public Chinese site cleaned')
if __name__=='__main__': main()
