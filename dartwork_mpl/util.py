from xml.dom import minidom
from tempfile import NamedTemporaryFile

import matplotlib.pyplot as plt

from IPython.display import display, HTML, SVG


def cm2in(cm):
    return cm / 2.54


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
            image_path = f.name

            fig.savefig(image_path, bbox_inches=None)
            plt.close(fig)

            show(image_path)
    else:
        fig.savefig(image_path, bbox_inches=None)
        plt.close(fig)

        show(image_path)