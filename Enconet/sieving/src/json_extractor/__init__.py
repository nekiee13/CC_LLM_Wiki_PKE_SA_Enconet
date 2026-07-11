# ------------------------
# src/json_extractor/__init__.py
# ------------------------
"""
JSON Extractor vNext
====================

A taxonomy-driven extraction and query system for nuclear quality assurance documents.

Supports:
- Strict Appendix B (10 CFR 50) 18-criterion taxonomy
- RULE vs DOCUMENT record separation
- Deterministic join semantics via composite keys (ref_code::ref_locator)
- Schema-driven querying with DSL filter syntax
- CSV/XLSX export with stable column ordering
"""

__version__ = "0.1.0"
__author__ = "JSON Extractor Team"

from .pipeline import run_pipeline, PipelineResult
from .config import Config

__all__ = [
    "run_pipeline",
    "PipelineResult",
    "Config",
]
