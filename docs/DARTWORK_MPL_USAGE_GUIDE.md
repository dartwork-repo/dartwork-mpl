# Usage Guide

## 1. Key Features

### 2.1 Style Management

#### Check Available Styles
```python
# List all individual styles
dm.list_styles()
# ['base', 'dmpl', 'dmpl_light', 'font-investment', 'font-presentation', 
#  'font-scientific', 'lang-kr', 'spine-no', 'spine-yes']

# Check available presets
dm.style.presets_dict()
# {'scientific': ['base', 'font-scientific'],
#  'investment': ['base', 'font-investment'],
#  'presentation': ['base', 'font-presentation'],
#  'scientific-kr': ['base', 'font-scientific', 'lang-kr'],
#  'investment-kr': ['base', 'font-investment', 'lang-kr'],
#  'presentation-kr': ['base', 'font-presentation', 'lang-kr']}
```

#### Apply Style
```python
# Use preset (Recommended)
dm.style.use_preset('scientific')  # For papers
dm.style.use_preset('presentation')  # For presentations
dm.style.use_preset('scientific-kr')  # For Korean papers

# Combine individual styles (Advanced)
dm.style.use(['base', 'spine-no', 'font-presentation'])

# Legacy API (backward compatibility)
dm.use_style('dmpl')
```

#### Inspect Style Content
```python
# Check content of a style file
style_dict = dm.load_style_dict('font-presentation')

# Check path of a style file
path = dm.style_path('base')

# Check path of presets definition file
preset_path = dm.style.presets_path()
```

### 2.2 Color System

#### dartwork-mpl Custom Colors
```python
# Use with dm. prefix
ax.plot(x, y, color='dm.red5')
ax.scatter(x, y, c='dm.blue2')
```

#### Tailwind CSS Colors
```python
# Use tw. or tailwind. prefix
# Format: tw.{color}:{weight}
ax.plot(x, y, color='tw.blue:500')
ax.fill_between(x, y1, y2, color='tailwind.gray:200')
```

#### Color Utilities
```python
# Mix two colors
mixed = dm.mix_colors('dm.red5', 'dm.blue5', alpha=0.5)

# Apply pseudo-transparency (mix with background)
transparent = dm.pseudo_alpha('dm.red5', alpha=0.3, background='white')
```

### 2.3 Layout Utilities

#### Recommended Figure Creation Pattern
```python
# Create figure for papers (Unit: cm -> inch conversion)
# Single column figure: 9cm width
fig = plt.figure(
    figsize=(dm.cm2in(9), dm.cm2in(7)),
    dpi=200
)

# Double column figure: 17cm width
fig = plt.figure(
    figsize=(dm.cm2in(17), dm.cm2in(7)),
    dpi=200
)

# Set layout with GridSpec
gs = fig.add_gridspec(
    nrows=1, ncols=1, 
    left=0.17, right=0.95, 
    top=0.95, bottom=0.17, 
    hspace=0.3, wspace=0
)
ax = fig.add_subplot(gs[0, 0])
```

#### Automatic Layout Adjustment

`simple_layout` is an improved version of `plt.tight_layout()`, providing more precise margin control and predictable results.

```python
# Basic usage (Recommended)
dm.simple_layout(fig)

# Adjust margins (Unit: inch, left, right, bottom, top)
dm.simple_layout(fig, margins=(0.1, 0.05, 0.1, 0.05))

# Apply only to specific GridSpec
dm.simple_layout(fig, gs=gs, margins=(0.08, 0.02, 0.08, 0.02))

# Optimize partial area using bbox (Figure coordinates: left, right, bottom, top)
# Entire figure (Default)
dm.simple_layout(fig, bbox=(0, 1, 0, 1))

# Optimize only left half
dm.simple_layout(fig, bbox=(0, 0.5, 0, 1))

# Optimize only right half
dm.simple_layout(fig, bbox=(0.5, 1, 0, 1))

# Optimize only top half
dm.simple_layout(fig, bbox=(0, 1, 0.5, 1))

# Apply to all axes (When multiple GridSpecs exist)
dm.simple_layout(fig, use_all_axes=True)
```

**Key Parameters:**
- `margins`: Margins in inches (left, right, bottom, top)
- `bbox`: Optimization target area in figure coordinates (left, right, bottom, top)
- `gs`: Specific GridSpec (Uses first GridSpec if None)
- `use_all_axes`: Consider all axes if True (Default: False)

**bbox Usage Example:**
When multiple subplots exist, you can optimize layout for specific areas individually. For example, `bbox=(0, 0.5, 0, 1)` optimizes layout only for the left half of the figure.

### 2.4 Font Utilities

```python
# Relative font size adjustment
title_size = dm.fs(2)   # base font size + 2
label_size = dm.fs(-1)  # base font size - 1

# Font weight adjustment (100 units)
bold_weight = dm.fw(2)  # base weight + 200

# Usage example
ax.set_title('Title', fontsize=dm.fs(2), fontweight=dm.fw(1))
ax.legend(fontsize=dm.fs(-2))
```

### 2.5 Save and Display

#### Multi-format Save
```python
# Save in multiple formats simultaneously
dm.save_formats(
    fig, 
    'output/figure',  # Without extension
    formats=('svg', 'png', 'pdf', 'eps'),
    bbox_inches='tight',
    dpi=600
)
```

