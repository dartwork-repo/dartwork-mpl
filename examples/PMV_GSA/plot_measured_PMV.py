# %% load library

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import dartwork_mpl as dm
import os
from matplotlib.path import Path
import sys
from pathlib import Path

# 현재 스크립트 경로 가져오기
script_path = Path(os.path.abspath(__file__))
script_dir = script_path.parent

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




#%% load data for occupancy duration probability
# occup_ratio.csv 파일 불러오기
data_path = script_dir / "measured_data"
df_occup = pd.read_csv(data_path / "occup_ratio.csv")

# 데이터를 분 단위로 변환 
df_occup = df_occup * 60


# %% Plotting occupancy duration probability

# 그래프 설정값 (필요시 수정)
FIGSIZE = (8.8, 7.0)  # 그래프 크기 (cm)
BAR_WIDTH = 0.6       # 막대 너비 (마진 없이 설정)
BAR_SPACING = 0.3     # 막대 사이 간격
COLORS = {
    'bar': "dm.teal3",      # 기본 막대 색상
    'special': "dm.red3",   # 특별 값 색상
    'edge': "dm.teal3",     # 테두리 색상
    'last_edge': "dm.teal3" # 마지막 막대 테두리 색상
}
YLIM = (0, 0.35)      # y축 범위
SAVE_PATH = script_dir / "figure_output" / "occupancy_duration_probability"  # 저장 경로
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
    range(len(probabilities)),
    probabilities,
    width=BAR_WIDTH,
    color=COLORS['bar'],
    linewidth=1.0,
    edgecolor=COLORS['edge'],
    bottom=0,
    label="Probability of occupancy within interval",
    zorder=3  # 그리드(zorder=0)보다 높은 값으로 설정
)


# 마지막 막대에 특별 색상 부분 추가 (정확히 60분인 데이터 비율)
if special_ratio > 0:
    last_bar = bars[special_bin_idx]
    last_bar_height = last_bar.get_height()
    
    # 마지막 막대의 테두리 색상 변경
    last_bar.set_edgecolor(COLORS['last_edge'])
    
    # 특별 값의 높이 계산
    special_height = last_bar_height * special_ratio
    
    # 특별 값 부분 추가
    special_bar = ax.bar(
        special_bin_idx,
        special_height,
        width=BAR_WIDTH,
        color=COLORS['special'],
        edgecolor=COLORS['last_edge'],
        linewidth=1.0,
        bottom=last_bar_height - special_height,
        label="Fraction of continuous 60-min occupancy in (50, 60]",
        zorder=4  # 일반 막대(zorder=3)보다 높게 설정
    )

# x축, y축 레이블 설정
ax.set_xlabel("Occupancy duration intervals [min]", fontsize=dm.fs(0))
ax.set_ylabel("Probability", fontsize=dm.fs(0))

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
output_dir = SAVE_PATH.parent
if not output_dir.exists():
    output_dir.mkdir(parents=True, exist_ok=True)

# 저장
dm.save_formats(fig, str(SAVE_PATH), formats=SAVE_FORMATS, bbox_inches="tight", dpi=DPI)

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

#%% load data for away event count histogram
# away_event_count.csv 파일 불러오기
data_path = script_dir / "measured_data"
df_away_event = pd.read_csv(data_path / "away_event_count.csv")


#%% Plotting away event count histogram
# 그래프 설정값 (필요시 수정)
FIGSIZE = (8.8, 7.0)  # 그래프 크기 (cm)
BAR_WIDTH = 0.8       # 막대 너비 (마진 없이 설정)
COLORS = {
    'bar': "dm.teal3",      # 기본 막대 색상
    'edge': "dm.gray8"      # 테두리 색상
}
YLIM = (0, 0.4)      # y축 범위
SAVE_PATH = script_dir / "figure_output" / "away_event_count_histogram"  # 저장 경로
SAVE_FORMATS = ('pdf', 'png')  # 저장 형식
DPI = 300             # 저장 해상도

# 정수 bin 설정 (0부터 12까지)
bins = np.arange(0, 14)  # 0, 1, 2, ..., 13 (마지막 bin은 경계값으로만 사용)
bin_labels = [str(i) for i in range(13)]  # 0, 1, 2, ..., 12

