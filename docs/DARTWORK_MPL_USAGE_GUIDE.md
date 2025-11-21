# Usage Guide

dartwork-mpl packages opinionated matplotlib styles, curated color libraries, and
layout utilities to quickly assemble publication-quality figures. Everything
below is based on the code shipped in this repository—no imaginary presets.

## Key Features
- Style presets for papers, presentations, and Korean documents (scientific,
  investment, presentation variants + `-kr` versions).
- Large color catalog: `dm.*` plus Tailwind (`tw.`), Material (`md.`), Ant
  (`ant.`), Chakra (`chakra.`), Primer (`primer.`), and opencolor sets.
- Layout helpers (`simple_layout`, `cm2in`, `make_offset`) to control margins
  predictably.
- Font utilities (`fs`, `fw`) and bundled fonts auto-registered on import.
- Save/display helpers for multi-format export and notebook-friendly previews.

## 1. Style Management

### 1.1 Available Styles and Presets
```python
import dartwork_mpl as dm

# Individual style files (asset/mplstyle)
dm.list_styles()
# ['base', 'dmpl', 'dmpl_light', 'font-investment', 'font-presentation',
#  'font-scientific', 'lang-kr', 'spine-no', 'spine-yes']

# Presets defined in presets.json (no other presets exist)
dm.style.presets_dict()
# {
#   'scientific': ['base', 'font-scientific'],
#   'investment': ['base', 'font-investment'],
#   'presentation': ['base', 'font-presentation'],
#   'scientific-kr': ['base', 'font-scientific', 'lang-kr'],
#   'investment-kr': ['base', 'font-investment', 'lang-kr'],
#   'presentation-kr': ['base', 'font-presentation', 'lang-kr'],
# }
```

> Tip: The package enables `dmpl_light` by default in `__init__.py`. Call
> `dm.style.use_preset(...)` or `dm.use_style(...)` to switch explicitly.

### 1.2 Apply Styles
```python
# Recommended: presets
dm.style.use_preset('scientific')      # Academic papers
dm.style.use_preset('presentation')    # Slides
dm.style.use_preset('scientific-kr')   # Korean documents

# Combine individual style files
dm.style.use(['base', 'spine-no', 'font-presentation'])

# Legacy helper
dm.use_style('dmpl_light')
```

### 1.3 Inspect Styles
```python
dm.load_style_dict('font-presentation')   # Key/value pairs from style file
dm.style_path('base')                     # Path to a style file
dm.style.presets_path()                   # Path to presets.json
```

## 2. Colors

### 2.1 Named Colors
On import, `dartwork_mpl.color` registers many named colors:
- `dm.*` (opencolor + xkcd set with `dm.` prefix)
- Tailwind CSS: `tw.{color}:{weight}` (e.g., `tw.blue:500`)
- Material Design: `md.{color}:{weight}`
- Ant Design: `ant.{color}:{weight}`
- Chakra UI: `chakra.{color}:{weight}`
- Primer: `primer.{color}:{weight}`

Use them like any matplotlib color:
```python
ax.plot(x, y, color='dm.red5')
ax.fill_between(x, y1, y2, color='tw.gray:200')
```

### 2.2 Color Utilities
```python
dm.mix_colors('dm.red5', 'dm.blue5', alpha=0.5)        # Blend two colors
dm.pseudo_alpha('dm.red5', alpha=0.3, background='white')  # Fake transparency
dm.classify_colormap(plt.colormaps['viridis'])         # -> category label
```

## 3. Layout Utilities

### 3.1 Figure Sizing Helpers
```python
fig = plt.figure(figsize=(dm.cm2in(17), dm.cm2in(12)), dpi=300)  # 17 cm wide
gs = fig.add_gridspec(2, 2, left=0.08, right=0.98, top=0.92, bottom=0.12)
```

### 3.2 Simple Layout Optimization
`simple_layout` adjusts margins more predictably than `tight_layout`.
```python
dm.simple_layout(fig)  # default margins
dm.simple_layout(fig, margins=(0.08, 0.08, 0.1, 0.08))  # (L, R, B, T) in inches
dm.simple_layout(fig, gs=gs, bbox=(0, 0.5, 0, 1))       # only left half
dm.simple_layout(fig, use_all_axes=True)                # consider all axes
```

### 3.3 Precise Offsets and Formatting
```python
offset = dm.make_offset(4, -4, fig)  # pt offsets
ax.text(0, 1, 'a', transform=ax.transAxes + offset, weight='bold')
dm.set_decimal(ax, xn=2, yn=1)       # tick label decimals
```

## 4. Fonts
Bundled fonts are registered automatically on import. Use utilities to offset
sizes/weights relative to the active style:
```python
ax.set_title("Title", fontsize=dm.fs(2), fontweight=dm.fw(1))
ax.legend(fontsize=dm.fs(-1))
```

## 5. Saving and Display

### 5.1 Multi-format Save
```python
dm.save_formats(fig, 'output/figure', formats=('svg', 'png', 'pdf', 'eps'),
                bbox_inches='tight', dpi=300)
```

### 5.2 Save + Show (Notebook-friendly)
```python
dm.save_and_show(fig, size=600)               # temp file + display
dm.save_and_show(fig, 'output/figure.svg', size=600)
dm.show('output/figure.svg', size=600)
```

## 6. Subplot Labels
```python
for ax, label in zip([ax1, ax2], 'ab'):
    ax.text(0, 1, label, transform=ax.transAxes + dm.make_offset(4, -4, fig),
            weight='bold', va='top')
```

## Reference: Package Defaults
- Default style applied on import: `dmpl_light` (`dartwork_mpl/__init__.py`).
- Style presets live in `asset/mplstyle/presets.json`.
- Color definitions live in `asset/color/*.txt` and JSON libraries.
- Fonts live in `asset/font` and are added via `font.py` on import.
