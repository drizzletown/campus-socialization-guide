from pathlib import Path
import re,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs'; CSS=(DOC/'assets/site.css').read_text(encoding='utf8')
checks=[]
def run_page(browser,path,width=390,search=None,screenshot=False):
    page=browser.new_page(viewport={'width':width,'height':850})
    jsfile=DOC/('en/site-en.js' if path.startswith('en/') else 'assets/site.js')
    source=(DOC/path).read_text(encoding='utf8')
    source=re.sub(r'<link[^>]+rel="stylesheet"[^>]*>', '',source)
    source=re.sub(r'<script\s+defer[^>]+></script>', '',source)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(source,wait_until='domcontentloaded')
    page.add_style_tag(content=CSS)
    if search:
        data=(DOC/('en/search-index.json' if path.startswith('en/') else 'search-index.json')).read_text(encoding='utf8')
        guides=(DOC/'search-guides.json').read_text(encoding='utf8')
        page.evaluate('''([a,b])=>{window.fetch=(u)=>Promise.resolve({ok:true,json:()=>Promise.resolve(u.includes('search-guides')?JSON.parse(b):JSON.parse(a))})}''',[data,guides])
        if not path.startswith('en/'):
            page.add_script_tag(content=(DOC/'assets/search-core.js').read_text(encoding='utf8'))
    page.add_script_tag(content=jsfile.read_text(encoding='utf8'))
    page.wait_for_timeout(100)
    overflow=page.evaluate('document.documentElement.scrollWidth - innerWidth')
    assert overflow<=1,(path,width,'horizontal overflow',overflow)
    assert not errors,(path,width,errors)
    if search:
        page.locator('#query').fill(search)
        page.wait_for_timeout(150)
        results=page.locator('#results a').all_text_contents()
        assert len(results)>0,(path,search)
        checks.append('search '+path+' '+search+': '+results[0][:70])
    if screenshot:
        name=path.replace('/','_').replace('.html','')
        page.screenshot(path=str(ROOT/f'preview_{name}_{width}.png'),full_page=False)
    checks.append(f'{path} at {width}px: no overflow / no script errors')
    return page
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    for lang in ['index.html','en/index.html']:
        for w in [1440,390,320]:
            page=run_page(browser,lang,w,'roommate makes noise at night' if lang.startswith('en') else '室友半夜连麦',screenshot=w==390)
            assert page.locator('.lang-toggle').count()==1
            page.close()
    for path in ['book/ch07.html','en/book/ch07.html','practice.html','en/practice.html','tools/tool01.html','en/tools/tool01.html','deep/07-rights.html','en/deep/07-rights.html']:
        page=run_page(browser,path,390,screenshot=False)
        if 'practice.html' in path:
            page.locator('details summary').first.click()
            assert page.locator('details').first.get_attribute('open') is not None
        if 'tools/tool' in path:
            page.locator('[contenteditable]').first.fill('This is a test')
            assert 'test' in page.locator('[contenteditable]').first.inner_text()
        page.close()
    browser.close()
print('\n'.join(checks))
