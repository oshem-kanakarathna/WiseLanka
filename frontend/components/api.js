/* One transport for all assessment and guidance requests. */
window.WiseAPI = (() => {
 const base=(window.WISELANKA_API_BASE||'').replace(/\/$/,'');
 function endpoint(path){
  if(!base)throw new Error('The API address is not configured. Set WISELANKA_API_BASE and rebuild the frontend.');
  return base+'/'+path.replace(/^\//,'');
 }
 async function request(path,options={}){
  const {timeout=45000,...init}=options;
  const target=/^https?:\/\//.test(path)?path:endpoint(path);
  const controller=new AbortController();
  const abort=()=>controller.abort(init.signal?.reason);
  if(init.signal?.aborted)abort();else init.signal?.addEventListener('abort',abort,{once:true});
  let timedOut=false;
  const timer=setTimeout(()=>{timedOut=true;controller.abort();},timeout);
  try{
   const response=await fetch(target,{...init,signal:controller.signal});
   if(!response.ok){
    const data=await response.json().catch(()=>({}));
    const detail=typeof data.detail==='string'?data.detail:Array.isArray(data.detail)?data.detail.map(e=>`${(e.loc||[]).slice(1).join(' / ')}: ${e.msg}`).join('; '):'';
    const error=new Error(detail||(response.status===503?'The guidance service is temporarily unavailable. Please try again.':`The request failed (${response.status}). Please try again.`));
    error.status=response.status;throw error;
   }
   // Consume the body under the same timeout, including stalled responses.
   const body=await response.text();
   return new Response(body,{status:response.status,statusText:response.statusText,headers:response.headers});
  }catch(error){
   if(timedOut)throw new Error('The service took too long to respond. It may be starting up. Please try again.');
   if(error.name==='AbortError')throw new Error('The request was cancelled.');
   if(error instanceof TypeError)throw new Error('Cannot reach the guidance service. Check your connection and try again.');
   throw error;
  }finally{clearTimeout(timer);init.signal?.removeEventListener('abort',abort);}
 }
 async function json(path,options){return (await request(path,options)).json();}
 return {base,endpoint,fetch:request,json};
})();