# 히스토그램 계산 (정규화된 확률 분포)
hist, bin_edges = np.histogram(df_away_event.values, bins=bins, density=True)

# 각 bin의 너비 계산
bin_widths = np.diff(bin_edges)

# 각 bin의 확률 계산 (밀도 * 너비 = 확률)
probabilities = hist * bin_widths

# 확률 합이 1이 되도록 정규화
probabilities = probabilities / np.sum(probabilities)

# 그래프 그리기
fig, ax = plt.subplots(figsize=(dm.cm2in(FIGSIZE[0]), dm.cm2in(FIGSIZE[1])))

# 히스토그램 그리기 (확률 분포로 정규화)
bars = ax.bar(
    range(len(bin_labels)),
    probabilities,
    width=BAR_WIDTH,
    color=COLORS['bar'],
    linewidth=0.0,
    edgecolor=COLORS['edge'],
    bottom=0,
    label="Probability",
    zorder=3  # 그리드(zorder=0)보다 높은 값으로 설정
)

# x축, y축 레이블 설정
ax.set_xlabel("Number of seat-leaving events per hour", fontsize=dm.fs(0))
ax.set_ylabel("Probability", fontsize=dm.fs(0))

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

# 범례
# ax.legend(loc='best', fontsize=dm.fs(-1.2))

# 그래프 저장
# 디렉토리 확인 및 생성
output_dir = SAVE_PATH.parent
if not output_dir.exists():
    output_dir.mkdir(parents=True, exist_ok=True)

# 저장
dm.save_formats(fig, str(SAVE_PATH), formats=SAVE_FORMATS, bbox_inches="tight", dpi=DPI)

# 그래프 표시
plt.show()

# 통계 정보 출력
print(f"평균 이벤트 수: {df_away_event.values.mean():.3f}")
print(f"최대 이벤트 수: {df_away_event.values.max():.0f}")
print(f"최소 이벤트 수: {df_away_event.values.min():.0f}")

# 각 구간별 확률 출력
print("\n구간별 확률:")
for i, (label, prob) in enumerate(zip(bin_labels, probabilities)):
    print(f"{label}: {prob:.4f} ({prob*100:.2f}%)")

# %% Load data for away event duration histogram
# away_duration.csv 파일 불러오기
data_path = script_dir / "measured_data"
df_away_duration = pd.read_csv(data_path / "away_duration.csv")

#%% Plotting away event duration histogram
# 그래프 설정값
FIGSIZE = (8.8, 7.0)  # 그래프 크기 (cm)
BAR_WIDTH = 1.0       # 막대 너비
COLORS = {
    'bar': "dm.teal3",      # 막대 색상
    'edge': "dm.gray8"      # 테두리 색상
}
YLIM = (0, 0.20)      # y축 범위
SAVE_PATH = script_dir / "figure_output" / "away_duration_histogram"  # 저장 경로
SAVE_FORMATS = ('pdf', 'png')  # 저장 형식
DPI = 300             # 저장 해상도

# 1분 간격의 bin 설정 (0부터 60분까지)
bins = np.arange(0, 61, 1)  # 0, 1, 2, ..., 60
bin_labels = [str(i) for i in range(0, 61, 5)]  # 5분 간격으로 레이블 표시

# 히스토그램 계산 (정규화된 확률 분포)
hist, bin_edges = np.histogram(df_away_duration.values, bins=bins, density=True)
bin_widths = np.diff(bin_edges)
probabilities = hist * bin_widths
probabilities = probabilities / np.sum(probabilities)

# 그래프 그리기
fig, ax = plt.subplots(figsize=(dm.cm2in(FIGSIZE[0]), dm.cm2in(FIGSIZE[1])))

# 히스토그램 그리기
bars = ax.bar(
    range(len(probabilities)),
    probabilities,
    width=BAR_WIDTH,
    color=COLORS['bar'],
    linewidth=0.2,
    edgecolor=COLORS['edge'],   
    label="Probability",
    zorder=3
)

