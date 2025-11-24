import json
import math
from pathlib import Path
import numpy as np
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
    
    Tailwind CSS colors are loaded with 'tw.' prefix,
    followed by the color name and weight (e.g., 'tw.blue:500', 
    'tw.gray:200'). Weights range from 50 to 950 in increments 
    of 50 or 100.
    
    Material Design colors are loaded with 'md.' prefix
    (e.g., 'md.blue:500', 'md.red:700'). Weights range from 50 to 900.
    
    Ant Design colors are loaded with 'ant.' prefix
    (e.g., 'ant.blue:5', 'ant.red:6'). Weights range from 1 to 10.
    
    Chakra UI colors are loaded with 'chakra.' prefix
    (e.g., 'chakra.blue:500', 'chakra.red:600'). Weights range from 50 to 900.
    
    Primer colors are loaded with 'primer.' prefix
    (e.g., 'primer.blue:5', 'primer.red:6'). Weights range from 0 to 9.
    """
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
            # Only use 'tw.' prefix, skip 'tailwind.' prefix since they are identical
            _color_dict[f'tw.{k}:{weight}'] = f'#{hex}'

    # Material Design colors.
    with open(root_dir / 'material_colors.json', 'r') as f:
        material_colors = json.load(f)

    for k, v in material_colors.items():
        k = k.lower().replace(' ', '')  # Remove spaces (e.g., "Deep Purple" -> "deeppurple")
        for weight, hex in v:
            _color_dict[f'md.{k}:{weight}'] = f'#{hex}'

    # Ant Design colors.
    with open(root_dir / 'ant_colors.json', 'r') as f:
        ant_colors = json.load(f)

    for k, v in ant_colors.items():
        k = k.lower()
        for weight, hex in v:
            _color_dict[f'ant.{k}:{weight}'] = f'#{hex}'

    # Chakra UI colors.
    with open(root_dir / 'chakra_colors.json', 'r') as f:
        chakra_colors = json.load(f)

    for k, v in chakra_colors.items():
        k = k.lower()
        for weight, hex in v:
            _color_dict[f'chakra.{k}:{weight}'] = f'#{hex}'

    # Primer colors.
    with open(root_dir / 'primer_colors.json', 'r') as f:
        primer_colors = json.load(f)

    for k, v in primer_colors.items():
        k = k.lower()
        for weight, hex in v:
            _color_dict[f'primer.{k}:{weight}'] = f'#{hex}'

    # Add color dict to matplotlib internal color mapping.
    mcolors.get_named_colors_mapping().update(_color_dict)
    
    # Remove xkcd colors from matplotlib's color mapping since we don't use them
    # and they clutter the 'other' category in color galleries.
    color_mapping = mcolors.get_named_colors_mapping()
    xkcd_keys = [k for k in list(color_mapping.keys()) if k.startswith('xkcd:')]
    for key in xkcd_keys:
        del color_mapping[key]


_load_colors()


# ============================================================================
# Color Conversion Functions
# ============================================================================

def _srgb_to_linear(c):
    """
    Convert sRGB to linear RGB (gamma decoding).
    
    Parameters
    ----------
    c : float or array
        sRGB value(s) in range [0, 1]
        
    Returns
    -------
    float or array
        Linear RGB value(s) in range [0, 1]
    """
    c = np.asarray(c)
    mask = c <= 0.04045
    return np.where(mask, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(c):
    """
    Convert linear RGB to sRGB (gamma encoding).
    
    Parameters
    ----------
    c : float or array
        Linear RGB value(s) in range [0, 1]
        
    Returns
    -------
    float or array
        sRGB value(s) in range [0, 1]
    """
    c = np.asarray(c)
    mask = c <= 0.0031308
    return np.where(mask, 12.92 * c, 1.055 * (c ** (1.0 / 2.4)) - 0.055)


def _linear_srgb_to_oklab(r, g, b):
    """
    Convert linear sRGB to OKLab.
    
    Based on the C++ implementation provided.
    
    Parameters
    ----------
    r, g, b : float
        Linear RGB values in range [0, 1]
        
    Returns
    -------
    tuple
        (L, a, b) OKLab coordinates
    """
    # Matrix multiplication to LMS
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    
    # Cube root
    l_ = np.cbrt(l)
    m_ = np.cbrt(m)
    s_ = np.cbrt(s)
    
    # Matrix multiplication to OKLab
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    
    return (L, a, b)


def _oklab_to_linear_srgb(L, a, b):
    """
    Convert OKLab to linear sRGB.
    
    Based on the C++ implementation provided.
    
    Parameters
    ----------
    L, a, b : float
        OKLab coordinates
        
    Returns
    -------
    tuple
        (r, g, b) linear RGB values in range [0, 1]
    """
    # Matrix multiplication to LMS
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    
    # Cube
    l = l_ * l_ * l_
    m = m_ * m_ * m_
    s = s_ * s_ * s_
    
    # Matrix multiplication to linear RGB
    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    
    return (r, g, b)


def _oklab_to_oklch(L, a, b):
    """
    Convert OKLab to OKLCH.
    
    Parameters
    ----------
    L, a, b : float
        OKLab coordinates
        
    Returns
    -------
    tuple
        (L, C, h) OKLCH coordinates, where h is in radians
    """
    C = math.sqrt(a * a + b * b)
    h = math.atan2(b, a)
    return (L, C, h)


def _oklch_to_oklab(L, C, h):
    """
    Convert OKLCH to OKLab.
    
    Parameters
    ----------
    L, C : float
        Lightness and Chroma
    h : float
        Hue in radians
        
    Returns
    -------
    tuple
        (L, a, b) OKLab coordinates
    """
    a = C * math.cos(h)
    b = C * math.sin(h)
    return (L, a, b)


def _parse_hex(hex_str):
    """
    Parse hex color string to RGB tuple.
    
    Parameters
    ----------
    hex_str : str
        Hex color string (#RGB or #RRGGBB)
        
    Returns
    -------
    tuple
        (r, g, b) in range [0, 1]
    """
    hex_str = hex_str.strip().lstrip('#')
    
    if len(hex_str) == 3:
        # #RGB format
        r = int(hex_str[0] * 2, 16) / 255.0
        g = int(hex_str[1] * 2, 16) / 255.0
        b = int(hex_str[2] * 2, 16) / 255.0
    elif len(hex_str) == 6:
        # #RRGGBB format
        r = int(hex_str[0:2], 16) / 255.0
        g = int(hex_str[2:4], 16) / 255.0
        b = int(hex_str[4:6], 16) / 255.0
    else:
        raise ValueError(f"Invalid hex color format: {hex_str}")
    
    return (r, g, b)


def _rgb_to_hex(r, g, b):
    """
    Convert RGB to hex string.
    
    Parameters
    ----------
    r, g, b : float
        RGB values in range [0, 1]
        
    Returns
    -------
    str
        Hex color string (#RRGGBB)
    """
    # Clamp to [0, 1]
    r = max(0.0, min(1.0, r))
    g = max(0.0, min(1.0, g))
    b = max(0.0, min(1.0, b))
    
    # Convert to 0-255 and format as hex
    r_int = int(round(r * 255))
    g_int = int(round(g * 255))
    b_int = int(round(b * 255))
    
    return f"#{r_int:02x}{g_int:02x}{b_int:02x}"


# ============================================================================
# Color Class
# ============================================================================

class Color:
    """
    A color class that supports OKLab, OKLCH, RGB, and hex color spaces.
    
    Colors are stored internally as OKLab coordinates for efficient conversion.
    Use classmethods to create Color instances: from_oklab(), from_oklch(),
    from_rgb(), from_hex().
    """
    
    def __init__(self, L, a, b):
        """
        Private constructor. Use classmethods to create Color instances.
        
        Parameters
        ----------
        L, a, b : float
            OKLab coordinates
        """
        self._L = float(L)
        self._a = float(a)
        self._b = float(b)
    
    @classmethod
    def from_oklab(cls, L, a, b):
        """
        Create a Color from OKLab coordinates.
        
        Parameters
        ----------
        L, a, b : float
            OKLab coordinates (L typically in [0, 1])
            
        Returns
        -------
        Color
            Color instance
        """
        return cls(L, a, b)
    
    @classmethod
    def from_oklch(cls, L, C, h):
        """
        Create a Color from OKLCH coordinates.
        
        Parameters
        ----------
        L, C : float
            Lightness and Chroma (L typically in [0, 1], C >= 0)
        h : float
            Hue in degrees [0, 360)
            
        Returns
        -------
        Color
            Color instance
        """
        # Convert degrees to radians for internal calculation
        h_rad = math.radians(h)
        _, a, b = _oklch_to_oklab(L, C, h_rad)
        return cls(L, a, b)
    
    @classmethod
    def from_rgb(cls, r, g, b):
        """
        Create a Color from RGB values.
        
        Automatically detects if values are in [0, 1] or [0, 255] range.
        If all values are <= 1.0, treats as [0, 1]. Otherwise, treats as [0, 255].
        
        Parameters
        ----------
        r, g, b : float
            RGB values (auto-detected range)
            
        Returns
        -------
        Color
            Color instance
        """
        # Auto-detect range
        if r > 1.0 or g > 1.0 or b > 1.0:
            # Assume 0-255 range
            r, g, b = r / 255.0, g / 255.0, b / 255.0
        
        # Convert sRGB to linear RGB
        r_linear = _srgb_to_linear(r)
        g_linear = _srgb_to_linear(g)
        b_linear = _srgb_to_linear(b)
        
        # Convert to OKLab
        L, a, b = _linear_srgb_to_oklab(r_linear, g_linear, b_linear)
        
        return cls(L, a, b)
    
    @classmethod
    def from_hex(cls, hex_str):
        """
        Create a Color from hex color string.
        
        Parameters
        ----------
        hex_str : str
            Hex color string (#RGB or #RRGGBB)
            
        Returns
        -------
        Color
            Color instance
        """
        r, g, b = _parse_hex(hex_str)
        return cls.from_rgb(r, g, b)
    
    @classmethod
    def from_name(cls, name):
        """
        Create a Color from matplotlib color name.
        
        Supports all matplotlib color names including:
        - Basic colors: 'red', 'blue', 'green', etc.
        - Named colors: 'aliceblue', 'antiquewhite', etc.
        - Custom dartwork-mpl colors: 'dm.red5', 'tw.blue:500', etc.
        
        Parameters
        ----------
        name : str
            Matplotlib color name (e.g., 'red', 'dm.blue5', 'tw.blue:500')
            
        Returns
        -------
        Color
            Color instance
            
        Raises
        ------
        ValueError
            If the color name is not recognized by matplotlib
        """
        try:
            # Use matplotlib's to_rgb to convert color name to RGB
            r, g, b = mcolors.to_rgb(name)
            return cls.from_rgb(r, g, b)
        except ValueError as e:
            raise ValueError(f"Invalid color name: {name}. {str(e)}")
    
    def to_oklab(self):
        """
        Convert to OKLab coordinates.
        
        Returns
        -------
        tuple
            (L, a, b) OKLab coordinates
        """
        return (self._L, self._a, self._b)
    
    def to_oklch(self):
        """
        Convert to OKLCH coordinates.
        
        Returns
        -------
        tuple
            (L, C, h) OKLCH coordinates, where h is in degrees [0, 360)
        """
        L, C, h_rad = _oklab_to_oklch(self._L, self._a, self._b)
        # Convert radians to degrees
        h_deg = math.degrees(h_rad)
        # Normalize to [0, 360)
        h_deg = h_deg % 360.0
        return (L, C, h_deg)
    
    def to_rgb(self):
        """
        Convert to RGB values.
        
        Returns
        -------
        tuple
            (r, g, b) RGB values in range [0, 1]
        """
        # Convert OKLab to linear RGB
        r_linear, g_linear, b_linear = _oklab_to_linear_srgb(self._L, self._a, self._b)
        
        # Clamp to valid range
        r_linear = max(0.0, min(1.0, r_linear))
        g_linear = max(0.0, min(1.0, g_linear))
        b_linear = max(0.0, min(1.0, b_linear))
        
        # Convert linear RGB to sRGB
        r = _linear_to_srgb(r_linear)
        g = _linear_to_srgb(g_linear)
        b = _linear_to_srgb(b_linear)
        
        return (r, g, b)
    
    def to_hex(self):
        """
        Convert to hex color string.
        
        Returns
        -------
        str
            Hex color string (#RRGGBB)
        """
        r, g, b = self.to_rgb()
        return _rgb_to_hex(r, g, b)
    
    def __repr__(self):
        """String representation of Color."""
        return f"Color(oklab=({self._L:.4f}, {self._a:.4f}, {self._b:.4f}))"


# ============================================================================
# Color Space Interpolation
# ============================================================================

def cspace(start_color, end_color, n, space='oklch'):
    """
    Generate a list of colors by interpolating between two colors in a specified color space.
    
    Inspired by np.linspace, but for colors.
    
    Parameters
    ----------
    start_color : Color or str
        Starting color (Color instance or hex string)
    end_color : Color or str
        Ending color (Color instance or hex string)
    n : int
        Number of colors to generate (including start and end)
    space : str, optional
        Color space for interpolation: 'oklch' (default), 'oklab', or 'rgb'
        
    Returns
    -------
    list of Color
        List of interpolated Color objects
    """
    # Convert input colors to Color objects if needed
    if isinstance(start_color, str):
        start_color = Color.from_hex(start_color)
    if isinstance(end_color, str):
        end_color = Color.from_hex(end_color)
    
    if not isinstance(start_color, Color):
        raise TypeError(f"start_color must be Color instance or hex string, got {type(start_color)}")
    if not isinstance(end_color, Color):
        raise TypeError(f"end_color must be Color instance or hex string, got {type(end_color)}")
    
    # Convert to target color space
    if space == 'oklch':
        start_L, start_C, start_h = start_color.to_oklch()  # h is in degrees
        end_L, end_C, end_h = end_color.to_oklch()  # h is in degrees
        
        # Handle hue wrapping (shortest path in degrees)
        h_diff = end_h - start_h
        # Normalize to [-180, 180] range for shortest path
        if h_diff > 180:
            end_h -= 360
        elif h_diff < -180:
            end_h += 360
        
        # Interpolate
        L_values = np.linspace(start_L, end_L, n)
        C_values = np.linspace(start_C, end_C, n)
        h_values = np.linspace(start_h, end_h, n)
        
        # Normalize hue values to [0, 360) before creating Color objects
        h_values = h_values % 360.0
        
        # Convert back to Color objects
        colors = [Color.from_oklch(L, C, h) for L, C, h in zip(L_values, C_values, h_values)]
        
    elif space == 'oklab':
        start_L, start_a, start_b = start_color.to_oklab()
        end_L, end_a, end_b = end_color.to_oklab()
        
        # Interpolate
        L_values = np.linspace(start_L, end_L, n)
        a_values = np.linspace(start_a, end_a, n)
        b_values = np.linspace(start_b, end_b, n)
        
        # Convert back to Color objects
        colors = [Color.from_oklab(L, a, b) for L, a, b in zip(L_values, a_values, b_values)]
        
    elif space == 'rgb':
        start_r, start_g, start_b = start_color.to_rgb()
        end_r, end_g, end_b = end_color.to_rgb()
        
        # Interpolate
        r_values = np.linspace(start_r, end_r, n)
        g_values = np.linspace(start_g, end_g, n)
        b_values = np.linspace(start_b, end_b, n)
        
        # Convert back to Color objects
        colors = [Color.from_rgb(r, g, b) for r, g, b in zip(r_values, g_values, b_values)]
        
    else:
        raise ValueError(f"Unsupported color space: {space}. Must be 'oklch', 'oklab', or 'rgb'")
    
    return colors


# ============================================================================
# Wrapper Functions
# ============================================================================

def oklab(L, a, b):
    """
    Convenience function to create a Color from OKLab coordinates.
    
    Parameters
    ----------
    L, a, b : float
        OKLab coordinates
        
    Returns
    -------
    Color
        Color instance
    """
    return Color.from_oklab(L, a, b)


def oklch(L, C, h):
    """
    Convenience function to create a Color from OKLCH coordinates.
    
    Parameters
    ----------
    L, C : float
        Lightness and Chroma
    h : float
        Hue in degrees [0, 360)
        
    Returns
    -------
    Color
        Color instance
    """
    return Color.from_oklch(L, C, h)


def rgb(r, g, b):
    """
    Convenience function to create a Color from RGB values.
    
    Parameters
    ----------
    r, g, b : float
        RGB values (auto-detected range: 0-1 or 0-255)
        
    Returns
    -------
    Color
        Color instance
    """
    return Color.from_rgb(r, g, b)


def hex(hex_str):
    """
    Convenience function to create a Color from hex color string.
    
    Parameters
    ----------
    hex_str : str
        Hex color string (#RGB or #RRGGBB)
        
    Returns
    -------
    Color
        Color instance
    """
    return Color.from_hex(hex_str)


def named(color_name):
    """
    Convenience function to create a Color from matplotlib color name.
    
    Parameters
    ----------
    color_name : str
        Matplotlib color name (e.g., 'red', 'dm.blue5', 'tw.blue:500')
        
    Returns
    -------
    Color
        Color instance
    """
    return Color.from_name(color_name)
