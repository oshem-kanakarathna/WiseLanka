import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';

export const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const pages=['index.html',...['about','pathways','eligibility','learner-profile','recommendations','scholarships'].map(name=>`frontend/pages/${name}.html`)];
const navigation=JSON.parse(await fs.readFile(path.join(root,'frontend/navigation.json'),'utf8'));
export function header(page,prefix=''){
 const link=item=>`<a class="wl-nav-link" href="${prefix+item.path}"${item.key===page?' aria-current="page"':''}>${item.title}</a>`;
 return `<!-- Generated from frontend/navigation.json by npm run sync -->\n<a class="wl-skip" href="#main-content">Skip to content</a><button class="wl-menu-toggle" type="button" aria-controls="main-navigation" aria-expanded="false">Menu</button><nav class="wl-navigation" id="main-navigation" aria-label="Main navigation"><div class="wl-nav-group">${navigation.slice(0,3).map(link).join('')}</div><a class="wl-emblem-link" href="${prefix}index.html" aria-label="WiseLanka home"><img class="wl-emblem" src="${prefix}assets/wiselanka-logo.png" alt="WiseLanka logo" width="80" height="76"></a><div class="wl-nav-group">${navigation.slice(3).map(link).join('')}</div></nav>`;
}
function renderHeader(html,file){return html.replace(/(<header\b[^>]*data-site-header[^>]*data-page="([^"]+)"[^>]*>)[\s\S]*?<\/header>/,(_,open,page)=>open+header(page,file==='index.html'?'':'../../')+'</header>');}
export async function sync(){for(const file of pages){const target=path.join(root,file);await fs.writeFile(target,renderHeader(await fs.readFile(target,'utf8'),file));}}
export async function build(output=path.join(root,'dist')){
 const localURL='http://127.0.0.1:8000';
 const configured=process.env.WISELANKA_API_BASE;
 if(process.env.VERCEL&&!configured)throw new Error('Set WISELANKA_API_BASE to your Render HTTPS URL in Vercel before building.');
 const api=new URL(configured||localURL);
 if(!['http:','https:'].includes(api.protocol)||api.username||api.password||api.search||api.hash)throw new Error('WISELANKA_API_BASE must be a plain HTTP(S) API URL.');
 if(process.env.VERCEL&&(api.protocol!=='https:'||['localhost','127.0.0.1'].includes(api.hostname)))throw new Error('Hosted builds require a public HTTPS backend URL.');
 output=path.resolve(output);
 if(output!==path.join(root,'dist'))throw new Error('Build output must remain in the project dist directory.');
 // The resolved output is checked above before replacing generated files.
 await fs.rm(output,{recursive:true,force:true});
 await fs.mkdir(output,{recursive:true});
 for(const dir of ['components','styles'])await fs.cp(path.join(root,'frontend',dir),path.join(output,'frontend',dir),{recursive:true});
 await fs.cp(path.join(root,'assets'),path.join(output,'assets'),{recursive:true});
 await fs.mkdir(path.join(output,'data/localisation'),{recursive:true});
 await fs.copyFile(path.join(root,'data/localisation/ui.json'),path.join(output,'data/localisation/ui.json'));
 for(const file of ['chatbot-neutral.png','chatbot-neutral-blink.mp4','chatbot-happy-blink.mp4','chatbot-thinking.mp4'])await fs.copyFile(path.join(root,file),path.join(output,file));
 await fs.writeFile(path.join(output,'frontend/components/config.js'),`window.WISELANKA_API_BASE = ${JSON.stringify(api.href.replace(/\/$/,''))};\n`);
 for(const file of pages){
  let html=renderHeader(await fs.readFile(path.join(root,file),'utf8'),file);
  const matches=[...html.matchAll(/<link\b[^>]*rel="stylesheet"[^>]*>/g)];
  let css='';
  for(const match of matches){
   const href=match[0].match(/href="([^"]+)"/)?.[1];if(!href)throw new Error('Stylesheet without href: '+file);
   const cssPath=path.resolve(root,path.dirname(file),href.split('?')[0]);
   if(!cssPath.startsWith(root+path.sep))throw new Error('Stylesheet outside project');
   let content=await fs.readFile(cssPath,'utf8');
   content=content.replace(/url\((['"]?)([^)'"\s]+)\1\)/g,(original,quote,ref)=>{
    if(/^(?:data:|https?:|\/|#)/.test(ref))return original;
    const absolute=path.resolve(path.dirname(cssPath),ref);
    return `url("/${path.relative(root,absolute).split(path.sep).join('/')}")`;
   });
   css+=`\n/* ${path.relative(root,cssPath)} */\n${content}\n`;
  }
  const name=path.basename(file,'.html');const hash=createHash('sha256').update(css).digest('hex').slice(0,12);
  const bundle=`frontend/styles/bundles/${name}.${hash}.css`;
  await fs.mkdir(path.dirname(path.join(output,bundle)),{recursive:true});await fs.writeFile(path.join(output,bundle),css);
  matches.forEach((match,index)=>html=html.replace(match[0],index===matches.length-1?`<link rel="stylesheet" href="/${bundle}">`:''));
  await fs.mkdir(path.dirname(path.join(output,file)),{recursive:true});await fs.writeFile(path.join(output,file),html);
 }
 console.log(`Built ${pages.length} public pages with bundled CSS. API: ${api.origin}`);
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 if(process.argv.includes('--sync'))await sync();else await build();
}
