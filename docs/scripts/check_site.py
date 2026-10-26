#!/usr/bin/env python3
"""Check the assembled Pages artifact, local links and exact PDF snapshots."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[2]
SITE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / '_site'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.headings = set(), [], 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs['id'])
        for key in ('src', 'href'):
            if key in attrs:
                self.links.append(attrs[key])
        if tag == 'h1':
            self.headings += 1
        if tag == 'canvas':
            assert attrs.get('aria-label'), 'Canvas needs a descriptive label'

pages = {}
for path in SITE.glob('*.html'):
    page = Page()
    page.feed(path.read_text())
    assert page.headings == 1, f'{path.name}: expected one h1'
    pages[path.name] = page
assert set(pages) == {'index.html', 'one-black.html', 'clock.html', 'wake.html',
                      'factors.html', 'memory.html', 'ports.html'}
for name, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (SITE / unquote(url.path or name)).resolve()
        assert target.is_relative_to(SITE), f'{name}: link escapes site: {link}'
        assert target.is_file(), f'{name}: missing {link}'
        if url.fragment and target.name in pages:
            assert unquote(url.fragment) in pages[target.name].ids, f'{name}: missing anchor {link}'
manifest = json.loads((SITE / 'site-manifest.json').read_text())
assert len(manifest['papers']) == 6
for paper in manifest['papers'].values():
    source, deployed = ROOT / paper['source'], SITE / paper['path']
    assert deployed.read_bytes().startswith(b'%PDF-')
    assert hashlib.sha256(deployed.read_bytes()).hexdigest() == paper['sha256']
    assert source.read_bytes() == deployed.read_bytes()
for unwanted in ('node_modules', 'scripts', 'tests', 'package-lock.json', 'sources.json'):
    assert not (SITE / unwanted).exists(), f'Development file deployed: {unwanted}'
print('Site checks passed: seven pages, local links, canvas labels, six exact PDFs.')
