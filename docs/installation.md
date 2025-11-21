# Installation

**dartwork-mpl** is a matplotlib wrapper for creating publication-quality figures with ease.

## Quick Install

Install **dartwork-mpl** directly from GitHub. The package includes matplotlib style presets, curated color palettes, and layout utilities.

::::{tab-set}

:::{tab-item} 🚀 uv
:sync: uv

[uv](https://github.com/astral-sh/uv) is a blazingly fast Python package manager written in Rust. It's recommended for modern Python projects.

```bash
# Add to your project dependencies (Recommended)
# This automatically updates your pyproject.toml
uv add git+https://github.com/dartwork-repo/dartwork-mpl

# Or install directly into the current environment
uv pip install git+https://github.com/dartwork-repo/dartwork-mpl

# Install a specific branch or tag
uv add git+https://github.com/dartwork-repo/dartwork-mpl@main
```

> **Why uv?** It's 10-100x faster than pip, handles dependency resolution better, and integrates seamlessly with modern Python workflows.

:::

:::{tab-item} 📦 pip
:sync: pip

Use the standard Python package installer. This works with any Python environment.

```bash
# Install from GitHub
pip install git+https://github.com/dartwork-repo/dartwork-mpl

# Upgrade to the latest version
pip install --upgrade git+https://github.com/dartwork-repo/dartwork-mpl

# Install a specific branch
pip install git+https://github.com/dartwork-repo/dartwork-mpl@main
```

> **Note:** Make sure you have Git installed on your system, as pip needs it to clone the repository.

:::

::::

## Basic Import

Once installed, import **dartwork-mpl** alongside matplotlib. The package is typically imported as `dm` for convenience.

```{code-block} python
:caption: example.py

import dartwork_mpl as dm
import matplotlib.pyplot as plt
import numpy as np

# Apply a style preset (Recommended)
dm.style.use_preset('scientific')  # Optimized for academic papers and publications
```

The `scientific` preset automatically configures:
- **Font sizes** optimized for readability in papers
- **Line widths** and marker sizes suitable for print
- **Color schemes** that work well in both color and grayscale
- **Grid and axis** styling for professional appearance

> **Tip:** You can also try other presets like `'minimal'` or `'poster'` depending on your use case. See the [Usage Guide](DARTWORK_MPL_USAGE_GUIDE.md) for all available presets.

## Verify Installation

After installation, verify that **dartwork-mpl** is properly installed and accessible:

```{code-block} python
:caption: verify.py

import dartwork_mpl as dm

# Check installed version
print(dm.__version__)  # Should print something like '0.1.1'

# List all available style presets
dm.list_styles()  # Shows: ['scientific', 'minimal', 'poster', ...]

# Verify color palettes are available
print(len(dm.colors.PALETTES))  # Should show available color collections
```

If these commands run without errors, you're all set! 🎉

> **Troubleshooting:** If you encounter import errors, make sure:
> - Your Python environment is activated (if using virtual environments)
> - The package was installed in the correct environment
> - You have matplotlib installed as a dependency
