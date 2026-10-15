const menu=document.querySelector('#menu');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));document.querySelector('#nav').classList.toggle('open',open)});
for(const link of document.querySelectorAll('#nav a'))if(link.pathname===location.pathname)link.setAttribute('aria-current','page');
const form=document.querySelector('#search-form');
if(form){
 const input=document.querySelector('#query'),results=document.querySelector('#results'),count=document.querySelector('#result-count');
 let articles;
 async function search(){
  const q=input.value.trim();history.replaceState(null,'',q?'?q='+encodeURIComponent(q):location.pathname);
  count.textContent='Բեռնում…';results.replaceChildren();
  try{
   if(!articles){const res=await fetch('/data.json');if(!res.ok)throw Error();articles=await res.json()}
   const norm=s=>s.toLocaleLowerCase('hy').normalize('NFC');
   const found=articles.filter(a=>norm(a.title+' '+a.excerpt).includes(norm(q)));
   count.textContent=found.length?`Գտնվել է ${found.length} ցուցադրական նյութ`:'Նյութեր չեն գտնվել։ Փորձեք այլ բառ։';
   for(const a of found){const card=document.createElement('a');card.className='card';card.href='/news/'+encodeURIComponent(a.slug)+'/';const badge=document.createElement('p');badge.className='meta';badge.textContent='ՑՈՒՑԱԴՐԱԿԱՆ ՆՅՈՒԹ · ՕՐԻՆԱԿ';const title=document.createElement('h3');title.textContent=a.title;const text=document.createElement('p');text.textContent=a.excerpt;card.append(badge,title,text);results.append(card)}
  }catch{count.textContent='Չհաջողվեց բեռնել նյութերը։ Փորձեք կրկին։'}
 }
 input.value=new URLSearchParams(location.search).get('q')||'';
 form.addEventListener('submit',e=>{e.preventDefault();search()});search();
}
