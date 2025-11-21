# Colormaps

High-DPI panels for every colormap bundled with dartwork-mpl, grouped by how
they should be used. Each gradient is wide enough to show subtle shifts, and
dartwork-specific maps are tagged directly on the image.

```python
import dartwork_mpl as dm
import matplotlib.pyplot as plt
import numpy as np

dm.use()
data = np.random.randn(30, 30).cumsum(axis=0)
plt.imshow(data, cmap="dm.sunset")
plt.colorbar(label="signal strength")
plt.show()
```

## Category overview

::::{grid} 2
:gutter: 1.2
:margin: 0 0 1.2rem 0

:::{grid-item-card} Sequential • Single-Hue
:class-card: colormap-card
:img-top: images/colormaps_sequential_single-hue.png
:img-style: width: 100%
:img-alt: Sequential single-hue colormaps
- Monochrome ramps with clean value progression
- Choose for density, intensity, and anything that only moves “up”
:::

:::{grid-item-card} Sequential • Multi-Hue
:class-card: colormap-card
:img-top: images/colormaps_sequential_multi-hue.png
:img-style: width: 100%
:img-alt: Sequential multi-hue colormaps
- Adds hue shifts for extra separation while staying perceptually smooth
- Use for heatmaps, continuous gradients, and scientific figures
:::

:::{grid-item-card} Diverging
:class-card: colormap-card
:img-top: images/colormaps_diverging.png
:img-style: width: 100%
:img-alt: Diverging colormaps
- Two anchored hues split around a neutral midpoint
- Best for deltas, anomalies, and any data with a meaningful zero
:::

:::{grid-item-card} Cyclical
:class-card: colormap-card
:img-top: images/colormaps_cyclical.png
:img-style: width: 100%
:img-alt: Cyclical colormaps
- Start equals end; perfect for angles, phases, or circular domains
- Prevents false “edges” in periodic data
:::

:::{grid-item-card} Categorical
:class-card: colormap-card
:img-top: images/colormaps_categorical.png
:img-style: width: 100%
:img-alt: Categorical colormaps
- Distinct, stepwise colors for class labels or clusters
- Use when values are discrete and order does not matter
:::
::::

## Naming, reversal, and fairness
- Any matplotlib colormap name works (`viridis`, `plasma`, `twilight`, etc.),
  plus the dartwork-specific set prefixed with `dm.`.
- Append `_r` to reverse direction (`dm.sunset_r`), helpful when your values read
  better with dark at the bottom or vice versa.
- Prefer perceptually uniform ramps for quantitative data; reserve categorical
  maps for truly discrete labels.

## Regenerate the panels
- Panels live in `docs/images/` and are regenerated automatically during a
  Sphinx build.
- To refresh manually, run `python docs/generate_gallery.py`; new PNGs will
  replace the existing ones.
