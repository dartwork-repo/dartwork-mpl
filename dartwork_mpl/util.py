import base64

from xml.dom import minidom
from tempfile import NamedTemporaryFile
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from matplotlib.transforms import ScaledTranslation
from IPython.display import display, HTML, SVG


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


def use_dmpl_style():
    plt.style.use(Path(__file__).parent / 'paper.mplstyle')    


def cm2in(cm):
    return cm / 2.54


def make_offset(x, y, fig):
    dx, dy = x / 72, y / 72
    offset = ScaledTranslation(dx, dy, fig.dpi_scale_trans)

    return offset


def save_formats(fig, image_stem, formats=('svg', 'png', 'pdf', 'eps'), bbox_inches=None, **kwargs):
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
    svg_obj.data = svg_obj.data.replace(f'width="{width}{unit}"', f'width="{desired_width}{unit}"')
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
        fig.savefig(image_path, bbox_inches=None)
        plt.close(fig)

        show(image_path, size=size, unit=unit)
