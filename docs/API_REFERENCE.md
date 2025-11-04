# API Reference

This document provides detailed information about all public functions and classes in `dartwork-mpl`.

## Table of Contents

1. [Style Management](#style-management)
2. [Layout Utilities](#layout-utilities)
3. [Color Utilities](#color-utilities)
4. [Font Utilities](#font-utilities)
5. [Unit Conversion](#unit-conversion)
6. [File I/O](#file-io)
7. [Visualization Tools](#visualization-tools)

---

## Style Management

### `dm.style.use_preset(preset_name)`

Apply a preset style configuration.

**Parameters:**
- `preset_name` (str): Name of the preset to apply.

**Available Presets:**
- `'scientific'`: Small fonts for academic papers
- `'presentation'`: Large fonts for presentations
- `'investment'`: Style for investment reports
- `'scientific-kr'`: Scientific style with Korean support
- `'presentation-kr'`: Presentation style with Korean support
- `'investment-kr'`: Investment style with Korean support

**Returns:** None

**Example:**
```python
import dartwork_mpl as dm
dm.style.use_preset('scientific')
```

---

### `dm.style.use(style_names)`

Use multiple individual styles in sequence.

**Parameters:**
- `style_names` (list of str): List of style names to apply.

**Returns:** None

**Example:**
```python
dm.style.use(['base', 'font-scientific', 'spine-no'])
```

---

### `dm.use_style(name='dmpl')`

Use a single matplotlib style from the package's style library.

**Parameters:**
- `name` (str, optional): Name of the style to use. Default is `'dmpl'`.

**Returns:** None

**Example:**
```python
dm.use_style('dmpl_light')
```

---

### `dm.list_styles()`

List all available individual styles.

**Parameters:** None

**Returns:**
- `list` of `str`: Sorted list of style names.

**Example:**
```python
styles = dm.list_styles()
print(styles)
# ['base', 'dmpl', 'dmpl_light', 'font-investment', ...]
```

---

### `dm.style.presets_dict()`

Get all available presets as a dictionary.

**Parameters:** None

**Returns:**
- `dict`: Dictionary mapping preset names to their style configuration lists.

**Example:**
```python
presets = dm.style.presets_dict()
print(presets['scientific'])
# ['base', 'font-scientific']
```

---

### `dm.load_style_dict(name)`

Load key-value pairs from a mplstyle file.

**Parameters:**
- `name` (str): Name of the style.

**Returns:**
- `dict`: Dictionary of style parameters.

**Example:**
```python
style_dict = dm.load_style_dict('font-scientific')
print(style_dict['font.size'])
# 9
```

---

### `dm.style_path(name)`

Get the path to a style file.

**Parameters:**
- `name` (str): Name of the style.

**Returns:**
- `Path`: Path to the style file.

**Raises:**
- `ValueError`: If the style is not found.

**Example:**
```python
from pathlib import Path
path = dm.style_path('base')
print(path)
# PosixPath('/path/to/dartwork_mpl/asset/mplstyle/base.mplstyle')
```

---

## Layout Utilities

### `dm.simple_layout(fig, gs=None, margins=(0.05, 0.05, 0.05, 0.05), bbox=(0, 1, 0, 1), ...)`

Apply optimized layout to figure for given grid spec. This is an improved alternative to `plt.tight_layout()`.

**Parameters:**
- `fig` (matplotlib.figure.Figure): Figure object to optimize.
- `gs` (matplotlib.gridspec.GridSpec, optional): Grid spec object. If None, uses the first grid spec. Default is None.
- `margins` (tuple of 4 floats, optional): Margins in inches, (left, right, bottom, top). Default is (0.05, 0.05, 0.05, 0.05).
- `bbox` (tuple of 4 floats, optional): Bounding box in figure coordinates, (left, right, bottom, top). Default is (0, 1, 0, 1).
- `verbose` (bool, optional): Print verbose output. Default is False.
- `gtol` (float, optional): Gradient tolerance for optimization. Default is 1e-2.
- `bound_margin` (float, optional): Margin for bounds generation. Default is 0.2.
- `use_all_axes` (bool, optional): Use all axes in the figure. If False, use only axes in the given grid spec. Default is False.
- `importance_weights` (tuple of 4 floats, optional): Importance weights for each target (left, right, bottom, top). Default is (1, 1, 1, 1).

**Returns:**
- `scipy.optimize.OptimizeResult`: Optimization result.

**Example:**
```python
import matplotlib.pyplot as plt
import dartwork_mpl as dm

fig = plt.figure(figsize=(dm.cm2in(9), dm.cm2in(7)))
gs = fig.add_gridspec(1, 1)
ax = fig.add_subplot(gs[0, 0])

# ... plotting code ...

# Basic usage
dm.simple_layout(fig)

# With custom margins (in inches)
dm.simple_layout(fig, margins=(0.1, 0.05, 0.1, 0.05))

# Optimize only left half of figure
dm.simple_layout(fig, bbox=(0, 0.5, 0, 1))
```

---

### `dm.make_offset(x, y, fig)`

Create a translation offset for figure elements in points.

**Parameters:**
- `x` (float): X offset in points.
- `y` (float): Y offset in points.
- `fig` (matplotlib.figure.Figure): Figure to create offset for.

**Returns:**
- `matplotlib.transforms.ScaledTranslation`: Offset transform.

**Example:**
```python
# Add subplot label with offset
offset = dm.make_offset(4, -4, fig)
ax.text(0, 1, 'a',
        transform=ax.transAxes + offset,
        weight='bold',
        verticalalignment='top')
```

---

## Color Utilities

### Using dartwork-mpl Colors

dartwork-mpl provides custom colors that can be used with the `dm.` or `dartwork_mpl.` prefix.

**Usage:**
```python
ax.plot(x, y, color='dm.red5')
ax.scatter(x, y, c='dm.blue2')
```

**Available colors:** Use `dm.plot_colors()` to see all available colors.

---

### Using Tailwind CSS Colors

Full Tailwind CSS color palette with weights from 50 to 950.

**Usage:**
```python
# Format: tw.{color}:{weight} or tailwind.{color}:{weight}
ax.plot(x, y, color='tw.blue:500')
ax.fill_between(x, y1, y2, color='tailwind.gray:200')
```

**Available colors:**
- Colors: blue, gray, red, green, yellow, purple, pink, indigo, etc.
- Weights: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950

---

### `dm.mix_colors(color1, color2, alpha=0.5)`

Mix two colors with specified weight.

**Parameters:**
- `color1` (color): First color (any format accepted by matplotlib).
- `color2` (color): Second color (any format accepted by matplotlib).
- `alpha` (float, optional): Weight of the first color, between 0 and 1. Default is 0.5.

**Returns:**
- `tuple`: RGB tuple of the mixed color.

**Example:**
```python
mixed = dm.mix_colors('dm.red5', 'dm.blue5', alpha=0.7)
ax.plot(x, y, color=mixed)
```

---

### `dm.pseudo_alpha(color, alpha=1.0, background='white')`

Return a color with pseudo alpha transparency by mixing with background.

**Parameters:**
- `color` (color): Color to apply pseudo-transparency to.
- `alpha` (float, optional): Alpha value between 0 and 1. Default is 1.0.
- `background` (color, optional): Background color to mix with. Default is 'white'.

**Returns:**
- `tuple`: RGB tuple of the resulting color.

**Example:**
```python
# Create semi-transparent red on white background
transparent_red = dm.pseudo_alpha('dm.red5', alpha=0.3, background='white')
ax.fill_between(x, y1, y2, color=transparent_red)
```

---

## Font Utilities

### `dm.fs(n)`

Return base font size + n.

**Parameters:**
- `n` (int or float): Value to add to base font size.

**Returns:**
- `float`: Base font size + n.

**Example:**
```python
ax.set_title('Title', fontsize=dm.fs(2))    # base + 2
ax.set_xlabel('X label', fontsize=dm.fs(0))  # base size
ax.legend(fontsize=dm.fs(-2))                # base - 2
```

---

### `dm.fw(n)`

Return base font weight + 100 * n. Only works for integer weights and n.

**Parameters:**
- `n` (int): Value to multiply by 100 and add to base font weight.

**Returns:**
- `int`: Base font weight + 100 * n.

**Example:**
```python
ax.set_title('Title', fontweight=dm.fw(1))   # base + 100
ax.set_xlabel('Label', fontweight=dm.fw(-1))  # base - 100
```

---

## Unit Conversion

### `dm.cm2in(cm)`

Convert centimeters to inches.

**Parameters:**
- `cm` (float): Value in centimeters.

**Returns:**
- `float`: Value in inches.

**Example:**
```python
# Create single-column figure (9 cm width)
fig = plt.figure(figsize=(dm.cm2in(9), dm.cm2in(7)))

# Create double-column figure (17 cm width)
fig = plt.figure(figsize=(dm.cm2in(17), dm.cm2in(10)))
```

---

## File I/O

### `dm.save_formats(fig, image_stem, formats=('svg', 'png', 'pdf', 'eps'), bbox_inches=None, **kwargs)`

Save a figure in multiple formats simultaneously.

**Parameters:**
- `fig` (matplotlib.figure.Figure): Figure to save.
- `image_stem` (str): Base filename without extension.
- `formats` (tuple, optional): Tuple of format extensions to save. Default is ('svg', 'png', 'pdf', 'eps').
- `bbox_inches` (str or Bbox, optional): Bounding box in inches. Default is None.
- `**kwargs`: Additional arguments passed to `savefig`.

**Returns:** None

**Example:**
```python
# Save in all 4 formats
dm.save_formats(fig, 'output/figure', dpi=600)
# Creates: figure.svg, figure.png, figure.pdf, figure.eps

# Save only SVG and PNG
dm.save_formats(fig, 'output/figure',
                formats=('svg', 'png'),
                bbox_inches='tight',
                dpi=300)
```

---

### `dm.save_and_show(fig, image_path=None, size=600, unit='pt', **kwargs)`

Save a figure and display it (for Jupyter notebooks).

**Parameters:**
- `fig` (matplotlib.figure.Figure): Figure to save and display.
- `image_path` (str, optional): Path to save the image. If None, uses a temporary file. Default is None.
- `size` (int, optional): Display width in specified units. Default is 600.
- `unit` (str, optional): Unit for size ('pt', 'px', etc.). Default is 'pt'.
- `**kwargs`: Additional arguments passed to `savefig`.

**Returns:** None

**Example:**
```python
# Save to temp file and display
dm.save_and_show(fig, size=600)

# Save to specific path and display
dm.save_and_show(fig, 'output/figure.svg', size=800)
```

---

### `dm.show(image_path, size=600, unit='pt')`

Display an SVG image with specified size (for Jupyter notebooks).

**Parameters:**
- `image_path` (str): Path to the SVG image.
- `size` (int, optional): Desired width in specified units. Default is 600.
- `unit` (str, optional): Unit for size ('pt', 'px', etc.). Default is 'pt'.

**Returns:** None

**Example:**
```python
dm.show('output/figure.svg', size=700)
```

---

## Visualization Tools

### `dm.plot_colormaps(cmap_list=None, ncols=3, group_by_type=True, group_spacing=0.5)`

Plot a list of colormaps in a single figure.

**Parameters:**
- `cmap_list` (list, optional): List of colormap names. If None, shows all available colormaps. Default is None.
- `ncols` (int, optional): Number of columns to display colormaps. Default is 3.
- `group_by_type` (bool, optional): If True, group colormaps by their type. Default is True.
- `group_spacing` (float, optional): Spacing between groups in inches. Default is 0.5.

**Returns:**
- `fig` (matplotlib.figure.Figure): Figure object.
- `axs` (numpy.ndarray): Array of Axes objects.

**Example:**
```python
# Show all colormaps grouped by type
fig, axs = dm.plot_colormaps()
plt.show()

# Show specific colormaps
fig, axs = dm.plot_colormaps(['viridis', 'plasma', 'inferno'], ncols=3)
plt.show()

# Show custom colormaps without grouping
fig, axs = dm.plot_colormaps(cmap_list=['dm.spectral'],
                              group_by_type=False)
plt.show()
```

---

### `dm.plot_colors(colors=None, ncols=4, sort_colors=True)`

Plot a grid of named colors with their names.

**Parameters:**
- `colors` (dict, optional): Dictionary mapping color names to color specifications. If None, uses all dartwork-mpl colors. Default is None.
- `ncols` (int, optional): Number of columns in the color grid. Default is 4.
- `sort_colors` (bool, optional): If True, sorts colors by hue, saturation, and value. Default is True.

**Returns:**
- `fig` (matplotlib.figure.Figure): Figure object.

**Example:**
```python
# Show all dartwork-mpl colors
fig = dm.plot_colors()
plt.show()

# Show custom colors
custom_colors = {'red': '#FF0000', 'green': '#00FF00', 'blue': '#0000FF'}
fig = dm.plot_colors(custom_colors, ncols=3, sort_colors=False)
plt.show()
```

---

### `dm.plot_fonts(font_dir=None, ncols=3, font_size=11)`

Plot available fonts in the specified directory.

**Parameters:**
- `font_dir` (str, optional): Directory path containing font files. If None, defaults to the package's font directory. Default is None.
- `ncols` (int, optional): Number of columns to display font families. Default is 3.
- `font_size` (int, optional): Font size for sample text. Default is 11.

**Returns:**
- `fig` (matplotlib.figure.Figure): Figure object.

**Example:**
```python
# Show all available fonts
fig = dm.plot_fonts()
plt.show()

# Show fonts from custom directory
fig = dm.plot_fonts('/path/to/fonts', ncols=2, font_size=14)
plt.show()
```

---

### `dm.classify_colormap(cmap)`

Classify a colormap into categories.

**Parameters:**
- `cmap` (matplotlib.colors.Colormap): Colormap to classify.

**Returns:**
- `str`: Category of the colormap. One of:
  - "Sequential Single-Hue"
  - "Sequential Multi-Hue"
  - "Diverging"
  - "Cyclical"
  - "Categorical"

**Example:**
```python
import matplotlib.pyplot as plt
import matplotlib.cm as cm

cmap = cm.get_cmap('viridis')
category = dm.classify_colormap(cmap)
print(category)
# 'Sequential Multi-Hue'
```

---

## Internal Utilities

### `dm.set_decimal(ax, xn=None, yn=None)`

Set decimal places for tick labels.

**Parameters:**
- `ax` (matplotlib.axes.Axes): Axes object to modify.
- `xn` (int, optional): Number of decimal places for x-axis tick labels. Default is None.
- `yn` (int, optional): Number of decimal places for y-axis tick labels. Default is None.

**Returns:** None

**Example:**
```python
# Set 2 decimal places for both axes
dm.set_decimal(ax, xn=2, yn=2)

# Set decimal places only for y-axis
dm.set_decimal(ax, yn=3)
```

---

## CLI Tools

### `dmpl` Command

The package provides a command-line interface for managing LLM integration files.

**Commands:**
```bash
# Install .llm.txt file to project root
dmpl install-llm

# Uninstall .llm.txt file from project root
dmpl uninstall-llm
```

These commands help integrate dartwork-mpl documentation with LLM-based coding assistants.

---

## Complete Example

Here's a complete example demonstrating various API features:

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Apply style
dm.style.use_preset('scientific')

# Create data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y1_data = y1 + np.random.normal(0, 0.1, size=len(y1))
y2_data = y2 + np.random.normal(0, 0.1, size=len(y2))

# Create figure with precise sizing
fig = plt.figure(
    figsize=(dm.cm2in(9), dm.cm2in(7)),
    dpi=200
)

# Set up layout
gs = fig.add_gridspec(
    nrows=1, ncols=1,
    left=0.17, right=0.95,
    top=0.95, bottom=0.17
)
ax = fig.add_subplot(gs[0, 0])

# Plot with custom colors
line1, = ax.plot(x, y1, c='dm.red5', lw=0.7)
line2, = ax.plot(x, y2, c='tw.blue:500', lw=0.7)
ax.scatter(x, y1_data, c='dm.red2', s=0.7)
ax.scatter(x, y2_data, c='tw.blue:200', s=0.7)

# Create legend handles
scatter1 = ax.scatter([], [], c='dm.red5', s=10)
scatter2 = ax.scatter([], [], c='tw.blue:500', s=10)

# Customize plot
ax.set_xlabel('Time [hours]')
ax.set_ylabel('Value [kW]')
ax.legend(
    [scatter1, line1, scatter2, line2],
    ['Sin data', 'Sin model', 'Cos data', 'Cos model'],
    loc='upper right',
    fontsize=dm.fs(-1),
    ncol=2
)

# Set ticks
ax.set_xticks([0, 2, 4, 6, 8, 10])
ax.set_yticks([-1, -0.5, 0, 0.5, 1])
ax.set_ylim(-1.2, 1.2)

# Add subplot label
offset = dm.make_offset(4, -4, fig)
ax.text(0, 1, 'a',
        transform=ax.transAxes + offset,
        weight='bold',
        verticalalignment='top')

# Optimize layout
dm.simple_layout(fig)

# Display in Jupyter
dm.save_and_show(fig, size=600)

# Save in multiple formats for publication
dm.save_formats(
    fig,
    'figures/example_figure',
    formats=('svg', 'png', 'pdf', 'eps'),
    bbox_inches='tight',
    dpi=600
)
```

---

## Style Reference

### Individual Styles

- `base`: Base configuration for all styles
- `dmpl`: Default dartwork-mpl style
- `dmpl_light`: Light variant of dmpl style
- `font-scientific`: Small fonts for papers
- `font-investment`: Medium fonts for reports
- `font-presentation`: Large fonts for presentations
- `lang-kr`: Korean language support
- `spine-no`: Remove axis spines
- `spine-yes`: Show axis spines

### Combining Styles

You can combine individual styles for custom configurations:

```python
# Scientific style without spines
dm.style.use(['base', 'font-scientific', 'spine-no'])

# Presentation style with Korean support
dm.style.use(['base', 'font-presentation', 'lang-kr'])
```

---

## Color Reference

### dartwork-mpl Color Naming

Colors follow the pattern `dm.{name}{number}`:
- Names: red, blue, green, yellow, purple, orange, etc.
- Numbers: typically 1-5, where higher numbers are more saturated

**Examples:**
- `dm.red1`, `dm.red2`, `dm.red3`, `dm.red4`, `dm.red5`
- `dm.blue1`, `dm.blue2`, `dm.blue3`, `dm.blue4`, `dm.blue5`

### Tailwind Color Naming

Colors follow the pattern `tw.{color}:{weight}`:
- Common colors: slate, gray, zinc, neutral, stone, red, orange, amber, yellow, lime, green, emerald, teal, cyan, sky, blue, indigo, violet, purple, fuchsia, pink, rose
- Weights: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950

**Examples:**
- `tw.blue:500` - Medium blue
- `tw.gray:200` - Light gray
- `tw.red:700` - Dark red

---

## Best Practices

1. **Use presets**: Start with a preset style that matches your use case
2. **Explicit layout**: Use GridSpec instead of subplots for better control
3. **Use simple_layout**: Replace `tight_layout()` with `dm.simple_layout()`
4. **Handle-based legends**: Create dummy plots for legend handles
5. **Explicit ticks**: Set tick positions explicitly with `set_xticks()` and `set_yticks()`
6. **Check saved output**: Use `save_and_show()` to preview actual saved results
7. **Use cm2in**: Specify figure sizes in cm for publication requirements

---

## Version Information

Current version: 0.1.1

For the latest updates and changelog, visit the [GitHub repository](https://github.com/dartwork-repo/dartwork-mpl).
