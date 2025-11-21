# Colors

A high-contrast, full-width view of every named palette that ships with
dartwork-mpl. Use the cards below to jump to the set you need; each PNG is
exported at high DPI so the labels stay readable in the browser or a slide deck.

## How the names work
- Colors follow `library.base:weight` (for example `tw.blue:500`, `md.red:700`).
- Libraries mirror the design systems they come from, so weights and hue names
  feel familiar if you already use those systems.
- All names are available through matplotlib directly—no custom APIs required.

```python
import dartwork_mpl as dm
import matplotlib.pyplot as plt

dm.use()
plt.plot(signal, color="opencolor.indigo:6", linewidth=2.4, label="Indigo 6")
plt.scatter(x, y, color="tw.rose:500")
plt.show()
```

## Palette explorer

::::{grid} 2
:gutter: 1.3
:margin: 0 0 1.2rem 0

:::{grid-item-card} OpenColor
:class-card: color-card
:img-top: images/colors_opencolor.png
:img-style: width: 100%
:img-alt: OpenColor palette
- Balanced neutrals and calm hues; great for dashboards and UI framing
- Subtle, even weight steps for layered backgrounds
:::

:::{grid-item-card} Tailwind (tw)
:class-card: color-card
:img-top: images/colors_tw.png
:img-style: width: 100%
:img-alt: Tailwind palette
- Broadest weight range (50–950) to tune contrast precisely
- Mirrors Tailwind naming for easy jump from CSS to matplotlib
:::

:::{grid-item-card} Material Design (md)
:class-card: color-card
:img-top: images/colors_md.png
:img-style: width: 100%
:img-alt: Material Design palette
- Saturated primaries and secondaries that pop on white backgrounds
- Consistent 50–900 weight steps for accessible pairings
:::

:::{grid-item-card} Ant Design (ant)
:class-card: color-card
:img-top: images/colors_ant.png
:img-style: width: 100%
:img-alt: Ant Design palette
- Compact 1–10 weight system tuned for data-heavy UIs
- Warm and cool tracks that stay legible in small marks
:::

:::{grid-item-card} Chakra UI (chakra)
:class-card: color-card
:img-top: images/colors_chakra.png
:img-style: width: 100%
:img-alt: Chakra palette
- Friendly, soft ramps for product illustrations and UI fills
- Excellent defaults for backgrounds and soft accents
:::

:::{grid-item-card} Primer (primer)
:class-card: color-card
:img-top: images/colors_primer.png
:img-style: width: 100%
:img-alt: Primer palette
- GitHub-inspired neutrals with lightweight tints and shadows
- Useful when you need desaturated accents with strong contrast
:::

:::{grid-item-card} Other & Matplotlib
:class-card: color-card
:img-top: images/colors_other.png
:img-style: width: 100%
:img-alt: Matplotlib named colors
- All remaining named colors, including matplotlib defaults and xkcd set
- Handy for quick sketches or when you need a familiar `C0`–`C9` cycle
:::
::::

## Picking weights that work
- Aim for weights 400–600 for primary lines and markers; 50–200 for backgrounds.
- Keep related elements on adjacent weights (e.g., line at 600, fill at 200).
- Prefer a single library per figure for cohesion; mix libraries only for
  intentional contrast (e.g., background from Primer, accents from Tailwind).

## Regenerate the sheets
- The PNGs above live in `docs/images/` and are regenerated automatically during
  a Sphinx build.
- Regenerate manually with `python docs/generate_gallery.py` if you are editing
  just the assets.
