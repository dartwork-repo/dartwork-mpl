import os
import math
import re
from xml.dom import minidom
from collections import defaultdict
from tempfile import NamedTemporaryFile
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.font_manager as fm

from matplotlib.patches import Rectangle
from matplotlib.transforms import ScaledTranslation
from IPython.display import display, HTML, SVG
from scipy.optimize import minimize
    
    
# Will be replaced to rich print.
PRINT = print


def _create_parent_path_if_not_exists(path):
    """
    Create parent directory if it doesn't exist.
    
    Parameters
    ----------
    path : str or Path
        Path to check and create parent directory for.
    """
    path = Path(path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
        print(f'Created a directory: {path.parent}')


def set_decimal(ax, xn=None, yn=None):
    """
    Set decimal places for tick labels.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to modify.
    xn : int, optional
        Number of decimal places for x-axis tick labels.
    yn : int, optional
        Number of decimal places for y-axis tick labels.
    """
    if xn is not None:
        xticks = ax.get_xticks()
        ax.set_xticks(xticks)
        ax.set_xticklabels([f'{x:.{xn}f}' for x in xticks])
        
    if yn is not None:
        yticks = ax.get_yticks()
        ax.set_yticks(yticks)
        ax.set_yticklabels([f'{y:.{yn}f}' for y in yticks])


def get_bounding_box(boxes):
    """
    Get the bounding box that contains all given boxes.
    
    Parameters
    ----------
    boxes : list
        List of box objects with p0, width, and height attributes.
        
    Returns
    -------
    tuple
        (min_x, min_y, bbox_width, bbox_height) of the bounding box.
    """
    # Initialize extremes
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')
    
    # Iterate through each box
    for box in boxes:
        # Update minimum x and y
        min_x = min(min_x, box.p0[0])
        min_y = min(min_y, box.p0[1])
        
        # Update maximum x and y
        max_x = max(max_x, box.p0[0] + box.width)
        max_y = max(max_y, box.p0[1] + box.height)
    
    # Calculate bounding box width and height
    bbox_width = max_x - min_x
    bbox_height = max_y - min_y
    
    return (min_x, min_y, bbox_width, bbox_height)


def simple_layout(
    fig,
    gs=None,
    margins=(0.05, 0.05, 0.05, 0.05),
    bbox=(0, 1, 0, 1),
    verbose=False,
    gtol=1e-2,
    bound_margin=0.2,
    use_all_axes=True,
    importance_weights=(1, 1, 1, 1),
):
    """Apply simple layout to figure for given grid spec.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object.
    gs : matplotlib.gridspec.GridSpec, optional(default=None)
        Grid spec object. If None, use the first grid spec.
    margins : tuple(float, float, float, float), optional(default=(0.05, 0.05, 0.05, 0.05))
        Margins in inches, (left, right, bottom, top).
    bbox : tuple(float, float, float, float), optional(default=(0, 1, 0, 1))
        Bounding box in figure coordinates, (left, right, bottom, top).
    verbose : bool, optional(default=True)
        Print verbose.
    gtol : float, optional(default=1e-2)
        Gradient tolerance. If the maximum change in the objective function is
        less than gtol, the optimization will stop.
    bound_margin : float, optional(default=0.1)
        Margin for bounds generation.
    use_all_axes : bool, optional(default=True)
        Use all axes in the figure. If False, use only axes in the given grid spec.
        IF True, use all axes in the figure.
    importance_weights : tuple(float, float, float, float), optional(default=(1, 1, 1, 1))
        Importance weights for each target. (left, right, bottom, top).
        
    Returns
    -------
    result : scipy.optimize.OptimizeResult
        Optimization result.

    TODO
    ----
    - Upgrade bounds generation algorithm.
    - Readable code.
    """
    if gs is None:
        gs = fig.axes[0].get_gridspec()

    if use_all_axes and verbose:
        print('Use all axes in the figure. Given grid spec will be ignored.')

    importance_weights = np.array(importance_weights)
    margins = np.array(margins) * fig.get_dpi()

    def fun(x):
        # print(gs.left, gs.right, gs.bottom, gs.top)
        gs.update(left=x[0], right=x[1], bottom=x[2], top=x[3])

        if use_all_axes:
            ax_bboxes = [ax.get_tightbbox() for ax in fig.axes]
        else:
            ax_bboxes = [
                ax.get_tightbbox() for ax in fig.axes
                if id(ax.get_gridspec()) == id(gs)
            ]

        all_bbox = get_bounding_box(ax_bboxes)

        values = np.array(all_bbox)

        # Targets.
        fbox = fig.bbox
        targets = np.array([
            fbox.width * bbox[0] + margins[0],
            fbox.height * bbox[2] + margins[2],
            fbox.width * (bbox[1] - bbox[0]) - 2 * margins[1],
            fbox.height * (bbox[3] - bbox[2]) - 2 * margins[3],
        ])
 
        scales = np.array([
            fbox.width,
            fbox.height,
            fbox.width,
            fbox.height,
        ])

        loss = np.square((values - targets) / scales * importance_weights).sum()
 
        if verbose:
            print('x', x)
            print('Loss', loss)
            print('Values: {0:.2f}, {1:.2f}, {2:.2f}, {3:.2f}'.format(*(values)))
            print('Targets: {0:.2f}, {1:.2f}, {2:.2f}, {3:.2f}'.format(*(targets)))

        return loss
    
    # Order: left, right, bottom, top.
    bounds = [
        (bbox[0], bbox[0] + bound_margin),
        (bbox[1] - bound_margin, bbox[1]),
        (bbox[2], bbox[2] + bound_margin),
        (bbox[3] - bound_margin, bbox[3]),
    ]

    result = minimize(
        fun, x0=np.array(bounds).mean(axis=1),
        bounds=bounds,
        # # Gradient-free optimization.
        # method='Nelder-Mead',    
        # # Relax convergence criteria.
        # options=dict(xatol=1e-3),
        method='L-BFGS-B',
        options=dict(gtol=gtol),
    )

    return result



def fs(n):
    """
    Return base font size + n.
    
    Parameters
    ----------
    n : int or float
        Value to add to base font size.
        
    Returns
    -------
    float
        Base font size + n.
    """
    return plt.rcParams['font.size'] + n


def fw(n):
    """
    Return base font weight + 100 * n. 
    Only works for integer weights and n.
    
    Parameters
    ----------
    n : int
        Value to multiply by 100 and add to base font weight.
        
    Returns
    -------
    int
        Base font weight + 100 * n.
    """
    return plt.rcParams['font.weight'] + 100 * n


def mix_colors(color1, color2, alpha=0.5):
    """
    Mix two colors.
    
    Parameters
    ----------
    color1 : color
        First color (any format accepted by matplotlib).
    color2 : color
        Second color (any format accepted by matplotlib).
    alpha : float, optional
        Weight of the first color, between 0 and 1.
        
    Returns
    -------
    tuple
        RGB tuple of the mixed color.
    """
    color1 = mcolors.to_rgb(color1)
    color2 = mcolors.to_rgb(color2)

    return tuple(alpha * c1 + (1 - alpha) * c2 for c1, c2 in zip(color1, color2))


def pseudo_alpha(color, alpha=1.0, background='white'):
    """
    Return a color with pseudo alpha.
    
    Parameters
    ----------
    color : color
        Color to apply pseudo-transparency to.
    alpha : float, optional
        Alpha value between 0 and 1.
    background : color, optional
        Background color to mix with.
        
    Returns
    -------
    tuple
        RGB tuple of the resulting color.
    """
    return mix_colors(color, background, alpha=alpha)


def cm2in(cm):
    """
    Convert centimeters to inches.
    
    Parameters
    ----------
    cm : float
        Value in centimeters.
        
    Returns
    -------
    float
        Value in inches.
    """
    return cm / 2.54


def make_offset(x, y, fig):
    """
    Create a translation offset for figure elements.
    
    Parameters
    ----------
    x : float
        X offset in points.
    y : float
        Y offset in points.
    fig : matplotlib.figure.Figure
        Figure to create offset for.
        
    Returns
    -------
    matplotlib.transforms.ScaledTranslation
        Offset transform.
    """
    dx, dy = x / 72, y / 72
    offset = ScaledTranslation(dx, dy, fig.dpi_scale_trans)

    return offset


def save_formats(fig, image_stem, formats=('svg', 'png', 'pdf', 'eps'), bbox_inches=None, **kwargs):
    """
    Save a figure in multiple formats.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to save.
    image_stem : str
        Base filename without extension.
    formats : tuple, optional
        Tuple of format extensions to save.
    bbox_inches : str or Bbox, optional
        Bounding box in inches.
    **kwargs
        Additional arguments passed to savefig.
    """
    _create_parent_path_if_not_exists(image_stem)
    for fmt in formats:
        fig.savefig(f'{image_stem}.{fmt}', bbox_inches=bbox_inches, **kwargs)


def show(image_path, size=600, unit='pt'):
    """
    Display an SVG image with specified size.
    
    Parameters
    ----------
    image_path : str
        Path to the SVG image.
    size : int, optional
        Desired width in specified units.
    unit : str, optional
        Unit for size ('pt', 'px', etc.).
    """
    # SVG 객체 생성
    svg_obj = SVG(data=image_path)

    # 원하는 가로 폭 또는 세로 높이 설정
    desired_width = size

    # SVG 코드에서 현재 가로 폭과 세로 높이 가져오기
    dom = minidom.parseString(svg_obj.data)
    width = float(dom.documentElement.getAttribute("width")[:-len(unit)])
    height = float(dom.documentElement.getAttribute("height")[:-len(unit)])

    # 비율 계산
    aspect_ratio = height / width
    desired_height = int(desired_width * aspect_ratio)

    # 가로 폭과 세로 높이 설정
    if f'width="{width}{unit}"' in svg_obj.data:
        svg_obj.data = svg_obj.data.replace(f'width="{width}{unit}"', f'width="{desired_width}{unit}"')
    else:
        width = int(width)
        svg_obj.data = svg_obj.data.replace(f'width="{width}{unit}"', f'width="{desired_width}{unit}"')

    if f'height="{height}{unit}"' in svg_obj.data:
        svg_obj.data = svg_obj.data.replace(f'height="{height}{unit}"', f'height="{desired_height}{unit}"')
    else:
        height = int(height)
        svg_obj.data = svg_obj.data.replace(f'height="{height}{unit}"', f'height="{desired_height}{unit}"')

    # HTML을 사용하여 SVG 이미지 표시
    svg_code = svg_obj.data
    display(HTML(svg_code))


def save_and_show(fig, image_path=None, size=600, unit='pt', **kwargs):
    """
    Save a figure and display it.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to save and display.
    image_path : str, optional
        Path to save the image. If None, uses a temporary file.
    size : int, optional
        Display size.
    unit : str, optional
        Unit for size.
    **kwargs
        Additional arguments passed to savefig.
    """
    if image_path is None:
        with NamedTemporaryFile(suffix='.svg') as f:
            f.close()
            image_path = f.name

            fig.savefig(image_path, bbox_inches=None, **kwargs)
            plt.close(fig)

            show(image_path, size=size, unit=unit)
    else:
        _create_parent_path_if_not_exists(image_path)
        fig.savefig(image_path, bbox_inches=None, **kwargs)
        plt.close(fig)

        show(image_path, size=size, unit=unit)


def classify_colormap(cmap):
    """Classify a colormap into one of the following categories:
    - Categorical
    - Sequential Single-Hue
    - Sequential Multi-Hue
    - Diverging
    - Cyclical
    
    Parameters
    ----------
    cmap : matplotlib.colors.Colormap
        Colormap to classify.
        
    Returns
    -------
    str
        Category of the colormap.
    """
    # Get colormap samples
    n_samples = 256
    samples = cmap(np.linspace(0, 1, n_samples))[:, :3]  # Ignore alpha
    
    # Convert to HSV for easier analysis
    hsv_samples = np.array([mcolors.rgb_to_hsv(rgb) for rgb in samples])
    hues = hsv_samples[:, 0]
    saturations = hsv_samples[:, 1]
    values = hsv_samples[:, 2]
    
    # Calculate differences between consecutive samples
    hue_diffs = np.abs(np.diff(hues))
    # Handle circular nature of hue
    hue_diffs = np.minimum(hue_diffs, 1 - hue_diffs)
    
    # Known categorical colormaps (hardcoded for better accuracy)
    categorical_cmaps = [
        'Accent', 'Dark2', 'Paired', 'Pastel1', 'Pastel2', 
        'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c',
        'Spectral', 'prism', 'hsv', 'gist_rainbow', 'rainbow', 'nipy_spectral'
    ]
    
    if hasattr(cmap, 'name') and cmap.name in categorical_cmaps:
        return "Categorical"
    
    # 1. Check if colormap is cyclical - stricter criteria
    # Cyclical maps start and end with almost identical colors
    start_end_diff = np.sqrt(np.sum((samples[0] - samples[-1])**2))
    if start_end_diff < 0.01:  # Stricter threshold
        # Also check if there's significant variation in the middle
        mid_idx = n_samples // 2
        mid_diff = np.sqrt(np.sum((samples[0] - samples[mid_idx])**2))
        if mid_diff > 0.3:  # Ensure there's variation in the middle
            return "Cyclical"
    
    # 2. Improved check for categorical colormaps based on repeated colors
    # Calculate color differences (Euclidean distance in RGB space)
    color_diffs = np.sqrt(np.sum(np.diff(samples, axis=0)**2, axis=1))
    
    # Find regions where colors are very similar (plateaus)
    plateau_mask = color_diffs < 0.001
    plateau_indices = np.where(plateau_mask)[0]
    
    # Find consecutive plateaus (runs of similar colors)
    if len(plateau_indices) > 0:
        # Split into runs of consecutive indices
        plateau_runs = np.split(plateau_indices, np.where(np.diff(plateau_indices) != 1)[0] + 1)
        
        # Count significant plateaus (runs longer than a threshold)
        significant_plateaus = [run for run in plateau_runs if len(run) >= 3]
        
        # If we have multiple significant plateaus, it's likely categorical
        if len(significant_plateaus) >= 3:
            # Check if plateaus are distributed throughout the colormap
            plateau_positions = [np.mean(run) for run in significant_plateaus]
            position_range = max(plateau_positions) - min(plateau_positions)
            
            if position_range > n_samples * 0.3:  # Plateaus are well distributed
                return "Categorical"
    
    # Additional check for categorical: large jumps in color
    large_color_jumps = np.where(color_diffs > 0.1)[0]
    if len(large_color_jumps) > 3 and len(large_color_jumps) < n_samples // 8:
        # Check if jumps are distributed (not all clustered)
        jump_diffs = np.diff(large_color_jumps)
        if np.std(jump_diffs) < np.mean(jump_diffs) * 0.8:  # Relatively evenly spaced jumps
            return "Categorical"
    
    # 3. Check if colormap is diverging
    # Diverging maps have a distinct middle with different values at ends
    mid_idx = n_samples // 2
    mid_value = values[mid_idx]
    start_value = values[0]
    end_value = values[-1]
    
    # Check if the middle is significantly different from the ends
    if ((mid_value > start_value + 0.2 and mid_value > end_value + 0.2) or 
        (mid_value < start_value - 0.2 and mid_value < end_value - 0.2)):
        # Also check if the hue changes significantly from start to end
        start_hue = hues[0]
        end_hue = hues[-1]
        hue_diff = min(abs(end_hue - start_hue), 1 - abs(end_hue - start_hue))
        if hue_diff > 0.1:  # Significant hue change
            return "Diverging"
    
    # 4. Improved check for sequential single-hue vs multi-hue
    # Focus on high saturation regions for better hue analysis
    high_sat_indices = np.where(saturations > 0.3)[0]
    
    # If we have enough high saturation samples
    if len(high_sat_indices) > n_samples // 4:
        high_sat_hues = hues[high_sat_indices]
        
        # Calculate hue range for high saturation colors
        if len(high_sat_hues) > 1:
            # Get the circular range of hues
            hue_min = np.min(high_sat_hues)
            hue_max = np.max(high_sat_hues)
            hue_range = hue_max - hue_min
            if hue_range > 0.5:  # Account for circular hue
                hue_range = 1 - hue_range
            
            # Stricter criteria for single-hue: very narrow hue range
            if hue_range < 0.01:  # Much stricter threshold
                return "Sequential Single-Hue"
            else:
                return "Sequential Multi-Hue"
    
    # If we couldn't decide based on high saturation, look at overall pattern
    
    # Calculate overall hue variation, accounting for circularity
    hue_min = np.min(hues)
    hue_max = np.max(hues)
    hue_range = hue_max - hue_min
    if hue_range > 0.5:  # Account for circular hue
        hue_range = 1 - hue_range
    
    # Check for monotonic value change (typical for sequential)
    is_monotonic = np.all(np.diff(values[:n_samples//2]) * np.diff(values[n_samples//2:]) >= 0)
    
    if hue_range < 0.01 and is_monotonic:
        return "Sequential Single-Hue"
    elif hue_range > 0.01:
        return "Sequential Multi-Hue"
    else:
        # For borderline cases, check the standard deviation of hue differences
        if np.std(hue_diffs) < 0.02:  # Very consistent hue changes
            return "Sequential Single-Hue"
        else:
            return "Sequential Multi-Hue"


def plot_colormaps(cmap_list=None, ncols=3, group_by_type=True, group_spacing=0.5):
    """Plot a list of colormaps.
    When group_by_type=True, creates separate figures for each category and displays them automatically.
    Original source code: https://matplotlib.org/stable/users/explain/colors/colormaps.html

    Parameters
    ----------
    cmap_list : list, optional(default=None)
        List of colormap names.
    ncols : int, optional(default=3)
        Number of columns to display colormaps.
    group_by_type : bool, optional(default=True)
        If True, group colormaps by their type and create separate figures for each category.
        Each figure is automatically displayed.
    group_spacing : float, optional(default=0.5)
        Spacing between groups in inches (unused when group_by_type=True).
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object. When group_by_type=True, returns the last category's figure.
    axs : numpy.ndarray of matplotlib.axes.Axes
        Array of Axes objects. When group_by_type=True, returns the last category's axes.
    
    Examples
    --------
    >>> fig, axs = plot_colormaps(['viridis', 'plasma', 'inferno'], ncols=3)
    >>> plt.show()
    >>> # Group by type - creates separate figures for each category
    >>> fig, axs = plot_colormaps(ncols=3, group_by_type=True)
    """
    if cmap_list is None:
        cmap_list = list(mpl.colormaps.keys())
        cmap_list = [c for c in cmap_list if not c.endswith('_r')]

    # Convert colormaps to matplotlib colormaps if cmap is a string.
    cmap_list = [mpl.cm.get_cmap(c) if isinstance(c, str) else c for c in cmap_list]
    
    if group_by_type:
        # Define category order
        category_order = [
            "Sequential Single-Hue",
            "Sequential Multi-Hue",
            "Diverging",
            "Cyclical",
            "Categorical"
        ]
        
        # Classify colormaps by type
        categories = {category: [] for category in category_order}
        
        for cmap in cmap_list:
            category = classify_colormap(cmap)
            categories[category].append(cmap)
        
        # Remove empty categories
        categories = {k: v for k, v in categories.items() if v}
        
        # Create gradient for colormap display
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))
        
        # Sort categories according to the defined order
        sorted_categories = [cat for cat in category_order if cat in categories]
        
        # Create a separate figure for each category
        fig = None
        axs = None
        
        for category in sorted_categories:
            cmaps = categories[category]
            
            # Sort colormaps: dm prefix first, then alphabetical order
            cmaps.sort(key=lambda cmap: (0 if cmap.name.startswith('dm.') else 1, cmap.name.lower()))
            
            # Calculate number of rows needed for this category
            nrows = (len(cmaps) + ncols - 1) // ncols
            
            # Create figure with appropriate size for this category
            figw = 6.4 * ncols / 1.5  # Adjust width based on number of columns
            # Add extra height for category title
            figh = 0.35 + 0.15 + (nrows + 1 + (nrows + 1 - 1) * 0.1) * 0.44
            
            # Create a new figure for this category
            fig = plt.figure(figsize=(figw, figh))
            
            # Create GridSpec with one extra row for the title
            gs = plt.GridSpec(nrows + 1, ncols, figure=fig, height_ratios=[0.3] + [1] * nrows)
            
            axs = []
            
            # Add category title
            title_ax = fig.add_subplot(gs[0, :])
            title_ax.text(0.5, 0.5, category, fontsize=14, fontweight='bold',
                         ha='center', va='center', transform=title_ax.transAxes)
            title_ax.set_axis_off()
            axs.append(title_ax)
            
            # Add colormaps for this category (column-major order: top to bottom)
            for i, cmap in enumerate(cmaps):
                row = i % nrows
                col = i // nrows
                ax = fig.add_subplot(gs[row + 1, col])
                ax.imshow(gradient, aspect='auto', cmap=cmap)
                ax.text(-0.01, 0.5, cmap.name, va='center', ha='right', fontsize=10,
                       transform=ax.transAxes)
                ax.set_axis_off()
                axs.append(ax)
            
            # Hide unused subplots
            total_subplots = (nrows + 1) * ncols
            for i in range(len(axs), total_subplots):
                ax = fig.add_subplot(gs[i // ncols, i % ncols])
                ax.set_visible(False)
            
            plt.tight_layout()
            
            # Automatically display each category figure
            plt.show()
        
        # Convert axs to numpy array for consistency with non-grouped version
        if axs is not None:
            axs = np.array(axs)
        
    else:
        # Original non-grouped implementation
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))

        # Sort colormaps: dm prefix first, then alphabetical order
        cmap_list.sort(key=lambda cmap: (0 if cmap.name.startswith('dm.') else 1, cmap.name.lower()))

        # Calculate number of rows based on number of colormaps and columns
        nrows = (len(cmap_list) + ncols - 1) // ncols
        
        # Create figure and adjust figure dimensions based on layout
        figw = 6.4 * ncols / 1.5  # Adjust width based on number of columns
        figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.44
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figw, figh))
        fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                            left=0.2 / ncols, right=0.99)
        
        # Handle case when axs is a single Axes object (when nrows=ncols=1)
        if nrows == 1 and ncols == 1:
            axs = np.array([axs])
        
        # Flatten axs array for easier iteration
        axs = axs.flatten()

        # Map colormaps to subplots in column-major order (top to bottom)
        for i, cmap in enumerate(cmap_list):
            if i < len(axs):
                # Calculate position in column-major order
                row = i % nrows
                col = i // nrows
                ax_idx = row * ncols + col
                if ax_idx < len(axs):
                    ax = axs[ax_idx]
                    ax.imshow(gradient, aspect='auto', cmap=cmap)
                    ax.text(-0.01, 0.5, cmap.name, va='center', ha='right', fontsize=10,
                            transform=ax.transAxes)

        # Turn off all ticks & spines
        for ax in axs:
            ax.set_axis_off()
        
        # Hide unused subplots
        for i in range(len(cmap_list), len(axs)):
            axs[i].set_visible(False)
        
        plt.tight_layout()
    
    return fig, axs


