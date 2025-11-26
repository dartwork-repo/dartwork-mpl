# Font Families

dartwork-mpl bundles 9 professional font families with a total of 130 font
variants. Each family is optimized for different use cases in data visualization.

## Roboto (Default)

:::{figure} images/font_roboto.png
:alt: Roboto font family preview
:width: 100%
:::

Google's flagship sans-serif typeface and the **default font in dartwork-mpl**.
Roboto features friendly, open curves while maintaining a mechanical skeleton,
making it highly legible at all sizes.

**Variants:** 15 (Thin, Light, Regular, Medium, Bold, Black + Italics)

**Best For:**
- General-purpose body text
- Axis labels and tick marks
- Legends and annotations

**Usage:**
```python
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Roboto'
plt.rcParams['font.weight'] = 300  # Light weight (dartwork default)
```

---

## Inter

:::{figure} images/font_inter.png
:alt: Inter font family preview
:width: 100%
:::

A modern sans-serif typeface designed specifically for computer screens. Inter
features a tall x-height for improved readability at small sizes and includes
many OpenType features.

**Variants:** 20 (Thin through Black, with Italics)

**Best For:**
- UI-style visualizations
- Presentations and slides
- Screen-first publications

**Usage:**
```python
plt.rcParams['font.family'] = 'Inter'
```

---

## InterDisplay

:::{figure} images/font_interdisplay.png
:alt: InterDisplay font family preview
:width: 100%
:::

The display variant of Inter, optimized for larger sizes. Features tighter
letter-spacing and refined details that shine at headline sizes.

**Variants:** 20 (Thin through Black, with Italics)

**Best For:**
- Figure titles
- Section headings
- Large callout text

**Usage:**
```python
ax.set_title("Main Title", fontfamily='Inter Display', fontsize=24)
```

---

## Noto Sans

:::{figure} images/font_notosans.png
:alt: Noto Sans font family preview
:width: 100%
:::

Google's Noto Sans provides harmonious typography across hundreds of languages.
The name "Noto" comes from "No Tofu"—the goal of eliminating the blank boxes
(tofu) that appear when a font lacks a glyph.

**Variants:** 15 (ExtraLight through Black, with Italics)

**Best For:**
- Multi-language documents
- International publications
- Unicode-heavy content

**Usage:**
```python
plt.rcParams['font.family'] = 'Noto Sans'
```

---

## Noto Sans Condensed

:::{figure} images/font_notosans_condensed.png
:alt: Noto Sans Condensed font family preview
:width: 100%
:::

The condensed variant of Noto Sans, providing the same excellent character
coverage in a narrower form factor.

**Variants:** 20 (Thin through Black, with Italics)

**Best For:**
- Tables with many columns
- Dense data visualizations
- Space-constrained layouts

**Usage:**
```python
plt.rcParams['font.family'] = 'Noto Sans Condensed'
```

---

## Noto Sans SemiCondensed

:::{figure} images/font_notosans_semicondensed.png
:alt: Noto Sans SemiCondensed font family preview
:width: 100%
:::

A middle ground between regular Noto Sans and the fully condensed variant.
Offers good space efficiency while maintaining excellent readability.

**Variants:** 20 (Thin through Black, with Italics)

**Best For:**
- Legends with many entries
- Compact labels
- Moderate space savings

**Usage:**
```python
plt.rcParams['font.family'] = 'Noto Sans SemiCondensed'
```

---

## Noto Sans ExtraCondensed

:::{figure} images/font_notosans_extracondensed.png
:alt: Noto Sans ExtraCondensed font family preview
:width: 100%
:::

The most condensed variant in the Noto Sans family. Use when space is at an
absolute premium.

**Variants:** 20 (Thin through Black, with Italics)

**Best For:**
- Very tight axis labels
- Narrow figure margins
- Maximum information density

**Usage:**
```python
plt.rcParams['font.family'] = 'Noto Sans ExtraCondensed'
```

---

## Noto Sans Math

:::{figure} images/font_notosansmath.png
:alt: Noto Sans Math font preview
:width: 100%
:::

A dedicated font for mathematical typesetting. Noto Sans Math provides
comprehensive coverage of mathematical symbols, operators, and special
characters used in scientific notation.

**Variants:** 1 (Regular only)

**Best For:**
- Scientific equations
- Mathematical notation
- Greek letters and symbols

**Usage in dartwork-mpl:**

Noto Sans Math is automatically configured for mathtext rendering:

```python
# These settings are applied by dartwork-mpl styles
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Noto Sans Math'
plt.rcParams['mathtext.it'] = 'Noto Sans Math:italic'
plt.rcParams['mathtext.bf'] = 'Noto Sans Math:bold'
```

**Example:**
```python
ax.set_xlabel(r'$\alpha = \frac{\Delta x}{\Delta t}$')
ax.set_ylabel(r'$\sum_{i=1}^{n} x_i^2$')
```

---

## Paperlogy

:::{figure} images/font_paperlogy.png
:alt: Paperlogy font family preview
:width: 100%
:::

A clean, professional typeface designed specifically for documents and papers.
Paperlogy offers excellent readability in dense text environments typical of
academic and business publications.

**Variants:** 9 (Light through Black)

**Best For:**
- Academic papers
- Technical reports
- Professional documents

**Usage:**
```python
plt.rcParams['font.family'] = 'Paperlogy'
```

---

## Font Weight Reference

All font families (except Noto Sans Math) include multiple weights:

| Weight Name | Numeric Value | Description |
|-------------|---------------|-------------|
| Thin | 100 | Extremely light |
| ExtraLight | 200 | Very light |
| Light | 300 | Light (dartwork default) |
| Regular | 400 | Normal |
| Medium | 500 | Slightly bold |
| SemiBold | 600 | Semi-bold |
| Bold | 700 | Bold |
| ExtraBold | 800 | Extra bold |
| Black | 900 | Maximum weight |

:::{figure} images/font_weights.png
:alt: Font weight comparison
:width: 100%
:::

**Using Weights:**
```python
# Direct weight specification
ax.set_title("Title", fontweight=700)

# Or use the fw() helper for relative weights
ax.set_title("Title", fontweight=dm.fw(2))  # base + 200
```