# 축 레이블 설정
ax.set_xlabel("Occupancy duration per hour [min]", fontsize=dm.fs(0))
ax.set_ylabel("Probability", fontsize=dm.fs(0))

# x축 눈금 설정 (5분 간격)
tick_positions = list(range(0, len(probabilities), 5))
tick_positions.append(60)
ax.set_xticks(tick_positions)
ax.set_xticklabels([str(pos) for pos in tick_positions], fontsize=dm.fs(0))

# y축 눈금 설정
yticks = np.arange(0, YLIM[1] + 0.001, 0.02)
ax.set_yticks(yticks)
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

# 그리드 및 레이아웃 설정
ax.grid(True, linestyle=":", axis="y", zorder=0)
ax.set_ylim(YLIM)
ax.set_xlim(-1, 61)
ax.xaxis.set_minor_locator(ticker.NullLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(1))

# 스파인 설정
for spine in ax.spines.values():
    spine.set_zorder(5)

# 레이아웃 최적화
dm.simple_layout(fig)

# 그래프 저장
output_dir = SAVE_PATH.parent
if not output_dir.exists():
    output_dir.mkdir(parents=True, exist_ok=True)
dm.save_formats(fig, str(SAVE_PATH), formats=SAVE_FORMATS, bbox_inches="tight", dpi=DPI)

# 그래프 표시 및 통계 출력
plt.show()
print(f"평균 이벤트 지속 시간: {df_away_duration.values.mean():.3f} 분")
print(f"최대 이벤트 지속 시간: {df_away_duration.values.max():.0f} 분")
print(f"최소 이벤트 지속 시간: {df_away_duration.values.min():.0f} 분")


#%% load data for met converted
# met_converted_PMV.csv 파일 불러오기
data_path = script_dir / "measured_data"
df_met_converted = pd.read_csv(data_path / "met_converted.csv")

#%% Plotting met converted 

# 그래프 설정값 (필요시 수정)
FIGSIZE = (8.8, 7.0)  # 그래프 크기 (cm)
COLORS = {
    'bar': "dm.teal3",      # 히스토그램 색상
    'line': "dm.red5",      # KDE 라인 색상
    'edge': "dm.gray8"      # 테두리 색상
}
YLIM = (0, 4.5)      # y축 범위
SAVE_PATH = script_dir / "figure_output" / "met_converted_histogram"  # 저장 경로
SAVE_FORMATS = ('pdf', 'png')  # 저장 형식
DPI = 300             # 저장 해상도

# 데이터 준비
data = df_met_converted.values.flatten()  # 1차원 배열로 변환

# 그래프 그리기
fig, ax = plt.subplots(figsize=(dm.cm2in(FIGSIZE[0]), dm.cm2in(FIGSIZE[1])))
# 히스토그램 빈 설정
bins = np.arange(1.0, 1.75, 0.05)  # 1.0에서 1.7까지 0.05 간격으로 빈 설정

# 히스토그램 그리기 (정규화된 확률 분포)
n, bins, patches = ax.hist(
    data, 
    bins=bins, 
    density=True,
    color=COLORS['bar'],
    edgecolor=COLORS['edge'],
    linewidth=0.3,
    alpha=0.7,
    label="Histogram",
    zorder=3
)

# KDE CSV 파일 불러오기
kde_path = script_dir / "measured_data" / "kde.csv"
kde_df = pd.read_csv(kde_path)

# KDE 라인 그리기
ax.plot(
    kde_df.iloc[:, 0],  # 첫 번째 열을 x 값으로 사용
    kde_df.iloc[:, 1],  # 두 번째 열을 y 값으로 사용
    color=COLORS['line'], 
    linewidth=1.0, 
    label="Kernel density estimate",
    zorder=4
)

# x축, y축 레이블 설정
ax.set_xlabel("Converted metabolic rate [met]", fontsize=dm.fs(0))
ax.set_ylabel("Probability", fontsize=dm.fs(0))

# 그리드 추가
ax.grid(True, linestyle=":", alpha=0.3, axis="both", zorder=0)  # zorder를 낮게 설정하여 뒤에 그려지도록 함

