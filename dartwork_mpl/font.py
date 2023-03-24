from pathlib import Path
from matplotlib import font_manager


def _add_fonts():
    """Add fonts in asset to matplotlib."""
    font_dir = [Path(__file__).parent / 'asset/font']
    for font in font_manager.findSystemFonts(font_dir):
        font_manager.fontManager.addfont(font)


_add_fonts()
