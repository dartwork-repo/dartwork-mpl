# Color System

The original “Color Gallery” is now a dedicated **Color System** hub with space
for both the named colors and the colormap collection. Jump into whichever view
you need, or skim both for a quick sense of what ships with dartwork-mpl.

::::{grid} 2
:gutter: 1.2
:margin: 0 0 1.5rem 0

:::{grid-item-card} Colors
:link: COLORS
:class-card: color-card
:img-top: images/colors_opencolor.png
:img-style: width: 100%
:img-alt: OpenColor palette preview
- Named palettes from OpenColor, Tailwind, Material, Ant Design, Chakra, Primer
- Weight-aware names like `tw.blue:500` or `md.red:700`
- Larger swatches so you can actually read the labels
:::

:::{grid-item-card} Colormaps
:link: COLORMAPS
:class-card: colormap-card
:img-top: images/colormaps_sequential_multi-hue.png
:img-style: width: 100%
:img-alt: Sequential multi-hue colormaps
- Grouped views for Sequential, Diverging, Cyclical, and Categorical ramps
- Highlights dartwork-specific maps directly in the panels
- Wide gradients sized for presentations and exported figures
:::
::::

## Quick recipe

```python
import dartwork_mpl as dm
import matplotlib.pyplot as plt

dm.use()  # style + fonts
plt.plot([0, 1, 2], color="tw.emerald:500", label="Tailwind emerald")
plt.imshow(data, cmap="dm.sunset")  # any matplotlib colormap name works
plt.legend()
plt.show()
```

## Regenerating assets

- The gallery PNGs live in `docs/images/`.
- Sphinx now runs `docs/generate_gallery.py` automatically during a build, or run
  it directly with `python docs/generate_gallery.py` if you just want the assets.
- Generated panels are high-DPI and designed to be embedded at full width in the
  new Colors and Colormaps pages.
