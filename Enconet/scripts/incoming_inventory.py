"""Inventory local incoming text without registering or approving sources."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def inventory(root):
    root = Path(root).resolve()
    records = []
    seen = {}
    for path in sorted((root / 'incoming').iterdir()):
        if not path.is_file():
            continue
        if path.is_symlink() or path.resolve().parent != root / 'incoming':
            raise ValueError('Redirected incoming file refused: ' + path.name)
        data = path.read_bytes()
        reason = None
        if path.name in {'.gitkeep', 'desktop.ini'}:
            reason = 'folder metadata, not audit evidence'
        elif path.name.startswith('+ 00 PROMPT'):
            reason = 'owner conversion instructions, not supplier evidence'
        elif path.suffix.lower() != '.md':
            reason = 'format needs explicit review'
        text = '' if reason else data.decode('utf-8-sig')
        heading = re.search(r'^#{1,6}\s+(.+)', text, re.M)
        publication = re.search(r'Datum objavljivanja[^\n]*?(\d{2})\.(\d{2})\.(\d{4})', text)
        date = None
        if publication:
            day, month, year = publication.groups()
            date = f'{year}-{month}-{day}'
        sha = hashlib.sha256(data).hexdigest()
        row = dict(filename=path.name, sha256=sha, bytes=len(data),
                   role='excluded' if reason else ('regulatory' if path.name.startswith(('10CFR', 'ASME_')) else 'vendor'),
                   exclusion=reason, title_observed=heading.group(1).strip() if heading else None,
                   publication_date_observed=date,
                   markdown_headings=len(re.findall(r'^#{1,6}\s+', text, re.M)),
                   duplicate_of=seen.get(sha), intake_status='not-registered')
        records.append(row)
        seen.setdefault(sha, path.name)
    return dict(created_utc=datetime.now(timezone.utc).isoformat(), project=str(root),
                approval_status='none-implied', files=records,
                counts={role:sum(r['role']==role for r in records) for role in ('vendor','regulatory','excluded')})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / 'out') or output.exists():
        parser.error('Use a fresh output under local out/')
    result = inventory(ROOT)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps(dict(output=str(output), counts=result['counts'])))


if __name__ == '__main__':
    main()
