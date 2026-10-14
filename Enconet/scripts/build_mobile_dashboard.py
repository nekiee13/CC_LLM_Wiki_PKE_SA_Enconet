"""Create a separate standalone mobile correction; never overwrite a release.

The only change is a screen-only wrapping rule for long metadata hashes.
Original bytes, including every script, data object and print rule, stay intact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

STYLE = (b'<style id="audit-mobile-wrap" media="screen">'
         b'@media(max-width:700px){#artifact-metadata{overflow-wrap:anywhere}}'
         b'</style>\n')


def mobile_copy(source: bytes) -> bytes:
    if (source.count(b'</head>') != 1 or b'id="artifact-metadata"' not in source
            or b'id="audit-mobile-wrap"' in source):
        raise ValueError('Expected an uncorrected dashboard with one head and metadata panel')
    return source.replace(b'</head>', STYLE + b'</head>', 1)


def build(source: Path, output: Path) -> dict:
    output = output.absolute()
    # Check before resolve so junction/symlink parents cannot hide a redirect.
    for item in (output, *output.parents):
        if item.is_symlink() or (item.exists() and getattr(item.stat(), 'st_file_attributes', 0) & 0x400):
            raise ValueError('Redirected destination refused')
    source = source.resolve(strict=True)
    if output.resolve() == source:
        raise ValueError('Output must not overwrite the source')
    if output.exists():
        raise FileExistsError('Choose a fresh revision; existing files are never overwritten')
    before = source.read_bytes()
    result = mobile_copy(before)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('xb') as stream:
        stream.write(result)
    assert source.read_bytes() == before
    assert result.replace(STYLE, b'', 1) == before
    return dict(source=str(source), output=str(output),
                source_sha256=hashlib.sha256(before).hexdigest(),
                output_sha256=hashlib.sha256(result).hexdigest(),
                original_bytes_preserved=True,
                scope='Screen-only metadata hash wrapping; no data, scripts, print or publication changes.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    receipt = args.output.with_suffix('.provenance.json')
    if receipt.exists():
        raise FileExistsError('Revision provenance already exists')
    result = build(args.source, args.output)
    with receipt.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