# ylim 설정
ax.set_ylim(YLIM)

# xlim 설정 (1.0과 1.7 기준으로 동일한 여백 추가)
margin = 0.03  # 고정된 마진 값
ax.set_xlim(1.0 - margin, 1.7 + margin)  # 1.0과 1.7 기준으로 동일한 마진 적용

# x축 minor tick 설정
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(1))

# y축 minor tick 설정 (메이저 틱 사이에 하나씩)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

# 스파인 zorder 설정 (그리드보다 위에 그려지도록)
for spine in ax.spines.values():
    spine.set_zorder(5)

# 레이아웃 최적화
dm.simple_layout(fig)

# 범례 추가
ax.legend(loc='best', fontsize=dm.fs(-1))

# 그래프 저장
# 디렉토리 확인 및 생성
output_dir = SAVE_PATH.parent
if not output_dir.exists():
    output_dir.mkdir(parents=True, exist_ok=True)

# 저장
dm.save_formats(fig, str(SAVE_PATH), formats=SAVE_FORMATS, bbox_inches="tight", dpi=DPI)

# 그래프 표시
plt.show()

# 통계 정보 출력
print(f"평균 대사율: {data.mean():.3f} met")
print(f"최대 대사율: {data.max():.3f} met")
print(f"최소 대사율: {data.min():.3f} met")
print(f"표준편차: {data.std():.3f} met")





#%% temp_measured.csv 파일 불러오기
data_path = script_dir / "measured_data"
df_temp_measured = pd.read_csv(data_path / "temp_measured.csv")

#%% Plotting air temperature
# 그래프 설정값 (필요시 수정)
FIGSIZE = (8.8, 7.0)  # 그래프 크기 (cm)
COLORS = {
    'bar': "dm.teal3",      # 히스토그램 색상
    'line': "dm.red5",      # KDE 라인 색상
    'edge': "dm.gray8"      # 테두리 색상
}
YLIM = (0, 0.7)      # y축 범위
SAVE_PATH = script_dir / "figure_output" / "air_temperature_histogram"  # 저장 경로
SAVE_FORMATS = ('pdf', 'png')  # 저장 형식
DPI = 300             # 저장 해상도

# 데이터 준비
data = df_temp_measured.values.flatten()  # 1차원 배열로 변환

# 그래프 그리기
fig, ax = plt.subplots(figsize=(dm.cm2in(FIGSIZE[0]), dm.cm2in(FIGSIZE[1])))

# 히스토그램 빈 설정
min_temp = np.floor(data.min() * 5) / 5  # 0.2 단위로 내림
max_temp = np.ceil(data.max() * 5) / 5   # 0.2 단위로 올림
bins = np.arange(min_temp, max_temp + 0.2, 0.2)  # 0.2 간격으로 빈 설정

# 히스토그램 그리기 (정규화된 확률 분포)
n, bins, patches = ax.hist(
    data, 
    bins=bins, 
    density=True,
    color=COLORS['bar'],
    edgecolor=COLORS['edge'],
    linewidth=0.3,
    alpha=0.7,
    label="Histogram",
    zorder=3
)

# SciPy를 사용한 Gaussian Mixture Model 구현
from scipy import stats
from scipy.optimize import minimize

# 데이터 준비
data_flat = data.flatten()

# EM 알고리즘을 직접 구현하는 대신, 간단한 방법으로 GMM 파라미터 추정
# 데이터를 n_components 개의 구간으로 나누어 각 구간에서 평균과 표준편차 계산
n_components = 1
weights = np.ones(n_components) / n_components  # 초기 가중치는 균등하게 설정

# 데이터 범위를 n_components 개의 구간으로 나누기
data_min, data_max = min_temp, max_temp
intervals = np.linspace(data_min, data_max, n_components + 1)
means = []
stds = []

