"""Resolve this audit's copied sieving library without a sibling project."""
from __future__ import annotations

import sys
from pathlib import Path


SIEVING_SRC = Path(__file__).resolve().parents[1] / "sieving" / "src"
if str(SIEVING_SRC) not in sys.path:
    sys.path.insert(0, str(SIEVING_SRC))
