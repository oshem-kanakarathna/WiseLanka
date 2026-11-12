/* Shared full navigation with a centered logo and responsive menu. */
(() => {
 const root=new URL('../../',document.currentScript.src);const url=path=>new URL(path,root).href;
 const chatStyle=document.createElement('link');chatStyle.rel='stylesheet';chatStyle.href=url('frontend/styles/floating-chat.css?v=deploy-1');document.head.appendChild(chatStyle);
 function loadChat(){const script=document.createElement('script');script.src=url('frontend/components/floating-chat.js?v=deploy-1');document.head.appendChild(script);}
 if('requestIdleCallback' in window)requestIdleCallback(loadChat,{timeout:1000});else setTimeout(loadChat,100);
 const header=document.querySelector('[data-site-header]');if(!header)return;
 const page=header.dataset.page||'home';document.body.dataset.view=location.pathname.endsWith('/recommendations.html')?'recommendations':page;
 const toggle=header.querySelector('button');const nav=header.querySelector('nav');
 function setOpen(open){toggle.setAttribute('aria-expanded',String(open));nav.dataset.open=String(open);toggle.textContent=open?'Close':'Menu';}
 toggle.addEventListener('click',()=>setOpen(toggle.getAttribute('aria-expanded')!=='true'));
 header.addEventListener('keydown',event=>{if(event.key==='Escape'){setOpen(false);toggle.focus();}});
 document.addEventListener('click',event=>{if(!header.contains(event.target))setOpen(false);});
 header.addEventListener('focusout',event=>{if(event.relatedTarget&&!header.contains(event.relatedTarget))setOpen(false);});
 nav.addEventListener('click',event=>{if(event.target.closest('a'))setOpen(false);});
 const prefetched=new Set();
 function prefetch(event){
  const anchor=event.target.closest('a');
  if(!anchor||navigator.connection?.saveData||location.protocol==='file:')return;
  const target=new URL(anchor.href);
  if(target.origin!==location.origin||target.pathname===location.pathname||prefetched.has(target.href))return;
  prefetched.add(target.href);
  const hint=document.createElement('link');hint.rel='prefetch';hint.as='document';hint.href=target.href;document.head.appendChild(hint);
 }
 nav.addEventListener('pointerover',prefetch);
 nav.addEventListener('focusin',prefetch);
})();
