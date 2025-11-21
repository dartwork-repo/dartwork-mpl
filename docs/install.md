# Installation

**dartwork-mpl** is a matplotlib wrapper for creating publication-quality figures with ease.

## Quick Install

::::{tab-set}

:::{tab-item} pip
:sync: pip

```bash
pip install git+https://github.com/dartwork-repo/dartwork-mpl
```

:::

:::{tab-item} uv
:sync: uv

[uv](https://github.com/astral-sh/uv) is a fast and efficient Python package manager.

```bash
# Add to project (Recommended)
uv add git+https://github.com/dartwork-repo/dartwork-mpl

# Or install directly
uv pip install git+https://github.com/dartwork-repo/dartwork-mpl

# Specify branch/tag
uv add git+https://github.com/dartwork-repo/dartwork-mpl@main
```

:::

::::

## Basic Import

```{code-block} python
:caption: example.py

import dartwork_mpl as dm
import matplotlib.pyplot as plt
import numpy as np

# Apply basic style (Recommended)
dm.style.use_preset('scientific')  # Basic style for academic papers
```

## Verify Installation

After installation, verify that everything works:

```{code-block} python
:caption: verify.py

import dartwork_mpl as dm

# Check version
print(dm.__version__)

# List available styles
dm.list_styles()
```