def _load_color_library_names():
    """Load color names from opencolor.txt file.
    
    Returns
    -------
    opencolor_names : set
        Set of opencolor color names (without prefix).
    """
    # Get the asset/color directory path
    asset_dir = Path(__file__).parent / 'asset' / 'color'
    
    opencolor_names = set()
    
    # Load opencolor colors
    opencolor_file = asset_dir / 'opencolor.txt'
    if opencolor_file.exists():
        with open(opencolor_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if ':' in line:
                        name = line.split(':')[0].strip()
                        opencolor_names.add(name)
    
    return opencolor_names


# Cache the color library names
_OPENCOLOR_NAMES = _load_color_library_names()


def _classify_color_library(color_name):
    """Classify a color name into its library category.
    
    Parameters
    ----------
    color_name : str
        Color name to classify.
    
    Returns
    -------
    str
        Library category: 'opencolor', 'tw', 'md', 'ant', 'chakra', 'primer', 'other'
    """
    # Check for tw. prefix
    if color_name.startswith('tw.'):
        return 'tw'
    
    # Check for md. prefix (Material Design)
    if color_name.startswith('md.'):
        return 'md'
    
    # Check for ant. prefix (Ant Design)
    if color_name.startswith('ant.'):
        return 'ant'
    
    # Check for chakra. prefix (Chakra UI)
    if color_name.startswith('chakra.'):
        return 'chakra'
    
    # Check for primer. prefix (Primer)
    if color_name.startswith('primer.'):
        return 'primer'
    
    # Check for dm. prefix
    if color_name.startswith('dm.'):
        name_without_prefix = color_name[3:]  # Remove 'dm.' prefix
        
        # Check if it's an opencolor color (pattern: {color}{number})
        # Match pattern like gray0, red1, blue2, etc.
        if re.match(r'^[a-z]+\d+$', name_without_prefix):
            if name_without_prefix in _OPENCOLOR_NAMES:
                return 'opencolor'
        
        # Check if it's an xkcd color
        if name_without_prefix in _XKCD_NAMES:
            return 'xkcd'
    
    return 'other'


def _detect_color_weight_system(color_names):
    """Detect the weight system used in a group of color names.
    
    Parameters
    ----------
    color_names : list
        List of color names (may contain prefix like 'dm.', 'tw.', etc.)
    
    Returns
    -------
    int or None
        The minimum weight value (lightest color), or None if no numbers found.
    """
    weights = []
    for color_name in color_names:
        weight = _extract_number_from_color_name(color_name)
        if weight is not None:
            weights.append(weight)
    
    if weights:
        return min(weights)
    return None


def _detect_weight_range(color_names):
    """Detect the weight range used in a group of color names.
    
    Parameters
    ----------
    color_names : list
        List of color names (may contain prefix like 'dm.', 'tw.', etc.)
    
    Returns
    -------
    tuple or None
        Tuple of (min_weight, max_weight), or None if no weights found.
    """
    weights = []
    for color_name in color_names:
        weight = _extract_number_from_color_name(color_name)
        if weight is not None:
            weights.append(weight)
    
    if weights:
        return (min(weights), max(weights))
    return None


def _extract_base_color_name(color_name):
    """Extract base color name from color name.
    
    Parameters
    ----------
    color_name : str
        Color name (may contain prefix like 'dm.', 'tw.', etc.)
    
    Returns
    -------
    str
        Base color name (e.g., 'neutral', 'red', 'dark blue')
    """
    # Remove prefixes
    name = color_name
    for prefix in ['dm.', 'tw.', 'md.', 'ant.', 'chakra.', 'primer.']:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    
    # Pattern 1: format with colon (tw.blue:500, md.blue:500, ant.blue:5, etc.) -> 'blue'
    match = re.search(r'^([^:]+):', name)
    if match:
        return match.group(1)
    
    # Pattern 2: opencolor format (dm.red5) -> 'red'
    match = re.search(r'^([a-z]+)\d+$', name)
    if match:
        return match.group(1)
    
    # Pattern 3: other colors - keep full name
    return name


def _extract_number_from_color_name(color_name):
    """Extract number from color name if present.
    
    Parameters
    ----------
    color_name : str
        Color name (may contain prefix like 'dm.', 'tw.', etc.)
    
    Returns
    -------
    int or None
        Extracted number, or None if no number found.
    """
    # Remove prefixes
    name = color_name
    for prefix in ['dm.', 'tw.', 'md.', 'ant.', 'chakra.', 'primer.']:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    
    # Try to extract number from patterns like:
    # - gray0, red1 (opencolor)
    # - blue:500, gray:200 (tailwind, material design, chakra)
    # - blue:5, red:6 (ant design, primer)
    # - red5, blue2 (opencolor)
    
    # Pattern 1: format with colon (tw.blue:500, md.blue:500, ant.blue:5, etc.)
    match = re.search(r':(\d+)$', name)
    if match:
        return int(match.group(1))
    
    # Pattern 2: opencolor format (gray0, red1)
    match = re.search(r'(\d+)$', name)
    if match:
        return int(match.group(1))
    
    return None


def _remove_duplicate_colors(colors):
    """Remove duplicate colors based on RGB values.
    
    Parameters
    ----------
    colors : dict
        Dictionary mapping color names to color specifications.
    
    Returns
    -------
    dict
        Dictionary with duplicate colors removed (keeps first occurrence).
    """
    seen_rgb = {}
    result = {}
    
    for color_name, color_spec in colors.items():
        try:
            rgb = mcolors.to_rgb(color_spec)
            # Convert RGB tuple to string for comparison
            rgb_key = tuple(round(c, 6) for c in rgb)  # Round to avoid floating point issues
            
            if rgb_key not in seen_rgb:
                seen_rgb[rgb_key] = color_name
                result[color_name] = color_spec
        except (ValueError, TypeError):
            # If color conversion fails, keep it
            result[color_name] = color_spec
    
    return result


def _separate_colors_by_library(colors):
    """Separate colors by library.
    
    Parameters
    ----------
    colors : dict
        Dictionary mapping color names to color specifications.
    
    Returns
    -------
    dict
        Dictionary mapping library names to color dictionaries.
    """
    library_groups = {
        'opencolor': {},
        'tw': {},
        'md': {},
        'ant': {},
        'chakra': {},
        'primer': {},
        'other': {}
    }
    
    for color_name, color_spec in colors.items():
        library = _classify_color_library(color_name)
        library_groups[library][color_name] = color_spec
    
    # Remove empty libraries
    return {lib: colors_dict for lib, colors_dict in library_groups.items() 
            if colors_dict}


def _sort_colors_by_library(colors):
    """Sort colors by library, then by base color name and number/brightness.
    
    Parameters
    ----------
    colors : dict
        Dictionary mapping color names to color specifications.
    
    Returns
    -------
    list
        Sorted list of color names with library titles.
    """
    # Group colors by library
    library_groups = {
        'opencolor': [],
        'tw': [],
        'md': [],
        'ant': [],
        'chakra': [],
        'primer': [],
        'other': []
    }
    
    for color_name in colors:
        library = _classify_color_library(color_name)
        library_groups[library].append(color_name)
    
    # Sort each library group
    sorted_names = []
    
    # Library order: opencolor -> tw -> md -> ant -> chakra -> primer -> other
    library_labels = {
        'opencolor': 'OpenColor Colors',
        'tw': 'Tailwind Colors',
        'md': 'Material Design Colors',
        'ant': 'Ant Design Colors',
        'chakra': 'Chakra UI Colors',
        'primer': 'Primer Colors',
        'other': 'Other Colors'
    }
    
    for library in ['opencolor', 'tw', 'md', 'ant', 'chakra', 'primer', 'other']:
        color_list = library_groups[library]
        
        if not color_list:
            continue
        
        # Add library title
        sorted_names.append(('__TITLE__', library_labels[library]))
        
        # Group by base color name (e.g., 'neutral', 'red', 'blue')
        base_color_groups = defaultdict(list)
        for color_name in color_list:
            base_color = _extract_base_color_name(color_name)
            try:
                rgb = mcolors.to_rgb(colors[color_name])
                hsv = mcolors.rgb_to_hsv(rgb)
                base_color_groups[base_color].append((color_name, hsv))
            except (ValueError, TypeError):
                # If color conversion fails, put in a default group
                base_color_groups[base_color].append((color_name, (0, 0, 0)))
        
        # Sort base color groups alphabetically
        sorted_base_colors = sorted(base_color_groups.items())
        
        # Sort within each base color group
        for base_color, color_items in sorted_base_colors:
            # Sort by: number (if present), otherwise by HSV value (brightness)
            def sort_key(x):
                color_name, hsv = x
                number = _extract_number_from_color_name(color_name)
                if number is not None:
                    # If number exists, sort by number only (small -> large)
                    return (0, number)
                else:
                    # If no number, sort by HSV value (bright -> dark)
                    return (1, -hsv[2])  # Negative value for descending order
            
            color_items.sort(key=sort_key)
            
            sorted_names.extend([(name, colors[name]) for name, _ in color_items])
    
    return sorted_names


def _group_colors_by_hue(colors):
    """Group colors by HSV hue ranges for better visual organization.
    
    Parameters
    ----------
    colors : dict
        Dictionary mapping color names to color specifications.
    
    Returns
    -------
    list of dict
        List of color groups, each containing 'base_color', 'colors', and 'min_weight'.
        Groups are sorted by average hue.
    """
    # Define hue ranges for color groups (in degrees, 0-360)
    # Hue wraps around, so we handle reds specially (0-30 and 330-360)
    hue_ranges = [
        ('red', [(0, 30), (330, 360)]),
        ('orange', [(30, 50)]),
        ('yellow', [(50, 90)]),
        ('green', [(90, 150)]),
        ('cyan', [(150, 180)]),
        ('blue', [(180, 240)]),
        ('purple', [(240, 270)]),
        ('pink', [(270, 330)]),
    ]
    
    # Also handle grayscale colors (low saturation)
    color_items = []
    for color_name, color_spec in colors.items():
        try:
            rgb = mcolors.to_rgb(color_spec)
            hsv = mcolors.rgb_to_hsv(rgb)
            color_items.append((color_name, color_spec, hsv))
        except (ValueError, TypeError):
            color_items.append((color_name, color_spec, (0, 0, 0)))
    
    # Separate grayscale colors (saturation < 0.1)
    grayscale = []
    colored = []
    for name, spec, hsv in color_items:
        if hsv[1] < 0.1:  # Low saturation = grayscale
            grayscale.append((name, spec, hsv))
        else:
            colored.append((name, spec, hsv))
    
    # Group colored items by hue ranges
    hue_groups = defaultdict(list)
    for name, spec, hsv in colored:
        hue = hsv[0] * 360  # Convert to degrees
        assigned = False
        for group_name, ranges in hue_ranges:
            for min_hue, max_hue in ranges:
                # Handle red group which spans 0-30 and 330-360
                if group_name == 'red':
                    if (0 <= hue < 30) or (330 <= hue < 360):
                        hue_groups[group_name].append((name, spec, hsv))
                        assigned = True
                        break
                elif min_hue <= hue < max_hue:
                    hue_groups[group_name].append((name, spec, hsv))
                    assigned = True
                    break
            if assigned:
                break
        if not assigned:
            # Fallback: assign to nearest group
            hue_groups['other'].append((name, spec, hsv))
    
    # Add grayscale group
    if grayscale:
        hue_groups['grayscale'] = grayscale
    
    # Sort groups by average hue, and colors within groups by brightness/value
    color_groups = []
    
    for group_name, items in hue_groups.items():
        if not items:
            continue
        
        # Calculate average hue for group (for sorting)
        if group_name == 'grayscale':
            avg_hue = -1  # Grayscale goes first (negative to sort before others)
        elif group_name == 'other':
            avg_hue = 1000  # Other goes last
        else:
            hues = [hsv[0] * 360 for _, _, hsv in items]
            # Normalize hues for red group (handle wrap-around)
            if group_name == 'red':
                normalized_hues = [h if h < 180 else h - 360 for h in hues]
                avg_hue = sum(normalized_hues) / len(normalized_hues)
            else:
                avg_hue = sum(hues) / len(hues)
        
        # Sort within group by brightness/value (light to dark)
        items.sort(key=lambda x: -x[2][2])  # Sort by value (brightness), descending
        
        color_groups.append({
            'base_color': group_name,
            'colors': [(name, spec) for name, spec, _ in items],
            'min_weight': None,  # Not applicable for hue-based grouping
            'avg_hue': avg_hue
        })
    
    # Sort groups by average hue (grayscale first, then by hue order)
    color_groups.sort(key=lambda g: g['avg_hue'])
    
    return color_groups


def _plot_single_library(colors, library_name, ncols=6, sort_colors=True):
    """Plot colors for a single library.
    
    Parameters
    ----------
    colors : dict
        Dictionary mapping color names to color specifications.
    library_name : str
        Name of the library (for title).
    ncols : int, optional
        Number of columns in the color grid, default is 6.
    sort_colors : bool, optional
        If True, sorts colors by base color name and number/brightness.
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure containing the color grid.
    """
    if not colors:
        return None
    
    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12
    
    # Sort colors within library
    if sort_colors:
        # Group by base color name (for opencolor, tailwind, etc.)
            base_color_groups = defaultdict(list)
            for color_name in colors:
                base_color = _extract_base_color_name(color_name)
                try:
                    rgb = mcolors.to_rgb(colors[color_name])
                    hsv = mcolors.rgb_to_hsv(rgb)
                    base_color_groups[base_color].append((color_name, hsv))
                except (ValueError, TypeError):
                    base_color_groups[base_color].append((color_name, (0, 0, 0)))
            
            # Sort base color groups alphabetically
            sorted_base_colors = sorted(base_color_groups.items())
            
            # Sort within each base color group and create groups with lightest color info
            color_groups = []
            for base_color, color_items in sorted_base_colors:
                def sort_key(x):
                    color_name, hsv = x
                    number = _extract_number_from_color_name(color_name)
                    if number is not None:
                        return (0, number)
                    else:
                        return (1, -hsv[2])
                
                color_items.sort(key=sort_key)
                sorted_names = [name for name, _ in color_items]
                
                # Detect weight system for this group
                min_weight = _detect_color_weight_system(sorted_names)
                weight_range = _detect_weight_range(sorted_names)
                
                color_groups.append({
                    'base_color': base_color,
                    'colors': [(name, colors[name]) for name in sorted_names],
                    'min_weight': min_weight,
                    'weight_range': weight_range
                })
    else:
        # If not sorting, treat all colors as one group
        color_groups = [{
            'base_color': 'all',
            'colors': [(name, colors[name]) for name in colors],
            'min_weight': None,
            'weight_range': None
        }]
    
    # Add space for title at the top with margin below title
    title_height = cell_height
    title_margin = 0.5  # Margin below title (in cell_height units)
    
    # Place colors group-by-group, ensuring each column starts with a group's lightest color
    # and ends with its darkest color. Each group must be placed completely in one column.
    # Add spacing between groups with different weight ranges or different base colors.
    color_grid = []  # List of (col, row, name, color_spec) tuples
    column_heights = [0] * ncols  # Track current height of each column
    prev_weight_range = None  # Track previous group's weight range
    prev_base_color_per_col = [None] * ncols  # Track previous base_color for each column
    
    for group_idx, group in enumerate(color_groups):
        group_colors = group['colors']
        group_size = len(group_colors)
        current_weight_range = group.get('weight_range')
        current_base_color = group.get('base_color')
        
        # Find the column with the least height to place this entire group
        # This ensures groups are not split across columns and each column
        # starts with a group's lightest color (weight 0) and ends with its darkest color (weight 9)
        min_height_col = min(range(ncols), key=lambda c: column_heights[c])
        target_col = min_height_col
        
        # Add spacing row when:
        # 1. Transitioning between different weight ranges (in any column)
        # 2. Transitioning between different base colors (in the target column)
        should_add_spacing = False
        
        if prev_weight_range is not None and current_weight_range is not None:
            if prev_weight_range != current_weight_range:
                # Different weight ranges - add spacing in all columns
                should_add_spacing = True
        
        if prev_base_color_per_col[target_col] is not None:
            if prev_base_color_per_col[target_col] != current_base_color:
                # Different base color in the same column - add spacing in target column
                column_heights[target_col] += 1
        
        if should_add_spacing:
            # Add empty row for spacing in all columns
            for col in range(ncols):
                column_heights[col] += 1
        
        # Place all colors from this group in the target column
        # The first color (lightest, weight 0) will be at the start of the column
        # The last color (darkest, weight 9) will be at the end of the column
        for color_idx, (name, color_spec) in enumerate(group_colors):
            row = column_heights[target_col]
            color_grid.append((target_col, row, name, color_spec))
            column_heights[target_col] += 1
        
        # Update previous values for next iteration
        prev_weight_range = current_weight_range
        prev_base_color_per_col[target_col] = current_base_color
    
    # Calculate actual number of rows needed based on column heights
    nrows = max(column_heights) if column_heights else 0
    
    width = cell_width * ncols + 2 * margin
    # Add title margin to total height
    total_title_height = title_height + title_margin * cell_height
    # Add extra space at bottom to ensure last row is fully visible
    bottom_extra_margin = 0.5 * cell_height
    height = cell_height * nrows + 2 * margin + total_title_height + bottom_extra_margin
    dpi = 72
    
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-margin)/height)
    ax.set_xlim(0, cell_width * ncols)
    # Adjust y-axis limits to account for title margin
    # Add extra space at bottom to ensure last row is fully visible
    bottom_extra_margin = 0.5 * cell_height
    ax.set_ylim(-total_title_height, cell_height * nrows + bottom_extra_margin)
    ax.invert_yaxis()  # Ensure smaller y-values render toward the top edge
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()
    
    # Add library title at the top (no background, like plot_colormaps)
    library_labels = {
        'opencolor': 'OpenColor Colors',
        'tw': 'Tailwind Colors',
        'md': 'Material Design Colors',
        'ant': 'Ant Design Colors',
        'chakra': 'Chakra UI Colors',
        'primer': 'Primer Colors',
        'other': 'Other Colors'
    }
    title_text = library_labels.get(library_name, library_name)
    title_y = -title_height / 2
    ax.text(
        cell_width * ncols / 2,
        title_y,
        title_text,
        fontsize=14,
        fontweight='bold',
        horizontalalignment='center',
        verticalalignment='center'
    )
    
    # Draw the grid using the group-aware placement
    # Colors start after title margin
    title_margin_offset = title_margin * cell_height
    for col, row, name, color_spec in color_grid:
        y = title_margin_offset + (row + 0.5) * cell_height
        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7
        
        ax.text(
            text_pos_x,
            y,
            name,
            fontsize=14,
            horizontalalignment='left',
            verticalalignment='center'
        )
        
        ax.add_patch(
            Rectangle(
                xy=(swatch_start_x, y - 9),
                width=swatch_width,
                height=18,
                facecolor=color_spec,
                edgecolor='0.7'
            )
        )
    
    return fig


