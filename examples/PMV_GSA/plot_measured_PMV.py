# %% load library

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import dartwork_mpl as dm
import os
from matplotlib.path import Path

# dartwork_mpl에서 제공하는 cm2in 함수와 pseudo_alpha 함수 사용
from dartwork_mpl.util import cm2in, fw


# %% plotting style
# dartwork_mpl 스타일 적용
dm.use_style("dmpl_light")

# 네 방향 모두 spine 추가
plt.rcParams['axes.spines.top'] = True
plt.rcParams['axes.spines.right'] = True
plt.rcParams['axes.spines.bottom'] = True
plt.rcParams['axes.spines.left'] = True

# 축 레이블 폰트 굵기 설정
plt.rcParams['axes.labelweight'] = dm.fw(1)




# %% load data
# occup_ratio.csv 파일 불러오기
data_path = "./measured_data/"  
df_occup = pd.read_csv(data_path + "occup_ratio.csv")

# 데이터를 분 단위로 변환 
df_occup = df_occup * 60


# %% Plotting

# 그래프 설정값 (필요시 수정)
FIGSIZE = (8.8, 7.0)  # 그래프 크기 (cm)
BAR_WIDTH = 0.65       # 막대 너비
BAR_SPACING = 0.3     # 막대 사이 간격
COLORS = {
    'bar': "dm.teal3",      # 기본 막대 색상
    'special': "dm.red3", # 특별 값 색상
    'edge': "dm.gray8"      # 테두리 색상
}
YLIM = (0, 0.35)      # y축 범위
SAVE_PATH = "./figure_output/occupancy_duration_probability"  # 저장 경로
SAVE_FORMATS = ('pdf', 'png')  # 저장 형식
DPI = 300             # 저장 해상도

# 10분 간격의 bin 설정 (0 구간 제외)
bins = [0, 10, 20, 30, 40, 50, 60]
bin_labels = [
    "(0, 10]",
    "(10, 20]",
    "(20, 30]",
    "(30, 40]",
    "(40, 50]",
    "(50, 60]",
]

# 0이 아닌 값만 필터링
non_zero_values = df_occup.values[df_occup.values > 0]

# 히스토그램 계산 (정규화된 확률 분포)
hist, bin_edges = np.histogram(non_zero_values, bins=bins, density=True)

# 각 bin의 너비 계산
bin_widths = np.diff(bin_edges)

# 각 bin의 확률 계산 (밀도 * 너비 = 확률)
probabilities = hist * bin_widths

# 확률 합이 1이 되도록 정규화
probabilities = probabilities / np.sum(probabilities)

# 특별 값 처리 (정확히 60분인 데이터)
special_value = 60
special_count = np.sum(df_occup.values == special_value)
special_bin_idx = len(bins) - 2  # 마지막 구간 (50, 60]
special_bin_count = np.sum((df_occup.values > 50) & (df_occup.values <= 60))

# 마지막 구간에서 정확히 60분인 데이터의 비율
if special_bin_count > 0:
    special_ratio = special_count / special_bin_count
else:
    special_ratio = 0

# 그래프 그리기
fig, ax = plt.subplots(figsize=(dm.cm2in(FIGSIZE[0]), dm.cm2in(FIGSIZE[1])))

# 히스토그램 그리기 (확률 분포로 정규화)
bars = ax.bar(
    range(len(bin_labels)),
    probabilities,
    width=BAR_WIDTH,
    color=COLORS['bar'],
    linewidth=0.3,
    edgecolor=COLORS['edge'],
    bottom=0,
    label="Probability of occupancy within interval",
    zorder=3  # 그리드(zorder=0)보다 높은 값으로 설정
)


# 마지막 막대에 특별 색상 부분 추가 (정확히 60분인 데이터 비율)
if special_ratio > 0:
    last_bar = bars[special_bin_idx]
    last_bar_height = last_bar.get_height()
    
    # 특별 값의 높이 계산
    special_height = last_bar_height * special_ratio
    
    # 특별 값 부분 추가
    special_bar = ax.bar(
        special_bin_idx,
        special_height,
        width=BAR_WIDTH,
        color=COLORS['special'],
        edgecolor=COLORS['edge'],
        linewidth=0.3,
        bottom=last_bar_height - special_height,
        label="Continuous 60-min occupancy fraction in (50, 60]",
        zorder=4  # 일반 막대(zorder=3)보다 높게 설정
    )

# x축, y축 레이블 설정
ax.set_xlabel("Occupancy duration [min]", fontsize=dm.fs(0))
ax.set_ylabel("Probability mass", fontsize=dm.fs(0))

# x축 눈금 설정
ax.set_xticks(range(len(bin_labels)))
ax.set_xticklabels(bin_labels, fontsize=dm.fs(0))

# 그리드 추가
ax.grid(True, linestyle=":", axis="y", zorder=0)  # zorder를 낮게 설정하여 뒤에 그려지도록 함

# ylim 설정
ax.set_ylim(YLIM)

# xlim 설정 (막대 사이 간격 고려)
left_margin = 0 - (BAR_WIDTH / 2) - BAR_SPACING
right_margin = (len(bin_labels) - 1) + (BAR_WIDTH / 2) + BAR_SPACING
ax.set_xlim(left_margin, right_margin)

# x축 minor tick 제거
ax.xaxis.set_minor_locator(ticker.NullLocator())

# y축 minor tick 설정 (메이저 틱 사이에 하나씩)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(1))

# 스파인 zorder 설정 (그리드보다 위에 그려지도록)
for spine in ax.spines.values():
    spine.set_zorder(5)

# 레이아웃 최적화
dm.simple_layout(fig)

# 범례 추가
ax.legend(loc='best', fontsize=dm.fs(-1.2))

# 그래프 저장
# 디렉토리 확인 및 생성
output_dir = os.path.dirname(SAVE_PATH)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 저장
dm.save_formats(fig, SAVE_PATH, formats=SAVE_FORMATS, bbox_inches="tight", dpi=DPI)

# 그래프 표시
plt.show()

# 통계 정보 출력
print(f"평균 재실 시간 (0 제외): {non_zero_values.mean():.3f} 분")
print(f"최대 재실 시간: {non_zero_values.max():.3f} 분")
print(f"최소 재실 시간 (0 제외): {non_zero_values.min():.3f} 분")

# 각 구간별 확률 출력
print("\n구간별 확률:")
for i, (label, prob) in enumerate(zip(bin_labels, probabilities)):
    print(f"{label}: {prob:.4f} ({prob*100:.2f}%)")

# 특별 값(60분) 정보 출력
print(f"\n정확히 60분인 데이터 수: {special_count}")
print(f"(50, 60] 구간 데이터 수: {special_bin_count}")
print(
    f"(50, 60] 구간에서 정확히 60분인 데이터 비율: {special_ratio:.4f} ({special_ratio*100:.2f}%)"
)

# %%
