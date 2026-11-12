/* Progressive enhancement: preserve the original form and assessment payload. */
(() => {
 const form = document.getElementById('learnerProfileForm');
 const fields = [...form.querySelectorAll(':scope > fieldset')];
 if (fields.length !== 7) return;
 const titles = ['Your education', 'Your interests', 'Your goals', 'Review your profile'];
 const hints = ['Add your results or an existing qualification.', 'Choose what interests you. You can skip this step.', 'Tell us what you prefer. Not sure? Leave the defaults.', 'Check your details, then find your pathways.'];
 const groups = [[fields[0],fields[1],fields[2]], [fields[4],fields[3]], [fields[5],fields[6]]];
 const submit = document.getElementById('submitProfile');
 const results = document.querySelector('.results-panel');
 const panel = document.querySelector('.profile-panel');
 let current = 0;
 form.noValidate = true;
 document.body.classList.add('profile-guided');
 const progress = document.createElement('nav'); progress.className='profile-progress'; progress.setAttribute('aria-label','Profile steps');
 const buttons = titles.map((title,i)=>{ const b=document.createElement('button'); b.type='button'; b.textContent=(i+1)+'. '+title; b.addEventListener('click',()=>go(i)); progress.append(b); return b; });
 form.before(progress);
 const heading=document.createElement('h3'); heading.className='profile-stage-title'; heading.tabIndex=-1;
 const hint=document.createElement('p'); hint.className='profile-stage-hint';
 const error=document.createElement('p'); error.className='profile-step-error'; error.setAttribute('role','alert'); error.tabIndex=-1; error.hidden=true;
 form.prepend(heading,hint,error);
 const sections=groups.map((group,i)=>{const section=document.createElement('section');section.className='profile-stage';section.setAttribute('aria-label',titles[i]);group.forEach(f=>section.append(f));form.insertBefore(section,submit);return section;});
 const review=document.createElement('section');review.className='profile-stage profile-review';review.setAttribute('aria-label','Profile review');form.insertBefore(review,submit);sections.push(review);
 const actions=document.createElement('div');actions.className='profile-step-actions';
 const back=document.createElement('button');back.type='button';back.className='secondary-button';back.textContent='Back';back.addEventListener('click',()=>go(current-1));
 const next=document.createElement('button');next.type='button';next.className='primary-button';next.addEventListener('click',()=>go(current+1));
 actions.append(back,next);form.insertBefore(actions,submit);
 function validate(){
  error.hidden=true;
  try { if(current===0 || current===3) collectProfile();
   const invalid=[...sections[current].querySelectorAll('input,select,textarea')].find(el=>el.offsetParent!==null && !el.checkValidity());
   if(invalid){invalid.reportValidity();return false;} return true;
  } catch(e){error.textContent=e.message;error.hidden=false;error.focus();return false;}
 }
 function selected(id){const el=document.getElementById(id);return el.selectedOptions ? el.selectedOptions[0]?.textContent.trim() : el.value.trim();}
 function renderReview(){
  review.replaceChildren();
  const rows=[['Education',selected('educationLevel'),0],['Existing qualifications',document.querySelectorAll('.qualification-row').length+' added',0],['Interests',[...form.querySelectorAll('input[name="interests"]:checked')].map(el=>el.value).join(', ')||'No preference',1],['Career',selected('careerGoal'),2],['Study mode',selected('studyMode'),2],['District',selected('district'),2]];
  const education=collectProfile().learner_profile.education;
  for(const [level,subjects] of Object.entries(education)) rows.splice(1,0,[level==='A_LEVEL'?'A/L results':'O/L results',Object.entries(subjects).map(([name,grade])=>name+': '+grade).join(' · ')||'No reported results',0]);
  rows.forEach(([label,value,step])=>{const row=document.createElement('div');const copy=document.createElement('div');const title=document.createElement('strong');title.textContent=label;const text=document.createElement('p');text.textContent=value;copy.append(title,text);const edit=document.createElement('button');edit.type='button';edit.className='profile-edit';edit.textContent='Edit';edit.setAttribute('aria-label','Edit '+label);edit.addEventListener('click',()=>go(step));row.append(copy,edit);review.append(row);});
 }
 function show(focus=true){sections.forEach((s,i)=>s.hidden=i!==current);buttons.forEach((b,i)=>{if(i===current)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});heading.textContent=titles[current];hint.textContent=hints[current];back.hidden=current===0;next.hidden=current===3;submit.hidden=current!==3;next.textContent=current===2?'Review my profile':'Continue';error.hidden=true;if(current===3)renderReview();if(focus)heading.focus();}
 function go(index){if(index<0||index>3)return;if(index>current&&!validate())return;if(index===3){try{collectProfile();}catch(e){current=0;show();error.textContent=e.message;error.hidden=false;error.focus();return;}}current=index;show();}
 form.addEventListener('submit',e=>{if(current!==3){e.preventDefault();e.stopImmediatePropagation();go(current+1);return;}if(!validate()){e.preventDefault();e.stopImmediatePropagation();return;}results.hidden=false;},true);
 form.addEventListener('invalid',e=>{const index=sections.findIndex(s=>s.contains(e.target));if(index>=0){current=index;show(false);}},true);
 function handleHash(){if(location.hash==='#resultsHeading')results.hidden=false;if(['#learnerProfileForm','#profileHeading'].includes(location.hash)){current=0;show(false);}}
 window.addEventListener('hashchange',handleHash);
 results.hidden=true;show(false);handleHash();
 // Keep detailed explanations available without interrupting the main choices.
 fields.forEach(field=>{[...field.querySelectorAll(':scope > p.field-help')].filter(p=>!p.id).forEach(p=>{const details=document.createElement('details');details.className='profile-detail';const summary=document.createElement('summary');summary.textContent='More information';p.before(details);details.append(summary,p);});});
 const labels=['Your background','Examination results','Other qualifications (optional)','Skills (optional)','Interests (optional)','Career goals (optional)','Study preferences (optional)'];
 fields.forEach((f,i)=>{f.querySelector('legend').textContent=labels[i];});
 document.getElementById('careerIntention').placeholder='e.g. I enjoy designing software';
})();
