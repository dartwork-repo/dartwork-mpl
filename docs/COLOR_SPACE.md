# Color Space

dartwork-mpl provides a powerful `Color` class for working with colors in different
color spaces, with a focus on OKLab and OKLCH for perceptually uniform color
operations. This page covers creating Color objects, converting between color
spaces, interpolating colors, and generating custom colormaps.

## Color object

The `Color` class is a unified interface for working with colors across multiple
color spaces. Internally, colors are stored as OKLab coordinates, which enables
efficient and accurate conversions between different color representations.

```python
import dartwork_mpl as dm

# All Color objects are stored internally as OKLab
color = dm.oklab(0.7, 0.1, 0.2)
print(color)  # Color(oklab=(0.7000, 0.1000, 0.2000))
```

## Creating Color objects

You can create Color objects from any supported color space using convenient
wrapper functions or class methods.

### From OKLab coordinates

```python
import dartwork_mpl as dm

# L: lightness (0-1), a, b: color-opponent dimensions
color = dm.oklab(0.7, 0.1, 0.2)
```

### From OKLCH coordinates

```python
import dartwork_mpl as dm

# L: lightness (0-1), C: chroma (>=0), h: hue in degrees (0-360)
color = dm.oklch(0.7, 0.2, 120)  # Greenish color
```

OKLCH uses degrees for hue, making it intuitive to work with (0° = red, 120° = green, 240° = blue).

### From RGB values

```python
import dartwork_mpl as dm

# Automatically detects range: 0-1 or 0-255
color1 = dm.rgb(0.8, 0.2, 0.3)    # 0-1 range
color2 = dm.rgb(200, 50, 75)      # 0-255 range (auto-detected)
```

The `rgb()` function automatically detects whether values are in the 0-1 or 0-255 range.

### From hex strings

```python
import dartwork_mpl as dm

color1 = dm.hex("#ff5733")
color2 = dm.hex("#f73")  # Short format also supported
```

### From matplotlib color names

```python
import dartwork_mpl as dm

# Works with any matplotlib color name
color1 = dm.named("red")
color2 = dm.named("dm.blue5")      # dartwork-mpl colors
color3 = dm.named("tw.blue:500")    # Tailwind colors
```

:::{figure} images/color_space_creation.png
:alt: Examples of creating Color objects from different sources
:width: 100%

**Creating Color objects.** Various ways to initialize Color objects from different
color representations. All methods produce equivalent Color instances that can be
converted to any supported color space.
:::

## Color space conversion

Once you have a Color object, you can convert it to any supported color space
using conversion methods.

```python
import dartwork_mpl as dm

color = dm.hex("#ff5733")

# Convert to different color spaces
L, a, b = color.to_oklab()        # OKLab coordinates
L, C, h = color.to_oklch()         # OKLCH (h in degrees)
r, g, b = color.to_rgb()           # RGB (0-1 range)
hex_str = color.to_hex()           # Hex string
```

### Color space overview

- **OKLab**: A perceptually uniform color space where equal distances correspond
  to equal perceived color differences. Ideal for color operations like blending
  and interpolation.

- **OKLCH**: OKLab in polar coordinates (Lightness, Chroma, Hue). The cylindrical
  representation makes it easy to adjust saturation (chroma) and hue independently
  while maintaining perceptual uniformity.

- **RGB**: The standard red-green-blue color space used by displays and most
  graphics software. Values are in the 0-1 range.

- **Hex**: Web-standard color representation as hexadecimal strings (e.g., `#ff5733`).

:::{figure} images/color_space_conversion.png
:alt: Converting a single color between different color spaces
:width: 100%

**Color space conversion.** A single color represented in different color spaces,
showing how the same color can be expressed in multiple ways.
:::

## Color interpolation with cspace

The `cspace()` function generates smooth color gradients by interpolating between
two colors in a specified color space. This is inspired by `np.linspace` but for
colors.

