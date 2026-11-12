/* Shared full navigation with a centered logo and responsive menu. */
(() => {
 const root=new URL('../../',document.currentScript.src);const url=path=>new URL(path,root).href;
 const chatStyle=document.createElement('link');chatStyle.rel='stylesheet';chatStyle.href=url('frontend/styles/floating-chat.css?v=4-thinking');document.head.appendChild(chatStyle);
 const chatScript=document.createElement('script');chatScript.src=url('frontend/components/floating-chat.js?v=4-thinking');document.head.appendChild(chatScript);
 const header=document.querySelector('[data-site-header]');if(!header)return;
 const page=header.dataset.page||'home';document.body.dataset.view=location.pathname.endsWith('/recommendations.html')?'recommendations':page;
 const link=(key,title,path)=>`<a class="wl-nav-link" href="${url(path)}"${page===key?' aria-current="page"':''}>${title}</a>`;
 header.innerHTML=`<a class="wl-skip" href="#main-content">Skip to content</a><button class="wl-menu-toggle" type="button" aria-controls="main-navigation" aria-expanded="false">Menu</button><nav class="wl-navigation" id="main-navigation" aria-label="Main navigation"><div class="wl-nav-group">${link('home','Home','index.html')}${link('pathways','Pathways','frontend/pages/pathways.html')}${link('eligibility','Eligibility','frontend/pages/eligibility.html')}</div><a class="wl-emblem-link" href="${url('index.html')}" aria-label="WiseLanka home"><img class="wl-emblem" src="${url('assets/wiselanka-logo.png')}" alt="WiseLanka logo" width="80" height="76"></a><div class="wl-nav-group">${link('scholarships','Scholarships','frontend/pages/scholarships.html')}${link('about','About','frontend/pages/about.html')}${link('profile','My Profile','frontend/pages/learner-profile.html')}</div></nav>`;
 const toggle=header.querySelector('button');const nav=header.querySelector('nav');
 function setOpen(open){toggle.setAttribute('aria-expanded',String(open));nav.dataset.open=String(open);toggle.textContent=open?'Close':'Menu';}
 toggle.addEventListener('click',()=>setOpen(toggle.getAttribute('aria-expanded')!=='true'));
 header.addEventListener('keydown',event=>{if(event.key==='Escape'){setOpen(false);toggle.focus();}});
 document.addEventListener('click',event=>{if(!header.contains(event.target))setOpen(false);});
 header.addEventListener('focusout',event=>{if(event.relatedTarget&&!header.contains(event.relatedTarget))setOpen(false);});
 nav.addEventListener('click',event=>{if(event.target.closest('a'))setOpen(false);});
})();
