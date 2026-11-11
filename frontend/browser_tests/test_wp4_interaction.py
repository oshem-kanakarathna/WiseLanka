"""Mocked browser speech events verify handling, not native transcription accuracy."""
import json
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
CATALOGUE=json.loads((ROOT/'data/localisation/ui.json').read_text())

class WP4Tests(unittest.TestCase):
 def setUp(self):
  self.p=sync_playwright().start();self.browser=self.p.chromium.launch(headless=True)
  self.page=self.browser.new_page();self.errors=[]
  self.page.on('pageerror',lambda e:self.errors.append(str(e)))
  self.page.add_init_script('''const originalFetch=window.fetch; window.fetch=(url,...args)=>String(url).includes('/data/localisation/ui.json')?Promise.resolve({ok:true,json:async()=> ('''+json.dumps(CATALOGUE)+''')}):originalFetch(url,...args);''')
  self.page.route('**/profile-options',lambda r:r.fulfill(json={'skills':[],'qualifications':[]}))
  self.page.route('**/assistant/options',lambda r:r.fulfill(json={'programmes':[{'programme_id':'PRG0009','programme_name':'Official Engineering Title'}]}))
 def open(self,mock_voice=False,unsupported=False):
  if mock_voice:
   self.page.add_init_script('''window.voiceStarts=0; window.SpeechRecognition=class { constructor(){window.voiceMock=this;} start(){window.voiceStarts++;this.onstart();} stop(){this.onend();} abort(){this.onend();} };''')
  if unsupported:
   self.page.add_init_script('''Object.defineProperty(window,'SpeechRecognition',{value:undefined});Object.defineProperty(window,'webkitSpeechRecognition',{value:undefined});''')
  self.page.goto((ROOT/'frontend/pages/learner-profile.html').as_uri())
  self.page.wait_for_function('window.WiseI18n.ready')
 def tearDown(self):
  self.browser.close();self.p.stop()
 def test_languages_preserve_profile_and_rendered_results(self):
  self.open()
  self.page.locator('#careerIntention').fill('Build software')
  self.page.locator('#alGrade1').select_option('C')
  self.page.evaluate("renderRecommendations({recommendations:[{programme_id:'SYNTHETIC',programme_name:'Official Programme Title',category:'ELIGIBLE',academic_gap_insights:{status:'NOT_ASSESSED',groups:[],next_step:'Official source content'}}]})")
  for lang in ['si','ta','en']:
   self.page.locator('#interfaceLanguage').select_option(lang)
   self.page.wait_for_function('document.documentElement.lang === '+json.dumps(lang))
   self.assertEqual(self.page.locator('#careerIntention').input_value(),'Build software')
   self.assertEqual(self.page.locator('#alGrade1').input_value(),'C')
   self.assertEqual(self.page.locator('#submitProfile').inner_text().replace('→','').strip(),CATALOGUE[lang]['submit'])
   self.assertIn(CATALOGUE[lang]['NOT_ASSESSED'],self.page.locator('.recommendation-meta').inner_text())
   self.assertIn('Official Programme Title',self.page.locator('#recommendationList').inner_text())
  self.assertEqual(self.errors,[])
 def test_localised_validation_and_dynamic_labels(self):
  self.open();self.page.locator('#interfaceLanguage').select_option('ta')
  self.page.locator('#submitProfile').click()
  self.assertIn(CATALOGUE['ta']['grades_error'],self.page.locator('#statusMessage').inner_text())
  self.assertEqual(self.page.locator('label[for="alSubject1"]').inner_text(),CATALOGUE['ta']['al_subject'].replace('{number}','1'))
 def test_assistant_request_text_and_keyboard(self):
  self.open()
  self.page.route('**/assistant/guidance',lambda r:r.fulfill(json={'status':'GROUNDED','summary':CATALOGUE['en']['guidance_note'],'blocks':[{'heading_key':'programme','content_language':'en','lines':['Official Engineering Title']}],'sources':[]}))
  self.page.locator('#assistantProgramme').select_option('PRG0009')
  self.page.locator('#assistantTopic').select_option('programme')
  self.page.locator('#assistantSend').focus();self.page.keyboard.press('Enter')
  self.page.get_by_text('Official Engineering Title',exact=True).last.wait_for()
  self.page.locator('#interfaceLanguage').select_option('si')
  self.assertEqual(self.page.locator('#assistantStatus').inner_text(),CATALOGUE['si']['guidance_note'])
  self.assertEqual(self.page.locator('#assistantProgramme').input_value(),'PRG0009')
 def test_native_unsupported_keeps_text_alternative(self):
  self.open(unsupported=True)
  self.page.locator('#voicePanel summary').click()
  self.assertTrue(self.page.locator('#voiceStart').is_disabled())
  self.assertIn('unavailable',self.page.locator('#voiceStatus').inner_text())
  self.page.locator('#assistantQuestion').fill('eligibility')
  self.assertTrue(self.page.locator('#assistantSend').is_enabled())
 def test_consent_and_permission_denial(self):
  self.open(mock_voice=True);self.page.locator('#voicePanel summary').click()
  self.page.locator('#voiceStart').click();self.assertEqual(self.page.evaluate('window.voiceStarts'),0)
  self.page.locator('#voiceConsent').check();self.page.locator('#voiceStart').click()
  self.page.evaluate("window.voiceMock.onerror({error:'not-allowed'});window.voiceMock.onend()")
  self.assertEqual(self.page.locator('#voiceStatus').inner_text(),CATALOGUE['en']['voice_denied'])
  self.assertTrue(self.page.locator('#voiceStart').is_enabled())
 def test_transcript_editable_not_auto_submitted(self):
  self.open(mock_voice=True);self.page.locator('#voicePanel summary').click()
  self.page.locator('#voiceConsent').check();self.page.locator('#voiceStart').click()
  self.page.evaluate("window.voiceMock.onresult({results:[[{transcript:'eligibility'}]]})")
  self.assertEqual(self.page.locator('#assistantQuestion').input_value(),'eligibility')
  self.assertEqual(self.page.locator('#assistantResponse').inner_text(),'')
  self.page.locator('#voiceStop').click()
  self.assertEqual(self.page.locator('#voiceStatus').inner_text(),CATALOGUE['en']['voice_stopped'])
  self.page.locator('#assistantQuestion').fill('skills')
 def test_recognition_language_unavailable(self):
  self.open(mock_voice=True);self.page.locator('#voicePanel summary').click()
  self.page.locator('#voiceLanguage').select_option('si-LK');self.page.locator('#voiceConsent').check();self.page.locator('#voiceStart').click()
  self.assertEqual(self.page.evaluate('window.voiceMock.lang'),'si-LK')
  self.page.evaluate("window.voiceMock.onerror({error:'language-not-supported'})")
  self.assertEqual(self.page.locator('#voiceStatus').inner_text(),CATALOGUE['en']['voice_language'])
 def test_network_and_transcription_errors(self):
  self.open(mock_voice=True);self.page.locator('#voicePanel summary').click();self.page.locator('#voiceConsent').check()
  for error in ('network','no-speech','audio-capture'):
   self.page.locator('#voiceStart').click();self.page.evaluate('window.voiceMock.onerror({error:'+json.dumps(error)+'})')
   self.assertEqual(self.page.locator('#voiceStatus').inner_text(),CATALOGUE['en']['voice_error'])
 def test_missing_translation_keys_fail_closed_to_english(self):
  broken=json.loads(json.dumps(CATALOGUE));del broken['ta']['submit']
  self.page.add_init_script('window.fetch=(url)=>Promise.resolve({ok:true,json:async()=> ('+json.dumps(broken)+')});')
  self.page.goto((ROOT/'frontend/pages/learner-profile.html').as_uri())
  self.page.wait_for_function('document.querySelector("#interfaceLanguage").disabled')
  self.assertIn('English remains available',self.page.locator('#translationNotice').inner_text())
 def test_mobile_reflow_in_all_languages(self):
  self.open();self.page.set_viewport_size({'width':390,'height':844})
  for language in ('en','si','ta'):
   self.page.locator('#interfaceLanguage').select_option(language)
   self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'))
 def test_assistant_error_after_success_not_overwritten_by_translation(self):
  self.open()
  self.page.route('**/assistant/guidance',lambda r:r.fulfill(json={'status':'GROUNDED','summary':CATALOGUE['en']['guidance_note'],'blocks':[],'sources':[]}))
  self.page.locator('#assistantSend').click()
  self.page.wait_for_function('!document.querySelector("#assistantSend").disabled')
  self.page.route('**/assistant/guidance',lambda r:r.abort())
  self.page.locator('#assistantSend').click()
  self.page.wait_for_function('!document.querySelector("#assistantSend").disabled')
  self.page.locator('#interfaceLanguage').select_option('ta')
  self.assertEqual(self.page.locator('#assistantStatus').inner_text(),CATALOGUE['ta']['chat_error'])
