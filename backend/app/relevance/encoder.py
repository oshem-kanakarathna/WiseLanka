"""Offline-only inference of the pinned Sentence Transformers MiniLM ONNX export."""
import hashlib
import json
import os
from functools import lru_cache
from pathlib import Path
from threading import Lock
from backend.app.data_loader import PROJECT_ROOT

MODEL_ID = 'sentence-transformers/all-MiniLM-L6-v2'
REVISION = '1110a243fdf4706b3f48f1d95db1a4f5529b4d41'
DEFAULT_DIR = PROJECT_ROOT / '.models' / REVISION


class LocalEncoder:
    def __init__(self, directory):
        os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
        import numpy as np
        import onnxruntime as ort
        from tokenizers import Tokenizer
        lock = json.loads(Path(__file__).with_name('model-lock.json').read_text())
        if lock['revision'] != REVISION:
            raise ValueError('Model lock revision mismatch')
        for name, digest in lock['sha256'].items():
            if hashlib.sha256((directory/name).read_bytes()).hexdigest() != digest:
                raise ValueError('Model artifact checksum mismatch')
        self.np = np
        self.tokenizer = Tokenizer.from_file(str(directory/'tokenizer.json'))
        self.tokenizer.enable_truncation(max_length=256)
        self.tokenizer.enable_padding(pad_id=0, pad_token='[PAD]')
        options = ort.SessionOptions()
        options.intra_op_num_threads = 1
        options.inter_op_num_threads = 1
        self.session = ort.InferenceSession(str(directory/'onnx/model.onnx'), options,
                                            providers=['CPUExecutionProvider'])
        self.lock = Lock()

    def encode(self, texts):
        np = self.np
        with self.lock:
            tokens = self.tokenizer.encode_batch(texts)
            inputs = {
                'input_ids': np.asarray([t.ids for t in tokens], dtype=np.int64),
                'attention_mask': np.asarray([t.attention_mask for t in tokens], dtype=np.int64),
                'token_type_ids': np.asarray([t.type_ids for t in tokens], dtype=np.int64),
            }
            names = {item.name for item in self.session.get_inputs()}
            vectors = self.session.run(None, {k:v for k,v in inputs.items() if k in names})[0]
            mask = inputs['attention_mask'][...,None]
            # Official model-card pooling: masked mean, then L2 normalisation.
            pooled = (vectors*mask).sum(axis=1)/np.maximum(mask.sum(axis=1), 1)
            normalised = pooled/np.maximum(np.linalg.norm(pooled,axis=1,keepdims=True),1e-12)
            if not np.isfinite(normalised).all():
                raise ValueError('Nonfinite embedding')
            return normalised


@lru_cache(maxsize=1)
def get_encoder():
    try:
        directory = Path(os.environ.get('WISELANKA_MODEL_DIR', str(DEFAULT_DIR)))
        return LocalEncoder(directory), None
    except (ImportError, OSError, ValueError, RuntimeError, KeyError) as error:
        return None, type(error).__name__