# 각 구간에서 평균과 표준편차 계산
for i in range(n_components):
    # 구간 내 데이터 선택
    mask = (data_flat >= intervals[i]) & (data_flat < intervals[i + 1])
    if np.sum(mask) > 10:  # 충분한 데이터가 있는 경우
        segment_data = data_flat[mask]
        means.append(np.mean(segment_data))
        stds.append(np.std(segment_data))
    else:  # 데이터가 부족한 경우 전체 데이터의 통계량 사용
        means.append(data_min + (i + 0.5) * (data_max - data_min) / n_components)
        stds.append(np.std(data_flat) / 2)

# 가중치 최적화 함수
def gmm_nll(weights, x, means, stds):
    """GMM의 음의 로그 가능도 계산"""
    weights = weights / np.sum(weights)  # 정규화
    pdf = np.zeros_like(x, dtype=float)
    for i in range(len(means)):
        pdf += weights[i] * stats.norm.pdf(x, means[i], stds[i])
    return -np.sum(np.log(pdf + 1e-10))  # 수치 안정성을 위해 작은 값 추가

# 가중치 최적화 (제약 조건: 합이 1)
bounds = [(0, 1)] * n_components
constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
result = minimize(
    gmm_nll, 
    weights, 
    args=(data_flat, means, stds),
    bounds=bounds,
    constraints=constraints
)
weights = result.x / np.sum(result.x)  # 정규화

# 예측을 위한 x 값 생성 (경계 밖으로 더 확장)
x_extend = 0.05
x_gmm = np.linspace(min_temp - x_extend, max_temp + x_extend, 1000)

# GMM PDF 계산
y_gmm = np.zeros_like(x_gmm)
for i in range(n_components):
    y_gmm += weights[i] * stats.norm.pdf(x_gmm, means[i], stds[i])

# 경계 근처에서 점진적으로 감소하는 가중치 적용
boundary_weight = np.ones_like(x_gmm)
transition_width = 0.3  # 전이 구간의 너비

# 왼쪽 경계에서의 점진적 감소
left_transition = (x_gmm >= min_temp - transition_width) & (x_gmm < min_temp)
if np.any(left_transition):
    # 선형 증가 (0에서 1로)
    boundary_weight[left_transition] = (x_gmm[left_transition] - (min_temp - transition_width)) / transition_width

# 오른쪽 경계에서의 점진적 감소
right_transition = (x_gmm > max_temp) & (x_gmm <= max_temp + transition_width)
if np.any(right_transition):
    # 선형 감소 (1에서 0으로)
    boundary_weight[right_transition] = 1 - (x_gmm[right_transition] - max_temp) / transition_width

# 경계 밖의 먼 영역은 0으로 설정
far_outside = (x_gmm < min_temp - transition_width) | (x_gmm > max_temp + transition_width)
boundary_weight[far_outside] = 0

# 가중치 적용
y_gmm = y_gmm * boundary_weight

# 정규화 (적분값이 1이 되도록)
dx = x_gmm[1] - x_gmm[0]
area = np.sum(y_gmm) * dx
y_gmm = y_gmm / area

# KDE 라인 그리기
ax.plot(
    x_gmm, 
    y_gmm, 
    color=COLORS['line'], 
    linewidth=1.0, 
    label=f"Gaussian mixture model ({n_components} components)",
    zorder=4
)

# x축, y축 레이블 설정
ax.set_xlabel("Measured air temperature [°C]", fontsize=dm.fs(0))
ax.set_ylabel("Probability", fontsize=dm.fs(0))

# 그리드 추가
ax.grid(True, linestyle=":", alpha=0.3, axis="both", zorder=0)  # zorder를 낮게 설정하여 뒤에 그려지도록 함

# ylim 설정
ax.set_ylim(YLIM)

# xlim 설정 (데이터 범위에 맞게 약간의 여백 추가)
margin = (data.max() - data.min()) * 0.1  # 10% 여백
ax.set_xlim(data.min() - margin, data.max() + margin)

# x축 minor tick 설정
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(1))

# y축 minor tick 설정 (메이저 틱 사이에 하나씩)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(1))

# 스파인 zorder 설정 (그리드보다 위에 그려지도록)
for spine in ax.spines.values():
    spine.set_zorder(5)

# 레이아웃 최적화
dm.simple_layout(fig)

# 범례 추가
ax.legend(loc='best', fontsize=dm.fs(-1))