```python
import dartwork_mpl as dm
import matplotlib.pyplot as plt
import numpy as np

dm.style.use_preset("scientific")

# Interpolate in OKLCH (default, perceptually uniform)
colors_oklch = dm.cspace("#ff5733", "#33ff57", n=10, space="oklch")

# Interpolate in OKLab (perceptually uniform)
colors_oklab = dm.cspace("#ff5733", "#33ff57", n=10, space="oklab")

# Interpolate in RGB
colors_rgb = dm.cspace("#ff5733", "#33ff57", n=10, space="rgb")
```

**Perceptually uniform spaces:** Both OKLCH and OKLab are perceptually uniform
color spaces, meaning equal distances in these spaces correspond to equal
perceived color differences. This makes them ideal for color interpolation,
producing smooth gradients where each step appears equally different to the human
eye. OKLCH (the default) is particularly convenient because its polar coordinate
system makes it easy to adjust saturation and hue independently.

RGB interpolation, in contrast, can produce muddy or uneven transitions,
especially in certain color ranges, because RGB is not perceptually uniform.

The function accepts Color objects or hex strings as input:

```python
import dartwork_mpl as dm

start = dm.named("dm.blue5")
end = dm.hex("#ff5733")
gradient = dm.cspace(start, end, n=20, space="oklch")
```

:::{figure} images/color_space_interpolation.png
:alt: Comparing color interpolation in different color spaces
:width: 100%

**Color interpolation comparison.** The same two colors interpolated in OKLCH,
OKLab, and RGB spaces. OKLCH produces the most perceptually uniform gradient.
:::

## Creating custom colormaps

You can use `cspace()` to generate custom colormaps for matplotlib. This is
especially useful for creating perceptually uniform sequential or diverging
colormaps.

```python
import dartwork_mpl as dm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

dm.style.use_preset("scientific")

# Create a custom sequential colormap
colors = dm.cspace("#1a237e", "#ff6f00", n=256, space="oklch")
cmap = mcolors.ListedColormap([c.to_rgb() for c in colors], name="custom_blue_orange")

# Use it in a plot
fig, ax = plt.subplots(figsize=(dm.cm2in(10), dm.cm2in(6)), dpi=300)
data = np.random.randn(100, 100)
im = ax.imshow(data, cmap=cmap)
plt.colorbar(im, ax=ax, label="Value")
dm.simple_layout(fig)
```

### Diverging colormaps

For diverging colormaps, interpolate from one color through a neutral midpoint
to another color:

```python
import dartwork_mpl as dm
import matplotlib.colors as mcolors

# Diverging: blue -> white -> red
colors1 = dm.cspace("#1a237e", "#ffffff", n=128, space="oklch")
colors2 = dm.cspace("#ffffff", "#c62828", n=128, space="oklch")
colors = colors1[:-1] + colors2  # Remove duplicate white
cmap_div = mcolors.ListedColormap([c.to_rgb() for c in colors], name="custom_diverging")
```

### Registering colormaps

To make your custom colormap available throughout your session:

```python
import matplotlib as mpl

mpl.colormaps.register(cmap=cmap)
# Now you can use it: plt.imshow(data, cmap="custom_blue_orange")
```

:::{figure} images/color_space_colormap.png
:alt: Custom colormaps created using cspace
:width: 100%

**Custom colormaps.** Examples of sequential and diverging colormaps created using
`cspace()` with OKLCH interpolation, applied to sample data.
:::

## Quick reference

```python
import dartwork_mpl as dm

# Create Color objects
color1 = dm.oklab(L, a, b)
color2 = dm.oklch(L, C, h)      # h in degrees
color3 = dm.rgb(r, g, b)        # auto-detects range
color4 = dm.hex("#ff5733")
color5 = dm.named("dm.blue5")

# Convert between spaces
L, a, b = color.to_oklab()
L, C, h = color.to_oklch()      # h in degrees
r, g, b = color.to_rgb()        # 0-1 range
hex_str = color.to_hex()

# Interpolate colors
gradient = dm.cspace(start, end, n=10, space="oklch")  # default
gradient = dm.cspace(start, end, n=10, space="oklab")
gradient = dm.cspace(start, end, n=10, space="rgb")
```

## See also

- [Colors](COLORS) for named color palettes
- [Colormaps](COLORMAPS) for predefined colormap collections
- [Usage Guide](DARTWORK_MPL_USAGE_GUIDE) for general dartwork-mpl patterns

