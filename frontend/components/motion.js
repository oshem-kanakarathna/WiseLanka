/* Small, optional enhancements; no navigation interception or hidden content. */
(() => {
 const reduced = matchMedia('(prefers-reduced-motion: reduce)');
 const header = document.querySelector('.wl-header');
 const progress = document.createElement('div');
 progress.className = 'wl-scroll-progress'; progress.setAttribute('aria-hidden','true'); header?.append(progress);
 let scheduled = false;
 function updateScroll() {
  scheduled = false;
  header?.classList.toggle('is-scrolled',scrollY > 24);
  const extent = document.documentElement.scrollHeight - innerHeight;
  progress.style.transform = 'scaleX(' + (extent > 0 ? Math.min(1, Math.max(0,scrollY / extent)) : 0) + ')';
 }
 function schedule() { if(!scheduled){scheduled=true;requestAnimationFrame(updateScroll);} }
 addEventListener('scroll',schedule,{passive:true}); addEventListener('resize',schedule);updateScroll();
 const animations = new Set();
 function reveal(el, delay=0) {
  if(reduced.matches || typeof el.animate !== 'function' || !el.getClientRects().length)return;
  const animation=el.animate([{opacity:0,translate:'0 18px'},{opacity:1,translate:'0 0'}],{duration:600,delay,easing:'cubic-bezier(.22,1,.36,1)',fill:'backwards'});
  animations.add(animation);animation.finished.catch(()=>{}).finally(()=>animations.delete(animation));
 }
 const cards = '.un-photo-card,.un-stat-grid > div,.un-process,.un-note,.ex-step,.ex-feature,.ex-tool-cards > article,.pathway-card,.journey-portrait,.wl-pathway-choice,.about-learners > a,.about-features article,.about-steps > li';
 const sections = '.un-reveal,.ex-reveal,.landing-intro,.landing-journey-heading,.landing-benefits,.pathways-title,.about-intro,.about-section > h2,.about-split > div,.about-start';
 if('IntersectionObserver' in window){
  const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(!entry.isIntersecting)return;observer.unobserve(entry.target);const siblings=[...entry.target.parentElement.children];const index=entry.target.matches(cards)?siblings.indexOf(entry.target)%4:0;reveal(entry.target,index*65);});},{threshold:.08});
  document.querySelectorAll(cards+','+sections).forEach(el=>observer.observe(el));
 }
 // Animate only a newly opened step or result, never hide controls to animate them.
 const stageObserver=new MutationObserver(records=>{
  const changed=new Set(records.map(r=>r.target));
  changed.forEach(el=>{if(!el.hidden&&!el.classList.contains('hidden'))reveal(el);});schedule();
 });
 document.querySelectorAll('.profile-stage,.tool-stage,.results-panel,.tool-results,#resultsSummary,#scholarshipResults,#errorResult,#resultCard').forEach(el=>stageObserver.observe(el,{attributes:true,attributeFilter:['hidden','class']}));
 const sectionLinks=[...document.querySelectorAll('.about-sections a[href^="#"]')];
 if(sectionLinks.length && 'IntersectionObserver' in window){
  const positions=new Map();
  const observer=new IntersectionObserver(entries=>{entries.forEach(e=>positions.set(e.target.id,e.isIntersecting));const active=sectionLinks.find(a=>positions.get(a.hash.slice(1)));sectionLinks.forEach(a=>{if(a===active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});},{rootMargin:'-18% 0px -50% 0px',threshold:0});
  sectionLinks.forEach(a=>{const section=document.getElementById(a.hash.slice(1));if(section)observer.observe(section);});
 }
 reduced.addEventListener('change',()=>{if(reduced.matches)animations.forEach(animation=>animation.cancel());});
 addEventListener('pageshow',schedule);
})();
