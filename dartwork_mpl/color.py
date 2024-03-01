from pathlib import Path
import matplotlib.colors as mcolors


def _parse_color_data(path):
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
    print('Load colors...')
    color_dict = {}

    root_dir = Path(__file__).parent / 'asset/color'
    for path in root_dir.glob('*.txt'):
        color_dict.update(_parse_color_data(path))

    # Append prefix to distinguish them from matplotlib colors.
    _color_dict = {f'dm.{k}': v for k, v in color_dict.items()}
    _color_dict.update({f'dartwork_mpl.{k}': v for k, v in color_dict.items()})

    # Add color dict to matplotlib internal color mapping.
    mcolors.get_named_colors_mapping().update(_color_dict)


_load_colors()