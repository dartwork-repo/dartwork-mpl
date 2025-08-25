from pathlib import Path
from matplotlib import font_manager


def _add_fonts():
    """
    Add custom fonts from the asset directory to matplotlib's font 
    manager.
    
    This function searches for font files in the asset/font directory 
    and registers them with matplotlib's font manager, making them 
    available for use in plots.
    """
    font_dir = [Path(__file__).parent / 'asset/font']
    for font in font_manager.findSystemFonts(font_dir):
        font_manager.fontManager.addfont(font)


_add_fonts()
