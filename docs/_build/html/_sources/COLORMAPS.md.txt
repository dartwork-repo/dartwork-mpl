# Colormaps

Single-column, wide gradients for every colormap bundled with dartwork-mpl. The
panels below stay legible on narrow viewports and match the naming used inside
matplotlib.

## Use them at a glance
- Any matplotlib name works (`viridis`, `plasma`, `twilight`, etc.) plus the
  dartwork-specific set prefixed with `dm.`.
- Add `_r` to reverse a map (`dm.sunset_r`) when dark-to-light needs flipping.
- Set `vmin`/`vmax` yourself for stable colorbars across facets or animations.
- `dm.use()` keeps colorbar labels and ticks consistent with the rest of the
  style.

```python
import dartwork_mpl as dm
import matplotlib.pyplot as plt
import numpy as np

dm.use()
data = np.random.randn(50, 50).cumsum(axis=0)
im = plt.imshow(data, cmap="dm.sunset", vmin=-8, vmax=8)
cb = plt.colorbar(im, extend="both", shrink=0.9, pad=0.02)
cb.set_label("normalized signal")
cb.outline.set_visible(False)
plt.show()
```

## Gradient panels (single column)

:::{figure} images/colormaps_sequential_single-hue.png
:alt: Sequential single-hue colormaps shown as wide horizontal gradients
:width: 100%

**Sequential · Single-Hue.** Monochrome ramps with clean value progression for
density plots, intensity maps, and anything that only moves upward.
:::

:::{figure} images/colormaps_sequential_multi-hue.png
:alt: Sequential multi-hue colormaps shown as wide horizontal gradients
:width: 100%

**Sequential · Multi-Hue.** Adds subtle hue shifts for extra separation while
staying perceptually smooth—ideal for heatmaps and continuous fields.
:::

:::{figure} images/colormaps_diverging.png
:alt: Diverging colormaps shown as wide horizontal gradients
:width: 100%

**Diverging.** Two anchored hues split around a neutral midpoint. Use for deltas
and anomalies where zero has meaning; set symmetric `vmin`/`vmax` when possible.
:::

:::{figure} images/colormaps_cyclical.png
:alt: Cyclical colormaps shown as wide horizontal gradients
:width: 100%

**Cyclical.** Start equals end, so there are no false edges. Perfect for angles,
phases, or any periodic domain.
:::

:::{figure} images/colormaps_categorical.png
:alt: Categorical colormaps shown as wide horizontal gradients
:width: 100%

**Categorical.** Distinct, stepwise colors for class labels or clusters where
order does not matter.
:::

## Colorbar and rendering notes
- Prefer perceptually uniform ramps for quantitative data; reserve categorical
  bars for truly discrete labels.
- Align colorbars with the plot width and hide outlines to keep the single
  column clean (`cb.outline.set_visible(False)`).
- For diverging data, pick symmetric limits and set `extend="both"` so extreme
  values remain visible without clipping.
- Use `imshow(..., interpolation="nearest")` when you want hard edges; drop the
  argument for smooth gradients.

## Refreshing the panels
- PNGs live in `docs/images/`.
- Sphinx runs `python docs/generate_gallery.py` during a build; run it directly
  after editing the colormap set to regenerate just these assets.
