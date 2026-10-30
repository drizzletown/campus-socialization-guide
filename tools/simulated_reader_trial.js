#!/usr/bin/env node
/** Reproducible text-only simulated-reader retrieval test. No human subjects. */
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const core=require(path.join(root,'docs/assets/search-core.js'));
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const catalog=read('docs/search-index.json');
const routes=read('docs/search-guides.json');
const groups=[['content/evaluation/role-trials.json','模拟读者（21个案例）'],['content/evaluation/paraphrase-tests.json','转述问题（20条）']];
let sums=[];let failures=[];
for(const [file,label] of groups){
  const tests=read(file),rows=[];
  for(const item of tests){
    const ranked=core.rank(item.query,routes,catalog).routes.map(x=>x.g.id);
    const at=ranked.indexOf(item.route);const result=at===0?'top1':at>=0&&at<3?'top3':'miss';
    // v1.3 full-sentence search relied on literal containment of the whole query in title/tags/text.
    const q=item.query.toLowerCase();
    const oldHits=catalog.filter(v=>v.title.toLowerCase().includes(q)||v.tags.join(' ').toLowerCase().includes(q)||v.text.toLowerCase().includes(q));
    rows.push({id:item.id||'-',query:item.query,expected:item.route,top:ranked.slice(0,3),status:result,legacyHit:oldHits.length>0});
    if(result==='miss')failures.push({label,...rows[rows.length-1]});
  }
  const count=(key)=>rows.filter(x=>x.status===key).length;
  const summary={label,total:rows.length,top1:count('top1'),top3:count('top3'),miss:count('miss'),oldHit:rows.filter(x=>x.legacyHit).length};sums.push(summary);
  console.log(label,JSON.stringify(summary));
}
const negative=['我是不是不合群','最近心情不好','不知道该怎么办','明天的天气怎么样','我好想有个朋友','学校好大','有人和我说话','我很紧张'];
const overlySpecific=negative.map(query=>({query,matches:core.rank(query,routes,catalog).routes.map(x=>x.g.id)})).filter(v=>v.matches.length>0);
console.log('模糊问句误路由检查',JSON.stringify({tested:negative.length,overlySpecific}));
if(failures.length)console.log('MISSES:',JSON.stringify(failures,null,2));
fs.writeFileSync(path.join(root,'SIMULATED_RETRIEVAL_RESULTS_v1.4.json'),JSON.stringify({summary:sums,failures,negativeTotal:negative.length,overlySpecific},null,2)+'\n');
if(failures.length||overlySpecific.length)process.exitCode=1;
