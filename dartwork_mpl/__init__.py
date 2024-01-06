import matplotlib.pyplot as plt

from pathlib import Path

from .font import *
from .color import *
from .util import *
from .constant import *

plt.style.use(Path(__file__).parent / 'paper.mplstyle')