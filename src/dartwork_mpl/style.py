"""Matplotlib style management utilities.

This module provides functions and classes for managing and applying
matplotlib styles from the package's style library.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt


def style_path(name: str) -> Path:
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
    path: Path = Path(__file__).parent / f"asset/mplstyle/{name}.mplstyle"
    if not path.exists():
        raise ValueError(f"Not found style: {name}")

    return path


def use_style(name: str = "dmpl") -> None:
    """
    Use a matplotlib style from the package's style library.

    Parameters
    ----------
    name : str, optional
        Name of the style to use. Default is "dmpl".
    """
    plt.rcParams.update(plt.rcParamsDefault)
    path: Path = style_path(name)

    plt.style.use(path)


def list_styles() -> list[str]:
    """
    List all available styles.

    Returns
    -------
    list[str]
        List of style names.
    """
    path: Path = Path(__file__).parent / "asset/mplstyle"
    return sorted([p.stem for p in path.glob("*.mplstyle")])


def load_style_dict(name: str) -> dict[str, float | str]:
    """
    Load key, value pairs from a mplstyle file.

    Parameters
    ----------
    name : str
        Name of the style.

    Returns
    -------
    dict[str, float | str]
        Dictionary of style parameters. Values are converted to float
        if possible, otherwise kept as strings.
    """
    # Load key, value pair from mplstyle files.
    path: Path = style_path(name)
    style_dict: dict[str, float | str] = {}
    with open(path, "r") as f:
        for line in f:
            if line.strip().startswith("#"):
                continue

            if line.strip() == "":
                continue

            key: str = line.split(":")[0].strip()
            value: str = line.split(":")[1].split()[0].strip()

            try:
                value_float: float = float(value)
                style_dict[key] = value_float
            except ValueError:
                style_dict[key] = value

    return style_dict


def use_dmpl_style() -> None:
    """
    Use the default dmpl style.

    This is a convenience function that applies the 'dmpl' style,
    which is the default style provided by the dartwork_mpl package.
    """
    use_style("dmpl")


class Style:
    """
    A class for managing and applying multiple matplotlib styles.

    This class provides functionality to load style presets and apply
    multiple styles in sequence.
    """

    def __init__(self) -> None:
        """Initialize Style instance and load presets."""
        self.presets: dict[str, list[str]] = {}
        # Load presets
        self.load_presets()

    @staticmethod
    def presets_path() -> Path:
        """
        Get the path to the presets file.

        Returns
        -------
        Path
            Path to the presets.json file containing style preset
            definitions.
        """
        return Path(__file__).parent / "asset/mplstyle/presets.json"

    def load_presets(self) -> None:
        """
        Load style presets from the JSON file.

        This method reads the presets.json file and stores the preset
        definitions in the instance's presets attribute.
        """
        with open(self.presets_path(), "r") as f:
            self.presets = json.load(f)

    @staticmethod
    def use(style_names: list[str]) -> None:
        """
        Use multiple styles.

        Parameters
        ----------
        style_names : list[str]
            List of style names to use.
        """
        plt.rcParams.update(plt.rcParamsDefault)
        plt.style.use(style_path(style_name) for style_name in style_names)

    def use_preset(self, preset_name: str) -> None:
        """
        Apply a preset style configuration.

        Parameters
        ----------
        preset_name : str
            Name of the preset to apply. Must be a key in the loaded
            presets dictionary.

        Raises
        ------
        KeyError
            If the preset name is not found in the presets dictionary.
        """
        if preset_name not in self.presets:
            raise KeyError(f"Preset '{preset_name}' not found")
        self.use(self.presets[preset_name])

    def presets_dict(self) -> dict[str, list[str]]:
        """
        Get all available presets as a dictionary.

        Returns
        -------
        dict[str, list[str]]
            Dictionary mapping preset names to their style configuration
            lists.
        """
        return {k: v for k, v in self.presets.items()}


style: Style = Style()
