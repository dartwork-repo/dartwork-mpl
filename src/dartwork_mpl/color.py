import json
from pathlib import Path
import matplotlib.colors as mcolors


def _parse_color_data(path):
    """
    Parse color data from a text file.
    
    Parameters
    ----------
    path : str or Path
        Path to the color data file. Each line should contain a 
        color name and value separated by a colon.
        
    Returns
    -------
    dict
        Dictionary mapping color names to color values.
    """
    color_dict = {}
    with open(path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Neglect comment line.
        if line.startswith('#'):
            continue

        # Neglect empty line.
        if not line.strip():
            continue

        k, v = line.split(':')
        color_dict[k.strip()] = v.strip()

    return color_dict


def _load_colors():
    """
    Load all color definitions from asset files and register them with 
    matplotlib.
    
    This function loads colors from text files and JSON files in the 
    asset/color directory. It adds 'dm.' and 'dartwork_mpl.' prefixes 
    to distinguish them from matplotlib's built-in colors. 
    
    Tailwind CSS colors are loaded with 'tailwind.' and 'tw.' prefixes,
    followed by the color name and weight (e.g., 'tw.blue:500', 
    'tailwind.gray:200'). Weights range from 50 to 950 in increments 
    of 50 or 100.
    """
    print('Load colors...')
    color_dict = {}

    root_dir = Path(__file__).parent / 'asset/color'
    for path in root_dir.glob('*.txt'):
        color_dict.update(_parse_color_data(path))

    # Append prefix to distinguish them from matplotlib colors.
    _color_dict = {f'dm.{k}': v for k, v in color_dict.items()}
    _color_dict.update({f'dartwork_mpl.{k}': v for k, v in color_dict.items()})

    # Tailwind colors.
    with open(root_dir / 'tailwind_colors.json', 'r') as f:
        tailwind_colors = json.load(f)

    for k, v in tailwind_colors.items():
        k = k.lower()
        for weight, hex in v:
            _color_dict[f'tailwind.{k}:{weight}'] = f'#{hex}'
            _color_dict[f'tw.{k}:{weight}'] = f'#{hex}'

    # Add color dict to matplotlib internal color mapping.
    mcolors.get_named_colors_mapping().update(_color_dict)


_load_colors()