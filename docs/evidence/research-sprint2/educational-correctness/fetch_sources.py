"""Snapshot active source URLs, without altering catalogue verification dates."""
import csv,hashlib,json,time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urldefrag
from urllib.error import HTTPError
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent

def get(row):
 url=urldefrag(row['source_url'])[0];name=row['source_id']
 started=datetime.now(timezone.utc).isoformat()
 result={'source_id':name,'requested_url':row['source_url'],'retrieved_utc':started,'historical_retrieved_date':row['retrieved_date']}
 try:
  with urlopen(Request(url,headers={'User-Agent':'WiseLanka-Academic-Source-Verification/1.0'}),timeout=18) as r:
   data=r.read();ctype=r.headers.get('Content-Type','');ext='.pdf' if data.startswith(b'%PDF') else '.html';path=OUT/'sources'/(name+ext);path.write_bytes(data)
   result.update(http_status=r.status,final_url=r.url,content_type=ctype,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),snapshot=str(path.relative_to(OUT)))
 except Exception as e:result.update(error=type(e).__name__+': '+str(e),http_status=getattr(e,'code',None))
 return result

def main():
 with (ROOT/'data/metadata/evidence_sources.csv').open(newline='') as f:rows=list(csv.DictReader(f))
 with ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(get,rows))
 (OUT/'FETCH_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
 for r in results:print(r['source_id'],r.get('http_status'),r.get('bytes'),r.get('error',''))
 if all('error' in r and ('nodename' in r['error'] or 'resolve' in r['error']) for r in results):raise SystemExit(2)
if __name__=='__main__':main()
