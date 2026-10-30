(function(){'use strict';
document.querySelectorAll('[data-print]').forEach(el=>el.addEventListener('click',()=>window.print()));
const storageKey='sscm-read-v1';
const button=document.querySelector('[data-complete]');
if(button){const id=button.getAttribute('data-complete');let checked=[];try{checked=JSON.parse(localStorage.getItem(storageKey)||'[]')}catch{}const paint=()=>{const yes=checked.includes(id);button.classList.toggle('is-done',yes);button.textContent=yes?'已读 ✓（点击取消）':'标记已读'};button.addEventListener('click',()=>{checked=checked.includes(id)?checked.filter(x=>x!==id):[...checked,id];try{localStorage.setItem(storageKey,JSON.stringify(checked))}catch{}paint()});paint()}
const query=document.getElementById('query'),results=document.getElementById('results'),count=document.getElementById('count');
if(query&&results){
 let catalog=null,guides=null;
 const make=(tag,content,cl)=>{const el=document.createElement(tag);if(cl)el.className=cl;el.textContent=content;return el};
 const render=()=>{
   const q=SSCMSearch.normalize(query.value);results.replaceChildren();
   if(!q){count.textContent='输入关键词或一句话，查看相关阅读路径';return}
   if(!guides||!catalog){count.textContent='正在加载本地检索目录…';return}
   const {routes:ranked,chapters}=SSCMSearch.rank(q,guides,catalog);
   count.textContent=ranked.length?`找到 ${ranked.length} 条问题阅读路径；请根据事实选择，而非仅凭关键词认定原因。`:`没有发现直接匹配的问题路径${chapters.length?'，以下是章节检索结果':''}。可缩短为关键词，或查看七类深读专题。`;
   ranked.forEach(({g})=>{
     const card=document.createElement('div');card.className='hit search-path';
     const kicker=make('small',g.category+(g.safety?' · 涉及权限或安全边界':''));
     const a=document.createElement('a');a.href=g.primary;a.append(make('strong',g.title));
     const desc=make('p',g.summary,'muted');
     const second=document.createElement('a');second.href=g.secondary;second.append(make('small','另一个阅读入口：对照章节或专题'));
     card.append(kicker,a,desc,second);results.append(card);
   });
   if(!ranked.length)chapters.forEach(({v})=>{
     const a=document.createElement('a');a.className='hit';a.href='book/ch'+String(v.id).padStart(2,'0')+'.html';
     a.append(make('strong','第'+String(v.id).padStart(2,'0')+'章 · '+v.title),make('small','第'+v.part+'辑 | '+v.tags.join('、')));results.append(a);
   });
   if(!ranked.length&&!chapters.length){const a=document.createElement('a');a.className='hit';a.href='deep/index.html';a.textContent='查看七类高频问题专题（课程、宿舍、科研、社团、亲密关系、就业与权益）';results.append(a)}
 };
 query.addEventListener('input',render);
 Promise.all([fetch('./search-index.json').then(r=>{if(!r.ok)throw Error('chapters');return r.json()}),fetch('./search-guides.json').then(r=>{if(!r.ok)throw Error('guides');return r.json()})])
    .then(([c,g])=>{catalog=c;guides=g;render()})
    .catch(()=>{count.textContent='无法读取本地检索目录。请从七类高频专题或下方目录进入。';const a=document.createElement('a');a.href='deep/index.html';a.textContent='七类高频问题专题';results.replaceChildren(a)});
}
})();