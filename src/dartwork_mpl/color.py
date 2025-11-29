"""Color management and conversion utilities for matplotlib.

This module provides color loading, registration, and conversion
functionality including support for OKLab, OKLCH, RGB, and hex color
spaces.
"""

import json
import math
from pathlib import Path

import matplotlib.colors as mcolors
import numpy as np


def _parse_color_data(path: str | Path) -> dict[str, str]:
    """
    Parse color data from a text file.

    Parameters
    ----------
    path : str or Path
        Path to the color data file. Each line should contain a
        color name and value separated by a colon.

    Returns
    -------
    dict[str, str]
        Dictionary mapping color names to color values.
    """
    color_dict: dict[str, str] = {}
    with open(path, "r") as f:
        lines: list[str] = f.readlines()

    for line in lines:
        # Neglect comment line.
        if line.startswith("#"):
            continue

        # Neglect empty line.
        if not line.strip():
            continue

        k: str
        v: str
        k, v = line.split(":")
        color_dict[k.strip()] = v.strip()

    return color_dict


def _load_colors() -> None:
    """
    Load all color definitions from asset files and register them.

    This function loads colors from text files and JSON files in the
    asset/color directory. It adds 'oc.' prefix
    to distinguish them from matplotlib's built-in colors.

    Tailwind CSS colors are loaded with 'tw.' prefix,
    followed by the color name and weight (e.g., 'tw.blue500',
    'tw.gray200'). Weights range from 50 to 950 in increments
    of 50 or 100.

    Material Design colors are loaded with 'md.' prefix
    (e.g., 'md.blue500', 'md.red700'). Weights range from 50 to 900.

    Ant Design colors are loaded with 'ad.' prefix
    (e.g., 'ad.blue5', 'ad.red6'). Weights range from 1 to 10.

    Chakra UI colors are loaded with 'cu.' prefix
    (e.g., 'cu.blue500', 'cu.red600'). Weights range from
    50 to 900.

    Primer colors are loaded with 'pr.' prefix
    (e.g., 'pr.blue5', 'pr.red6'). Weights range from 0 to 9.

    Notes
    -----
    This function is automatically called when the module is imported.
    """
    color_dict: dict[str, str] = {}

    root_dir: Path = Path(__file__).parent / "asset/color"
    for path in root_dir.glob("*.txt"):
        color_dict.update(_parse_color_data(path))

    # Append prefix to distinguish them from matplotlib colors.
    _color_dict: dict[str, str] = {f"oc.{k}": v for k, v in color_dict.items()}

    # Tailwind colors.
    with open(root_dir / "tailwind_colors.json", "r") as f:
        tailwind_colors: dict[str, list[tuple[int, str]]] = json.load(f)

    for k, v in tailwind_colors.items():
        k_lower: str = k.lower().replace(" ", "")
        for weight, hex_val in v:
            # Only use 'tw.' prefix, skip 'tw.' prefix since they
            # are identical
            _color_dict[f"tw.{k_lower}{weight}"] = f"#{hex_val}"

    # Material Design colors.
    with open(root_dir / "material_colors.json", "r") as f:
        material_colors: dict[str, list[tuple[int, str]]] = json.load(f)

    for k, v in material_colors.items():
        # Remove spaces (e.g., "Deep Purple" -> "deeppurple")
        k_lower: str = k.lower().replace(" ", "")
        for weight, hex_val in v:
            _color_dict[f"md.{k_lower}{weight}"] = f"#{hex_val}"

    # Ant Design colors.
    with open(root_dir / "ant_colors.json", "r") as f:
        ant_colors: dict[str, list[tuple[int, str]]] = json.load(f)

    for k, v in ant_colors.items():
        k_lower: str = k.lower().replace(" ", "")
        for weight, hex_val in v:
            _color_dict[f"ad.{k_lower}{weight}"] = f"#{hex_val}"

    # Chakra UI colors.
    with open(root_dir / "chakra_colors.json", "r") as f:
        chakra_colors: dict[str, list[tuple[int, str]]] = json.load(f)

    for k, v in chakra_colors.items():
        k_lower: str = k.lower().replace(" ", "")
        for weight, hex_val in v:
            _color_dict[f"cu.{k_lower}{weight}"] = f"#{hex_val}"

    # Primer colors.
    with open(root_dir / "primer_colors.json", "r") as f:
        primer_colors: dict[str, list[tuple[int, str]]] = json.load(f)

    for k, v in primer_colors.items():
        k_lower: str = k.lower().replace(" ", "")
        for weight, hex_val in v:
            _color_dict[f"pr.{k_lower}{weight}"] = f"#{hex_val}"

    # Add color dict to matplotlib internal color mapping.
    mcolors.get_named_colors_mapping().update(_color_dict)

    # Remove xkcd colors from matplotlib's color mapping since we don't
    # use them and they clutter the 'other' category in color galleries.
    color_mapping: dict[str, str] = mcolors.get_named_colors_mapping()
    xkcd_keys: list[str] = [
        k for k in list(color_mapping.keys()) if k.startswith("xkcd:")
    ]
    for key in xkcd_keys:
        del color_mapping[key]


