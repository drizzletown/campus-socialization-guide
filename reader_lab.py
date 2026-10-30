#!/usr/bin/env python3
"""Generate 21 fictional-reader exercises from editable JSON data. No user data."""
from pathlib import Path
from html import escape
import json
from build import ROOT,DOCS,CONTENT,html_shell

def run():
    tests=json.loads((CONTENT/'evaluation/role-trials.json').read_text(encoding='utf8'))
    routes={x['id']:x for x in json.loads((CONTENT/'search/intent-routes.json').read_text(encoding='utf8'))}
    categories=list(dict.fromkeys(x['category'] for x in tests))
    headings=[];parts=[]
    notes=['# 21个模拟读者任务：从问题到行动','',
           '> 全部人物和情境由编辑构造，用于检查读物是否容易找到、读懂和转化为行动；**没有邀请真实学生参加**，不得把它当成经验研究或行为效果证据。','',
           '## 如何使用','',
           '先只阅读“现实情境”，写下你准备核实的事实、可能解释、可以做的第一步和不能跨越的边界；再查看编辑给出的讨论路径。不同处境可以有多种合理行动。遇到即时危险，优先联系当地紧急服务，不继续普通练习。','']
    for i,cat in enumerate(categories,1):
        cc=[x for x in tests if x['category']==cat];assert len(cc)==3
        headings.append(f'<a href="#group{i}">{escape(cat)}（3题）</a>')
        rows=[];notes+=[f'## {i}. {cat}','']
        for t in cc:
            route=routes[t['route']]; url=route['primary']
            notes += [f'### {t["id"]} · {t["query"]}', '',f'**现实情境：** {t["scene"]}', '',
                     '**先独立思考：** 需要核实哪些事实？有没有两种可能解释？谁有处理权限？下一步做什么？怎样守住边界？','',
                     f'**应当辨认：** {t["diagnosis"]}', '',f'**可以先做：** {t["action"]}', '',
                     f'**应当由组织回应：** {t["owner"]}', '',f'**注意边界：** {t["boundary"]}', '',
                     f'**阅读入口：** [{route["title"]}](../../docs/{url})','']
            rows.append(f'<article class="trial-card"><h3>{escape(t["id"])} · {escape(t["query"])}</h3><p><b>现实情境</b>：{escape(t["scene"])}</p><p><strong>先想一想：</strong>哪些是事实？有哪些解释？谁有处理权限？如何先行一步？</p><details><summary>展开编辑讨论路径（先尝试再看）</summary><p><strong>辨认原因：</strong>{escape(t["diagnosis"])}</p><p><strong>可执行的第一步：</strong>{escape(t["action"])}</p><p><strong>需要组织回应：</strong>{escape(t["owner"])}</p><p><strong>重要边界：</strong>{escape(t["boundary"])}</p><p><a href="{escape(url)}">阅读专题：{escape(route["title"])} ↗</a></p></details></article>')
        parts.append(f'<section class="trial-group" id="group{i}"><h2>{escape(cat)}</h2><div class="trial-grid">{"".join(rows)}</div></section>')
    md='\n'.join(notes)+'\n'
    (CONTENT/'guides/reader-lab.md').write_text(md,encoding='utf8')
    introduction='<div class="guide"><p class="eyebrow">SSCM / SIMULATED READER TASKS</p><h1>如果你正在遇到一件难事</h1><p>从七类主题中任选一个虚构情境，先独立判断，再展开参考路径。每条参考路径说明可能原因、一个可执行的动作、组织应承担的责任以及应遵守的安全边界。这里不评分，也没有唯一标准答案。</p><div class="info"><strong>重要说明：</strong>21项均由编辑构造，只用于模拟试读、内容审校及检索测试，不是对真实大学生进行的问卷、访谈或行为研究。若你正在遭遇真实危险，应联系当地紧急服务与有权限的保护机构，不必先完成练习。</div><div class="trial-links">'+''.join(headings)+'</div></div>'
    (DOCS/'reader-lab.html').write_text(html_shell('21个模拟读者任务',introduction+''.join(parts),'.'),encoding='utf8')
    print('Generated simulated reader laboratory, 21 fictional role tasks')
if __name__=='__main__':run()
