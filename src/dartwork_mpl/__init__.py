import matplotlib.pyplot as plt

from pathlib import Path

__version__ = "0.1.0"

from .font import *
from .color import *
from .color import Color, cspace, oklab, oklch, rgb, hex, named
from .cmap import *
from .util import *
from .constant import *

from .style import (
    use_style,
    style_path,
    list_styles,
    load_style_dict,
    use_dmpl_style,
    Style,
    style,
)

from .install import (
    install_llm_txt,
    uninstall_llm_txt,
)

# use_dmpl_style()
use_style('dmpl_light')