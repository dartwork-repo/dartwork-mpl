from pathlib import Path
import matplotlib as mpl
import matplotlib.colors as mcolors


def _parse_colormap(path):
    path = Path(path)

    colors = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            color = [float(v) for v in line.split()]
            colors.append(color)

    return mcolors.ListedColormap(colors, name=f'dm.{path.stem}')


def _load_colormaps():
    print('Load colormaps...')
    root_dir = Path(__file__).parent / 'asset/cmap'
    for path in root_dir.glob('*.txt'):
        cmap = _parse_colormap(path)
        mpl.colormaps.register(cmap=cmap)


_load_colormaps()