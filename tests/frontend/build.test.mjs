import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {build,root} from '../../scripts/build-frontend.mjs';
test('production output contains public pages and Render configuration only',async()=>{
 const previous=process.env.WISELANKA_API_BASE;process.env.WISELANKA_API_BASE='https://wiselanka-api.example.test';
 try{
  await build();const output=path.join(root,'dist');
  const config=await fs.readFile(path.join(output,'frontend/components/config.js'),'utf8');assert.match(config,/https:\/\/wiselanka-api.example.test/);assert.doesNotMatch(config,/127\.0\.0\.1/);
  for(const privatePath of ['backend','docs','tests','data/reference','frontend/browser_tests','frontend/pages/research-evaluation.html'])await assert.rejects(fs.access(path.join(output,privatePath)));
  const files=['index.html',...['about','pathways','eligibility','learner-profile','recommendations','scholarships'].map(p=>'frontend/pages/'+p+'.html')];
  for(const file of files){const html=await fs.readFile(path.join(output,file),'utf8');assert.equal((html.match(/class="wl-nav-link"/g)||[]).length,6);assert.equal((html.match(/rel="stylesheet"/g)||[]).length,1);for(const match of html.matchAll(/<(?:script|link)\b[^>]*(?:src|href)="([^"]+)"/g)){const ref=match[1].split('?')[0];if(/^https?:/.test(ref))continue;await fs.access(ref.startsWith('/')?path.join(output,ref):path.resolve(output,path.dirname(file),ref));}}
 }finally{if(previous===undefined)delete process.env.WISELANKA_API_BASE;else process.env.WISELANKA_API_BASE=previous;}
});
test('Vercel build refuses an unconfigured backend',async()=>{
 const prior=process.env.VERCEL;const base=process.env.WISELANKA_API_BASE;process.env.VERCEL='1';delete process.env.WISELANKA_API_BASE;
 try{await assert.rejects(build(),/Set WISELANKA_API_BASE/);}finally{if(prior===undefined)delete process.env.VERCEL;else process.env.VERCEL=prior;if(base!==undefined)process.env.WISELANKA_API_BASE=base;}
});
