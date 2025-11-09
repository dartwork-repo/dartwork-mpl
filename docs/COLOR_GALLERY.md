# Color and Colormap Gallery

This document provides visual samples of all available colors and colormaps in dartwork-mpl. These images are generated from `plot_colormaps()` and `plot_colors()` functions.

## Quick Start

dartwork-mpl provides a comprehensive color system with named colors from various design systems and a wide selection of colormaps for data visualization.

### Using Colors

Colors can be used directly in matplotlib plotting functions:

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y, color='tw.blue:500', label='Sine wave')
ax.plot(x, np.cos(x), color='md.red:700', label='Cosine wave')
ax.legend()
plt.show()
```

### Using Colormaps

Colormaps are used with functions that map data values to colors:

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Generate sample data
data = np.random.randn(10, 10)

fig, ax = plt.subplots()
im = ax.imshow(data, cmap='viridis')
plt.colorbar(im)
plt.show()
```

### Reversing Colormaps

Add `_r` suffix to reverse any colormap:

```python
ax.imshow(data, cmap='viridis_r')  # Reversed viridis
```

## Colormaps

Colormaps are organized by type. Each category shows all available colormaps with their names.

### Sequential Single-Hue

Sequential colormaps that use a single hue with varying lightness. Best for representing ordered data that progresses from low to high values.

**When to use:**
- Representing magnitude or intensity (e.g., temperature, density, concentration)
- Data that has a natural ordering from low to high
- When you want a clean, professional appearance

**Example:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Temperature data
x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y) + 2  # Temperature-like data

fig, ax = plt.subplots()
im = ax.contourf(X, Y, Z, levels=20, cmap='Blues')
plt.colorbar(im, label='Temperature')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
```

![Sequential Single-Hue Colormaps](images/colormaps_sequential_single-hue.png)

### Sequential Multi-Hue

Sequential colormaps that use multiple hues. Provide more visual distinction than single-hue colormaps while maintaining the sequential nature.

**When to use:**
- When you need more visual contrast than single-hue colormaps
- Heatmaps and density plots
- Scientific visualizations where color transitions are important
- Popular choices: `viridis`, `plasma`, `inferno`, `magma`

**Example:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Heatmap data
data = np.random.randn(20, 20)
data = np.cumsum(data, axis=0)  # Create smooth variation

fig, ax = plt.subplots()
im = ax.imshow(data, cmap='viridis', aspect='auto')
plt.colorbar(im, label='Value')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
```

![Sequential Multi-Hue Colormaps](images/colormaps_sequential_multi-hue.png)

### Diverging

Diverging colormaps that have distinct middle values and different colors at the ends. Ideal for data centered around a meaningful zero point or threshold.

**When to use:**
- Data with a meaningful zero point (e.g., deviations from mean, temperature anomalies)
- Correlation matrices
- Data that diverges from a central value
- When you need to highlight both positive and negative values

**Example:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Anomaly data centered around zero
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)  # Centered around zero

fig, ax = plt.subplots()
im = ax.contourf(X, Y, Z, levels=20, cmap='RdBu_r')
plt.colorbar(im, label='Anomaly')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
```

![Diverging Colormaps](images/colormaps_diverging.png)

### Cyclical

Cyclical colormaps that start and end with similar colors, suitable for periodic data where the highest and lowest values should appear similar.

**When to use:**
- Periodic or circular data (e.g., angles, time of day, phase data)
- Data where the endpoints are conceptually connected
- Wind direction, wave phase, or any circular measurement

**Example:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Phase data (0 to 2π)
theta = np.linspace(0, 2*np.pi, 100)
r = np.linspace(0, 5, 50)
R, Theta = np.meshgrid(r, theta)
Z = np.sin(Theta)  # Periodic data

fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
im = ax.contourf(Theta, R, Z, levels=20, cmap='hsv')
plt.colorbar(im, label='Phase')
plt.show()
```

![Cyclical Colormaps](images/colormaps_cyclical.png)

### Categorical

Categorical colormaps with distinct colors for different categories. Use when you need to distinguish between discrete, unordered groups.

**When to use:**
- Discrete categories without inherent ordering
- Classifying data into distinct groups
- Bar charts, pie charts, or scatter plots with categories
- When each category should be visually distinct

**Example:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Categorical data
categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]
colors = plt.cm.get_cmap('Set2')(np.linspace(0, 1, len(categories)))

fig, ax = plt.subplots()
bars = ax.bar(categories, values, color=colors)
ax.set_xlabel('Category')
ax.set_ylabel('Value')
plt.show()
```

![Categorical Colormaps](images/colormaps_categorical.png)

## Colors

Colors are organized by library. Each library shows all available named colors with their names.

### OpenColor

OpenColor color palette. A carefully designed color system for user interfaces.

**Usage:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color='dm.gray9', label='Gray9')
ax.plot(x, np.cos(x), color='dm.red9', label='Red9')
ax.legend()
plt.show()
```

