"""Optional QA preview: Playwright plus pypdf (separate QA tooling)."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1];out=root/'poster'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':1740,'height':1300},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((out/'research-poster.html').as_uri());page.locator('img').wait_for()
 assert page.locator('img').evaluate('(img)=>img.complete && img.naturalWidth>0')
 page.locator('main').screenshot(path=str(out/'poster-preview.png'))
 page.pdf(path=str(out/'research-poster-draft.pdf'),print_background=True,prefer_css_page_size=True)
 record={'image_loaded':True,'page_errors':errors,'screen_dimensions':page.locator('main').bounding_box(),'print_pages':len(PdfReader(out/'research-poster-draft.pdf').pages)}
 assert record['print_pages']==1,record
 assert not errors,errors
 (out/'POSTER_RENDER_CHECK.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(record,indent=2))
 browser.close()
