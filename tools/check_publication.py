#!/usr/bin/env python3
"""Check article identities, explicit source lists and local documentation links."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = re.compile(
    r'(^|/)(?:PREPRINT_REVIEW\.md|LITERATURE_REVIEW\.md|LITERATURE\.md|'
    r'INTEGRATION\.(?:md|json)|PROVENANCE\.json|review-[^/]*|import-[^/]*|'
    r'publication-receipt\.json|standalone-check\.json|review-checks\.[^/]+|'
    r'prepared-source-manifest\.json|delivery-manifest\.json|'
    r'latest-version-check\.json|previous-version-check\.json|'
    r'candidate|reviews?|revisions)(/|$)')


def safe_file(base, name):
    path = (base / name).resolve()
    if not path.is_relative_to(base.resolve()) or not path.is_file():
        raise ValueError('Missing or unsafe file: ' + name)
    return path


def check(root=ROOT):
    articles = json.loads((root / 'publications.json').read_text())
    listed = set()
    for project, article in articles.items():
        home = root / project
        manifest = safe_file(root, article['sources'])
        sources = json.loads(manifest.read_text())['sha256']
        assert sources and 'reproduce.py' in sources
        for name, expected in sources.items():
            full = project + '/' + name
            assert not FORBIDDEN.search(full), 'Operational file in source list: ' + full
            actual = safe_file(home, name)
            assert hashlib.sha256(actual.read_bytes()).hexdigest() == expected, full
            listed.add(full)
        pdf = safe_file(root, article['pdf'])
        assert pdf.read_bytes().startswith(b'%PDF-'), project
        assert hashlib.sha256(pdf.read_bytes()).hexdigest() == article['pdf_sha256'], project
        listed.update((article['pdf'], article['sources']))
    # Site sources and root entrypoints also have explicit ownership.
    site_files = json.loads((root / 'docs/sources.json').read_text())['files']
    for name in site_files:
        safe_file(root / 'docs', name)
        listed.add('docs/' + name)
    listed.update({'AGENTS.md', 'README.md', 'PREPRINTS.md', 'publications.json',
                   '.gitignore', 'docs/sources.json', 'tools/check_publication.py',
                   '.github/workflows/deploy-pages.yml', 'research/README.md',
                   'research/NEXT_QUESTIONS.md', 'research/SELF_WRITING_MEDIA.md'})
    tracked = subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=root
    ).decode().split('\0')
    for name in sorted(set(tracked)):
        path = root / name
        if not name or not path.is_file():
            continue
        assert not FORBIDDEN.search(name), 'Operational file in publication tree: ' + name
        assert name in listed, 'File absent from explicit source list: ' + name
        if path.suffix == '.md':
            # Check navigational links, allowing scholarly external URLs and anchors.
            text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
            for target in re.findall(r'\]\(([^\s)]+)\)', text):
                url = urlsplit(target)
                if url.scheme or url.netloc or not url.path:
                    continue
                linked = (path.parent / unquote(url.path)).resolve()
                assert linked.is_relative_to(root.resolve()) and linked.exists(), (name, target)
    print(f'Publication checks passed: {len(articles)} articles; {len(listed)} listed files.')


if __name__ == '__main__':
    check()
