"""Preview/install a copied local additive requirement-seeding tool."""
from pathlib import Path
import bootstrap_sieving as core

REQUIREMENT_SEED = core.BundleSpec(
    bundle=Path(__file__).resolve().parent / 'requirement_seed' / 'v1',
    version='1.0.0', scope='requirement-seed-only', roots=frozenset({'scripts'}),
    journal_name='requirement-seed-v1', lock_name='.requirement-seed-bootstrap.lock',
    exact_paths=frozenset({'scripts/seed_requirements.py',
                          'scripts/tests/test_seed_requirements.py'}),
)

if __name__ == '__main__':
    raise SystemExit(core.main(None, REQUIREMENT_SEED))
