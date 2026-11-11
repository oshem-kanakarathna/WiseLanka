"""Explicit network-only setup. No learner information is read or transmitted."""
import hashlib
import json
import shutil
import sys
import urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.app.relevance.encoder import DEFAULT_DIR, REVISION, MODEL_ID


def main():
    lock = Path(__file__).resolve().parents[1]/'backend/app/relevance/model-lock.json'
    metadata = json.loads(lock.read_text())
    if metadata['revision'] != REVISION:
        raise ValueError('Model lock revision mismatch')
    expected = metadata['sha256']
    for name in ('onnx/model.onnx', 'tokenizer.json', 'README.md'):
        path = DEFAULT_DIR/name
        path.parent.mkdir(parents=True,exist_ok=True)
        temporary = path.with_suffix(path.suffix+'.download')
        url = f'https://huggingface.co/{MODEL_ID}/resolve/{REVISION}/{name}'
        with urllib.request.urlopen(url, timeout=120) as response, temporary.open('wb') as file:
            shutil.copyfileobj(response,file)
        digest = hashlib.sha256(temporary.read_bytes()).hexdigest()
        if expected and digest != expected[name]:
            raise ValueError(f'Checksum mismatch for {name}; model was not activated')
        temporary.replace(path)
        print(name, digest, flush=True)
    print('Model ready:',DEFAULT_DIR)

if __name__=='__main__': main()
