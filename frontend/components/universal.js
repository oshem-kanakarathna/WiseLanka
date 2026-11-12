/* Keep the template's expandable content keyboard-native and readable. */
(() => {
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 document.querySelectorAll('.un-faq details').forEach(item=>item.addEventListener('toggle',()=>{
  if(!item.open)return;
  const content=item.querySelector('p');
  if(content?.animate&&!reduced.matches)content.animate([{opacity:0,translate:'0 -5px'},{opacity:1,translate:'0 0'}],{duration:260,easing:'ease-out'});
 }));

 const hero=document.querySelector('[data-hero-slideshow]');
 if(hero){
  let inView=true;
  const update=()=>hero.classList.toggle('is-paused',!inView||document.hidden);
  if('IntersectionObserver' in window)new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;update();}).observe(hero);
  document.addEventListener('visibilitychange',update);
  update();
 }
})();
