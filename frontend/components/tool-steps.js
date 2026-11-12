/* Shared guided flow for assessment tools; existing handlers own API requests. */
(() => {
 const view=document.body.dataset.view;
 if(!['eligibility','scholarships','recommendations'].includes(view))return;
 const one=s=>document.querySelector(s);
 const workspace=one('main > .workspace');
 const panel=workspace?.firstElementChild;
 const originalForm=view==='scholarships'?one('#scholarshipForm'):null;
 const host=originalForm||panel;
 const submit=one(view==='recommendations'?'#recommendButton':'#checkButton');
 if(!host||!submit)return;
 let definitions;
 if(view==='eligibility')definitions=[
  ['Choose a programme','Select the programme you want to check.',[one('label[for="programme"]'),one('#programme')]],
  ['Add your results','Choose your three A/L subjects and actual grades.',[...panel.querySelectorAll('.subject-row')]]
 ];
 if(view==='recommendations')definitions=[
  ['Choose your level','Select the examination results you want to use.',[one('.education-level-section')]],
  ['Add your results','Enter your actual subjects and grades.',[one('#alResultsForm'),one('#olResultsForm')]],
  ['Choose a destination','Optional. Leave the target empty to explore available options.',[one('.target-programme-section')]]
 ];
 if(view==='scholarships')definitions=[
  ['Choose a scholarship','Select the scholarship you want to explore.',[one('#scholarshipId')?.closest('.field')]],
  ['Your background','Choose the details you know. Missing information may remain unassessed.',[one('#citizenship')?.closest('.field'),one('#age')?.closest('.field'),one('#stateStudent')?.closest('.field')]],
  ['Education & study field','Add your examination details and intended field of study.',[...originalForm.querySelectorAll('.field-grid'),one('#field')?.closest('.field')]]
 ];
 if(definitions.some(d=>d[2].some(n=>!n)))return;
 const stages=definitions.map(([title,hint,nodes])=>{const el=document.createElement('section');el.className='tool-stage';el.setAttribute('aria-label',title);nodes.forEach(n=>el.append(n));host.insertBefore(el,submit);return el;});
 definitions.push(['Review & check','Check these details. Use Edit to change anything before submitting.',[]]);
 const review=document.createElement('section');review.className='tool-stage tool-review';host.insertBefore(review,submit);stages.push(review);
 const progress=document.createElement('nav');progress.className='tool-progress';progress.setAttribute('aria-label','Assessment steps');
 const heading=document.createElement('h2');heading.className='tool-step-heading';heading.tabIndex=-1;
 const hint=document.createElement('p');hint.className='tool-step-hint';
 host.prepend(progress,heading,hint);
 const buttons=definitions.map(([title],i)=>{const b=document.createElement('button');b.type='button';b.textContent=(i+1)+'. '+title;b.addEventListener('click',()=>go(i));progress.append(b);return b;});
 const actions=document.createElement('div');actions.className='tool-actions';
 const back=document.createElement('button');back.type='button';back.className='secondary-button';back.textContent='Back';back.addEventListener('click',()=>go(current-1));
 const next=document.createElement('button');next.type='button';next.className='primary-button';next.addEventListener('click',()=>go(current+1));actions.append(back,next);host.insertBefore(actions,submit);
 const results=document.createElement('div');results.className='tool-results';results.hidden=true;results.tabIndex=-1;results.setAttribute('role','region');results.setAttribute('aria-label','Assessment results');
 [...workspace.children].filter(n=>n!==panel).forEach(n=>results.append(n));workspace.append(results);
 let current=0;
 document.body.classList.add('tool-guided');
 if(originalForm)originalForm.noValidate=true;
 function activeControls(index){return [...stages[index].querySelectorAll('input,select,textarea')].filter(el=>!el.disabled&&!el.closest('.hidden')&&el.type!=='hidden');}
 function valid(index){const invalid=activeControls(index).find(el=>!el.checkValidity());if(!invalid)return true;current=index;show(false);invalid.reportValidity();return false;}
 function buildReview(){review.replaceChildren();stages.slice(0,-1).forEach((stage,i)=>{
  const block=document.createElement('div');block.className='tool-review-group';const title=document.createElement('h3');title.textContent=definitions[i][0];const edit=document.createElement('button');edit.type='button';edit.className='tool-edit';edit.textContent='Edit';edit.setAttribute('aria-label','Edit '+definitions[i][0]);edit.addEventListener('click',()=>go(i));block.append(title,edit);
  const list=document.createElement('dl');activeControls(i).forEach(el=>{if(['button','submit'].includes(el.type))return;const label=el.labels?.[0]?.textContent.trim()||el.getAttribute('aria-label')||'Selection';const dt=document.createElement('dt');dt.textContent=label;const dd=document.createElement('dd');dd.textContent=el.selectedOptions?el.selectedOptions[0]?.textContent.trim()||'Not provided':el.type==='checkbox'?(el.checked?'Yes':'No'):el.value.trim()||'Not provided';list.append(dt,dd);});
  stage.querySelectorAll('[aria-pressed="true"]').forEach(el=>{const dt=document.createElement('dt');dt.textContent='Education level';const dd=document.createElement('dd');dd.textContent=el.textContent.replace(/\s+/g,' ').trim();list.append(dt,dd);});block.append(list);review.append(block);
 });}
 function show(focus=true){stages.forEach((stage,i)=>stage.hidden=i!==current);buttons.forEach((b,i)=>{if(i===current)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});heading.textContent=definitions[current][0];hint.textContent=definitions[current][1];back.hidden=current===0;next.hidden=current===stages.length-1;submit.hidden=current!==stages.length-1;next.textContent=current===stages.length-2?'Review my details':'Continue';if(current===stages.length-1)buildReview();if(focus)heading.focus();}
 function go(index){if(index<0||index>=stages.length||submit.disabled)return;if(index>current){for(let i=0;i<=Math.min(index-1,stages.length-2);i++)if(!valid(i))return;}current=index;show();}
 function guard(event){if(current!==stages.length-1){event.preventDefault();event.stopImmediatePropagation();go(current+1);return;}for(let i=0;i<stages.length-1;i++)if(!valid(i)){event.preventDefault();event.stopImmediatePropagation();return;}results.hidden=false;}
 submit.addEventListener('click',guard,true);
 if(originalForm)originalForm.addEventListener('submit',guard,true);
 show(false);
})();
