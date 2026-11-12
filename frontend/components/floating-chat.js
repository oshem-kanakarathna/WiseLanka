/* Shared, local guidance chat. Programme assessments use the existing assistant. */
(() => {
 const root=new URL('../../',document.currentScript.src);
 const url=path=>new URL(path,root).href;
 if(document.querySelector('.wl-chat'))return;
 const widget=document.createElement('aside');
 widget.className='wl-chat';
 widget.setAttribute('aria-label','WiseLanka chat');
 widget.innerHTML=`<section class="wl-chat-panel" id="wl-chat-panel" aria-labelledby="wl-chat-title" hidden>
  <header class="wl-chat-heading"><video src="${url('chatbot-neutral-blink.mp4')}" poster="${url('chatbot-neutral.png')}" width="40" height="40" autoplay muted loop playsinline preload="auto" aria-hidden="true" tabindex="-1"></video><div><h2 id="wl-chat-title">WiseLanka guide</h2><p>Let's find your next step</p></div><button type="button" class="wl-chat-close" aria-label="Close chat">×</button></header>
  <div class="wl-chat-messages" role="log" aria-live="polite" aria-relevant="additions" tabindex="0" aria-label="Chat messages"></div>
  <div class="wl-chat-topics" aria-label="Suggested questions"><button type="button">Explore pathways</button><button type="button">Build my profile</button><button type="button">Scholarships</button><button type="button">Check eligibility</button></div>
  <form class="wl-chat-form"><label class="wl-chat-label" for="wl-chat-question">Your question</label><input id="wl-chat-question" placeholder="What would you like to explore?" maxlength="300" autocomplete="off" required><button type="submit" aria-label="Send question">↑</button></form>
  <p class="wl-chat-footnote">Quick guidance · Confirm requirements with providers.</p>
 </section><button type="button" class="wl-chat-launcher" aria-controls="wl-chat-panel" aria-expanded="false" aria-label="Open WiseLanka chat"><video src="${url('chatbot-neutral-blink.mp4')}" poster="${url('chatbot-neutral.png')}" width="68" height="68" autoplay muted loop playsinline preload="auto" aria-hidden="true" tabindex="-1"></video><span class="wl-chat-hint">Need a little guidance?</span></button>`;
 document.body.appendChild(widget);
 const panel=widget.querySelector('.wl-chat-panel');
 const launcher=widget.querySelector('.wl-chat-launcher');
 const happyIcon=launcher.querySelector('video').cloneNode(true);
 happyIcon.src=url('chatbot-happy-blink.mp4');
 happyIcon.className='wl-chat-happy';
 launcher.appendChild(happyIcon);
 const thinkingIcon=happyIcon.cloneNode(true);
 thinkingIcon.src=url('chatbot-thinking.mp4');
 thinkingIcon.className='wl-chat-thinking';
 launcher.appendChild(thinkingIcon);
 widget.querySelector('.wl-chat-heading video').src=url('chatbot-happy-blink.mp4');
 const input=widget.querySelector('input');
 const messages=widget.querySelector('.wl-chat-messages');
 function message(text,user=false,link){
  const bubble=document.createElement('div');
  bubble.className=user?'wl-chat-message wl-chat-user':'wl-chat-message';
  const p=document.createElement('p');p.textContent=text;bubble.appendChild(p);
  if(link){const a=document.createElement('a');a.textContent=link[0]+' ↗';a.href=url(link[1]);bubble.appendChild(a);}
  messages.appendChild(bubble);messages.scrollTop=messages.scrollHeight;
 }
 function setOpen(open){panel.hidden=!open;launcher.setAttribute('aria-expanded',String(open));launcher.setAttribute('aria-label',open?'Close WiseLanka chat':'Open WiseLanka chat');if(open)input.focus();else launcher.focus();}
 launcher.addEventListener('click',()=>setOpen(panel.hidden));
 widget.querySelector('.wl-chat-close').addEventListener('click',()=>setOpen(false));
 widget.addEventListener('keydown',event=>{if(event.key==='Escape'&&!panel.hidden)setOpen(false);});
 let thinking=false;
 async function reply(question){
  if(thinking)return;
  message(question,true);
  thinking=true;
  widget.classList.add('is-thinking');
  const headerVideo=widget.querySelector('.wl-chat-heading video');
  headerVideo.src=url('chatbot-thinking.mp4');
  headerVideo.play().catch(()=>{});
  const controls=widget.querySelectorAll('.wl-chat-topics button,.wl-chat-form button');
  controls.forEach(button=>button.disabled=true);
  messages.setAttribute('aria-busy','true');
  const indicator=document.createElement('div');
  indicator.className='wl-chat-message';
  indicator.textContent='Preparing your guidance…';
  messages.appendChild(indicator);
  messages.scrollTop=messages.scrollHeight;
  try{
  // Local replies are immediate; allow a brief, visible thinking state.
  await new Promise(resolve=>window.setTimeout(resolve,1200));
  indicator.remove();
  messages.setAttribute('aria-busy','false');
  const q=question.toLowerCase();
  if(/scholar|fund|financial/.test(q))message('Explore scholarship guidance and funding conditions. Each opportunity may have its own academic and other requirements.',false,['Explore scholarships','frontend/pages/scholarships.html']);
  else if(/eligib|qualif|results|requirement/.test(q))message('Use the eligibility tool to understand how your qualifications match recorded programme requirements. A match does not guarantee admission.',false,['Check eligibility','frontend/pages/eligibility.html']);
  else if(/profile|start|begin/.test(q))message('Build your learner profile step by step: education, interests, goals, then review. This gives WiseLanka a starting point for your guidance.',false,['Build my profile','frontend/pages/learner-profile.html']);
  else if(/path|ordinary|advanced|diploma|hnd|nvq|tvet|course|study/.test(q))message('Explore the route that matches your starting point: O/L, A/L, TVET/NVQ, or Diploma/HND. You can then review the next steps for that route.',false,['Explore pathways','frontend/pages/pathways.html']);
  else if(/about|wise.?lanka/.test(q))message('WiseLanka helps Sri Lankan learners explore education and career pathways using their qualifications, interests and goals.',false,['About WiseLanka','frontend/pages/about.html']);
  else if(/hello|hi\b|hey/.test(q))message('Hello! Choose a topic below, or ask about pathways, your profile, scholarships or eligibility.');
  else message('I can help you find the right WiseLanka tools. For a question about a specific programme or your results, open the guided assistant and select your topic and programme.',false,['Open guided assistant','frontend/pages/learner-profile.html#guidedAssistant']);
  }finally{
   indicator.remove();
   thinking=false;
   widget.classList.remove('is-thinking');
   messages.setAttribute('aria-busy','false');
   controls.forEach(button=>button.disabled=false);
   headerVideo.src=url('chatbot-happy-blink.mp4');
   headerVideo.play().catch(()=>{});
  }
 }
 widget.querySelector('form').addEventListener('submit',event=>{event.preventDefault();const question=input.value.trim();if(!question)return;input.value='';reply(question);});
 widget.querySelectorAll('.wl-chat-topics button').forEach(button=>button.addEventListener('click',()=>reply(button.textContent)));
 message('Hi! I’m your WiseLanka guide. What would you like help with today?');
})();
