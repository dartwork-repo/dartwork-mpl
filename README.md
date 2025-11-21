# dartwork-mpl: matplotlib utilities and assets library engineered by dartwork

`dartwork-mpl` is a sophisticated utility collection designed to elevate `matplotlib` visuals to publication-level elegance with added convenience features. It is being developed to resolve personal inconveniences in visualization using matplotlib and to provide more intuitive customization especially to beginners.
<br/>

## Features

`dartwork-mpl` enriches plotting experience with:

- **Enhanced Aesthetics**: Apply our curated themes to make your charts visually appealing.
- **Easy Customization**: Effortlessly adjust plot styles to fit your publication's needs.
- **Advanced Color System**: Use custom colors with simple prefixes (`dm.`, `tw.`) and extended Tailwind CSS palette.
- **Streamlined Workflow**: Simplify your plotting code with our intuitive interface, saving time and reducing complexity.
- **Publication-Ready Layout**: Automatic layout optimization with `simple_layout()` for professional results.
<br/>


## Getting Started

### Installation

#### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. To install `dartwork-mpl` with uv:

```shell
# Add to your project
uv add git+https://github.com/dartwork-repo/dartwork-mpl

# Or install directly
uv pip install git+https://github.com/dartwork-repo/dartwork-mpl
```

#### Using pip

```shell
pip install git+https://github.com/dartwork-repo/dartwork-mpl
```

### Quick Start

After installation, import and apply a style preset:

```python
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Apply scientific publication style
dm.style.use_preset('scientific')

# For Korean text support
dm.style.use_preset('scientific-kr')
```
<br/>


## Core Features

### Style Management
- **Preset Styles**: Ready-to-use presets for scientific papers, presentations, and reports
- **Flexible Customization**: Combine individual styles for fine-grained control
- **Korean Language Support**: Built-in Korean font support with `-kr` presets

### Color System
- **dartwork-mpl Colors**: Custom color palette with `dm.red5`, `dm.blue2`, etc.
- **Tailwind CSS Integration**: Full Tailwind palette with `tw.blue:500`, `tailwind.gray:200`, etc.
- **Color Utilities**: Mix colors and apply pseudo-transparency

### Layout & Utilities
- **Smart Layout Optimization**: `simple_layout()` replaces `tight_layout()` with better control
- **Unit Conversion**: `cm2in()` for precise figure sizing
- **Multi-format Export**: Save figures in SVG, PNG, PDF, and EPS simultaneously
- **Font Utilities**: Relative font size (`fs()`) and weight (`fw()`) adjustments

### Visualization Tools
- **Colormap Explorer**: Preview and classify colormaps by type
- **Color Palette Viewer**: Display all available colors with names
- **Font Gallery**: Preview available fonts

<br/>


## Example Usage

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Set style
dm.style.use_preset('scientific')

# Create figure with precise sizing (single-column paper figure)
fig = plt.figure(figsize=(dm.cm2in(9), dm.cm2in(7)), dpi=200)

# Set up layout
gs = fig.add_gridspec(nrows=1, ncols=1,
                      left=0.17, right=0.95,
                      top=0.95, bottom=0.17)
ax = fig.add_subplot(gs[0, 0])

# Plot with custom colors
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), c='dm.red5', lw=0.7, label='Sin')
ax.plot(x, np.cos(x), c='tw.blue:500', lw=0.7, label='Cos')

# Customize
ax.set_xlabel('X value')
ax.set_ylabel('Y value')
ax.legend(fontsize=dm.fs(-1))

# Optimize layout and save
dm.simple_layout(fig)
dm.save_and_show(fig)  # Display in Jupyter

# Export in multiple formats
dm.save_formats(fig, 'output/figure',
                formats=('svg', 'png', 'pdf', 'eps'),
                dpi=600)
```

<br/>


## Documentation

📚 **[Full Documentation](https://dartwork-repo.github.io/dartwork-mpl/)** - Complete Sphinx documentation with:
- **[Usage Guide](https://dartwork-repo.github.io/dartwork-mpl/DARTWORK_MPL_USAGE_GUIDE.html)** - Comprehensive guide to all features
- **[Example Gallery](https://dartwork-repo.github.io/dartwork-mpl/gallery/index.html)** - Interactive examples with code and plots
- **[Color System](https://dartwork-repo.github.io/dartwork-mpl/COLOR_SYSTEM.html)** - Full-width Colors and Colormaps reference
- **[API Reference](https://dartwork-repo.github.io/dartwork-mpl/API_REFERENCE.html)** - Detailed API documentation

<br/>


## Example Gallery

Explore our comprehensive [example gallery](https://dartwork-repo.github.io/dartwork-mpl/gallery/index.html) featuring:

- **Basic Usage** - Getting started with dartwork-mpl
- **Color System** - Custom colors and Tailwind CSS integration
- **Layout Optimization** - Advanced layout control with `simple_layout()`
- **Scientific Figures** - Multi-panel publication-ready plots
- **Statistical Plots** - Probability density, violin, and box plots
- **Advanced Visualizations** - Heatmaps, contours, streamplots, and 3D plots

Each example includes complete source code and rendered output.

<br/>


## Available Presets

| Preset | Description |
|--------|-------------|
| `scientific` | Small fonts for academic papers |
| `presentation` | Large fonts for presentations |
| `investment` | Style for investment reports |
| `scientific-kr` | Scientific style with Korean support |
| `presentation-kr` | Presentation style with Korean support |
| `investment-kr` | Investment style with Korean support |

<br/>


## Reporting Issues
Encountered a bug or have a feature request? Please open an issue through our [GitHub issue tracker](https://github.com/dartwork-repo/dartwork-mpl/issues). We appreciate your feedback and contributions.
