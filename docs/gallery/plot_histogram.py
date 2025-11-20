"""
Histogram Variations
====================

This example demonstrates various histogram plotting techniques including
basic histograms, stacked histograms, and histograms with KDE overlay.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import dartwork_mpl as dm

# Apply scientific style preset
# Default: font.size=7.5, lines.linewidth=0.5, axes.linewidth=0.3
dm.style.use_preset('scientific')

# Generate sample data
np.random.seed(42)
data1 = np.random.normal(0, 1, 1000)
data2 = np.random.normal(2, 1.5, 1000)
data3 = np.random.normal(-1, 0.8, 1000)

# Create figure
# Double column figure: 17cm width
fig = plt.figure(figsize=(dm.cm2in(17), dm.cm2in(6)), dpi=200)

# Create GridSpec for 3 subplots
gs = fig.add_gridspec(
    nrows=1, ncols=3,
    left=0.08, right=0.98,
    top=0.92, bottom=0.15,
    wspace=0.3
)

# Panel A: Basic histogram
ax1 = fig.add_subplot(gs[0, 0])
# Explicit parameters: bins=30, alpha=0.7, edgecolor, linewidth=0.3
n1, bins1, patches1 = ax1.hist(data1, bins=30, color='dm.blue5', 
                               alpha=0.7, edgecolor='dm.blue7', 
                               linewidth=0.3, label='Distribution')
ax1.set_xlabel('Value', fontsize=dm.fs(0))
ax1.set_ylabel('Frequency', fontsize=dm.fs(0))
ax1.set_title('Basic Histogram', fontsize=dm.fs(1))
ax1.legend(loc='upper right', fontsize=dm.fs(-1), ncol=1)
# Set explicit ticks
ax1.set_xticks([-4, -2, 0, 2, 4])
ax1.set_yticks([0, 50, 100, 150])

# Panel B: Stacked histogram
ax2 = fig.add_subplot(gs[0, 1])
# Explicit parameters: bins=30, alpha=0.7 for each
n2, bins2, patches2 = ax2.hist([data1, data2, data3], bins=30, 
                                color=['dm.blue5', 'dm.red5', 'dm.green5'],
                                alpha=0.7, edgecolor='dm.gray7', 
                                linewidth=0.3, label=['Group A', 'Group B', 'Group C'],
                                stacked=True)
ax2.set_xlabel('Value', fontsize=dm.fs(0))
ax2.set_ylabel('Frequency', fontsize=dm.fs(0))
ax2.set_title('Stacked Histogram', fontsize=dm.fs(1))
ax2.legend(loc='upper right', fontsize=dm.fs(-1), ncol=1)
# Set explicit ticks
ax2.set_xticks([-4, -2, 0, 2, 4, 6])

# Panel C: Histogram with KDE overlay
ax3 = fig.add_subplot(gs[0, 2])
# Histogram: bins=30, alpha=0.5
n3, bins3, patches3 = ax3.hist(data1, bins=30, color='dm.blue5', 
                               alpha=0.5, edgecolor='dm.blue7', 
                               linewidth=0.3, density=True, label='Histogram')
# KDE overlay
x_kde = np.linspace(data1.min(), data1.max(), 200)
kde = stats.gaussian_kde(data1)
y_kde = kde(x_kde)
# KDE line: lw=0.7
ax3.plot(x_kde, y_kde, color='dm.red5', lw=0.7, label='KDE')
ax3.set_xlabel('Value', fontsize=dm.fs(0))
ax3.set_ylabel('Density', fontsize=dm.fs(0))
ax3.set_title('Histogram with KDE', fontsize=dm.fs(1))
ax3.legend(loc='upper right', fontsize=dm.fs(-1), ncol=1)
# Set explicit ticks
ax3.set_xticks([-4, -2, 0, 2, 4])
ax3.set_yticks([0, 0.1, 0.2, 0.3, 0.4])

# Optimize layout
dm.simple_layout(fig, gs=gs)

# Show plot
plt.show()

