"""dartwork-mpl: Enhanced matplotlib styling and color utilities.

This package provides enhanced styling, color management, and utility
functions for matplotlib visualizations.
"""

__version__ = "0.1.0"

# Import font module to register fonts (no public exports)
from . import font  # noqa: F401

# Import color module exports
from .color import (
    Color,
    cspace,
    hex,
    named,
    oklab,
    oklch,
    rgb,
)

# Import cmap module to register colormaps (no public exports)
from . import cmap  # noqa: F401

# Import util module exports
from .util import *  # noqa: F403

# Import asset_viz module exports
from .asset_viz import *  # noqa: F403

# Import constant module exports
from .constant import DW, SW

# Import style module exports
from .style import (
    Style,
    list_styles,
    load_style_dict,
    style,
    style_path,
)

# Import install module exports
from .install import (
    install_llm_txt,
    uninstall_llm_txt,
)

# Define __all__ for explicit exports
__all__ = [
    # Color module
    "Color",
    "cspace",
    "hex",
    "named",
    "oklab",
    "oklch",
    "rgb",
    # Constant module
    "DW",
    "SW",
    # Style module
    "Style",
    "list_styles",
    "load_style_dict",
    "style",
    "style_path",
    # Install module
    "install_llm_txt",
    "uninstall_llm_txt",
]
