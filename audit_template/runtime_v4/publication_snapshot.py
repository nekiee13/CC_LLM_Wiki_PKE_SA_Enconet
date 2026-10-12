"""Seal an existing run snapshot without rewriting any approved artifact.

Uses the same hash-pinned owner exception and G5/G6 checks as first-copy
publication. All artifact source/destination pairs must be identical. The
marker is created last with no overwrite; failures never delete artifacts.
"""
import hashlib
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime, timezone


def seal(contract_path, *, root, execute, validator, permissions):
    import publish_audit_release as publisher
    contract = json.loads(Path(contract_path).read_text(encoding='utf-8'))
    rows, result_path = publisher.checked_plan(contract, root, allow_existing_snapshot=True)
    if not all(source == destination for source, destination, digest in rows):
        raise publisher.ReleaseError('snapshot seal requires only identical source/destination paths')
    if not execute:
        return {'preview': True, 'mode': 'seal-existing-snapshot',
                'contract_sha256': publisher.fingerprint(contract), 'artifacts': contract['artifacts']}
    if validator is None:
        raise publisher.ReleaseError('execute requires a post-publication validator')
    validator()
    publisher.checked_plan(contract, root, allow_existing_snapshot=True)
    result = {'schema_version': 1, 'run_id': contract['run_id'],
              'published_at': datetime.now(timezone.utc).isoformat(),
              'review_status': 'deferred', 'owner_exception': contract['owner_exception'],
              'contract_sha256': publisher.fingerprint(contract), 'artifacts': contract['artifacts'],
              'mode': 'seal-existing-snapshot'}
    payload = (json.dumps(result, indent=2) + '\n').encode('utf-8')
    digest = hashlib.sha256(payload).hexdigest()
    installed = False
    with tempfile.TemporaryDirectory(prefix='release-seal-', dir=root) as temporary:
        marker = Path(temporary) / 'result.json'
        marker.write_bytes(payload)
        publisher.checked_plan(contract, root, allow_existing_snapshot=True)
        result_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(marker, result_path)
            installed = True
            marker.unlink()
            permissions(result_path)
        except BaseException:
            # Own marker only. Never roll back the already-existing artifacts.
            if installed and result_path.is_file() and hashlib.sha256(result_path.read_bytes()).hexdigest() == digest:
                result_path.unlink()
            raise
    return result