# 그래프 저장
# 디렉토리 확인 및 생성
output_dir = SAVE_PATH.parent
if not output_dir.exists():
    output_dir.mkdir(parents=True, exist_ok=True)

# 저장
dm.save_formats(fig, str(SAVE_PATH), formats=SAVE_FORMATS, bbox_inches="tight", dpi=DPI)

# 그래프 표시
plt.show()

# 통계 정보 출력
print(f"평균 실내 온도: {data.mean():.3f} °C")
print(f"최대 실내 온도: {data.max():.3f} °C")
print(f"최소 실내 온도: {data.min():.3f} °C")
print(f"표준편차: {data.std():.3f} °C")





#%% load data for measured relative humidity

# rh_measured.csv 파일 불러오기
data_path = script_dir / "measured_data"
df_rh_measured = pd.read_csv(data_path / "rh_measured.csv")

#%% Plotting relative humidity

# 그래프 설정값 (필요시 수정)
FIGSIZE = (8.8, 7.0)  # 그래프 크기 (cm)
COLORS = {
    'bar': "dm.teal3",      # 히스토그램 색상
    'line': "dm.red5",      # KDE 라인 색상
    'edge': "dm.gray8"      # 테두리 색상
}
YLIM = (0, 0.32)      # y축 범위
SAVE_PATH = script_dir / "figure_output" / "relative_humidity_histogram"  # 저장 경로
SAVE_FORMATS = ('pdf', 'png')  # 저장 형식
DPI = 300             # 저장 해상도

# 데이터 준비
data = df_rh_measured.values.flatten()  # 1차원 배열로 변환

# 그래프 그리기
fig, ax = plt.subplots(figsize=(dm.cm2in(FIGSIZE[0]), dm.cm2in(FIGSIZE[1])))

# 히스토그램 빈 설정
min_rh = np.floor(data.min() * 4) / 4  # 0.25 단위로 내림
max_rh = np.ceil(data.max() * 4) / 4   # 0.25 단위로 올림
bins = np.arange(min_rh, max_rh + 0.25, 0.25)  # 0.25 간격으로 빈 설정

# 히스토그램 그리기 (정규화된 확률 분포)
n, bins, patches = ax.hist(
    data, 
    bins=bins, 
    density=True,
    color=COLORS['bar'],
    edgecolor=COLORS['edge'],
    linewidth=0.3,
    alpha=0.7,
    label="Histogram",
    zorder=3
)

# SciPy를 사용한 Gaussian Mixture Model 구현
from scipy import stats
from scipy.optimize import minimize

# 데이터 준비
data_flat = data.flatten()

# EM 알고리즘을 직접 구현하는 대신, 간단한 방법으로 GMM 파라미터 추정
# 데이터를 n_components 개의 구간으로 나누어 각 구간에서 평균과 표준편차 계산
n_components = 3
weights = np.ones(n_components) / n_components  # 초기 가중치는 균등하게 설정

# 데이터 범위를 n_components 개의 구간으로 나누기
data_min, data_max = min_rh, max_rh
intervals = np.linspace(data_min, data_max, n_components + 1)
means = []
stds = []

# 각 구간에서 평균과 표준편차 계산
for i in range(n_components):
    # 구간 내 데이터 선택
    mask = (data_flat >= intervals[i]) & (data_flat < intervals[i + 1])
    if np.sum(mask) > 10:  # 충분한 데이터가 있는 경우
        segment_data = data_flat[mask]
        means.append(np.mean(segment_data))
        stds.append(np.std(segment_data))
    else:  # 데이터가 부족한 경우 전체 데이터의 통계량 사용
        means.append(data_min + (i + 0.5) * (data_max - data_min) / n_components)
        stds.append(np.std(data_flat) / 2)

# 가중치 최적화 함수
def gmm_nll(weights, x, means, stds):
    """GMM의 음의 로그 가능도 계산"""
    weights = weights / np.sum(weights)  # 정규화
    pdf = np.zeros_like(x, dtype=float)
    for i in range(len(means)):
        pdf += weights[i] * stats.norm.pdf(x, means[i], stds[i])
    return -np.sum(np.log(pdf + 1e-10))  # 수치 안정성을 위해 작은 값 추가

