"""Create a separate, standalone dark presentation of a verified light snapshot.

Only a screen stylesheet is added. Body, JavaScript, audit data and print styles
are preserved verbatim; the source is never written. UMBRA-inspired, not a claim
of strict draft-system conformance (offline fonts and audit-specific components).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

STYLE = Path(__file__).with_name('dashboard_dark.css')


def dark_copy(source: str) -> str:
    if 'id="ekonerg-dark-skin"' in source:
        raise ValueError('Dark skin is already present')
    if source.count('</head>') != 1:
        raise ValueError('Expected one head in the source dashboard')
    css = STYLE.read_text(encoding='utf-8')
    return source.replace('</head>', '<style id="ekonerg-dark-skin" media="screen">\n'
                          + css + '\n</style>\n</head>', 1)


def build(source: Path, output: Path) -> dict:
    source = source.resolve(strict=True)
    output = output.resolve()
    if source == output:
        raise ValueError('Output must not overwrite the source')
    before = source.read_bytes()
    result = dark_copy(before.decode('utf-8')).encode('utf-8')
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError('Choose a fresh output; published snapshots are not overwritten')
    output.write_bytes(result)
    assert source.read_bytes() == before
    return {'source': str(source), 'source_sha256': hashlib.sha256(before).hexdigest(),
            'output': str(output), 'dark_sha256': hashlib.sha256(result).hexdigest(),
            'stylesheet_sha256': hashlib.sha256(STYLE.read_bytes()).hexdigest(),
            'scope': 'Screen-only CSS overlay; original body, script and print CSS unchanged.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    receipt = build(args.source, args.output)
    args.output.with_suffix('.provenance.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
