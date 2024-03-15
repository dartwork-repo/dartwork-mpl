from xml.dom import minidom
from tempfile import NamedTemporaryFile
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from matplotlib.transforms import ScaledTranslation
from IPython.display import display, HTML, SVG
from scipy.optimize import minimize

# Will be replaced to rich print.
PRINT = print


def _create_parent_path_if_not_exists(path):
    path = Path(path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
        print(f'Created a directory: {path.parent}')


def set_decimal(ax, xn=None, yn=None):
    if xn is not None:
        xticks = ax.get_xticks()
        ax.set_xticks(xticks)
        ax.set_xticklabels([f'{x:.{xn}f}' for x in xticks])
        
    if yn is not None:
        yticks = ax.get_yticks()
        ax.set_yticks(yticks)
        ax.set_yticklabels([f'{y:.{yn}f}' for y in yticks])


def get_bounding_box(boxes):
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

    margins = np.array(margins) * fig.get_dpi()

    def fun(x):
        # print(gs.left, gs.right, gs.bottom, gs.top)
        gs.update(left=x[0], right=x[1], bottom=x[2], top=x[3])

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

        loss = np.square((values - targets) / scales).sum()
 
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
    """
    return plt.rcParams['font.size'] + n


def mix_colors(color1, color2, alpha=0.5):
    """
    Mix two colors.
    """
    color1 = mcolors.to_rgb(color1)
    color2 = mcolors.to_rgb(color2)

    return tuple(alpha * c1 + (1 - alpha) * c2 for c1, c2 in zip(color1, color2))


def pseudo_alpha(color, alpha=0.5, background='white'):
    """
    Return a color with pseudo alpha.
    """
    return mix_colors(color, background, alpha=alpha)


def use_style(name='dmpl'):
    path = Path(__file__).parent / f'asset/mplstyle/{name}.mplstyle'
    if not path.exists():
        raise ValueError(f'Not found style: {name}')

    plt.style.use(path)    


def use_dmpl_style():
    use_style('dmpl')


def cm2in(cm):
    return cm / 2.54


def make_offset(x, y, fig):
    dx, dy = x / 72, y / 72
    offset = ScaledTranslation(dx, dy, fig.dpi_scale_trans)

    return offset


def save_formats(fig, image_stem, formats=('svg', 'png', 'pdf', 'eps'), bbox_inches=None, **kwargs):
    _create_parent_path_if_not_exists(image_stem)
    for fmt in formats:
        fig.savefig(f'{image_stem}.{fmt}', bbox_inches=bbox_inches, **kwargs)


def show(image_path, size=600, unit='pt'):
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


def save_and_show(fig, image_path=None, size=600, unit='pt'):
    if image_path is None:
        with NamedTemporaryFile(suffix='.svg') as f:
            f.close()
            image_path = f.name

            fig.savefig(image_path, bbox_inches=None)
            plt.close(fig)

            show(image_path, size=size, unit=unit)
    else:
        _create_parent_path_if_not_exists(image_path)
        fig.savefig(image_path, bbox_inches=None)
        plt.close(fig)

        show(image_path, size=size, unit=unit)


def plot_colormaps(cmap_list=None):
    """Plot a list of colormaps in a single figure.
    Original source code: https://matplotlib.org/stable/users/explain/colors/colormaps.html

    Parameters
    ----------
    cmap_list : list, optional(default=None)
        List of colormap names.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object.
    axs : list of matplotlib.axes.Axes
    """
    if cmap_list is None:
        cmap_list = list(mpl.colormaps.keys())
        cmap_list = [c for c in cmap_list if not c.endswith('_r')]

    # Convert colormaps to matplotlib colormaps if cmap is a string.
    cmap_list = [mpl.cm.get_cmap(c) if isinstance(c, str) else c for c in cmap_list]

    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                        left=0.2, right=0.99)
    # axs[0].set_title(f'{category} colormaps', fontsize=14)

    for ax, cmap in zip(axs, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=cmap)
        ax.text(-0.01, 0.5, cmap.name, va='center', ha='right', fontsize=10,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()

    return fig, axs