def plot_colors(colors=None, *, ncols=6, sort_colors=True):
    """Plot a grid of named colors with their names.
    
    Creates separate plots for each color library (opencolor, tw/tailwind, other).
    
    Parameters
    ----------
    colors : dict, optional
        Dictionary mapping color names to color specifications.
        If None, uses all named colors from matplotlib except those
        starting with 'dartwork_mpl.'.
    ncols : int, optional
        Number of columns in the color grid, default is 6.
    sort_colors : bool, optional
        If True, sorts colors by base color name (e.g., 'neutral', 'red', 'blue'),
        and finally by number (small -> large) or HSV value (bright -> dark).
        Duplicate colors (same RGB values) are automatically removed.
        If False, uses the order from the input dictionary.
    
    Returns
    -------
    list of matplotlib.figure.Figure
        List of figures, one for each color library.
        
    Examples
    --------
    >>> figs = plot_colors()
    >>> plt.show()
    >>> # Custom colors
    >>> custom_colors = {'red': '#FF0000', 'green': '#00FF00', 'blue': '#0000FF'}
    >>> figs = plot_colors(custom_colors, ncols=3)
    >>> plt.show()
    """
    # # Ensure ncols is 6 if not explicitly provided
    # # This is a safeguard in case the default value isn't being used due to caching
    # if ncols == 4:  # If somehow the old default is being used
    #     ncols = 6
    
    if colors is None:
        colors = {
            k: v for k, v in mcolors.get_named_colors_mapping().items()
            if not k.startswith('dartwork_mpl.')
        }

    # Separate colors by library first, then remove duplicates within each library
    # This preserves colors from different libraries even if they have the same RGB values
    library_colors = _separate_colors_by_library(colors)
    
    # Remove duplicates within each library separately
    # Note: For tailwind colors and similar systems, we don't remove duplicates because different color names
    # (e.g., zinc:50 and neutral:50) may have the same RGB values but serve different purposes
    skip_duplicate_removal = {'tw', 'md', 'ant', 'chakra', 'primer'}
    for library_name in library_colors:
        if library_name not in skip_duplicate_removal:
            library_colors[library_name] = _remove_duplicate_colors(library_colors[library_name])
    
    # Library order: opencolor -> tw -> md -> ant -> chakra -> primer -> other (xkcd last)
    library_order = ['opencolor', 'tw', 'md', 'ant', 'chakra', 'primer', 'other']
    
    # Create a separate plot for each library
    figures = []
    for library_name in library_order:
        if library_name in library_colors:
            fig = _plot_single_library(
                library_colors[library_name], 
                library_name, 
                ncols=ncols, 
                sort_colors=sort_colors
            )
            if fig is not None:
                figures.append(fig)
    
    return figures


