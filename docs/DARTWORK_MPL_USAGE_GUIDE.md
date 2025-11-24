# Usage Guide

dartwork-mpl bundles stylistic presets, curated colors/colormaps, and layout/font helpers so you get **predictable results** fast. The snippets below keep only the core code—check the Examples Gallery if you need to see the rendered figures.

## Quick start

```python
import matplotlib.pyplot as plt
import dartwork_mpl as dm
import numpy as np

dm.style.use_preset("scientific")  # presentation, investment, scientific-kr, ...
fig, ax = plt.subplots(figsize=(dm.cm2in(9), dm.cm2in(6)), dpi=300)
x = np.linspace(0, 10, 200)
ax.plot(x, np.sin(x), color="dm.blue5", label="signal")
ax.set_xlabel("Time [s]", fontsize=dm.fs(0))
ax.set_ylabel("Amplitude", fontsize=dm.fs(0))
dm.simple_layout(fig)
dm.save_and_show(fig, size=720)  # quick preview for notebooks/slides
```

- `style.use_preset` sets palette, fonts, and line weights in one call
- `cm2in` for real-world sizing, `fs` for relative font scaling
- `simple_layout` cleans up margins and overlaps

## Styles and presets

```python
import dartwork_mpl as dm
dm.style.use_preset("presentation")   # slides/reports
dm.style.use_preset("scientific")     # papers/technical
dm.style.use_preset("investment")     # finance decks
dm.style.use_preset("scientific-kr")  # includes KR fonts
```

- Style files: `asset/mplstyle/*.mplstyle`
- Preset definitions: `asset/mplstyle/presets.json`
- Default applied on import: `dmpl_light`

## Colors and colormaps

```python
import matplotlib.pyplot as plt
import dartwork_mpl as dm
dm.style.use_preset("presentation")

fig, ax = plt.subplots(figsize=(dm.cm2in(8), dm.cm2in(5)), dpi=300)
ax.plot([0, 1, 2], [1, 2, 1.5], marker="o", color="dm.green5", label="dm.*")
ax.plot([0, 1, 2], [1.2, 1.6, 2.1], marker="s", color="tw.blue:500", label="Tailwind")
ax.fill_between([0, 1, 2], 0.9, 1.3, color="md.orange:200", alpha=0.6, label="Material")
ax.legend(fontsize=dm.fs(-1))
dm.simple_layout(fig)
```

```python
# Check colormap name/category
import matplotlib.pyplot as plt
import dartwork_mpl as dm
cmap = plt.colormaps["dm.mint"]
print(cmap.name, dm.classify_colormap(cmap))
```

- Color sources: `asset/color/*.txt` + Tailwind/Material/Ant/Chakra/Primer/opencolor JSON
- Palette/colormap previews: `images/colors_*.png`, `images/colormaps_*.png`

## Layout and annotations

```python
import matplotlib.pyplot as plt
import dartwork_mpl as dm
import numpy as np
dm.style.use_preset("scientific")

fig = plt.figure(figsize=(dm.cm2in(15), dm.cm2in(10)), dpi=300)
gs = fig.add_gridspec(2, 2, left=0.08, right=0.98, top=0.9, bottom=0.12, hspace=0.35, wspace=0.25)
axes = [fig.add_subplot(gs[i, j]) for i in range(2) for j in range(2)]
for ax, label in zip(axes, "ABCD"):
    ax.plot(np.linspace(0, 1, 40), np.random.rand(40), color="dm.blue6", lw=0.8)
    ax.text(0, 1, label, transform=ax.transAxes + dm.make_offset(4, -4, fig),
            weight="bold", va="top", fontsize=dm.fs(0))
    dm.set_decimal(ax, xn=2, yn=1)
dm.simple_layout(fig, gs=gs)
```

- `simple_layout(fig, gs=gs)` respects your GridSpec margins
- `make_offset` gives consistent point-based text offsets
- `set_decimal(ax, xn, yn)` formats tick labels neatly

## Typography

```python
import matplotlib.pyplot as plt
import dartwork_mpl as dm
dm.style.use_preset("scientific-kr")  # English/Korean fonts set together

fig, ax = plt.subplots(figsize=(dm.cm2in(10), dm.cm2in(6)), dpi=300)
ax.plot([0, 1, 2], [0, 1, 0.4], color="dm.green6", lw=1.0)
ax.set_title("Experiment result", fontsize=dm.fs(2), fontweight=dm.fw(1))
ax.set_xlabel("Time", fontsize=dm.fs(0))
ax.set_ylabel("Response", fontsize=dm.fs(0))
dm.simple_layout(fig)
```

- `fs(delta)`: font size relative to the active preset
- `fw(delta)`: weight relative to the preset default
- Fonts: `asset/font/*` (auto-registered on import)

## Save and preview

```python
import matplotlib.pyplot as plt
import dartwork_mpl as dm
import numpy as np
dm.style.use_preset("investment")

fig, ax = plt.subplots(figsize=(dm.cm2in(11), dm.cm2in(7)), dpi=300)
ax.plot(np.arange(50), np.cumsum(np.random.randn(50)) + 20, color="dm.blue6")
dm.simple_layout(fig)

dm.save_formats(fig, "output/forecast", formats=("png", "svg"), dpi=300, bbox_inches="tight")
dm.save_and_show(fig, size=720)  # preview + plt.show()
```

- `save_formats` writes multiple formats in one call
- `save_and_show` emits a small preview (PNG) and shows the figure

## Where things live

- Styles: `asset/mplstyle/*.mplstyle`, presets: `asset/mplstyle/presets.json`
- Colors/colormaps: `asset/color/*.txt`, palette sheets: `images/colors_*.png`, colormap panels: `images/colormaps_*.png`
- Fonts: `asset/font/*` (loaded by `dartwork_mpl.font`)
- Utilities: `simple_layout`, `cm2in`, `make_offset`, `set_decimal`, `save_formats`, `save_and_show` (all in `dartwork_mpl`)

## See more

- Examples Gallery (`docs/examples_gallery.md`) for finished plots by category
- Color System (`docs/COLOR_SYSTEM.md`) for naming rules and weight choices