_load_colors()


# ============================================================================
# Color Conversion Functions
# ============================================================================


def _srgb_to_linear(c: float | np.ndarray) -> float | np.ndarray:
    """
    Convert sRGB to linear RGB (gamma decoding).

    Parameters
    ----------
    c : float or array
        sRGB value(s) in range [0, 1].

    Returns
    -------
    float or array
        Linear RGB value(s) in range [0, 1].
    """
    c_arr: np.ndarray = np.asarray(c)
    mask: np.ndarray = c_arr <= 0.04045
    return np.where(mask, c_arr / 12.92, ((c_arr + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(c: float | np.ndarray) -> float | np.ndarray:
    """
    Convert linear RGB to sRGB (gamma encoding).

    Parameters
    ----------
    c : float or array
        Linear RGB value(s) in range [0, 1].

    Returns
    -------
    float or array
        sRGB value(s) in range [0, 1].
    """
    c_arr: np.ndarray = np.asarray(c)
    mask: np.ndarray = c_arr <= 0.0031308
    return np.where(mask, 12.92 * c_arr, 1.055 * (c_arr ** (1.0 / 2.4)) - 0.055)


def _linear_srgb_to_oklab(r: float, g: float, b: float) -> tuple[float, float, float]:
    """
    Convert linear sRGB to OKLab.

    Based on the C++ implementation provided.

    Parameters
    ----------
    r, g, b : float
        Linear RGB values in range [0, 1].

    Returns
    -------
    tuple[float, float, float]
        (L, a, b) OKLab coordinates.
    """
    # Matrix multiplication to LMS
    lms_l: float = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    lms_m: float = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    lms_s: float = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    # Cube root
    lms_l_cbrt: float = np.cbrt(lms_l)
    lms_m_cbrt: float = np.cbrt(lms_m)
    lms_s_cbrt: float = np.cbrt(lms_s)

    # Matrix multiplication to OKLab
    L: float = (
        0.2104542553 * lms_l_cbrt
        + 0.7936177850 * lms_m_cbrt
        - 0.0040720468 * lms_s_cbrt
    )
    a: float = (
        1.9779984951 * lms_l_cbrt
        - 2.4285922050 * lms_m_cbrt
        + 0.4505937099 * lms_s_cbrt
    )
    b_val: float = (
        0.0259040371 * lms_l_cbrt
        + 0.7827717662 * lms_m_cbrt
        - 0.8086757660 * lms_s_cbrt
    )

    return (L, a, b_val)


def _oklab_to_linear_srgb(L: float, a: float, b: float) -> tuple[float, float, float]:
    """
    Convert OKLab to linear sRGB.

    Based on the C++ implementation provided.

    Parameters
    ----------
    L, a, b : float
        OKLab coordinates.

    Returns
    -------
    tuple[float, float, float]
        (r, g, b) linear RGB values in range [0, 1].
    """
    # Matrix multiplication to LMS
    lms_l_cbrt: float = L + 0.3963377774 * a + 0.2158037573 * b
    lms_m_cbrt: float = L - 0.1055613458 * a - 0.0638541728 * b
    lms_s_cbrt: float = L - 0.0894841775 * a - 1.2914855480 * b

    # Cube
    lms_l: float = lms_l_cbrt * lms_l_cbrt * lms_l_cbrt
    lms_m: float = lms_m_cbrt * lms_m_cbrt * lms_m_cbrt
    lms_s: float = lms_s_cbrt * lms_s_cbrt * lms_s_cbrt

    # Matrix multiplication to linear RGB
    r: float = +4.0767416621 * lms_l - 3.3077115913 * lms_m + 0.2309699292 * lms_s
    g: float = -1.2684380046 * lms_l + 2.6097574011 * lms_m - 0.3413193965 * lms_s
    b_val: float = -0.0041960863 * lms_l - 0.7034186147 * lms_m + 1.7076147010 * lms_s

    return (r, g, b_val)


def _oklab_to_oklch(L: float, a: float, b: float) -> tuple[float, float, float]:
    """
    Convert OKLab to OKLCH.

    Parameters
    ----------
    L, a, b : float
        OKLab coordinates.

    Returns
    -------
    tuple[float, float, float]
        (L, C, h) OKLCH coordinates, where h is in radians.
    """
    C: float = math.sqrt(a * a + b * b)
    h: float = math.atan2(b, a)
    return (L, C, h)


def _oklch_to_oklab(L: float, C: float, h: float) -> tuple[float, float, float]:
    """
    Convert OKLCH to OKLab.

    Parameters
    ----------
    L, C : float
        Lightness and Chroma.
    h : float
        Hue in radians.

    Returns
    -------
    tuple[float, float, float]
        (L, a, b) OKLab coordinates.
    """
    a: float = C * math.cos(h)
    b: float = C * math.sin(h)
    return (L, a, b)


def _parse_hex(hex_str: str) -> tuple[float, float, float]:
    """
    Parse hex color string to RGB tuple.

    Parameters
    ----------
    hex_str : str
        Hex color string (#RGB or #RRGGBB).

    Returns
    -------
    tuple[float, float, float]
        (r, g, b) in range [0, 1].

    Raises
    ------
    ValueError
        If the hex string format is invalid.
    """
    hex_clean: str = hex_str.strip().lstrip("#")

    if len(hex_clean) == 3:
        # #RGB format
        r: float = int(hex_clean[0] * 2, 16) / 255.0
        g: float = int(hex_clean[1] * 2, 16) / 255.0
        b: float = int(hex_clean[2] * 2, 16) / 255.0
    elif len(hex_clean) == 6:
        # #RRGGBB format
        r = int(hex_clean[0:2], 16) / 255.0
        g = int(hex_clean[2:4], 16) / 255.0
        b = int(hex_clean[4:6], 16) / 255.0
    else:
        raise ValueError(f"Invalid hex color format: {hex_str}")

    return (r, g, b)


def _rgb_to_hex(r: float, g: float, b: float) -> str:
    """
    Convert RGB to hex string.

    Parameters
    ----------
    r, g, b : float
        RGB values in range [0, 1].

    Returns
    -------
    str
        Hex color string (#RRGGBB).
    """
    # Clamp to [0, 1]
    r_clamped: float = max(0.0, min(1.0, r))
    g_clamped: float = max(0.0, min(1.0, g))
    b_clamped: float = max(0.0, min(1.0, b))

    # Convert to 0-255 and format as hex
    r_int: int = int(round(r_clamped * 255))
    g_int: int = int(round(g_clamped * 255))
    b_int: int = int(round(b_clamped * 255))

    return f"#{r_int:02x}{g_int:02x}{b_int:02x}"


# ============================================================================
# Color Class
# ============================================================================


class Color:
    """
    A color class that supports OKLab, OKLCH, RGB, and hex color spaces.

    Colors are stored internally as OKLab coordinates for efficient
    conversion. Use classmethods to create Color instances:
    from_oklab(), from_oklch(), from_rgb(), from_hex().
    """

    def __init__(self, L: float, a: float, b: float) -> None:
        """
        Private constructor. Use classmethods to create Color instances.

        Parameters
        ----------
        L, a, b : float
            OKLab coordinates.
        """
        self._L: float = float(L)
        self._a: float = float(a)
        self._b: float = float(b)

    @classmethod
    def from_oklab(cls, L: float, a: float, b: float) -> "Color":
        """
        Create a Color from OKLab coordinates.

        Parameters
        ----------
        L, a, b : float
            OKLab coordinates (L typically in [0, 1]).

        Returns
        -------
        Color
            Color instance.
        """
        return cls(L, a, b)

    @classmethod
    def from_oklch(cls, L: float, C: float, h: float) -> "Color":
        """
        Create a Color from OKLCH coordinates.

        Parameters
        ----------
        L, C : float
            Lightness and Chroma (L typically in [0, 1], C >= 0).
        h : float
            Hue in degrees [0, 360).

        Returns
        -------
        Color
            Color instance.
        """
        # Convert degrees to radians for internal calculation
        h_rad: float = math.radians(h)
        _, a, b = _oklch_to_oklab(L, C, h_rad)
        return cls(L, a, b)

    @classmethod
    def from_rgb(cls, r: float, g: float, b: float) -> "Color":
        """
        Create a Color from RGB values.

        Automatically detects if values are in [0, 1] or [0, 255] range.
        If all values are <= 1.0, treats as [0, 1]. Otherwise, treats as
        [0, 255].

        Parameters
        ----------
        r, g, b : float
            RGB values (auto-detected range).

        Returns
        -------
        Color
            Color instance.
        """
        # Auto-detect range
        r_norm: float = r
        g_norm: float = g
        b_norm: float = b
        if r > 1.0 or g > 1.0 or b > 1.0:
            # Assume 0-255 range
            r_norm = r / 255.0
            g_norm = g / 255.0
            b_norm = b / 255.0

        # Convert sRGB to linear RGB
        r_linear: float | np.ndarray = _srgb_to_linear(r_norm)
        g_linear: float | np.ndarray = _srgb_to_linear(g_norm)
        b_linear: float | np.ndarray = _srgb_to_linear(b_norm)

        # Convert to OKLab
        L: float
        a: float
        b_val: float
        L, a, b_val = _linear_srgb_to_oklab(
            float(r_linear), float(g_linear), float(b_linear)
        )

        return cls(L, a, b_val)

    @classmethod
    def from_hex(cls, hex_str: str) -> "Color":
        """
        Create a Color from hex color string.

        Parameters
        ----------
        hex_str : str
            Hex color string (#RGB or #RRGGBB).

        Returns
        -------
        Color
            Color instance.
        """
        r: float
        g: float
        b: float
        r, g, b = _parse_hex(hex_str)
        return cls.from_rgb(r, g, b)

    @classmethod
    def from_name(cls, name: str) -> "Color":
        """
        Create a Color from matplotlib color name.

        Supports all matplotlib color names including:
        - Basic colors: 'red', 'blue', 'green', etc.
        - Named colors: 'aliceblue', 'antiquewhite', etc.
        - Custom dartwork-mpl colors: 'oc.red5', 'tw.blue500', etc.

        Parameters
        ----------
        name : str
            Matplotlib color name (e.g., 'red', 'oc.blue5',
            'tw.blue500').

        Returns
        -------
        Color
            Color instance.

        Raises
        ------
        ValueError
            If the color name is not recognized by matplotlib.
        """
        try:
            # Use matplotlib's to_rgb to convert color name to RGB
            r: float
            g: float
            b: float
            r, g, b = mcolors.to_rgb(name)
            return cls.from_rgb(r, g, b)
        except ValueError as e:
            raise ValueError(f"Invalid color name: {name}. {str(e)}")

    def to_oklab(self) -> tuple[float, float, float]:
        """
        Convert to OKLab coordinates.

        Returns
        -------
        tuple[float, float, float]
            (L, a, b) OKLab coordinates.
        """
        return (self._L, self._a, self._b)

    def to_oklch(self) -> tuple[float, float, float]:
        """
        Convert to OKLCH coordinates.

        Returns
        -------
        tuple[float, float, float]
            (L, C, h) OKLCH coordinates, where h is in degrees [0, 360).
        """
        L: float
        C: float
        h_rad: float
        L, C, h_rad = _oklab_to_oklch(self._L, self._a, self._b)
        # Convert radians to degrees
        h_deg: float = math.degrees(h_rad)
        # Normalize to [0, 360)
        h_deg = h_deg % 360.0
        return (L, C, h_deg)

    def to_rgb(self) -> tuple[float, float, float]:
        """
        Convert to RGB values.

        Returns
        -------
        tuple[float, float, float]
            (r, g, b) RGB values in range [0, 1].
        """
        # Convert OKLab to linear RGB
        r_linear: float
        g_linear: float
        b_linear: float
        r_linear, g_linear, b_linear = _oklab_to_linear_srgb(self._L, self._a, self._b)

        # Clamp to valid range
        r_linear_clamped: float = max(0.0, min(1.0, r_linear))
        g_linear_clamped: float = max(0.0, min(1.0, g_linear))
        b_linear_clamped: float = max(0.0, min(1.0, b_linear))

        # Convert linear RGB to sRGB
        r: float | np.ndarray = _linear_to_srgb(r_linear_clamped)
        g: float | np.ndarray = _linear_to_srgb(g_linear_clamped)
        b: float | np.ndarray = _linear_to_srgb(b_linear_clamped)

        # Convert numpy scalars/arrays to Python floats
        r_float: float = float(np.asarray(r).item())
        g_float: float = float(np.asarray(g).item())
        b_float: float = float(np.asarray(b).item())

        return (r_float, g_float, b_float)

    def to_hex(self) -> str:
        """
        Convert to hex color string.

        Returns
        -------
        str
            Hex color string (#RRGGBB).
        """
        r: float
        g: float
        b: float
        r, g, b = self.to_rgb()
        return _rgb_to_hex(r, g, b)

    def __repr__(self) -> str:
        """
        String representation of Color.

        Returns
        -------
        str
            String representation showing OKLab coordinates.
        """
        return f"Color(oklab=({self._L:.4f}, {self._a:.4f}, {self._b:.4f}))"


# ============================================================================
# Color Space Interpolation
# ============================================================================


def cspace(
    start_color: Color | str,
    end_color: Color | str,
    n: int,
    space: str = "oklch",
) -> list[Color]:
    """
    Generate a list of colors by interpolating between two colors.

    Inspired by np.linspace, but for colors.

    Parameters
    ----------
    start_color : Color or str
        Starting color (Color instance or hex string).
    end_color : Color or str
        Ending color (Color instance or hex string).
    n : int
        Number of colors to generate (including start and end).
    space : str, optional
        Color space for interpolation: 'oklch' (default), 'oklab', or
        'rgb'. Default is 'oklch'.

    Returns
    -------
    list[Color]
        List of interpolated Color objects.

    Raises
    ------
    TypeError
        If start_color or end_color is not a Color instance or hex
        string.
    ValueError
        If space is not one of the supported color spaces.
    """
    # Convert input colors to Color objects if needed
    start_color_obj: Color
    if isinstance(start_color, str):
        start_color_obj = Color.from_hex(start_color)
    else:
        start_color_obj = start_color

    end_color_obj: Color
    if isinstance(end_color, str):
        end_color_obj = Color.from_hex(end_color)
    else:
        end_color_obj = end_color

    if not isinstance(start_color_obj, Color):
        raise TypeError(
            f"start_color must be Color instance or hex string, got {type(start_color)}"
        )
    if not isinstance(end_color_obj, Color):
        raise TypeError(
            f"end_color must be Color instance or hex string, got {type(end_color)}"
        )

    # Convert to target color space
    if space == "oklch":
        start_L: float
        start_C: float
        start_h: float
        start_L, start_C, start_h = start_color_obj.to_oklch()
        # h is in degrees

        end_L: float
        end_C: float
        end_h: float
        end_L, end_C, end_h = end_color_obj.to_oklch()
        # h is in degrees

        # Handle hue wrapping (shortest path in degrees)
        h_diff: float = end_h - start_h
        # Normalize to [-180, 180] range for shortest path
        if h_diff > 180:
            end_h -= 360
        elif h_diff < -180:
            end_h += 360

        # Interpolate
        L_values: np.ndarray = np.linspace(start_L, end_L, n)
        C_values: np.ndarray = np.linspace(start_C, end_C, n)
        h_values: np.ndarray = np.linspace(start_h, end_h, n)

        # Normalize hue values to [0, 360) before creating Color objects
        h_values = h_values % 360.0

        # Convert back to Color objects
        colors: list[Color] = [
            Color.from_oklch(L, C, h) for L, C, h in zip(L_values, C_values, h_values)
        ]

    elif space == "oklab":
        start_L, start_a, start_b = start_color_obj.to_oklab()
        end_L, end_a, end_b = end_color_obj.to_oklab()

        # Interpolate
        L_values = np.linspace(start_L, end_L, n)
        a_values: np.ndarray = np.linspace(start_a, end_a, n)
        b_values: np.ndarray = np.linspace(start_b, end_b, n)

        # Convert back to Color objects
        colors = [
            Color.from_oklab(L, a, b) for L, a, b in zip(L_values, a_values, b_values)
        ]

    elif space == "rgb":
        start_r: float
        start_g: float
        start_b: float
        start_r, start_g, start_b = start_color_obj.to_rgb()
        end_r: float
        end_g: float
        end_b: float
        end_r, end_g, end_b = end_color_obj.to_rgb()

        # Interpolate
        r_values: np.ndarray = np.linspace(start_r, end_r, n)
        g_values: np.ndarray = np.linspace(start_g, end_g, n)
        b_values = np.linspace(start_b, end_b, n)

        # Convert back to Color objects
        colors = [
            Color.from_rgb(r, g, b) for r, g, b in zip(r_values, g_values, b_values)
        ]

    else:
        raise ValueError(
            f"Unsupported color space: {space}. Must be 'oklch', 'oklab', or 'rgb'"
        )

    return colors


# ============================================================================
# Wrapper Functions
# ============================================================================


def oklab(L: float, a: float, b: float) -> Color:
    """
    Convenience function to create a Color from OKLab coordinates.

    Parameters
    ----------
    L, a, b : float
        OKLab coordinates.

    Returns
    -------
    Color
        Color instance.
    """
    return Color.from_oklab(L, a, b)


def oklch(L: float, C: float, h: float) -> Color:
    """
    Convenience function to create a Color from OKLCH coordinates.

    Parameters
    ----------
    L, C : float
        Lightness and Chroma.
    h : float
        Hue in degrees [0, 360).

    Returns
    -------
    Color
        Color instance.
    """
    return Color.from_oklch(L, C, h)


def rgb(r: float, g: float, b: float) -> Color:
    """
    Convenience function to create a Color from RGB values.

    Parameters
    ----------
    r, g, b : float
        RGB values (auto-detected range: 0-1 or 0-255).

    Returns
    -------
    Color
        Color instance.
    """
    return Color.from_rgb(r, g, b)


def hex(hex_str: str) -> Color:
    """
    Convenience function to create a Color from hex color string.

    Parameters
    ----------
    hex_str : str
        Hex color string (#RGB or #RRGGBB).

    Returns
    -------
    Color
        Color instance.
    """
    return Color.from_hex(hex_str)


def named(color_name: str) -> Color:
    """
    Convenience function to create a Color from matplotlib color name.

    Parameters
    ----------
    color_name : str
        Matplotlib color name (e.g., 'red', 'oc.blue5',
        'tw.blue500').

    Returns
    -------
    Color
        Color instance.
    """
    return Color.from_name(color_name)
