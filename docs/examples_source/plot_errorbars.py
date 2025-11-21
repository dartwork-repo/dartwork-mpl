"""
Error Bars
==========

Error bars and confidence intervals.
"""

import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Apply scientific style preset
# Default: font.size=7.5, lines.linewidth=0.5, axes.linewidth=0.3
dm.style.use_preset('scientific')

# Generate sample data
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 3, 2.5, 4, 3.5])
yerr = np.array([0.3, 0.4, 0.2, 0.5, 0.3])
xerr = np.array([0.1, 0.15, 0.1, 0.2, 0.15])

# Asymmetric error bars
yerr_lower = np.array([0.2, 0.3, 0.15, 0.4, 0.25])
yerr_upper = np.array([0.4, 0.5, 0.25, 0.6, 0.35])

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

# Panel A: Vertical error bars
ax1 = fig.add_subplot(gs[0, 0])
# Explicit parameters: elinewidth=0.7, capsize=2, capthick=0.7, markersize=4
ax1.errorbar(x, y, yerr=yerr, fmt='o', color='dm.blue5',
             ecolor='dm.blue7', elinewidth=0.7, capsize=2, 
             capthick=0.7, markersize=4, label='Data')
ax1.set_xlabel('X value', fontsize=dm.fs(0))
ax1.set_ylabel('Y value', fontsize=dm.fs(0))
ax1.set_title('Vertical Error Bars', fontsize=dm.fs(1))
ax1.legend(loc='upper left', fontsize=dm.fs(-1), ncol=1)
# Set explicit ticks
ax1.set_xticks([1, 2, 3, 4, 5])
ax1.set_yticks([0, 1, 2, 3, 4, 5])

# Panel B: Horizontal error bars
ax2 = fig.add_subplot(gs[0, 1])
# Explicit parameters: xerr instead of yerr
ax2.errorbar(x, y, xerr=xerr, fmt='s', color='dm.red5',
             ecolor='dm.red7', elinewidth=0.7, capsize=2,
             capthick=0.7, markersize=4, label='Data')
ax2.set_xlabel('X value', fontsize=dm.fs(0))
ax2.set_ylabel('Y value', fontsize=dm.fs(0))
ax2.set_title('Horizontal Error Bars', fontsize=dm.fs(1))
ax2.legend(loc='upper left', fontsize=dm.fs(-1), ncol=1)
# Set explicit ticks
ax2.set_xticks([1, 2, 3, 4, 5])
ax2.set_yticks([0, 1, 2, 3, 4, 5])

# Panel C: Asymmetric error bars
ax3 = fig.add_subplot(gs[0, 2])
# Explicit parameters: yerr=[yerr_lower, yerr_upper] for asymmetric
ax3.errorbar(x, y, yerr=[yerr_lower, yerr_upper], fmt='^', 
             color='dm.green5', ecolor='dm.green7', 
             elinewidth=0.7, capsize=2, capthick=0.7, 
             markersize=4, label='Data')
ax3.set_xlabel('X value', fontsize=dm.fs(0))
ax3.set_ylabel('Y value', fontsize=dm.fs(0))
ax3.set_title('Asymmetric Error Bars', fontsize=dm.fs(1))
ax3.legend(loc='upper left', fontsize=dm.fs(-1), ncol=1)
# Set explicit ticks
ax3.set_xticks([1, 2, 3, 4, 5])
ax3.set_yticks([0, 1, 2, 3, 4, 5])

# Optimize layout
dm.simple_layout(fig, gs=gs)

# Show plot
plt.show()

