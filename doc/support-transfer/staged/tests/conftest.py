import shutil
import sys
from pathlib import Path

STAGED_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_COORD = STAGED_DIR.parent / "templates" / "coordination"

# The staged modules are standalone target-local scripts (no package
# __init__), so make the directory importable the same way it will be
# importable once copied into a target's scripts/ or tools/ tree.
sys.path.insert(0, str(STAGED_DIR))

import pytest  # noqa: E402


@pytest.fixture
def coord_root(tmp_path: Path) -> Path:
    """A disposable target-shaped root with an installed coordination/ tree.

    Mirrors T4.2 installation: schemas are seeded from the Wiki's own T4
    design-candidate templates (test-time only -- the validator module never
    reads this path itself), and messages/archive/claims start empty.
    """
    root = tmp_path / "target"
    coord = root / "coordination"
    for sub in ("messages", "archive", "claims", "schemas"):
        (coord / sub).mkdir(parents=True)
    for name in ("message.schema.json", "claim.schema.json",
                 "resolution-manifest.schema.json"):
        shutil.copy(TEMPLATES_COORD / name, coord / "schemas" / name)
    return root
