# Usage Guide

dartwork-mpl bundles stylistic presets, curated colors/colormaps, and layout/font helpers so you get **predictable results** fast. The snippets below keep only the core code—check the Examples Gallery if you need to see the rendered figures.

## Quick start

```python
import matplotlib.pyplot as plt
import dartwork_mpl as dm
import numpy as np

dm.style.use_preset("scientific")  # preset keys: see API › Style Management
fig, ax = plt.subplots(figsize=(dm.cm2in(9), dm.cm2in(6)), dpi=300)
x = np.linspace(0, 10, 200)
ax.plot(x, np.sin(x), color="dm.blue5", label="signal")
ax.set_xlabel("Time [s]", fontsize=dm.fs(0))
ax.set_ylabel("Amplitude", fontsize=dm.fs(0))
dm.simple_layout(fig)           # API › Layout Utilities
dm.save_and_show(fig, size=720) # API › File I/O
```

- `style.use_preset` configures palette, fonts, and line weights in one shot (API › Style Management)
- `cm2in` and `fs` keep figures to scale and fonts relative to the active preset (API › Font Utilities)
- `simple_layout` and `save_and_show` handle margin cleanup plus preview/export (API › Layout Utilities, File I/O)

## Styles and presets

```python
import dartwork_mpl as dm

dm.use_style("dmpl_light")                    # load one .mplstyle file
dm.Style.use(["grid.clean", "font-modern"])   # stack multiple styles
dm.style.use_preset("presentation")           # slides/reports
dm.style.use_preset("scientific")             # papers/technical
dm.style.use_preset("investment")             # finance decks
dm.style.use_preset("scientific-kr")          # includes KR fonts

available_styles = dm.list_styles()
style_dict = dm.load_style_dict("font-presentation")
```

- Style files: `asset/mplstyle/*.mplstyle`
- Preset definitions: `asset/mplstyle/presets.json`
- Default applied on import: `dmpl_light`
- See **API › Style Management** for every helper and argument

## Colors and colormaps

```python
import matplotlib.pyplot as plt
import dartwork_mpl as dm
dm.style.use_preset("presentation")

fig, ax = plt.subplots(figsize=(dm.cm2in(8), dm.cm2in(5)), dpi=300)
ax.plot([0, 1, 2], [1, 2, 1.5], marker="o", color="dm.green5", label="dm.*")
ax.plot([0, 1, 2], [1.2, 1.6, 2.1], marker="s", color="tw.blue:500", label="Tailwind")
highlight = dm.mix_colors("md.orange:600", "white", alpha=0.45)  # API › Color Utilities
ax.fill_between([0, 1, 2], 0.9, 1.3, color=highlight, label="Mixed shade")
muted_line = dm.pseudo_alpha("primer.blue5", alpha=0.65, background="white")
ax.plot([0, 1, 2], [0.8, 1.1, 1.4], color=muted_line, label="Pseudo alpha")
ax.legend(fontsize=dm.fs(-1))
dm.simple_layout(fig)
```

```python
# Check colormap name/category (API › Color Utilities)
import matplotlib.pyplot as plt
import dartwork_mpl as dm
cmap = plt.colormaps["dm.mint"]
print(cmap.name, dm.classify_colormap(cmap))
```

- Color sources: `asset/color/*.txt` + Tailwind/Material/Ant/Chakra/Primer/opencolor JSON
- Palette/colormap previews: `images/colors_*.png`, `images/colormaps_*.png`
- Diagnostic helpers live in **API › Color Utilities** and **Visualization Tools**

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

dm.simple_layout(
    fig,
    gs=gs,
    margins=(0.05, 0.08, 0.06, 0.08),
    importance_weights=(1, 1, 2, 1),
    verbose=False
)
bbox = dm.get_bounding_box(
    ax.get_tightbbox(fig.canvas.get_renderer()) for ax in axes
)
```

- `simple_layout(fig, gs=gs)` respects your GridSpec margins (API › Layout Utilities)
- `make_offset` gives consistent point-based text offsets
- `set_decimal(ax, xn, yn)` formats tick labels neatly
- `get_bounding_box` merges multiple axes bounds so you can gauge remaining space quickly

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

# Preview bundled fonts before exporting (API › Visualization Tools / Font Utilities)
dm.plot_fonts(ncols=4, font_size=12)
```

- `fs(delta)`: font size relative to the active preset
- `fw(delta)`: weight relative to the preset default
- Fonts: `asset/font/*` (auto-registered on import)
- API details: **Font Utilities** and **Visualization Tools**

## Save and preview

```python
import matplotlib.pyplot as plt
import dartwork_mpl as dm
import numpy as np
dm.style.use_preset("investment")

fig, ax = plt.subplots(figsize=(dm.cm2in(11), dm.cm2in(7)), dpi=300)
ax.plot(np.arange(50), np.cumsum(np.random.randn(50)) + 20, color="dm.blue6")
dm.simple_layout(fig)

dm.save_formats(
    fig,
    "output/forecast",
    formats=("png", "svg", "pdf"),
    dpi=300,
    bbox_inches="tight"
)
dm.save_and_show(fig, size=720)  # preview + plt.show()
dm.show("output/forecast.svg", size=540)
```

- `save_formats` writes multiple formats in one call
- `save_and_show` emits a small preview (PNG/SVG) and shows the figure
- `show` reuses an existing SVG for notebooks or reports
- Argument details live in **API › File I/O**

## Where things live

- Styles: `asset/mplstyle/*.mplstyle`, presets: `asset/mplstyle/presets.json`
- Colors/colormaps: `asset/color/*.txt`, palette sheets: `images/colors_*.png`, colormap panels: `images/colormaps_*.png`
- Fonts: `asset/font/*` (loaded by `dartwork_mpl.font`)
- Utilities: `simple_layout`, `cm2in`, `make_offset`, `set_decimal`, `save_formats`, `save_and_show` (all in `dartwork_mpl`)
- Every function/argument is cataloged in `docs/api/index.rst`

## See more

- Examples Gallery for finished plots by category
- [Color System](../color_system/index.md) for naming rules and weight choices
- [API Reference](../api/index.rst) for detailed call signatures across styles, layout, colors, fonts, I/O, and visualization tools

## Diagnostics & previews

```python
import dartwork_mpl as dm

dm.plot_colors(ncols=5, sort_colors=True)          # inspect each color library
dm.plot_colormaps(group_by_type=True, ncols=4)     # compare sequential/diverging sets
dm.plot_fonts(font_size=11, ncols=3)               # audit bundled fonts
```

- For quick asset audits, lean on **API › Visualization Tools** (`plot_colors`, `plot_colormaps`, `plot_fonts`).
