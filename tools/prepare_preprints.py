#!/usr/bin/env python3
"""Prepare local PDF/source/manifest packages. No network or submission actions.

Includes working-tree changes explicitly: base_commit identifies ancestry,
while snapshot_sha256 and per-file hashes identify the actual review content.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = {
    'one_black': ('0.2.0', 'paper.pdf', 'One-Black-Standard-Trace.pdf', 'retain-published'),
    'clock_escape': ('0.4.0', 'review.pdf', 'An-Ant-on-the-Clock.pdf', 'new-version'),
    'four_cell_port': ('0.1.0', 'review.pdf', 'Four-Black-Cells.pdf', 'first-release'),
    'wake_synthesis': ('0.2.0', 'build/paper.pdf', 'Standard-Wake-Uniqueness.pdf', 'new-version'),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(data):
    return (json.dumps(data, indent=2, sort_keys=True) + '\n').encode()


def check_one_black():
    project = ROOT / 'one_black'
    report = json.loads((project / 'evidence/report.json').read_text())
    for name, sha in report['sha256'].items():
        assert digest((project / 'lean' / name).read_bytes()) == sha, name
    receipt = json.loads((project / 'release/publication-receipt.json').read_text())
    pdf = next(item for item in receipt['files'] if item['filename'].endswith('.pdf'))
    assert digest((project / 'paper/paper.pdf').read_bytes()) == pdf['sha256']
    return {'lean_sources_match_retained_clean_build': len(report['sha256']),
            'published_pdf_matches_receipt': True, 'new_lean_build_this_batch': False}


def prepare(project):
    version, pdf_name, delivery_name, action = PROJECTS[project]
    home = ROOT / project
    metadata_bytes = (home / 'release/metadata.json').read_bytes()
    metadata = json.loads(metadata_bytes)
    paths = subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', project],
        cwd=ROOT).decode().split('\0')
    sources = {}
    for name in sorted(set(paths)):
        p = ROOT / name
        if (not name or not p.is_file() or p.suffix == '.pdf' or
                any(part in {'release', 'media', 'build', '.lake', '__pycache__'}
                    for part in Path(name).parts)):
            continue
        sources[name] = p.read_bytes()
    assert sources and any(name.endswith('reproduce.py') for name in sources)
    pdf_data = (home / 'paper' / pdf_name).read_bytes()
    base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    hashes = {name: digest(data) for name, data in sources.items()}
    manifest = {'schema': 'local-preprint-candidate-v1', 'project': project,
                'version': version, 'intended_action': action,
                'owner_approval_required': True, 'submitted': False,
                'base_commit': base, 'working_tree_sources_included': True,
                'snapshot_sha256': digest(encoded(hashes)), 'source_sha256': hashes,
                'pdf': {'path': f'{project}/paper/{pdf_name}', 'sha256': digest(pdf_data)},
                'metadata_sha256': digest(metadata_bytes)}
    if project == 'one_black':
        manifest['verification'] = check_one_black()
    (home / 'release/candidate-manifest.json').write_bytes(encoded(manifest))
    out = home / 'release/candidate'
    out.mkdir(exist_ok=True)
    (out / delivery_name).write_bytes(pdf_data)
    archive = out / f'{project}-{version}-source.zip'
    readme = (f'# {metadata["title"]}\n\n'
              f'Local review source snapshot, version {version}.\n'
              f'Run `python3 {project}/reproduce.py` from this directory.\n'
              f'Build: `make -C {project}/paper`.\n'
              'The PDF is delivered separately. Historical release records and media exports\n'
              'are omitted; proof sources, manuscript figures and verification evidence are included.\n'
              'See the project README for exact dependencies and verification scope.\n')
    entries = {**sources, 'README.md': readme.encode(),
               'artifact-manifest.json': encoded(manifest), 'metadata.json': metadata_bytes}
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name, sha in hashes.items():
            assert digest(z.read(name)) == sha
    files = {p.name: {'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}
             for p in (out / delivery_name, archive)}
    (out / 'files.json').write_bytes(encoded({'project': project, 'version': version,
                                            'submitted': False, 'files': files}))
    print(f'{project}: {len(hashes)} source files; PDF and ZIP hashes verified; {out.relative_to(ROOT)}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', choices=[*PROJECTS, 'all'], default='all')
    args = parser.parse_args()
    for project in PROJECTS if args.project == 'all' else [args.project]:
        prepare(project)


if __name__ == '__main__':
    main()
