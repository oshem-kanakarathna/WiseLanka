from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
import re,json
O=Path(__file__).resolve().parent
class T(HTMLParser):
 def __init__(self):super().__init__();self.ignore=0;self.parts=[]
 def handle_starttag(self,t,a):
  if t in ('script','style','noscript'):self.ignore+=1
  if t in ('p','div','li','h1','h2','h3','h4','br','tr'):self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style','noscript'):self.ignore=max(0,self.ignore-1)
  if t in ('p','div','li','h1','h2','h3','h4','tr'):self.parts.append('\n')
 def handle_data(self,d):
  if not self.ignore:self.parts.append(d)
for p in sorted((O/'sources').glob('*')):
 if p.suffix=='.html':
  t=T();t.feed(p.read_text(errors='replace'));text='\n'.join(s for line in ''.join(t.parts).splitlines() if (s:=' '.join(line.split())))
 elif p.suffix=='.pdf':
  r=PdfReader(p);text='\n\n'.join('PDF PAGE '+str(i+1)+'\n'+(page.extract_text() or '') for i,page in enumerate(r.pages))
 else:continue
 (O/'sources'/(p.stem+'.txt')).write_text(text)
 print(p.stem,len(text),'characters')
