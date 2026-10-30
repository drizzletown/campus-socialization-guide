#!/usr/bin/env python3
"""Regenerate Markdown sources and the dependency-light GitHub Pages site.
Install requirement: pip install -r requirements.txt
Run from project root: python build.py
"""
from pathlib import Path
from html import escape
import re,json
import mistune

ROOT=Path(__file__).parent
CONTENT=ROOT/'content'
DOCS=ROOT/'docs'
BOOK=DOCS/'book'
VOL=[
 ('认识社会化','从日常关系出发，学会把笼统评价变成可分析的事件。','理解自己'),
 ('课程与学业','从选课、答疑、小组作业到学术诚信，把学习组织成真正的能力发展。','学会学习'),
 ('生活与家庭','处理空间、时间、金钱、健康与家庭的真实约束，形成可靠的生活安排。','照顾生活'),
 ('友谊与亲密关系','在差异、友谊、冲突与亲密中学习同意、责任和边界。','理解关系'),
 ('组织与公共参与','参与社团、承担公共职责、创造价值，也保留协商与退出权。','进入组织'),
 ('科研与专业实践','从科研入门到实验伦理、比赛与实习，学习真实专业责任。','走向实践'),
 ('数字社会与AI','理解线上连接、信息可信度、数据安全与工具使用的责任。','认识数字社会'),
 ('专业选择与未来','面对转专业、升学、求职、职业联系和创业，作出有证据的决定。','选择道路'),
 ('权益、风险与支持','在公平争议、骚扰、财务纠纷与危机中辨明权责，找到可靠帮助。','维护权益'),
 ('长期发展与重建','学会面对挫折、角色冲突、迁移与毕业后的网络变化。','持续成长')]

def parse():
    """Read editable Markdown chapter files as the canonical source."""
    docs=[]
    for n in range(1,51):
        p=(n-1)//5+1
        src=CONTENT/f'part{p:02d}'/f'ch{n:02d}.md'
        if not src.exists():raise FileNotFoundError(src)
        raw=src.read_text(encoding='utf8')
        fm=re.match(r'^---\n(.*?)\n---\n',raw,re.S)
        if not fm:raise ValueError(f'missing frontmatter: {src}')
        meta=dict(line.split(': ',1) for line in fm.group(1).splitlines() if ': ' in line)
        h=re.search(r'^# 第\d+章 (.+)$',raw,re.M)
        if not h:raise ValueError(f'missing title: {src}')
        if int(meta.get('chapter','-1'))!=n or int(meta.get('part','-1'))!=p:raise ValueError(f'invalid metadata: {src}')
        docs.append({'id':n,'title':h.group(1),'part':p,'tags':meta.get('tags','').split(','),'markdown':raw,'text':raw})
    return docs

md=mistune.create_markdown(plugins=['table','strikethrough'])
def clean_front(s):return re.sub(r'^---\n.*?\n---\n','',s,flags=re.S)

