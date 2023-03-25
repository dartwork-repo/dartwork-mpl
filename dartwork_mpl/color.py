from pathlib import Path

# Color dictionary.
CD = {}


def _load_color_dict(path):
    color_dict = {}
    with open(path, 'r') as f:
        for line in f.readlines():
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
    color_dict = {}

    root_dir = Path(__file__).parent / 'asset/color'
    for path in root_dir.glob('*.txt'):
        color_dict.update(_load_color_dict(path))

    CD.update(color_dict)


_load_colors()