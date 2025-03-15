import matplotlib.pyplot as plt

from pathlib import Path

from .font import *
from .color import *
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
# use_dmpl_style()
use_style('dmpl_light')