def html_shell(title,body,rel='.',subtitle='',toc=''):
    css=f'{rel}/assets/site.css';js=f'{rel}/assets/site.js'
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="description" content="{escape(subtitle or '基于SSCM大学生社会化网络认知模型的成长与行动指南')}"><title>{escape(title)} · 走进大学，学会与世界相处</title><link rel="stylesheet" href="{css}"><script defer src="{rel}/assets/search-core.js"></script><script defer src="{js}"></script></head><body>
<a class="skip" href="#main">跳转正文</a><header class="topbar"><a class="brand" href="{rel}/index.html"><span class="brandmark">见</span><span>走进大学<br><small>学会与世界相处</small></span></a><nav aria-label="主导航"><a href="{rel}/preface.html">导读</a><a href="{rel}/index.html#read">阅读全书</a><a href="{rel}/index.html#problems">按问题找</a><a href="{rel}/decision-lab.html">情境分流</a><a href="{rel}/deep/index.html">问题深读</a><a href="{rel}/reader-lab.html">模拟试读</a><a href="{rel}/cases/index.html">情境案例</a><a href="{rel}/tools/index.html">行动工具</a><a href="{rel}/pilot.html">读者试用</a><a href="{rel}/campus-policies.html">校规核验</a><a href="{rel}/about.html">关于本书</a></nav></header>
<main id="main">{body}</main><footer><p>《走进大学，学会与世界相处》· SSCM 大学生社会化成长与行动读物</p><p>尊重个体差异与自主选择。全站内容可离线阅读；不会将个人填写内容上传到服务器。发生紧急危险时，请联系当地紧急服务。</p><a href="{rel}/about.html">理论依据、使用边界与版权说明</a> · <a href="{rel}/campus-policies.html">校规与政策核验</a></footer></body></html>'''

DEEP_TOPICS=[
('01-learning','课程求助与公平评价',[7,8,9]),
('02-dorm','宿舍生活的三重边界',[11,18]),
('03-research','科研参与的完整路径',[26,27,28,29,30]),
('04-organizations','社团权责与共同治理',[21,22,23,24,25,47]),
('05-relationships','友谊与亲密关系的自主边界',[16,17,18,19,20,42]),
('06-career','从校园走向工作',[30,36,37,38,39,40]),
('07-rights','申诉、保护与紧急支持',[35,41,42,43,44,45])]

def build_deep():
    deep_dir=DOCS/'deep';deep_dir.mkdir(parents=True,exist_ok=True)
    cards=[]
    for slug,name,chapters in DEEP_TOPICS:
        src=CONTENT/'deep'/f'{slug}.md'
        assert src.exists(),src
        txt=src.read_text(encoding='utf8')
        links='、'.join(f'<a href="../book/ch{n:02d}.html">第{n:02d}章</a>' for n in chapters)
        body='<div class="guide"><p class="eyebrow"><a href="index.html">← 七类高频问题深读</a></p><article class="bookarticle">'+md(txt)+'</article><p class="muted">回到全书：'+links+'</p></div>'
        (deep_dir/f'{slug}.html').write_text(html_shell(name,body,'..'),encoding='utf8')
        cards.append(f'<a class="chlink" href="{slug}.html"><span>专题</span>{escape(name)}<span aria-hidden="true">↗</span></a>')
    intro="这些专题适合问题复杂、简单提示不够用时查阅。每篇区分至少两种不同处境，明确个人行动、组织责任与安全边界。它们是编辑构造的教学案例，不是实际学生访谈或验证结果。"
    body='<div class="guide"><p class="eyebrow">SSCM / DEEP READING</p><h1>七类高频问题深读</h1><p>'+intro+'</p><div class="chapterlist">'+''.join(cards)+'</div></div>'
    (deep_dir/'index.html').write_text(html_shell('七类高频问题深读',body,'..'),encoding='utf8')
    print('Generated 7 deep-reading topics and landing page')

def render_ch(d,ds):
    n=d['id'];p=d['part']; prev=f'ch{n-1:02d}.html' if n>1 else None;next=f'ch{n+1:02d}.html' if n<50 else None
    txt=d["markdown"]
    side=''.join(f'<a class="{("active" if x["id"]==n else "")}" href="ch{x["id"]:02d}.html">{x["id"]:02d}. {escape(x["title"])}</a>' for x in ds if x['part']==p)
    nav=f'<a href="{prev}" rel="prev">← 上一章</a>' if prev else '<span></span>'
    nav+=f'<a href="{next}" rel="next">下一章 →</a>' if next else '<span></span>'
    deep_links=''.join(f'<a href="../deep/{slug}.html">深入阅读：{escape(label)} ↗</a>' for slug,label,chapters in DEEP_TOPICS if n in chapters)
    extra=f'<div class="info"><strong>关联专题：</strong>{deep_links}</div>' if deep_links else ''
    body=f'''<div class="read-layout"><aside class="bookside"><a href="../index.html#part{p}">← 第{p}辑 · {escape(VOL[p-1][0])}</a><h3>本辑章节</h3>{side}<a href="../tools/index.html">行动工具箱 ↗</a></aside><div class="reader"><div class="chapter-meta">第{p}辑 · {escape(VOL[p-1][0])} <span>｜</span> {escape(' / '.join(d['tags']))}</div><div class="reading-actions"><span>第 {n} / 50 章</span><button type="button" class="done" data-complete="{n}">标记已读</button><button type="button" data-print="true">打印本章</button></div><article class="bookarticle">{md(clean_front(txt))}</article>{extra}<div class="chapter-nav">{nav}</div></div></div>'''
    (BOOK/f'ch{n:02d}.html').write_text(html_shell(d['title'],body,'..',d['markdown'][:150].replace('\n',' ')),encoding='utf8')

def main_index(ds):
    part_section=''
    for p,(name,desc,kicker) in enumerate(VOL,1):
        items=''.join(f'<a class="chlink" href="book/ch{c["id"]:02d}.html"><span>{c["id"]:02d}</span>{escape(c["title"])}<span aria-hidden="true">↗</span></a>' for c in ds if c['part']==p)
        part_section+=f'<section class="part-block" id="part{p}"><div><div class="eyebrow">第{p}辑 · {escape(kicker)}</div><h3>{escape(name)}</h3><p>{escape(desc)}</p></div><div class="chapterlist">{items}</div></section>'
    problems=[('刚到大学，什么都不熟悉',[1,2,5,6,11]),('课程压力大，不知道怎么求助',[7,8,12,14]),('小组作业有人不负责',[9,18,47]),('宿舍或同学关系冲突',[11,17,18,44]),('不想参加聚会，又怕得罪人',[16,20,21,25]),('遭遇不合理要求',[20,22,41,42]),('想做科研或参加比赛',[26,27,28,29]),('社团负责人难以协调工作',[22,24,25,47]),('总被社交媒体比较困扰',[31,32,33]),('不确定怎样使用AI工具',[10,34,35]),('在犹豫转专业、升学或就业',[36,37,38,48]),('遇到欺凌、风险或紧急问题',[35,41,42,45])]
    probs=''.join(f'<div class="problem"><div>{escape(q)}</div><p>{" · ".join(f"<a href=\"book/ch{n:02d}.html\">第{n:02d}章</a>" for n in ns)}</p></div>' for q,ns in problems)
    body=f'''<section class="hero"><div class="eyebrow">SSCM · OPEN STUDENT GUIDE / 2026</div><h1>走进大学，<em>学会与世界相处。</em></h1><p class="lead">一部从社会网络、能力、角色、贡献和自主选择出发的大学生成长行动读物。50章 · 10辑 · 12张行动工具卡。没有社交排名，也不要求你变成另一种人。</p><div class="hero-actions"><a class="primary" href="book/ch01.html">从第一章开始 →</a><a class="secondary" href="decision-lab.html">我正在遇到一个问题</a><a class="secondary" href="book-all.html">连续阅读全书</a></div><div class="hero-points"><div><b>看见</b><span>把感觉化成可核实的事实</span></div><div><b>判断</b><span>区分能力、机会与权责</span></div><div><b>行动</b><span>选择能承担的第一步</span></div><div><b>修正</b><span>根据反馈改变方案</span></div></div></section>