#### Save and Display in Jupyter
```python
# Use instead of plt.show() - Save to temp file and display (Recommended)
dm.save_and_show(fig, size=600)

# Save to specific path and display
dm.save_and_show(fig, 'output/figure.svg', size=600)

# Display existing file
dm.show('output/figure.svg', size=600)
```

### 2.6 Subplot Labeling

```python
# Add subplot labels (a, b, c...)
axs = [ax1, ax2]
for ax, label in zip(axs, 'ab'):
    # Must use make_offset for text offset
    offset = dm.make_offset(4, -4, fig)  # x=4pt, y=-4pt
    ax.text(
        0, 1, label, 
        transform=ax.transAxes + offset,
        weight='bold',
        verticalalignment='top'
    )
```

**Important**: Always use `dm.make_offset()` when adjusting text position. This function provides precise offsets in points (pt), ensuring consistent results regardless of DPI.

### 2.7 Colormap Visualization

```python
# Check available colormaps
fig, axs = dm.plot_colormaps(
    cmap_list=['viridis', 'dm.spectral'],  # All if None
    ncols=3,
    group_by_type=True  # Group by type
)

# Check color palette
fig = dm.plot_colors()  # Show all colors

# Check fonts
fig = dm.plot_fonts()  # Show available fonts
```

## 3. Recommended Workflow

### Steps for Publication-Quality Graphs

1. **Separate Data Preparation and Plotting Code**
```python
# Data preparation cell
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Plot cell (Separate)
fig = plt.figure(figsize=(dm.cm2in(9), dm.cm2in(7)))
# ...
```

2. **GridSpec Based Layout**
```python
gs = fig.add_gridspec(
    nrows=2, ncols=1,
    left=0.17, right=0.95,
    top=0.95, bottom=0.17,
    hspace=0.3
)
```

3. **Handle Based Legend**
```python
line1, = ax.plot(x, y1, color='dm.red5', lw=0.7)
scatter1 = ax.scatter([], [], c='dm.red5', s=1)  # Dummy for legend
ax.legend([scatter1, line1], ['Data', 'Model'])
```

4. **Explicit Tick Setting**
```python
ax.set_xticks([0, 2, 4, 6, 8, 10])
ax.set_yticks([-1, -0.5, 0, 0.5, 1])
```

5. **Check Save Result**
```python
# Use instead of plt.show() - Check actual saved result
dm.save_and_show(fig)
```

## 4. Korean Support

```python
# Apply Korean font
dm.style.use(['base', 'lang-kr'])

# Or use preset
dm.style.use_preset('scientific-kr')
```

## 5. Preset Styles

Available Presets:
- `scientific`: For academic papers (Small fonts)
- `investment`: For investment reports
- `presentation`: For presentations (Large fonts)
- `scientific-kr`, `investment-kr`, `presentation-kr`: Korean versions

## 6. Precautions

1. **Avoid tight_layout**: Recommend using `dm.simple_layout()`
2. **Savefig Criteria**: Work based on saved files, not `plt.show()`
3. **Check Units**: matplotlib uses various units (inch, point, pixel)
4. **Color Naming**: Distinguish `dm.`, `tw.`, `tailwind.` prefixes

## 7. Complete Example

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Set style
dm.style.use_preset('scientific')

# Generate data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y1_data = y1 + np.random.normal(0, 0.1, size=len(y1))
y2_data = y2 + np.random.normal(0, 0.1, size=len(y2))

# Create Figure
fig = plt.figure(
    figsize=(dm.cm2in(9), dm.cm2in(7)),
    dpi=200
)

# GridSpec Layout
gs = fig.add_gridspec(
    nrows=1, ncols=1,
    left=0.17, right=0.95,
    top=0.95, bottom=0.17
)
ax = fig.add_subplot(gs[0, 0])

# Plot Data
line1, = ax.plot(x, y1, c='dm.red5', lw=0.7)
line2, = ax.plot(x, y2, c='dm.blue5', lw=0.7)
ax.scatter(x, y1_data, c='dm.red2', s=0.7)
ax.scatter(x, y2_data, c='dm.blue2', s=0.7)

# Dummy plots for legend
scatter1 = ax.scatter([], [], c='dm.red5', s=10)
scatter2 = ax.scatter([], [], c='dm.blue5', s=10)

# Labels and Legend
ax.set_xlabel('X value [Hour]')
ax.set_ylabel('Y value [kW]')
ax.legend(
    [scatter1, line1, scatter2, line2],
    ['Sin data', 'Sin model', 'Cos data', 'Cos model'],
    loc='upper right',
    fontsize=dm.fs(-1),
    ncol=2
)

# Set Ticks
ax.set_xticks([0, 2, 4, 6, 8, 10])
ax.set_yticks([-1, -0.5, 0, 0.5, 1])
ax.set_ylim(-1.2, 1.2)

# Optimize Layout
dm.simple_layout(fig)

# Preview in Jupyter
dm.save_and_show(fig)

# Save in multiple formats for submission
dm.save_formats(
    fig,
    'figures/example_figure',  # Base filename without extension
    formats=('svg', 'png', 'pdf', 'eps'),  # Save all 4 formats
    bbox_inches='tight',
    dpi=600
)
```