**Available colors:** Use `dm.plot_colors()` to see all available OpenColor colors.

![OpenColor Colors](images/colors_opencolor.png)

### Tailwind (tw)

Tailwind CSS color palette. Colors are named with the format `tw.{color}:{weight}` (e.g., `tw.blue:500`).

**Usage:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color='tw.blue:500', label='Blue 500')
ax.plot(x, np.cos(x), color='tw.red:600', label='Red 600')
ax.fill_between(x, 0, np.sin(x), color='tw.gray:100', alpha=0.3)
ax.legend()
plt.show()
```

**Available colors:**
- Colors: blue, gray, red, green, yellow, purple, pink, indigo, cyan, teal, emerald, lime, amber, orange, slate, zinc, neutral, stone, etc.
- Weights: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950

![Tailwind Colors](images/colors_tw.png)

### Material Design (md)

Material Design color palette. Colors are named with the format `md.{color}:{weight}` (e.g., `md.blue:500`).

**Usage:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color='md.blue:500', linewidth=2, label='Blue 500')
ax.plot(x, np.cos(x), color='md.red:700', linewidth=2, label='Red 700')
ax.scatter(x[::10], np.sin(x[::10]), color='md.green:600', s=50, zorder=5)
ax.legend()
plt.show()
```

**Available colors:**
- Colors: red, pink, purple, deep purple, indigo, blue, light blue, cyan, teal, green, light green, lime, yellow, amber, orange, deep orange, brown, grey, blue grey
- Weights: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900

![Material Design Colors](images/colors_md.png)

### Ant Design (ant)

Ant Design color palette. Colors are named with the format `ant.{color}:{weight}` (e.g., `ant.blue:5`).

**Usage:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color='ant.blue:5', label='Blue 5')
ax.plot(x, np.cos(x), color='ant.red:6', label='Red 6')
ax.fill_between(x, np.sin(x), np.cos(x), color='ant.green:4', alpha=0.3)
ax.legend()
plt.show()
```

**Available colors:**
- Colors: red, volcano, orange, gold, yellow, lime, green, cyan, blue, geek blue, purple, magenta, grey
- Weights: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

![Ant Design Colors](images/colors_ant.png)

### Chakra UI (chakra)

Chakra UI color palette. Colors are named with the format `chakra.{color}:{weight}` (e.g., `chakra.blue:500`).

**Usage:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color='chakra.blue:500', label='Blue 500')
ax.plot(x, np.cos(x), color='chakra.red:600', label='Red 600')
ax.scatter(x[::10], np.sin(x[::10]), color='chakra.purple:500', s=50)
ax.legend()
plt.show()
```

**Available colors:**
- Colors: red, orange, yellow, green, teal, blue, cyan, purple, pink, gray
- Weights: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900

![Chakra UI Colors](images/colors_chakra.png)

### Primer (primer)

Primer color palette. Colors are named with the format `primer.{color}:{weight}` (e.g., `primer.blue:5`).

**Usage:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color='primer.blue:5', label='Blue 5')
ax.plot(x, np.cos(x), color='primer.red:6', label='Red 6')
ax.fill_between(x, -1, 1, color='primer.gray:1', alpha=0.1)
ax.legend()
plt.show()
```

**Available colors:**
- Colors: blue, green, yellow, orange, red, purple, pink, coral, gray
- Weights: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

![Primer Colors](images/colors_primer.png)

### Other Colors

Other named colors from matplotlib and dartwork-mpl. Includes standard matplotlib colors and custom dartwork-mpl colors.

**Usage:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color='C0', label='C0')
ax.plot(x, np.cos(x), color='C1', label='C1')
ax.plot(x, np.tan(x/2), color='C2', label='C2')
ax.legend()
plt.show()
```

**Note:** Standard matplotlib color cycle colors (C0, C1, C2, etc.) and other named colors are available.

![Other Colors](images/colors_other.png)

### XKCD Colors

XKCD color survey colors. These are named colors from the XKCD color survey, providing a wide range of intuitive color names.

**Usage:**
```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color='xkcd:sky blue', label='Sky Blue')
ax.plot(x, np.cos(x), color='xkcd:tomato', label='Tomato')
ax.plot(x, np.sin(x)*np.cos(x), color='xkcd:mint green', label='Mint Green')
ax.legend()
plt.show()
```

**Note:** XKCD colors use the `xkcd:` prefix. Use `dm.plot_colors()` to see all available XKCD color names.

