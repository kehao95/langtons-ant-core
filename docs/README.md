# Interactive proof labs

[Live site](https://www.kehao.me/langtons-ant-core/) · [Interaction design](DESIGN.md)

The overview routes readers into six mathematical questions:

| Page | Reader's action | Proof owner |
|---|---|---|
| `one-black.html` | Inspect exhaustive placement classes and certified evolution | [One-black](../one_black/) |
| `clock.html` | Edit the complete field and watch an exact clock spend its finite range | [Clock and escape](../clock_escape/) |
| `wake.html` | Shift highway phase, edit odd classes, test mixed-wake parity | [Wake rigidity](../wake_synthesis/) |
| `factors.html` | Move interval boundaries, inspect bad ten-windows and realize the sharp mass constant | [Factor language](../factor_language/) |
| `memory.html` | Follow births and readbacks, change memory and spatial cutoffs, inspect exact long lifetimes | [Memory and feedback](../memory_feedback/) |
| `ports.html` | Replay a port, compose compatible collisions and inspect return to an old wake | [Ports and scattering](../four_cell_port/) |

`labs/common.mjs` owns literal reversible ant dynamics and drawing helpers.
Proof-specific algorithms live beside each page in `labs/`; data in `data/`
is deterministically exported from publication-owned checkers. The original
one-black `app.js`, `proof-map.json` and styling retain their existing behavior.
The browser's finite demonstrations accompany the proofs in the six owners.
Formalization scope and all-parameter arguments stay explicit in those sources.

## Build and verify

From the repository root, with Python 3.10+ and Node 22:

```sh
npm ci --prefix docs
docs/node_modules/.bin/playwright install chromium
python3 docs/scripts/export_wake_factors.py --check
python3 docs/scripts/export_memory.py --check
python3 docs/scripts/export_ports.py --check
npm test --prefix docs
python3 docs/scripts/build_site.py
python3 docs/scripts/check_site.py
npm run test:browser --prefix docs
python3 -m http.server 4173 --bind 127.0.0.1 --directory _site
```

Open `http://127.0.0.1:4173/`. The browser test starts its own server beneath
`/langtons-ant-core/`, exercises all seven pages at desktop and mobile widths,
checks visible formulas and actual control effects, and downloads all six PDFs.
It needs a working system font configuration; `FONTCONFIG_FILE` can select a
local configuration on hosts with broken font aliases. CI installs browser
libraries with Playwright's `--with-deps` option.

Run an exporter without `--check` only when deliberately refreshing its data
from the canonical sources, then inspect the diff and run the tests. These
scoped export and browser checks do not rerun the full Lean proof or the wake
enumeration. Each owner's `reproduce.py` remains the full proof entrypoint.

`build_site.py` copies static assets into ignored `_site/`, excludes development
tools, and adds exact manuscript PDFs under `papers/`. It records source paths,
SHA-256 hashes, the source commit and publication status in `site-manifest.json`.
One-black and clock use published snapshots; the other four use current
review candidates. Rebuilding the site never rebuilds or alters those PDFs.
The Pages workflow runs the same checks before uploading `_site/`.

## Export one-black figures and animations

With the local server above running:

```sh
node docs/scripts/export_scattering_panels.mjs
node docs/scripts/export_x_gifs.mjs
```

Both tools now open `one-black.html`. The first writes manuscript figures to
`one_black/paper/figures/`. The second requires ffmpeg and writes animations
to `one_black/media/`. Set `PLAYWRIGHT_MODULE` for a nonstandard installation.
