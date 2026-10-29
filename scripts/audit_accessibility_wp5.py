"""Pinned axe-core check plus automated reflow probes; not WCAG certification."""
import hashlib
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/wp5'
AXE=Path(os.environ.get('WISELANKA_AXE_PATH','/private/tmp/wiselanka-wp5-axe.min.js'))
EXPECTED='880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb'
API=os.environ.get('WISELANKA_API_BASE','http://127.0.0.1:8000')


def main():
 assert hashlib.sha256(AXE.read_bytes()).hexdigest()==EXPECTED,'Use the pinned axe-core 4.10.3 artifact'
 records=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  try:
   for name,language,filled in [('learner-profile',language,filled) for language in ('en','si','ta') for filled in (False,True)]+[(name,'en',False) for name in ('eligibility','recommendations','scholarships')]:
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.add_init_script('window.WISELANKA_API_BASE='+json.dumps(API))
    page.goto('http://127.0.0.1:5500/frontend/pages/'+name+'.html')
    if name=='learner-profile':
     page.wait_for_function('window.WiseI18n.ready')
     if filled:
      for n in (1,2,3):page.locator('#alGrade'+str(n)).select_option('C')
      page.locator('#careerIntention').fill('Software engineering')
      with page.expect_response(lambda r:r.url==API+'/personalised-recommendations'):
       page.locator('#submitProfile').click()
      page.wait_for_function("!document.querySelector('#submitProfile').disabled")
     page.locator('#interfaceLanguage').select_option(language)
     page.locator('#voicePanel summary').click()
    page.add_script_tag(path=str(AXE))
    result=page.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
    reflow={}
    for width in (390,320):
     page.set_viewport_size({'width':width,'height':844})
     reflow[str(width)]=page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    records.append({'page':name,'language':language,'filled':filled,'violations':result['violations'],'incomplete':result['incomplete'],'passes':len(result['passes']),'reflow':reflow})
    print(name,language,filled,[(v['id'],v['impact'],len(v['nodes'])) for v in result['violations']],reflow,flush=True)
    page.close()
  finally:browser.close()
 report={'axe_version':'4.10.3','axe_sha256':EXPECTED,'automated_only':True,'records':records,'serious_or_critical':sum(v['impact'] in ('serious','critical') for r in records for v in r['violations'])}
 (OUT/'accessibility-final.json').write_text(json.dumps(report,indent=2)+'\n')
 assert report['serious_or_critical']==0,'Resolve serious/critical automated findings'
 assert all(all(r['reflow'].values()) for r in records),'Reflow check failed'

if __name__=='__main__':main()
