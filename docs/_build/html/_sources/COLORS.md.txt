# Colors

Wide, single-column sheets for every named palette in dartwork-mpl. Each preview
below is full-width so the swatch labels stay readable on both desktop and
mobile.

## How to read the labels
- Format: `library.base:weight` (`tw.blue:500`, `md.red:700`, `opencolor.gray:6`).
- Works anywhere matplotlib accepts a color—no extra API layer required.
- `dm.use()` loads the dartwork style so these names look consistent across
  lines, fills, markers, and legends.

```python
import dartwork_mpl as dm
import matplotlib.pyplot as plt
import numpy as np

dm.use()
t = np.linspace(0, 2 * np.pi, 200)
plt.plot(t, np.sin(t), color="opencolor.indigo:6", linewidth=2.4, label="Indigo 6")
plt.scatter(t[::12], np.cos(t[::12]), color="tw.rose:500", edgecolor="none")
plt.legend()
plt.show()
```

## Palette sheets (single column)

:::{figure} images/colors_opencolor.png
:alt: OpenColor palette sheet with labeled swatches
:width: 100%

**OpenColor.** Balanced neutrals and calm hues for dashboards and UI frames. Even
weight steps make layered backgrounds straightforward.
:::

:::{figure} images/colors_tw.png
:alt: Tailwind palette sheet with labeled swatches
:width: 100%

**Tailwind.** The broadest weight range (50–950) for precise contrast tuning.
Perfect when you already think in Tailwind classes.
:::

:::{figure} images/colors_md.png
:alt: Material Design palette sheet with labeled swatches
:width: 100%

**Material Design.** Saturated primaries and secondaries that read clearly on
white backgrounds, with consistent 50–900 steps.
:::

:::{figure} images/colors_ant.png
:alt: Ant Design palette sheet with labeled swatches
:width: 100%

**Ant Design.** Compact 1–10 weight system tuned for dense, data-heavy UIs with
both warm and cool tracks that stay legible in small marks.
:::

:::{figure} images/colors_chakra.png
:alt: Chakra UI palette sheet with labeled swatches
:width: 100%

**Chakra UI.** Soft, friendly ramps ideal for product illustrations, covers, and
muted backgrounds that do not overpower overlays.
:::

:::{figure} images/colors_primer.png
:alt: Primer palette sheet with labeled swatches
:width: 100%

**Primer.** GitHub-inspired neutrals with subtle tints and shadows—great when
you need desaturated accents with strong contrast.
:::

:::{figure} images/colors_other.png
:alt: Other and matplotlib palettes sheet with labeled swatches
:width: 100%

**Other & Matplotlib.** Everything else, including matplotlib defaults and the
xkcd set, for quick sketches or when you want the familiar `C0`–`C9` cycle.
:::

## Rendering guidance
- Use weights 400–600 for lines and markers; 50–200 for fills and backgrounds.
- Pair adjacent weights for related elements (e.g., line at 600, fill at 200).
- Keep a single library per figure unless you need deliberate contrast (Primer
  background with Tailwind accents, for example).
- Turn off `edgecolor` on dense scatters to keep swatches clean in exports.

## Refreshing the sheets
- All PNGs live in `docs/images/`.
- A Sphinx build runs `python docs/generate_gallery.py`; run it directly if you
  tweak palette data and want to update only the assets.