# 가중치 최적화 (제약 조건: 합이 1)
bounds = [(0, 1)] * n_components
constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
result = minimize(
    gmm_nll, 
    weights, 
    args=(data_flat, means, stds),
    bounds=bounds,
    constraints=constraints
)
weights = result.x / np.sum(result.x)  # 정규화

# 예측을 위한 x 값 생성 (경계 밖으로 더 확장)
x_extend = 0.05
x_gmm = np.linspace(min_rh - x_extend, max_rh + x_extend, 1000)

# GMM PDF 계산
y_gmm = np.zeros_like(x_gmm)
for i in range(n_components):
    y_gmm += weights[i] * stats.norm.pdf(x_gmm, means[i], stds[i])

# 경계 근처에서 점진적으로 감소하는 가중치 적용
boundary_weight = np.ones_like(x_gmm)
transition_width = 0.3  # 전이 구간의 너비

# 왼쪽 경계에서의 점진적 감소
left_transition = (x_gmm >= min_rh - transition_width) & (x_gmm < min_rh)
if np.any(left_transition):
    # 선형 증가 (0에서 1로)
    boundary_weight[left_transition] = (x_gmm[left_transition] - (min_rh - transition_width)) / transition_width

# 오른쪽 경계에서의 점진적 감소
right_transition = (x_gmm > max_rh) & (x_gmm <= max_rh + transition_width)
if np.any(right_transition):
    # 선형 감소 (1에서 0으로)
    boundary_weight[right_transition] = 1 - (x_gmm[right_transition] - max_rh) / transition_width

# 경계 밖의 먼 영역은 0으로 설정
far_outside = (x_gmm < min_rh - transition_width) | (x_gmm > max_rh + transition_width)
boundary_weight[far_outside] = 0

# 가중치 적용
y_gmm = y_gmm * boundary_weight

# 정규화 (적분값이 1이 되도록)
dx = x_gmm[1] - x_gmm[0]
area = np.sum(y_gmm) * dx
y_gmm = y_gmm / area

# KDE 라인 그리기
ax.plot(
    x_gmm, 
    y_gmm, 
    color=COLORS['line'], 
    linewidth=1.0, 
    label=f"Gaussian mixture model ({n_components} components)",
    zorder=4
)

# x축, y축 레이블 설정
ax.set_xlabel("Measured relative humidity [%]", fontsize=dm.fs(0))
ax.set_ylabel("Probability", fontsize=dm.fs(0))

# 그리드 추가
ax.grid(True, linestyle=":", alpha=0.3, axis="both", zorder=0)  # zorder를 낮게 설정하여 뒤에 그려지도록 함

# ylim 설정
ax.set_ylim(YLIM)

# xlim 설정 (데이터 범위에 맞게 약간의 여백 추가)
margin = (data.max() - data.min()) * 0.1  # 10% 여백
ax.set_xlim(data.min() - margin, data.max() + margin)

# x축 minor tick 설정
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(1))

# y축 minor tick 설정 (메이저 틱 사이에 하나씩)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(1))

# 스파인 zorder 설정 (그리드보다 위에 그려지도록)
for spine in ax.spines.values():
    spine.set_zorder(5)

# 레이아웃 최적화
dm.simple_layout(fig)

# 범례 추가
ax.legend(loc='best', fontsize=dm.fs(-1))

# 그래프 저장
# 디렉토리 확인 및 생성
output_dir = SAVE_PATH.parent
if not output_dir.exists():
    output_dir.mkdir(parents=True, exist_ok=True)

# 저장
dm.save_formats(fig, str(SAVE_PATH), formats=SAVE_FORMATS, bbox_inches="tight", dpi=DPI)

# 그래프 표시
plt.show()

# 통계 정보 출력
print(f"평균 상대 습도: {data.mean():.3f} %")
print(f"최대 상대 습도: {data.max():.3f} %")
print(f"최소 상대 습도: {data.min():.3f} %")
print(f"표준편차: {data.std():.3f} %")


# %%
