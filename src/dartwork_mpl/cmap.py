from pathlib import Path
import matplotlib as mpl
import matplotlib.colors as mcolors


def _parse_colormap(path, reverse=False):
    """
    Parse a colormap from a text file and create a matplotlib 
    ListedColormap.
    
    Parameters
    ----------
    path : str or Path
        Path to the colormap text file containing RGB values.
    reverse : bool, optional
        If True, reverse the colormap order. Default is False.
        
    Returns
    -------
    matplotlib.colors.ListedColormap
        A ListedColormap object with the parsed colors.
        The colormap name will be 'dm.{filename}' or 'dm.{filename}_r' 
        if reversed.
    """
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
    """
    Load all colormap files from the asset/cmap directory and register 
    them with matplotlib.
    
    This function automatically discovers all .txt files in the 
    asset/cmap directory, parses them as colormaps, and registers both 
    normal and reversed versions with matplotlib's colormap registry.
    """
    root_dir = Path(__file__).parent / 'asset/cmap'
    for path in root_dir.glob('*.txt'):
        cmap = _parse_colormap(path)
        mpl.colormaps.register(cmap=cmap)

        cmap_r = _parse_colormap(path, reverse=True)
        mpl.colormaps.register(cmap=cmap_r)


_load_colormaps()
