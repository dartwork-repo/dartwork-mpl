"""
Inset Axes
==========

Creating inset axes for zoomed views and detail plots.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
import dartwork_mpl as dm

dm.style.use_preset('scientific')

np.random.seed(42)
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-x/10) + np.random.randn(100)*0.05

fig = plt.figure(figsize=(dm.cm2in(17), dm.cm2in(10)), dpi=200)
gs = fig.add_gridspec(nrows=2, ncols=2, left=0.08, right=0.98,
                      top=0.95, bottom=0.08, wspace=0.3, hspace=0.4)

# Panel A: Basic inset
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(x, y, color='dm.blue5', lw=0.7)
ax1.set_xlabel('X', fontsize=dm.fs(0))
ax1.set_ylabel('Y', fontsize=dm.fs(0))
ax1.set_title('Basic Inset', fontsize=dm.fs(1))
# Create inset
axins1 = inset_axes(ax1, width="40%", height="40%", loc='upper right')
axins1.plot(x, y, color='dm.blue5', lw=0.5)
axins1.set_xlim(0, 2)
axins1.set_ylim(-0.2, 1.2)
axins1.tick_params(labelsize=dm.fs(-2))

# Panel B: Inset with marker
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(x, y, color='dm.red5', lw=0.7)
ax2.set_xlabel('X', fontsize=dm.fs(0))
ax2.set_ylabel('Y', fontsize=dm.fs(0))
ax2.set_title('Inset with Zoom Box', fontsize=dm.fs(1))
axins2 = inset_axes(ax2, width="45%", height="45%", loc='upper left')
axins2.plot(x, y, color='dm.red5', lw=0.5)
x1, x2, y1, y2 = 4, 6, -0.3, 0.5
axins2.set_xlim(x1, x2)
axins2.set_ylim(y1, y2)
axins2.tick_params(labelsize=dm.fs(-2))
mark_inset(ax2, axins2, loc1=2, loc2=4, fc="none", ec="dm.gray7", lw=0.5)

# Panel C: Multiple insets
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(x, y, color='dm.green5', lw=0.7)
ax3.set_xlabel('X', fontsize=dm.fs(0))
ax3.set_ylabel('Y', fontsize=dm.fs(0))
ax3.set_title('Multiple Insets', fontsize=dm.fs(1))
# Inset 1
axins3a = inset_axes(ax3, width="30%", height="30%", loc='upper right')
axins3a.plot(x, y, color='dm.green5', lw=0.5)
axins3a.set_xlim(0, 2)
axins3a.set_ylim(0.5, 1.2)
axins3a.tick_params(labelsize=dm.fs(-3))
# Inset 2
axins3b = inset_axes(ax3, width="30%", height="30%", loc='lower left')
axins3b.plot(x, y, color='dm.green5', lw=0.5)
axins3b.set_xlim(8, 10)
axins3b.set_ylim(-0.15, 0.15)
axins3b.tick_params(labelsize=dm.fs(-3))

# Panel D: Different inset plot type
ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(x, y, color='dm.purple5', lw=0.7)
ax4.set_xlabel('X', fontsize=dm.fs(0))
ax4.set_ylabel('Y', fontsize=dm.fs(0))
ax4.set_title('Histogram Inset', fontsize=dm.fs(1))
# Histogram inset
axins4 = inset_axes(ax4, width="40%", height="40%", loc='center right')
axins4.hist(y, bins=20, color='dm.purple5', alpha=0.7, edgecolor='dm.purple7', linewidth=0.3)
axins4.tick_params(labelsize=dm.fs(-3))
axins4.set_xlabel('Y', fontsize=dm.fs(-2))
axins4.set_ylabel('Count', fontsize=dm.fs(-2))

dm.simple_layout(fig, gs=gs)
dm.save_and_show(fig)
