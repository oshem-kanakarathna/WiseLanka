/* Visual choices and predictable next actions; assessment logic stays in page tools. */
(() => {
 const root=new URL('../../',document.currentScript.src);
 const url=path=>new URL(path,root).href;
 const form=document.getElementById('learnerProfileForm');
 function disclosure(element,title,className='ux-background-details'){
  if(!element)return null;
  const details=document.createElement('details');details.className=className;
  const summary=document.createElement('summary');summary.textContent=title;
  element.before(details);details.append(summary,element);return details;
 }
 if(form){
  const education=document.getElementById('educationLevel');
  const category=document.getElementById('learnerCategory');
  const section=form.querySelector('[data-profile-section="education"]');
  const picker=document.createElement('fieldset');picker.className='ux-education-picker';
  const legend=document.createElement('legend');legend.textContent='Choose your starting point';
  const options=document.createElement('div');options.className='ux-education-options';
  const selectedStage=document.createElement('button');selectedStage.type='button';selectedStage.className='ux-current-stage';selectedStage.hidden=true;selectedStage.setAttribute('aria-expanded','false');
  options.id='ux-stage-options';selectedStage.setAttribute('aria-controls',options.id);
  selectedStage.addEventListener('click',()=>{options.hidden=!options.hidden;selectedStage.setAttribute('aria-expanded',String(!options.hidden));});
  picker.append(legend,selectedStage,options);section.before(picker);
  const stages=[['ordinary','O/L results','ordinary-level.jpeg','O_LEVEL','AL_LEARNER'],['advanced','A/L results','advanced-level.jpeg','A_LEVEL','AL_LEARNER'],['vocational','TVET / NVQ','tvet-nvq.jpeg','NONE','VOCATIONAL_LEARNER'],['diploma','Diploma / HND','diploma-hnd.jpeg','NONE','EARLY_CAREER']];
  const qualificationDetails=disclosure(form.querySelector('[data-profile-section="qualifications"]'),'Add another qualification (optional)');
  const background=disclosure(form.querySelector('[data-profile-section="context"]'),'More about your background');if(background)section.after(background);
  disclosure(form.querySelector('[data-profile-section="skills"]'),'Add skills (optional)');
  function update(){
   options.querySelectorAll('button').forEach((button,index)=>{
    const stage=stages[index];const active=education.value===stage[3]&&(education.value!=='NONE'||category.value===stage[4]);
    button.setAttribute('aria-pressed',String(active));
    if(active){selectedStage.replaceChildren();const img=document.createElement('img');img.src=url('assets/landing/'+stage[2]);img.alt='';const label=document.createElement('strong');label.textContent=stage[1];const change=document.createElement('span');change.textContent='Change';selectedStage.append(img,label,change);}
   });
   if(qualificationDetails){qualificationDetails.open=education.value==='NONE'||document.querySelectorAll('.qualification-row').length>0;qualificationDetails.querySelector('summary').textContent=education.value==='NONE'?'Add your qualification':'Add another qualification (optional)';}
  }
  stages.forEach(([key,title,photo,level,learner])=>{
   const button=document.createElement('button');button.type='button';button.className='ux-education-option';button.dataset.educationStage=key;
   const img=document.createElement('img');img.src=url('assets/landing/'+photo);img.alt='';img.width=140;img.height=100;
   const label=document.createElement('strong');label.textContent=title;button.append(img,label);
   button.addEventListener('click',()=>{const changed=education.value!==level;education.value=level;category.value=learner;if(changed)education.dispatchEvent(new Event('change',{bubbles:true}));category.dispatchEvent(new Event('change',{bubbles:true}));update();options.hidden=true;selectedStage.hidden=false;selectedStage.setAttribute('aria-expanded','false');selectedStage.focus();});
   options.append(button);
  });
  education.classList.add('ux-native-stage');education.labels?.forEach(label=>label.classList.add('ux-native-stage'));
  education.addEventListener('change',update);category.addEventListener('change',update);update();
  const requested=stages.find(stage=>stage[0]===new URLSearchParams(location.search).get('journey'));
  if(requested&&(education.value!==requested[3]||category.value!==requested[4])){education.value=requested[3];category.value=requested[4];education.dispatchEvent(new Event('change',{bubbles:true}));category.dispatchEvent(new Event('change',{bubbles:true}));update();}
  if(new URLSearchParams(location.search).has('journey')||window.WiseProfile?.read()){options.hidden=true;selectedStage.hidden=false;}
  const language=disclosure(document.querySelector('.language-panel'),'Language & accessibility','ux-settings');
  if(language)language.open=document.getElementById('interfaceLanguage').value!=='en';
  const assistant=disclosure(document.getElementById('guidedAssistant'),'Need help with a programme? Ask WiseLanka','ux-assistant-details');
  function openAssistant(){if(assistant&&location.hash==='#guidedAssistant'){assistant.open=true;requestAnimationFrame(()=>document.getElementById('guidedAssistant').scrollIntoView({block:'start'}));}}
  addEventListener('hashchange',openAssistant);openAssistant();
  const results=document.querySelector('.results-panel');
  disclosure(document.getElementById('learnerInsights'),'About these results','ux-result-details');
  form.addEventListener('input',()=>{if(results)results.hidden=true;});
  form.addEventListener('change',()=>{if(results)results.hidden=true;});
 }
 const view=document.body.dataset.view;
 if(['eligibility','scholarships'].includes(view)){
  const select=document.getElementById(view==='eligibility'?'programme':'scholarshipId');
  if(select?.options.length===1){
   const card=document.createElement('section');card.className='ux-selection-summary';card.setAttribute('aria-label',view==='eligibility'?'Selected course':'Selected scholarship');
   const tag=document.createElement('span');tag.textContent=view==='eligibility'?'COURSE TO CHECK':'SCHOLARSHIP TO CHECK';
   const title=document.createElement('strong');title.textContent=select.selectedOptions[0].textContent.replace(/\s+/g,' ').trim();card.append(tag,title);select.before(card);select.classList.add('ux-native-stage');select.labels?.forEach(label=>label.classList.add('ux-native-stage'));
  }
 }
 if(['profile','eligibility','scholarships'].includes(view)){
  const panel=document.querySelector(view==='profile'?'.profile-panel':'.tool-guided main>.workspace>:first-child');
  const progress=panel?.querySelector(view==='profile'?'.profile-progress':'.tool-progress');
  if(panel&&progress){
   document.body.classList.add('ux-task-layout');
   const body=document.createElement('div');body.className='ux-task-body';
   [...panel.childNodes].forEach(node=>body.append(node));
   const rail=document.createElement('aside');rail.className='ux-task-rail';rail.setAttribute('aria-label','Task progress');
   const title=document.createElement('h2');title.className='ux-rail-title';title.textContent=view==='profile'?'My profile':view==='eligibility'?'Course check':'Scholarship check';
   const intro=document.createElement('p');intro.className='ux-rail-caption';intro.textContent='One step at a time';
   rail.append(title,intro,progress);
   const draft=body.querySelector('.wl-draft');if(draft)rail.append(draft);
   panel.append(rail,body);
  }
 }
 const hero=document.querySelector('main>.hero');
 const heroText={eligibility:['Check a course','Choose a course. Add your results. See what matches.'],recommendations:['Find study options','Add your results to explore available routes.'],scholarships:['Check scholarship support','Choose a scholarship, then check your details.']};
 if(hero&&heroText[view]){const [title,description]=heroText[view];hero.querySelector('h1').textContent=title;const p=hero.querySelector('p');if(p)p.textContent=description;}
 const results=document.querySelector(view==='profile'?'.results-panel':'.tool-results');
 if(results){
  const next=document.createElement('section');next.className='ux-next-steps';next.hidden=true;
  const title=document.createElement('h3');title.textContent='Choose your next step';const actions=document.createElement('div');
  const links=view==='profile'?[['Check a course','frontend/pages/eligibility.html'],['Check funding','frontend/pages/scholarships.html']]:[['Explore my study options','frontend/pages/learner-profile.html'],['Ask about a programme','frontend/pages/learner-profile.html#guidedAssistant']];
  links.forEach(([label,path],index)=>{const a=document.createElement('a');a.className=index===0?'ux-primary':'ux-secondary';a.href=url(path);a.textContent=label+' →';actions.append(a);});next.append(title,actions);results.after(next);
  if(view==='scholarships'){const edit=document.createElement('button');edit.type='button';edit.className='ux-primary';edit.textContent='Edit my scholarship details';edit.addEventListener('click',()=>{document.dispatchEvent(new Event('wiselanka:edit-assessment'));document.querySelector('.tool-step-heading')?.scrollIntoView({block:'start'});});actions.firstElementChild.replaceWith(edit);}
  const submit=document.querySelector(view==='recommendations'?'#recommendButton':'#checkButton');let awaitingResult=false;
  if(view!=='profile')submit?.addEventListener('click',()=>{if(!submit.hidden)awaitingResult=true;});
  function update(){
   if(view==='profile')results.querySelectorAll('.recommendation-card:not([data-ux-ready])').forEach(card=>{
    card.dataset.uxReady='true';
    const details=document.createElement('details');details.className='ux-result-details';const summary=document.createElement('summary');summary.textContent='View requirements & explanations';details.append(summary);
    const direct=[...card.children].filter(el=>el.classList.contains('recommendation-detail'));
    let official;
    direct.forEach(el=>{
     const a=el.querySelector(':scope > a');
     if(a){official=el;a.classList.add('ux-course-link');a.textContent='View course details ↗';return;}
     const heading=el.querySelector(':scope > strong')?.textContent||'';
     if(heading.startsWith('Academic requirements:')){el.classList.add('ux-assessment-summary');return;}
     details.append(el);
    });
    if(details.children.length>1){if(official)official.before(details);else card.append(details);}
   });
   const ready=view==='profile'?!!results.querySelector('.recommendation-card'):!!results.querySelector('#resultCard:not(.hidden),#scholarshipResults:not(.hidden),.recommendation-card');next.hidden=results.hidden||results.getAttribute('aria-busy')==='true'||!ready;
   if(view!=='profile'&&ready&&!results.hidden&&!submit?.disabled&&awaitingResult){awaitingResult=false;results.focus({preventScroll:true});results.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}
  }
  if(view!=='profile'&&submit)new MutationObserver(update).observe(submit,{attributes:true,attributeFilter:['disabled']});
  new MutationObserver(update).observe(results,{subtree:true,childList:true,attributes:true,attributeFilter:['hidden','class','aria-busy']});update();
 }
})();
