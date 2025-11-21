# Color System

A single, scrollable hub for everything color-related in dartwork-mpl. Each
section below is a full-width preview; click through to the dedicated page if
you want the complete sheets and usage details.

```{toctree}
:maxdepth: 1
:titlesonly:
:hidden:

Colors <COLORS>
Colormaps <COLORMAPS>
```

:::{figure} images/colors_opencolor.png
:alt: OpenColor palette preview with labeled swatches
:width: 100%

**Colors.** All named palettes ship as weight-aware labels you can drop straight
into matplotlib (`tw.blue:500`, `md.red:700`, `opencolor.gray:6`, and more).
Every sheet uses generous spacing so labels stay legible.  
[Open the full color sheets →](COLORS)
:::

:::{figure} images/colormaps_sequential_multi-hue.png
:alt: Sequential multi-hue colormap preview
:width: 100%

**Colormaps.** Sequential, diverging, cyclical, and categorical ramps—plus the
dartwork-specific set prefixed with `dm.`—rendered as wide gradients sized for
slides and exports.  
[Browse the colormap panels →](COLORMAPS)
:::

## Quick start

```python
import dartwork_mpl as dm
import matplotlib.pyplot as plt
import numpy as np

dm.use()  # style + fonts
x = np.linspace(0, 10, 200)
signal = np.sin(x) * np.exp(-0.08 * x)

plt.plot(x, signal, color="tw.emerald:500", linewidth=2.6, label="Emerald 500")
plt.imshow(np.outer(signal, signal), cmap="dm.sunset")
plt.colorbar(label="normalized response")
plt.legend()
plt.show()
```

## Regenerating the visuals

- All preview PNGs live in `docs/images/`.
- Sphinx runs `docs/generate_gallery.py` during a build; run it manually to
  refresh assets after editing colors or colormaps.
- Exports are high-DPI so the single-column layouts remain crisp when embedded.
