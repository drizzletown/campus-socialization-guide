/* SSCM v1.4: local-only question-to-reading routing. The result is not a diagnosis. */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  if(root)root.SSCMSearch=api;
})(typeof window!=='undefined'?window:null,function(){
 'use strict';
 const normalize=s=>String(s||'').toLowerCase().replace(/[\s\u3000，。！？；：、,.!?;:"“”‘’（）()\[\]【】]/g,'');
 const routeScore=(q,g)=>{
   const terms=g.aliases.map(normalize).filter(w=>w.length>=2&&q.includes(w));
   if(terms.length)return 12+Math.max(...terms.map(w=>w.length))*2+Math.min(12,(terms.length-1)*3);
   if(q.length>=2&&q.length<=5&&normalize(g.title).includes(q))return 6;
   return 0;
 };
 const rank=(query,guides,catalog)=>{
   const q=normalize(query);
   if(!q)return {routes:[],chapters:[]};
   const routes=(guides||[]).map(g=>({g,score:routeScore(q,g)})).filter(x=>x.score>0)
     .sort((a,b)=>b.score-a.score||a.g.id.localeCompare(b.g.id)).slice(0,6);
   const chapters=(catalog||[]).map(v=>({v,score:(normalize(v.title).includes(q)?8:0)+(v.tags.some(t=>normalize(t).includes(q))?5:0)+(normalize(v.text).includes(q)?2:0)}))
     .filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.v.id-b.v.id).slice(0,6);
   return {routes,chapters};
 };
 return {normalize,rank,routeScore};
});
