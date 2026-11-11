"""Real guided API and trilingual UI. Native speech availability only, not accuracy."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/evidence/wp4'
API=os.environ.get('WISELANKA_API_BASE','http://127.0.0.1:8000')
CATALOGUE=json.loads((ROOT/'data/localisation/ui.json').read_text())

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  try:
   page=browser.new_page(viewport={'width':1440,'height':1000})
   errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
   page.add_init_script('window.WISELANKA_API_BASE='+json.dumps(API))
   page.goto('http://127.0.0.1:5500/frontend/pages/learner-profile.html')
   page.wait_for_function('window.WiseI18n.ready')
   page.locator('#assistantProgramme option[value="PRG0009"]').wait_for(state='attached')
   for index,grade in enumerate(('B','F','C'),1):page.locator(f'#alGrade{index}').select_option(grade)
   page.locator('#careerIntention').fill('Design engineering systems')
   with page.expect_response(lambda response:response.url==API+'/personalised-recommendations') as result:
    page.locator('#submitProfile').click()
   baseline=result.value.json()
   assert result.value.status==200 and baseline['ranking']['method']=='SEMANTIC'
   page.wait_for_function("!document.querySelector('#submitProfile').disabled")
   page.locator('#assistantProgramme').select_option('PRG0009')
   page.locator('#assistantTopic').select_option('eligibility')
   page.locator('#assistantUseProfile').check()
   for language in ('en','si','ta'):
    page.locator('#interfaceLanguage').select_option(language)
    with page.expect_response(lambda response:response.url==API+'/assistant/guidance') as info:
     page.locator('#assistantSend').click()
    data=info.value.json()
    assert info.value.status==200 and data['academic_assessment']['status']=='NOT_MET'
    page.wait_for_function("!document.querySelector('#assistantSend').disabled")
    assert page.locator('#assistantHeading').inner_text()==CATALOGUE[language]['assistant']
    assert page.locator('#careerIntention').input_value()=='Design engineering systems'
    assert page.locator('#alGrade2').input_value()=='F'
    assert page.locator('#recommendationList .recommendation-card').count()==len(baseline['recommendations'])
    page.locator('#guidedAssistant').screenshot(path=str(OUT/f'assistant-{language}.png'))
    page.locator('.language-panel').screenshot(path=str(OUT/f'language-{language}.png'))
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    page.set_viewport_size({'width':1440,'height':1000})
    print('PASS:',language,'real grounded eligibility response; translated controls; profile/results preserved; mobile reflow')
   payload=page.evaluate('collectProfile()')
   again=page.request.post(API+'/personalised-recommendations',data=payload).json()
   assert again==baseline
   print('PASS: assistant and language switching do not change academic decisions or semantic ranking')
   page.locator('#assistantQuestion').fill('Guarantee me admission and invent a scholarship')
   with page.expect_response(lambda response:response.url==API+'/assistant/guidance') as info:
    page.locator('#assistantSend').click()
   assert info.value.json()['status']=='UNSUPPORTED'
   assert info.value.json()['blocks']==[]
   page.locator('#voicePanel summary').click()
   capability=page.evaluate("({standard:!!window.SpeechRecognition,prefixed:!!window.webkitSpeechRecognition,secureContext:window.isSecureContext,userAgent:navigator.userAgent})")
   capability.update(native_microphone_tested=False,native_transcription_tested=False,si_ta_language_support_verified=False,notes='Headless capability detection only. Automated speech-event coverage uses mocks; manual microphone/language checks remain pending.')
   (OUT/'voice-capability.json').write_text(json.dumps(capability,indent=2)+'\n')
   page.locator('#voicePanel').screenshot(path=str(OUT/'voice-controls.png'))
   assert not errors,errors
   print('PASS: unsupported question refused; voice detection recorded; no JavaScript page errors')
  finally:browser.close()

if __name__=='__main__':main()