<section class="search-area" id="search"><div class="eyebrow">快速检索</div><h2>从一个真实的问题开始</h2><label for="query">搜索章节标题、关键词或内容</label><input id="query" class="searchbox" type="search" placeholder="例如：室友半夜连麦我睡不着；投简历没人回应……" autocomplete="off"><p id="count" class="muted" aria-live="polite">输入关键词即可搜索全书，也可以描述遇到的事情</p><p class="muted">检索仅提供阅读入口，不判断事实或危险等级。涉及即时人身危险，请优先寻求当地紧急服务。</p><div id="results" class="search-results" aria-live="polite"></div></section>
<section id="problems"><div class="eyebrow">按问题阅读</div><h2>不必从头读到尾</h2><p>先看和你眼前事务最有关的章节，再决定是否继续追问。每个入口都可以根据实际情况跳转。</p><div class="problem-grid">{probs}</div></section><section class="search-area"><div class="eyebrow">七类模拟试读问题</div><h2>问题复杂时，再读一篇完整推演</h2><p>七类高频问题专题分别说明不同情境、组织责任与风险边界；可先通过自然语言搜索，或直接查看专题与模拟学生试读材料。</p><a class="primary" href="deep/index.html">打开七类问题深读 →</a> <a class="secondary" href="reader-lab.html">练习21个模拟读者情境 →</a></section><section id="read"><div class="eyebrow">全书目录</div><h2>十辑，五十件值得认真讨论的事</h2><p>章节并非能力等级，也没有固定阅读年龄、年级或先后阶段。</p>{part_section}</section>
<section class="bottom-banner"><h2>遇到难事，可以先拿出一张工具卡。</h2><p>把事实、解释、权责、备选行动和反馈写清楚；可以直接打印，不必填写真实姓名或敏感资料。</p><a class="primary" href="tools/index.html">打开行动工具箱 →</a></section>'''
    (DOCS/'index.html').write_text(html_shell('首页',body,'.'),encoding='utf8')

def build():
    ds=parse()
    for x in BOOK.glob('ch*.html'):x.unlink()
    BOOK.mkdir(parents=True,exist_ok=True)
    for d in ds:
        render_ch(d,ds)
    main_index(ds)
    build_deep()
    pre=(CONTENT/'guides'/'preface.md').read_text(encoding='utf8')
    theory=(CONTENT/'guides'/'model.md').read_text(encoding='utf8')
    chapters='\n\n---\n\n'.join(clean_front(d['markdown']) for d in ds)
    whole='# 走进大学，学会与世界相处\n\n'+'基于SSCM大学生社会化网络认知模型的成长与行动指南\n\n'+pre+'\n\n---\n\n'+theory+'\n\n---\n\n'+chapters
    (ROOT/'BOOK_FULL.md').write_text(whole,encoding='utf8')
    shifted=re.sub(r'^(#{1,5}) (.+)$',lambda m:'#'+m.group(1)+' '+m.group(2), pre+'\n\n---\n\n'+theory+'\n\n---\n\n'+chapters, flags=re.M)
    (DOCS/'book-all.html').write_text(html_shell('全书连续阅读版','<div class="guide"><div class="bookarticle"><h1>走进大学，学会与世界相处</h1>'+md(shifted)+'</div></div>','.'),encoding='utf8')
    (DOCS/'search-index.json').write_text(json.dumps([{'id':d['id'],'title':d['title'],'part':d['part'],'tags':d['tags'],'text':d['markdown']} for d in ds],ensure_ascii=False),encoding='utf8')
    routes=json.loads((CONTENT/'search/intent-routes.json').read_text(encoding='utf8'))
    (DOCS/'search-guides.json').write_text(json.dumps(routes,ensure_ascii=False),encoding='utf8')
    pilot=(ROOT/'PILOT_READING_GUIDE.md').read_text(encoding='utf8')
    (DOCS/'pilot.html').write_text(html_shell('读者试用与改稿', '<div class="guide"><div class="bookarticle">'+md(pilot)+'</div></div>','.'),encoding='utf8')
    policy=(CONTENT/'guides'/'campus-policies.md').read_text(encoding='utf8')
    (DOCS/'campus-policies.html').write_text(html_shell('校规与政策核验', '<div class="guide"><div class="bookarticle">'+md(policy)+'</div></div>','.'), encoding='utf8')
    print(f'Generated {len(ds)} chapter HTML pages from editable Markdown, {sum(len(d['markdown']) for d in ds):,} source chars')

if __name__=='__main__':build()
