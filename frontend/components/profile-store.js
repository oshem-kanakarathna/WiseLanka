/* Versioned browser-local drafts. No learner data is sent while saving. */
window.WiseProfile = (() => {
 const key='wiselanka.profile.v1';
 function read(){try{const data=JSON.parse(localStorage.getItem(key));return data?.version===1?data:null;}catch{return null;}}
 function clear(){try{localStorage.removeItem(key);}catch{}document.dispatchEvent(new Event('wiselanka:draft-cleared'));}
 const form=document.getElementById('learnerProfileForm');
 const getProfile=()=>{if(form){try{return collectProfile().learner_profile;}catch{return null;}}return read()?.profile||null;};
 if(form){
  const banner=document.createElement('div');banner.className='wl-draft';
  const status=document.createElement('p');status.setAttribute('role','status');
  status.textContent='Saved on this device';status.title='Your progress is stored only in this browser. Clear the saved draft to remove it.';
  const clearButton=document.createElement('button');clearButton.type='button';clearButton.className='secondary-button';clearButton.textContent='Clear saved draft';
  let clearing=false;
  clearButton.addEventListener('click',()=>{clearing=true;clear();location.replace(location.pathname);});
  banner.append(status,clearButton);form.before(banner);
  const saved=read();
  function restoreSkills(){if(!saved)return;form.querySelectorAll('[data-skill-id]').forEach(el=>{el.value=saved.skills?.[el.dataset.skillId]||'';});form.querySelectorAll('.qualification-row select').forEach((el,index)=>el.value=saved.awards?.[index]?.id||'');}
  if(saved){
   const olCount=Math.min(25,Number(saved.olCount)||0);
   while(form.querySelectorAll('[data-ol-row]').length<olCount)addOlSubject();
   const awardCount=Math.min(20,Number(saved.awardCount)||0);
   while(form.querySelectorAll('.qualification-row').length<awardCount)addQualification();
   for(const [id,value] of Object.entries(saved.fields||{})){
    const el=document.getElementById(id);if(!el||!form.contains(el))continue;
    if(el.type==='checkbox'||el.type==='radio')el.checked=!!value;else el.value=String(value).slice(0,1000);
   }
   form.querySelectorAll('input[name="interests"]').forEach(el=>el.checked=(saved.interests||[]).includes(el.value));
   form.querySelectorAll('[data-ol-row]').forEach((row,index)=>{const entry=saved.subjects?.[index];if(!entry)return;row.querySelector('select.subject-select').value=entry.subject;row.querySelector('select:not(.subject-select)').value=entry.grade;row.querySelector('input').value=entry.custom||'';});
   form.querySelectorAll('.qualification-row').forEach((row,index)=>{const entry=saved.awards?.[index];if(!entry)return;row.querySelectorAll('[data-qualification-field]').forEach(el=>el.value=entry[el.dataset.qualificationField]||'');});
   const complete=document.getElementById('educationComplete').checked;
   updateEducationLevel();document.getElementById('educationComplete').checked=complete;
   form.querySelectorAll('select.subject-select').forEach(el=>el.dispatchEvent(new Event('change')));
   restoreSkills();status.textContent='Draft restored';
  }
  document.addEventListener('wiselanka:profile-options',restoreSkills,{once:true});
  let timer;
  function save(){
   if(clearing)return;
   const fields={};form.querySelectorAll('input[id],select[id],textarea[id]').forEach(el=>{if(!['password','file'].includes(el.type))fields[el.id]=el.type==='checkbox'||el.type==='radio'?el.checked:el.value;});
   const data={version:1,updatedAt:Date.now(),fields,olCount:form.querySelectorAll('[data-ol-row]').length,awardCount:form.querySelectorAll('.qualification-row').length,interests:[...form.querySelectorAll('input[name="interests"]:checked')].map(el=>el.value),skills:Object.fromEntries([...form.querySelectorAll('[data-skill-id]')].map(el=>[el.dataset.skillId,el.value])),profile:getProfile()};
   data.subjects=[...form.querySelectorAll('[data-ol-row]')].map(row=>({subject:row.querySelector('select.subject-select').value,grade:row.querySelector('select:not(.subject-select)').value,custom:row.querySelector('input').value}));
   data.awards=[...form.querySelectorAll('.qualification-row')].map(row=>({id:row.querySelector('select').value,...Object.fromEntries([...row.querySelectorAll('[data-qualification-field]')].map(el=>[el.dataset.qualificationField,el.value]))}));
   try{localStorage.setItem(key,JSON.stringify(data));status.textContent='Saved on this device';}catch{status.textContent='Could not save. Keep this page open.';}
  }
  function schedule(){clearTimeout(timer);timer=setTimeout(save,250);}
  form.addEventListener('input',schedule);form.addEventListener('change',schedule);
  form.addEventListener('click',event=>{if(event.target.closest('button'))schedule();});
  addEventListener('pagehide',save);
 }
 document.addEventListener('DOMContentLoaded',()=>{
  if(form||!['eligibility','recommendations','scholarships'].includes(document.body.dataset.view)||!read()?.profile)return;
  const host=document.querySelector('main > .workspace');if(!host)return;
  const notice=document.createElement('div');notice.className='wl-draft';
  const label=document.createElement('p');label.textContent=document.body.classList.contains('ux-task-layout')?'Reuse results from your saved profile.':'A learner profile is saved on this browser. You can reuse its reported exam results.';
  const button=document.createElement('button');button.type='button';button.className='secondary-button';button.textContent='Use saved results';
  notice.append(label,button);host.before(notice);
  button.addEventListener('click',()=>{
   const education=getProfile()?.education||{};const view=document.body.dataset.view;
   function set(id,value){const el=document.getElementById(id);if(!el||value===undefined)return false;if(el.tagName==='SELECT'&&![...el.options].some(o=>o.value===value)){const option=new Option(value,value);el.appendChild(option);}el.value=value;el.dispatchEvent(new Event('change',{bubbles:true}));return true;}
   const al=Object.entries(education.A_LEVEL||{});
   if(view==='scholarships'){set('olEnglish',education.O_LEVEL?.English);set('alEnglish',education.A_LEVEL?.English);if(al.length&&getProfile()?.education_complete?.A_LEVEL===true)set('alPasses',String(al.filter(([,grade])=>['A','B','C','S'].includes(grade)).length));label.textContent='Reported exam details copied. Review them and supply citizenship, age and other scholarship details.';return;}
   if(al.length){if(view==='recommendations')setEducationLevel('A_LEVEL');[1,2,3].forEach(i=>{set('subject'+i,'');set('grade'+i,'');});al.slice(0,3).forEach(([subject,grade],i)=>{set('subject'+(i+1),subject);set('grade'+(i+1),grade);});label.textContent='Reported A/L results copied. Review all fields before checking.';}
   else if(view==='recommendations'&&education.O_LEVEL){setEducationLevel('O_LEVEL');set('olMathematics',education.O_LEVEL.Mathematics);set('olEnglish',education.O_LEVEL.English);Object.entries(education.O_LEVEL).filter(([s])=>!['Mathematics','English'].includes(s)).slice(0,4).forEach(([subject,grade],i)=>{set('olSubject'+(i+3),subject);set('olGrade'+(i+3),grade);});label.textContent='Reported O/L results copied. Review all fields before checking.';}
   else label.textContent='This tool needs A/L results. Use your learner profile for guidance on other qualifications.';
  });
 });
 return {getProfile,clear,read};
})();
