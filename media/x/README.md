# X-ready proof animations

These looping GIFs are exported from the interactive proof app and encoded for
upload through `x.com`. They are explanatory visualizations; the Lean proof and
its checked certificates remain authoritative.

| Animation | Case | Duration | Dimensions |
|---|---|---:|---:|
| [`one-black-q-7-7.gif`](./one-black-q-7-7.gif) | The 106,258-step certified prefix transient for `q = (7, 7)` | 17.6 s | 720 × 564 |
| [`scattering-all-22.gif`](./scattering-all-22.gif) | All 22 pristine scattering phases in a 2 × 2 grid: straight, right, reverse, and left outcomes; phases ascend within each panel | 7.2 s | 720 × 562 |
| [`reverse-highway-phase-72.gif`](./reverse-highway-phase-72.gif) | The phase-72 reverse-highway mechanism at physical depth 15 | 22.0 s | 720 × 562 |
| [`blank-plane-to-p104.gif`](./blank-plane-to-p104.gif) | The unperturbed blank-plane orbit entering its period-104 highway at `t = 9,977` | 14.0 s | 720 × 562 |
| [`first-contact-coupling.gif`](./first-contact-coupling.gif) | Side-by-side blank and `q = (-16, 9)` runs: the ant paths agree until the first read at `t = 9,971` | 15.0 s | 720 × 314 |
| [`ordinary-p61-depth-induction.gif`](./ordinary-p61-depth-induction.gif) | Representative P61 depths crossing from direct finite replay to stable induction | 6.0 s | 720 × 562 |
| [`stage-03-04-boundary-p61.gif`](./stage-03-04-boundary-p61.gif) | The P61 classification boundary: depth 14 intersects history; depth 15 is the separated stable entry | 11.2 s | 720 × 562 |
| [`affine-hit-law-depth-15-16-20-30.gif`](./affine-hit-law-depth-15-16-20-30.gif) | Reverse-channel depths 15, 16, 20, and 30 in one P104-entry coordinate frame and a common 800-step/s clock from `t = 50,000`; their hit times are 54,223, 54,431, 55,263, and 57,343 | 22.0 s | 720 × 562 |
| [`global-map-to-22-rays.gif`](./global-map-to-22-rays.gif) | A conceptual fade from the exhaustive global partition to the 21 ordinary rays plus one exceptional ray | 4.8 s | 720 × 562 |

Each file loops indefinitely and is below X's 5 MB mobile and 15 MB web-upload
limits. The scattering spectrum groups the four outgoing classes into a 2 × 2
grid; each panel cycles through its phases in ascending order, including the
exceptional reverse phase 72. Evolution GIFs use the app's exact replay and certified boundary
data; beige is the realized footprint and green is the terminal P104 tail. The
global contraction is intentionally a set-visibility animation, not a simulated
ant trajectory.

For a short introductory post, start with the blank-plane baseline and the
`q = (7, 7)` transient. For a proof-focused thread, the first-contact coupling,
P61 boundary, affine hit law, and 22-phase scattering grid expose the main
mechanisms most directly.

## Regeneration

Serve the app from the repository root:

```console
python3 -m http.server 4173 --bind 127.0.0.1 --directory docs
```

In a second shell, run:

```console
node scripts/export_x_gifs.mjs
```

The exporter requires Playwright with Chromium and `ffmpeg`. Set
`PLAYWRIGHT_MODULE` when Playwright is installed outside the default Node
module search path.

On an unsupported newer Ubuntu release, Playwright can use its Ubuntu 24.04
fallback browser by adding `PLAYWRIGHT_HOST_PLATFORM_OVERRIDE=ubuntu24.04-x64`
to both the browser-install and exporter commands.
