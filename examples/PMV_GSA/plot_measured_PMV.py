# %% load library

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import dartwork_mpl as dm
import os

# dartwork_mpl에서 제공하는 cm2in 함수와 pseudo_alpha 함수 사용
from dartwork_mpl.util import cm2in, pseudo_alpha, fw


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

# 최종 확률 배열 생성
all_probabilities = probabilities

# (50, 60] 구간에서 정확히 60분인 데이터의 비율 계산
exact_60_count = np.sum(df_occup.values == 60)
last_bin_count = np.sum((df_occup.values > 50) & (df_occup.values <= 60))

# 마지막 구간에서 정확히 60분인 데이터의 비율
if last_bin_count > 0:
    exact_60_ratio = exact_60_count / last_bin_count
else:
    exact_60_ratio = 0

# 그래프 그리기 (dartwork_mpl의 SW 상수 사용)
fig, ax = plt.subplots(figsize=(dm.cm2in(8.8), dm.cm2in(7.0)))

# 그래프 설정
bar_width = 0.7  # 막대 너비 (한 번만 정의)
margin_factor = 1.0  # 마진 계수

# 히스토그램 그리기 (확률 분포로 정규화)
bars = ax.bar(
    range(len(bin_labels)),
    all_probabilities,
    width=bar_width,  # 정의된 변수 사용
    color=pseudo_alpha("dm.teal4", 0.9),
    linewidth=0.3,
    edgecolor="dm.gray8",
    bottom=0,
    label=" Probability of occupancy within interval" 
)

# 마지막 막대에 오렌지색 부분 추가 (정확히 60분인 데이터 비율)
if len(all_probabilities) > 0 and exact_60_ratio > 0:
    last_bar = bars[-1]
    last_bar_height = last_bar.get_height()

    # 오렌지색 부분의 높이 (마지막 구간 확률 * 정확히 60분인 데이터 비율)
    orange_height = last_bar_height * exact_60_ratio

    # 오렌지색 부분 추가
    orange_bar = ax.bar(
        len(bin_labels) - 1,  # 마지막 인덱스는 이제 5 (0 구간 제거)
        orange_height,
        width=bar_width,  # 정의된 변수 사용
        color=pseudo_alpha("dm.orange4", 0.9),
        edgecolor="dm.gray8",
        linewidth=0.3,
        bottom=last_bar_height - orange_height,
        label="Continuous 60-min occupancy fraction in (50, 60]"  
    )

# x축, y축 레이블 설정
ax.set_xlabel("Occupancy duration [min]", fontsize=dm.fs(0))
ax.set_ylabel("Probability density", fontsize=dm.fs(0))

# x축 눈금 설정
ax.set_xticks(range(len(bin_labels)))
ax.set_xticklabels(bin_labels, fontsize=dm.fs(0))

# 그리드 추가
ax.grid(True, linestyle="--", alpha=0.3, axis="y")

# ylim 설정
ax.set_ylim(0, 0.35)

# xlim 설정 (간단하게 bar width의 절반과 bar 사이 간격만큼 여백 설정)
bar_spacing = 0.3  # 막대 사이의 간격 (bar_width가 0.7이므로)

# 양 끝에 여백 설정
left_margin = 0 - (bar_width / 2) - bar_spacing  # 첫 번째 막대의 왼쪽에 여백
right_margin = (len(bin_labels) - 1) + (bar_width / 2) + bar_spacing  # 마지막 막대의 오른쪽에 여백

ax.set_xlim(left_margin, right_margin)




# x축 minor tick 제거
ax.xaxis.set_minor_locator(ticker.NullLocator())

# y축 minor tick 설정 (메이저 틱 사이에 하나씩)
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(1))

# 레이아웃 최적화
dm.simple_layout(fig)

# 범례 추가
ax.legend(loc='best', fontsize=dm.fs(-1))

# 그래프 표시
plt.show()

# 그래프 저장
# figure_output 폴더에 PDF와 PNG 형식으로 저장
output_dir = "./figure_output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# dartwork_mpl의 save_formats 함수 사용
output_path = os.path.join(output_dir, "occupancy_duration_probability")
dm.save_formats(fig, output_path, formats=('pdf', 'png'), bbox_inches="tight", dpi=300) 

# 기본 통계 정보 출력
print(f"평균 재실 시간 (0 제외): {non_zero_values.mean():.3f} 분")
print(f"최대 재실 시간: {non_zero_values.max():.3f} 분")
print(f"최소 재실 시간 (0 제외): {non_zero_values.min():.3f} 분")

# 각 구간별 확률 출력
print("\n구간별 확률:")
for i, (label, prob) in enumerate(zip(bin_labels, all_probabilities)):
    print(f"{label}: {prob:.4f} ({prob*100:.2f}%)")

# 정확히 60분인 데이터 정보 출력
print(f"\n정확히 60분인 데이터 수: {exact_60_count}")
print(f"(50, 60] 구간 데이터 수: {last_bin_count}")
print(
    f"(50, 60] 구간에서 정확히 60분인 데이터 비율: {exact_60_ratio:.4f} ({exact_60_ratio*100:.2f}%)"
)



# dm.save_and_show(fig)

# %%
