# Interactive one-black proof guide

Serve the existing site with:

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory docs
```

The explanatory guide is published at
[kehao95.github.io/langtons-ant-core](https://kehao95.github.io/langtons-ant-core/).
The [one-black project](../one_black/README.md) owns the theorem and proof.

## Export figures and animations

With Playwright/Chromium installed, while the local server is running:

```sh
node docs/scripts/export_scattering_panels.mjs
node docs/scripts/export_x_gifs.mjs
```

The first writes the manuscript figures to `one_black/paper/figures/`.
The second also requires ffmpeg and writes animations to `one_black/media/`.
Set `PLAYWRIGHT_MODULE` for a nonstandard Playwright installation.
