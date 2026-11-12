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
  <div class="wl-chat-context"><label for="wl-chat-topic">Guidance topic</label><select id="wl-chat-topic"><option value="programme">Programme information</option><option value="eligibility">Eligibility</option><option value="progression">Progression routes</option><option value="careers">Career relationships</option><option value="scholarships">Scholarships</option><option value="help">Supported topics</option></select><label for="wl-chat-programme">Programme</label><select id="wl-chat-programme"><option value="">Choose a programme</option></select><label><input id="wl-chat-profile" type="checkbox"> Use my saved learner profile</label><p class="wl-chat-options-status" role="status"></p></div><div class="wl-chat-topics" aria-label="Suggested questions"><button type="button" data-intent="programme">Programme info</button><button type="button" data-intent="eligibility">Eligibility</button><button type="button" data-intent="scholarships">Scholarships</button><button type="button" data-intent="help">Supported topics</button></div>
  <form class="wl-chat-form"><label class="wl-chat-label" for="wl-chat-question">Your question</label><input id="wl-chat-question" placeholder="Optional question about a supported topic" maxlength="300" autocomplete="off"><button type="submit" aria-label="Send question">↑</button></form>
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
 let thinking=false;
 let hovered=false;
 const headerVideo=widget.querySelector('.wl-chat-heading video');
 const neutralIcon=launcher.querySelector('video');
 const videos=[neutralIcon,happyIcon,thinkingIcon,headerVideo];
 videos.forEach(video=>{video.autoplay=false;video.pause();});
 function syncPlayback(){
  const activeIcon=thinking?thinkingIcon:(!panel.hidden||hovered||launcher.matches(':focus-visible')?happyIcon:neutralIcon);
  videos.forEach(video=>{
   const visible=!document.hidden&&(video===activeIcon||(video===headerVideo&&!panel.hidden));
   if(visible&&video.paused)video.play().catch(()=>{});
   else if(!visible&&!video.paused)video.pause();
  });
 }
 launcher.addEventListener('pointerenter',event=>{if(event.pointerType==='mouse'){hovered=true;syncPlayback();}});
 launcher.addEventListener('pointerleave',()=>{hovered=false;syncPlayback();});
 launcher.addEventListener('focus',syncPlayback);
 launcher.addEventListener('blur',syncPlayback);
 document.addEventListener('visibilitychange',syncPlayback);
 syncPlayback();
 const input=widget.querySelector('#wl-chat-question');
 const messages=widget.querySelector('.wl-chat-messages');
 function message(text,user=false,link){
  const bubble=document.createElement('div');
  bubble.className=user?'wl-chat-message wl-chat-user':'wl-chat-message';
  const p=document.createElement('p');p.textContent=text;bubble.appendChild(p);
  if(link){const a=document.createElement('a');a.textContent=link[0]+' ↗';a.href=url(link[1]);bubble.appendChild(a);}
  messages.appendChild(bubble);messages.scrollTop=messages.scrollHeight;
 }
 function setOpen(open){if(open)loadOptions();panel.hidden=!open;launcher.setAttribute('aria-expanded',String(open));launcher.setAttribute('aria-label',open?'Close WiseLanka chat':'Open WiseLanka chat');if(open)input.focus();else launcher.focus();syncPlayback();}
 launcher.addEventListener('click',()=>setOpen(panel.hidden));
 widget.querySelector('.wl-chat-close').addEventListener('click',()=>setOpen(false));
 widget.addEventListener('keydown',event=>{if(event.key==='Escape'&&!panel.hidden)setOpen(false);});

 let optionsLoaded=false;
 let optionsPending=false;
 async function loadOptions(){
  if(optionsLoaded||optionsPending)return;
  optionsPending=true;
  const status=widget.querySelector('.wl-chat-options-status');status.textContent='Loading programmes?';
  try{
   const data=await window.WiseAPI.json('assistant/options');
   if(!Array.isArray(data.programmes))throw new Error('Programme choices are unavailable.');
   const select=widget.querySelector('#wl-chat-programme');
   data.programmes.forEach(p=>{const option=document.createElement('option');option.value=p.programme_id;option.textContent=p.programme_name;select.appendChild(option);});
   optionsLoaded=true;status.textContent='Programme choices loaded.';
  }catch(error){status.replaceChildren(document.createTextNode(error.message+' '));const retry=document.createElement('button');retry.type='button';retry.textContent='Retry';retry.addEventListener('click',loadOptions);status.appendChild(retry);}
  finally{optionsPending=false;}
 }
 function renderAnswer(data){
  if(!Array.isArray(data.blocks))throw new Error('The service returned an unexpected response. Please try again.');
  message(data.summary||'Guidance received.');
  if(data.supported_topics)message('Supported topics: '+Object.values(data.supported_topics).join(', '));
  data.blocks.forEach(block=>message((block.lines||[]).join('\n')));
  (data.sources||[]).forEach(source=>{try{const parsed=new URL(source.url);if(['https:','http:'].includes(parsed.protocol))message('Official source',false,[source.title,parsed.href]);}catch{}});
  if(data.status==='NEEDS_PROFILE')message('Build or complete your learner profile, then select ?Use my saved learner profile?.',false,['Build my profile','frontend/pages/learner-profile.html']);
 }
 async function reply(question){
  if(thinking)return;
  const intent=widget.querySelector('#wl-chat-topic').value;
  const programme=widget.querySelector('#wl-chat-programme').value;
  if(!['scholarships','help'].includes(intent)&&!programme){message('Choose a programme above before asking for this guidance.');widget.querySelector('#wl-chat-programme').focus();return;}
  const useProfile=widget.querySelector('#wl-chat-profile').checked;
  const profile=useProfile?window.WiseProfile?.getProfile():null;
  if(useProfile&&!profile){message('No complete profile is available on this browser yet.',false,['Build my profile','frontend/pages/learner-profile.html']);return;}
  message(question||widget.querySelector('#wl-chat-topic').selectedOptions[0].textContent,true);
  input.value='';thinking=true;widget.classList.add('is-thinking');
  headerVideo.src=url('chatbot-thinking.mp4');syncPlayback();
  const controls=widget.querySelectorAll('.wl-chat-topics button,.wl-chat-form button,.wl-chat-form input,.wl-chat-context select,.wl-chat-context input');
  controls.forEach(control=>control.disabled=true);
  const indicator=document.createElement('div');indicator.className='wl-chat-message';indicator.textContent='Getting guidance?';messages.appendChild(indicator);messages.scrollTop=messages.scrollHeight;
  try{
   const data=await window.WiseAPI.json('assistant/guidance',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({intent,programme_id:programme,question,language:window.WiseI18n?.language||'en',...(profile?{learner_profile:profile}:{})})});
   indicator.remove();renderAnswer(data);
  }catch(error){
   indicator.textContent=error.message+' ';
   const retry=document.createElement('button');retry.type='button';retry.textContent='Retry question';retry.addEventListener('click',()=>{indicator.remove();reply(question);});indicator.appendChild(retry);
  }finally{
   thinking=false;widget.classList.remove('is-thinking');controls.forEach(control=>control.disabled=false);
   headerVideo.src=url('chatbot-happy-blink.mp4');syncPlayback();
  }
 }
 widget.querySelector('form').addEventListener('submit',event=>{event.preventDefault();reply(input.value.trim());});
 widget.querySelectorAll('.wl-chat-topics button').forEach(button=>button.addEventListener('click',()=>{widget.querySelector('#wl-chat-topic').value=button.dataset.intent;reply('');}));
 message('Hi! Choose a topic and programme to get guidance from WiseLanka. You can also use your learner profile saved on this browser.');
})();