![XKCD Colors](images/colors_xkcd.png)

## Best Practices

### Choosing Colormaps

1. **Sequential vs Diverging**
   - Use **sequential** colormaps for data that progresses from low to high (e.g., temperature, density, counts)
   - Use **diverging** colormaps for data centered around a meaningful zero point (e.g., deviations, anomalies, correlations)
   - Use **categorical** colormaps for discrete, unordered categories

2. **Color Accessibility**
   - Avoid using color as the only way to convey information
   - Use colorblind-friendly colormaps (e.g., `viridis`, `plasma`, `inferno`) for scientific publications
   - Test your visualizations with colorblind simulators if possible
   - Consider using patterns or textures in addition to color for accessibility

3. **Perceptual Uniformity**
   - Prefer perceptually uniform colormaps (e.g., `viridis`, `plasma`, `inferno`, `magma`) over traditional ones like `jet`
   - Perceptually uniform colormaps ensure that equal steps in data correspond to equal steps in perceived color change

4. **Reversing Colormaps**
   - Use the `_r` suffix to reverse any colormap when needed
   - Sometimes reversing a colormap can better match your data or improve readability

### Choosing Colors

1. **Color Weights**
   - Lower weights (50-300) are lighter colors, suitable for backgrounds or subtle elements
   - Middle weights (400-600) are balanced colors, good for primary elements
   - Higher weights (700-900) are darker colors, suitable for text or emphasis

2. **Consistency**
   - Stick to one color library within a single visualization for consistency
   - Use similar weights for similar elements (e.g., all primary lines use weight 500-600)

3. **Contrast**
   - Ensure sufficient contrast between foreground and background colors
   - Use darker colors for text and lighter colors for backgrounds

4. **Mixing Colors**
   - Use `dm.mix_colors()` to create custom colors by blending existing ones
   - Useful for creating gradients or intermediate shades

## Common Patterns

### Multi-line Plot with Different Colors

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()

# Use different colors from the same library for consistency
colors = ['tw.blue:500', 'tw.red:500', 'tw.green:500', 'tw.purple:500']
labels = ['Series A', 'Series B', 'Series C', 'Series D']

for i, (color, label) in enumerate(zip(colors, labels)):
    y = np.sin(x + i * np.pi / 4)
    ax.plot(x, y, color=color, label=label, linewidth=2)

ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
```

### Heatmap with Appropriate Colormap

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Generate correlation-like data
data = np.random.randn(10, 10)
data = np.corrcoef(data)

fig, ax = plt.subplots()
im = ax.imshow(data, cmap='RdBu_r', vmin=-1, vmax=1)
plt.colorbar(im, label='Correlation')
ax.set_xlabel('Variable')
ax.set_ylabel('Variable')
plt.show()
```

### Scatter Plot with Color Mapping

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Generate data
x = np.random.randn(100)
y = np.random.randn(100)
colors_data = np.random.randn(100)  # Color by this value

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=colors_data, cmap='viridis', s=50, alpha=0.6)
plt.colorbar(scatter, label='Value')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
```

### Categorical Plot with Distinct Colors

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

categories = ['Category A', 'Category B', 'Category C', 'Category D']
values = [23, 45, 56, 78]

# Use categorical colormap
cmap = plt.cm.get_cmap('Set2')
colors = [cmap(i) for i in np.linspace(0, 1, len(categories))]

fig, ax = plt.subplots()
bars = ax.bar(categories, values, color=colors)
ax.set_xlabel('Category')
ax.set_ylabel('Value')
plt.show()
```

### Filled Area with Custom Colors

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots()
ax.fill_between(x, y1, y2, color='tw.blue:200', alpha=0.3, label='Between')
ax.plot(x, y1, color='tw.blue:600', linewidth=2, label='Sin')
ax.plot(x, y2, color='tw.red:600', linewidth=2, label='Cos')
ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
```

### Mixing Colors for Custom Shades

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

x = np.linspace(0, 10, 100)

# Mix two colors
mixed_color = dm.mix_colors('tw.blue:500', 'tw.red:500', alpha=0.7)

fig, ax = plt.subplots()
ax.plot(x, np.sin(x), color=mixed_color, linewidth=2, label='Mixed Color')
ax.plot(x, np.cos(x), color='tw.blue:500', linewidth=2, label='Blue', alpha=0.5)
ax.plot(x, -np.cos(x), color='tw.red:500', linewidth=2, label='Red', alpha=0.5)
ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
```

## Regenerating Images

To regenerate these images, run the `generate_gallery.py` script:

```bash
python docs/generate_gallery.py
```

The script will generate PNG images in the `docs/images/` directory. Make sure you have dartwork-mpl installed and all dependencies are available.

