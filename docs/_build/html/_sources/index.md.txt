# dartwork-mpl

**dartwork-mpl** is a matplotlib wrapper for creating publication-quality figures with ease.

## Installation

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast and efficient Python package manager.

```bash
# Add to project (Recommended)
uv add git+https://github.com/dartwork-repo/dartwork-mpl

# Or install directly
uv pip install git+https://github.com/dartwork-repo/dartwork-mpl

# Specify branch/tag
uv add git+https://github.com/dartwork-repo/dartwork-mpl@main
```

### Using pip

```bash
pip install git+https://github.com/dartwork-repo/dartwork-mpl
```

### Basic Import

```python
import dartwork_mpl as dm
import matplotlib.pyplot as plt
import numpy as np

# Apply basic style (Recommended)
dm.style.use_preset('scientific')  # Basic style for academic papers
```

```{toctree}
:maxdepth: 2
:hidden:

DARTWORK_MPL_USAGE_GUIDE
COLOR_GALLERY
gallery/index
api/index
```
