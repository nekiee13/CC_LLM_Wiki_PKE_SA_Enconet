"""Run the installed indexers against CU-4.2's pinned explicit corpora.

Use under one INDEX-REFRESH claim. Documentation byte sources are retained;
live code must match the pinned commit and keep its existing neutral identity.
"""
import argparse
import json
from pathlib import Path
import subprocess


def validate_contract(manifest, tracked):
    import prepare_shared_index_snapshot as contract
    expected = dict(profiles=contract.profiles(tracked), excludes=contract.EXCLUDED,
                    code_excludes=contract.CODE_EXCLUDED,
                    controlled_excludes=contract.CONTROLLED_EXCLUDED,
                    global_excludes=contract.GLOBAL_EXCLUDED)
    if any(manifest.get(key) != value for key, value in expected.items()):
        raise ValueError('Explicit corpus or exclusions differ from neutral committed contract')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads(args.snapshot.read_text(encoding='utf-8'))
    tracked = subprocess.check_output(['git', '-C', str(root), 'ls-tree', '-rz', '--name-only',
                                       manifest['head']]).decode('utf-8').split('\0')
    validate_contract(manifest, (p for p in tracked if p))
    snapshot = Path(manifest['snapshot'])
    expected = root / '.tmp' / ('index-source-' + manifest['head'][:12])
    if snapshot != expected or snapshot.resolve() != expected:
        raise ValueError('Foreign or redirected snapshot refused')
    if args.output.exists() or not args.output.absolute().is_relative_to(root / 'PKE_SA_NQA1_doc/plans/cleanup-cu4'):
        raise ValueError('Fresh CU-4 receipt required')
    for folder in (root, snapshot):
        head = subprocess.check_output(['git', '-C', str(folder), 'rev-parse', 'HEAD'], text=True).strip()
        if head != manifest['head']:
            raise ValueError('HEAD changed since preparation')
    if subprocess.check_output(['git', '-C', str(snapshot), 'status', '--porcelain', '--untracked-files=no']).strip():
        raise ValueError('Snapshot is dirty')
    code_paths = ['Enconet/' + p for p in manifest['profiles']['Enconet-0a063bd7']]
    for offset in range(0, len(code_paths), 100):
        subprocess.run(['git', '-C', str(root), 'diff', '--quiet', manifest['head'], '--',
                        *code_paths[offset:offset + 100]], check=True)
    from jdocmunch_mcp.tools.index_local import index_local
    from jdocmunch_mcp.tools.verify_index import verify_index
    from jcodemunch_mcp.tools.index_folder import index_folder, _resolve_repo_identity
    from jcodemunch_mcp.storage.index_store import IndexStore
    owner, name, _ = _resolve_repo_identity(root / 'Enconet', mode='config', store=IndexStore())
    if (owner, name) != ('local', 'Enconet-0a063bd7'):
        raise ValueError('Existing code identity would change')
    ownership = ['AGENTS.md', 'CLAUDE.md', '**/AGENTS.md', '**/CLAUDE.md', '**/CC_*',
                 '.agents/**', '.claude/**', '**/.agents/**', '**/.claude/**', '**/settings.local.json']
    results = dict(head=manifest['head'], docs={}, code=None)
    for profile in ('PKE_SA_NQA1_Enconet_docs', 'PKE_SA_NQA1_Enconet_controlled', 'PKE_SA_NQA1_global_docs'):
        global_docs = profile.endswith('global_docs')
        folder = snapshot / ('PKE_SA_NQA1_doc' if global_docs else 'Enconet')
        ignores = manifest['global_excludes'] if global_docs else manifest['excludes']
        if profile.endswith('controlled'):
            ignores = ignores + manifest['controlled_excludes']
        result = index_local(str(folder), name=profile, paths=manifest['profiles'][profile],
                             extra_ignore_patterns=ignores + ownership, incremental=False,
                             follow_symlinks=False, use_ai_summaries=False, use_embeddings=False)
        verification = verify_index('local/' + profile)
        results['docs'][profile] = dict(index=result, verification=verification)
        if (not result.get('success') or not result.get('sha_certified')
                or result.get('head_sha') != manifest['head']
                or any(verification.get(k, 1) != 0 for k in ('drift_count', 'missing_count', 'error_count'))):
            raise ValueError('Document refresh/verification failed: ' + profile)
        print(json.dumps(dict(profile=profile, docs=result.get('file_count'),
                              verified=verification['clean_count'], skipped=verification['skipped_count'])), flush=True)
    result = index_folder(str(root / 'Enconet'), paths=manifest['profiles']['Enconet-0a063bd7'],
                          extra_ignore_patterns=manifest['code_excludes'] + ownership,
                          incremental=False, follow_symlinks=False, use_ai_summaries=False,
                          context_providers=False, identity_mode='config')
    results['code'] = result
    if not result.get('success') or result.get('repo') != 'local/Enconet-0a063bd7':
        raise ValueError('Code rebuild failed or identity changed')
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(results, stream, indent=2, ensure_ascii=False)
    print(json.dumps(dict(code=result.get('repo'), files=result.get('file_count'), symbols=result.get('symbol_count'))))


if __name__ == '__main__':
    main()
