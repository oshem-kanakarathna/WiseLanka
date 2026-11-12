import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import fs from 'node:fs/promises';
const source=await fs.readFile(new URL('../../frontend/components/api.js',import.meta.url),'utf8');
function client(fetch){const context=vm.createContext({window:{WISELANKA_API_BASE:'https://api.example.test'},fetch,AbortController,Response,TypeError,Error,setTimeout,clearTimeout});vm.runInContext(source,context);return context.window.WiseAPI;}
test('uses configured origin and preserves JSON payloads',async()=>{
 let seen;const api=client(async(url,options)=>{seen={url,options};return Response.json({status:'GROUNDED'});});
 assert.deepEqual(await api.json('assistant/guidance',{method:'POST',body:'{"intent":"help"}'}),{status:'GROUNDED'});
 assert.equal(seen.url,'https://api.example.test/assistant/guidance');assert.equal(seen.options.body,'{"intent":"help"}');
});
test('normalises validation errors',async()=>{
 const api=client(async()=>Response.json({detail:[{loc:['body','programme_id'],msg:'Required'}]},{status:422}));
 await assert.rejects(api.json('assistant/guidance'),/programme_id: Required/);
});
test('aborts stalled requests and gives a retryable message',async()=>{
 const api=client((url,{signal})=>new Promise((resolve,reject)=>signal.addEventListener('abort',()=>reject(new DOMException('Aborted','AbortError')))));
 await assert.rejects(api.json('profile-options',{timeout:15}),/took too long/);
});
test('network failures have a user-facing connection error',async()=>{
 const api=client(async()=>{throw new TypeError('Failed to fetch');});
 await assert.rejects(api.json('profile-options'),/Cannot reach the guidance service/);
});
