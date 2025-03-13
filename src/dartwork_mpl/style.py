import json
from pathlib import Path
import matplotlib.pyplot as plt


def style_path(name):
    """
    Get the path to a style file.
    
    Parameters
    ----------
    name : str
        Name of the style.
        
    Returns
    -------
    Path
        Path to the style file.
        
    Raises
    ------
    ValueError
        If the style is not found.
    """
    path = Path(__file__).parent / f'asset/mplstyle/{name}.mplstyle'
    if not path.exists():
        raise ValueError(f'Not found style: {name}')

    return path


def use_style(name='dmpl'):
    """
    Use a matplotlib style from the package's style library.
    
    Parameters
    ----------
    name : str, optional
        Name of the style to use.
    """
    plt.rcParams.update(plt.rcParamsDefault)
    path = style_path(name)

    plt.style.use(path)    


def list_styles():
    """
    List all available styles.
    
    Returns
    -------
    list
        List of style names.
    """
    path = Path(__file__).parent / 'asset/mplstyle'
    return sorted([p.stem for p in path.glob('*.mplstyle')])


def load_style_dict(name):
    """
    Load key, value pairs from a mplstyle file.
    
    Parameters
    ----------
    name : str
        Name of the style.
        
    Returns
    -------
    dict
        Dictionary of style parameters.
    """
    # Load key, value pair from mplstyle files.
    path = style_path(name)
    with open(path, 'r') as f:
        style_dict = {}
        for line in f:
            if line.strip().startswith('#'):
                continue

            if line.strip() == '':
                continue

            key = line.split(':')[0].strip()
            value = line.split(':')[1].split()[0].strip()

            try:
                value = float(value)
            except ValueError:
                pass

            style_dict[key] = value

    return style_dict
                    

def use_dmpl_style():
    """
    Use the default dmpl style.
    """
    use_style('dmpl')


class Style:
    """
    A class for managing and applying multiple matplotlib styles.
    """
    def __init__(self):
        # Load presets
        self.load_presets()

    @staticmethod
    def presets_path():
        """
        Get the path to the presets file.
        """
        return Path(__file__).parent / 'asset/mplstyle/presets.json'

    def load_presets(self):
        """
        Load presets from a JSON file.
        """
        with open(self.presets_path(), 'r') as f:
            self.presets = json.load(f)

    @staticmethod
    def use(style_names):
        """
        Use multiple styles.
        
        Parameters
        ----------
        style_names : list
            List of style names to use.
        """
        plt.rcParams.update(plt.rcParamsDefault)
        plt.style.use(
            style_path(style_name)
            for style_name in style_names
        )

    def use_preset(self, preset_name):
        """
        Use a preset.
        """
        self.use(self.presets[preset_name])

    def presets_dict(self):
        """
        List all available presets.
        """
        return {k: v for k, v in self.presets.items()}


style = Style() 