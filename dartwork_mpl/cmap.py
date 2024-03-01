from pathlib import Path
import matplotlib as mpl
import matplotlib.colors as mcolors


def _parse_colormap(path, reverse=False):
    path = Path(path)

    colors = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            color = [float(v) for v in line.split()]
            colors.append(color)

    if reverse:
        colors = colors[::-1]
        name=f'dm.{path.stem}_r'
    else:
        name=f'dm.{path.stem}'

    return mcolors.ListedColormap(colors, name=name)


def _load_colormaps():
    print('Load colormaps...')
    root_dir = Path(__file__).parent / 'asset/cmap'
    for path in root_dir.glob('*.txt'):
        cmap = _parse_colormap(path)
        mpl.colormaps.register(cmap=cmap)

        cmap_r = _parse_colormap(path, reverse=True)
        mpl.colormaps.register(cmap=cmap_r)


_load_colormaps()