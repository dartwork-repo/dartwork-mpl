import os
import math
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
    use_all_axes=False,
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
    use_all_axes : bool, optional(default=False)
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


def pseudo_alpha(color, alpha=0.5, background='white'):
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


style = Style()


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
    sat_diffs = np.diff(saturations)
    value_diffs = np.diff(values)
    
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
    """Plot a list of colormaps in a single figure.
    Original source code: https://matplotlib.org/stable/users/explain/colors/colormaps.html

    Parameters
    ----------
    cmap_list : list, optional(default=None)
        List of colormap names.
    ncols : int, optional(default=3)
        Number of columns to display colormaps.
    group_by_type : bool, optional(default=True)
        If True, group colormaps by their type.
    group_spacing : float, optional(default=0.5)
        Spacing between groups in inches.
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object.
    axs : numpy.ndarray of matplotlib.axes.Axes
        Array of Axes objects.
    
    Examples
    --------
    >>> fig, axs = plot_colormaps(['viridis', 'plasma', 'inferno'], ncols=3)
    >>> plt.show()
    >>> # Group by type
    >>> fig, axs = plot_colormaps(ncols=3, group_by_type=True)
    >>> plt.show()
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
        
        # Create a new figure
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))
        
        # Calculate total number of colormaps and rows needed
        total_rows = 0
        category_rows = {}
        
        for category, cmaps in categories.items():
            rows = (len(cmaps) + ncols - 1) // ncols
            category_rows[category] = rows
            total_rows += rows
        
        # Add extra rows for category titles and spacing
        total_rows_with_titles = total_rows + len(categories)
        
        # Create figure with appropriate size
        figw = 6.4 * ncols / 1.5  # Adjust width based on number of columns
        # Add extra height for category titles and spacing
        figh = 0.35 + 0.15 + (total_rows_with_titles + (total_rows_with_titles - 1) * 0.1) * 0.22 + len(categories) * group_spacing
        
        fig = plt.figure(figsize=(figw, figh))
        
        # Create a single GridSpec for the entire figure
        gs = plt.GridSpec(total_rows_with_titles, ncols, figure=fig)
        
        # Start position for the first subplot
        current_row = 0
        axs = []
        
        # Sort categories according to the defined order
        sorted_categories = [cat for cat in category_order if cat in categories]
        
        for category in sorted_categories:
            cmaps = categories[category]
            
            # Add category title
            title_ax = fig.add_subplot(gs[current_row, :])
            title_ax.text(0.5, 0.5, category, fontsize=14, fontweight='bold',
                         ha='center', va='center', transform=title_ax.transAxes)
            title_ax.set_axis_off()
            axs.append(title_ax)
            current_row += 1
            
            # Calculate rows needed for this category
            rows_needed = category_rows[category]
            
            # Add colormaps for this category
            for i, cmap in enumerate(cmaps):
                row = i // ncols
                col = i % ncols
                ax = fig.add_subplot(gs[current_row + row, col])
                ax.imshow(gradient, aspect='auto', cmap=cmap)
                ax.text(-0.01, 0.5, cmap.name, va='center', ha='right', fontsize=10,
                       transform=ax.transAxes)
                ax.set_axis_off()
                axs.append(ax)
            
            # Update current row
            current_row += rows_needed
        
        # Convert axs to numpy array for consistency with non-grouped version
        axs = np.array(axs)
        
    else:
        # Original non-grouped implementation
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))

        # Calculate number of rows based on number of colormaps and columns
        nrows = (len(cmap_list) + ncols - 1) // ncols
        
        # Create figure and adjust figure dimensions based on layout
        figw = 6.4 * ncols / 1.5  # Adjust width based on number of columns
        figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figw, figh))
        fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                            left=0.2 / ncols, right=0.99)
        
        # Handle case when axs is a single Axes object (when nrows=ncols=1)
        if nrows == 1 and ncols == 1:
            axs = np.array([axs])
        
        # Flatten axs array for easier iteration
        axs = axs.flatten()

        for i, cmap in enumerate(cmap_list):
            if i < len(axs):
                ax = axs[i]
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


def plot_colors(colors=None, *, ncols=4, sort_colors=True):
    """Plot a grid of named colors with their names.
    
    Parameters
    ----------
    colors : dict, optional
        Dictionary mapping color names to color specifications.
        If None, uses all named colors from matplotlib except those
        starting with 'dartwork_mpl.'.
    ncols : int, optional
        Number of columns in the color grid, default is 4.
    sort_colors : bool, optional
        If True, sorts colors by hue, saturation, and value.
        If False, uses the order from the input dictionary.
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure containing the color grid.
        
    Examples
    --------
    >>> fig = plot_colors()
    >>> plt.show()
    >>> # Custom colors
    >>> custom_colors = {'red': '#FF0000', 'green': '#00FF00', 'blue': '#0000FF'}
    >>> fig = plot_colors(custom_colors, ncols=3)
    >>> plt.show()
    """
    if colors is None:
        colors = {
            k: v for k, v in mcolors.get_named_colors_mapping().items()
            if not k.startswith('dartwork_mpl.')
        }

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12

    # Sort colors by hue, saturation, value and name.
    if sort_colors is True:
        names = sorted(
            colors, key=lambda c: tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(c))))
    else:
        names = list(colors)

    n = len(names)
    nrows = math.ceil(n / ncols)

    width = cell_width * ncols + 2 * margin
    height = cell_height * nrows + 2 * margin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-margin)/height)
    ax.set_xlim(0, cell_width * ncols)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(
            Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                      height=18, facecolor=colors[name], edgecolor='0.7')
        )

    return fig


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