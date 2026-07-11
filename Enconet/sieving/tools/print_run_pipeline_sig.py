from __future__ import annotations
import inspect
from src.json_extractor.pipeline import run_pipeline

sig = inspect.signature(run_pipeline)
print(sig)
for name, p in sig.parameters.items():
    print(name, p.kind, "default=" + (repr(p.default) if p.default is not inspect._empty else "<required>"))
