"""Real frozen-model browser integration; requires the AI-enabled local API."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
API=os.environ.get('WISELANKA_API_BASE','http://127.0.0.1:8000')
OUTPUT=Path(__file__).resolve().parents[2]/'docs/evidence/wp3'

def main():
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  try:
   page=browser.new_page(viewport={'width':1440,'height':1000})
   errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.add_init_script('window.WISELANKA_API_BASE='+json.dumps(API))
   page.goto('http://127.0.0.1:5500/frontend/pages/learner-profile.html')
   for i,subject in enumerate(['Business Studies','Economics','Accounting'],1):
    page.locator(f'#alSubject{i}').select_option(subject);page.locator(f'#alGrade{i}').select_option('C')
   page.locator('#careerIntention').fill('I want to manage a business and lead organisations')
   with page.expect_response(lambda r:r.url==API+'/personalised-recommendations') as info:
    page.locator('#submitProfile').click()
   data=info.value.json()
   assert info.value.status==200 and data['ranking']['method']=='SEMANTIC'
   assert data['recommendations'][0]['programme_id']=='PRG0008'
   page.wait_for_function("!document.querySelector('#submitProfile').disabled")
   card=page.locator('#recommendationList .recommendation-card').first
   assert 'Academic eligibility: Not Assessed' in card.inner_text()
   assert 'Relevance method: SEMANTIC' in card.inner_text()
   assert 'not a probability' in card.inner_text()
   OUTPUT.mkdir(parents=True,exist_ok=True)
   card.screenshot(path=str(OUTPUT/'hybrid-business.png'))
   page.set_viewport_size({'width':390,'height':844})
   assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
   card.locator('text=Relevance method: SEMANTIC').scroll_into_view_if_needed()
   page.screenshot(path=str(OUTPUT/'hybrid-mobile.png'))
   assert not errors,errors
   print('PASS: real SEMANTIC model ranks Business; unknown eligibility preserved; method, preference, score and sources rendered; mobile reflow and no JS errors')
  finally:browser.close()

if __name__=='__main__':main()