def plot_fonts(font_dir=None, ncols=3, font_size=11):
    """Plot available fonts in the specified directory.
    
    Parameters
    ----------
    font_dir : str, optional
        Directory path containing font files. If None, defaults to the 'asset/font' 
        directory within the package.
    ncols : int, optional
        Number of columns to display font families, by default 3
    font_size : int, optional
        Font size for sample text, by default 11
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object
    """
    if font_dir is None:
        font_dir = os.path.join(os.path.dirname(__file__), 'asset', 'font')

    # 폰트 파일 리스트 가져오기
    font_files = [f for f in os.listdir(font_dir) if f.endswith('.ttf')]

    # 폰트 패밀리별로 그룹화
    font_families = defaultdict(list)
    for font in font_files:
        family = font.split('-')[0]
        font_families[family].append(font)

    # 각 패밀리 내에서 폰트 정렬 함수
    def sort_fonts(fonts):
        """
        Sort font files by weight and style within a font family.
        
        Parameters
        ----------
        fonts : list
            List of font file names to sort.
            
        Returns
        -------
        list
            Sorted list of font files, ordered by weight (Thin to Black)
            and then by style (regular before italic).
        """
        weight_order = {
            'Thin': 1,
            'ExtraLight': 2,
            'Light': 3,
            'Regular': 4,
            'Medium': 5,
            'SemiBold': 6,
            'Bold': 7,
            'ExtraBold': 8,
            'Black': 9
        }
        
        def get_weight_score(font):
            base_weight = 4  # Regular 기본값
            italic_score = 0.5 if 'Italic' in font else 0
            
            for weight, score in weight_order.items():
                if weight in font:
                    base_weight = score
                    break
                    
            return (base_weight, italic_score)
        
        return sorted(fonts, key=get_weight_score)

    # 패밀리별로 정렬
    sorted_families = sorted(font_families.items())

    # 전체 폰트 개수와 열 수 설정
    total_families = len(sorted_families)
    families_per_column = math.ceil(total_families / ncols)

    # 패밀리 간 간격 설정
    family_spacing = 3  # 패밀리 간 간격
    max_fonts_in_family = max(len(fonts) for _, fonts in sorted_families)

    # 그래프 크기 설정 (패밀리 간 간격 포함)
    total_height = families_per_column * (max_fonts_in_family + family_spacing)
    fig, ax = plt.subplots(figsize=(14, total_height * 0.3))
    
    # 축 설정
    ax.set_xlim(0, ncols * 7)
    ax.set_ylim(0, total_height)
    ax.axis('off')

    # 각 열별로 폰트 패밀리 출력
    for family_idx, (family, fonts) in enumerate(sorted_families):
        # 열과 행 위치 계산
        column = family_idx // families_per_column
        family_row = family_idx % families_per_column
        
        # x 위치는 열 번호에 따라 조정
        x_pos = column * 7
        
        # y 위치 계산 (패밀리 간 간격 포함)
        base_y_pos = family_row * (max_fonts_in_family + family_spacing)
        
        # 패밀리 제목 출력 (밑줄 추가)
        title_y = base_y_pos + max_fonts_in_family + 0.5
        ax.text(x_pos, title_y, f"Font Family: {family}", size=12, weight='bold')
        ax.plot([x_pos, x_pos + 6], [title_y - 0.3, title_y - 0.3], 
                color='lightgray', linestyle='-', linewidth=0.5)
        
        # 정렬된 폰트 출력
        sorted_fonts = sort_fonts(fonts)
        for font_idx, font_file in enumerate(sorted_fonts):
            font_path = os.path.join(font_dir, font_file)
            font_name = os.path.splitext(font_file)[0]
            
            font_prop = fm.FontProperties(fname=font_path)
            
            y_pos = base_y_pos + (max_fonts_in_family - font_idx - 1)
            
            ax.text(x_pos, y_pos, f'This font is "{font_name}"', 
                    fontproperties=font_prop, size=font_size)
    
    return fig