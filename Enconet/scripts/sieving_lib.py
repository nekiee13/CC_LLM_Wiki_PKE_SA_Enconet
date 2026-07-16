"""Resolve the integral vendored sieving library for project scripts.

The project does not require an editable site-package install: scripts add the
single documented ``sieving/src`` source root and then import ``json_extractor``.
No crumb-processing implementation belongs in this adapter.
"""
from __future__ import annotations

import sys
from pathlib import Path

SIEVING_SRC = Path(__file__).resolve().parents[1] / "sieving" / "src"
if str(SIEVING_SRC) not in sys.path:
    sys.path.insert(0, str(SIEVING_SRC))
