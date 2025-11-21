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
time = np.linspace(0, 20, 400)
trend = 0.05 * time
signal = np.sin(time) + 0.5 * np.sin(0.5 * time + 0.8)
spike = 2.5 * np.exp(-0.5 * ((time - 6) / 0.18) ** 2)
dip = -1.8 * np.exp(-0.5 * ((time - 14) / 0.30) ** 2)
noise = 0.08 * np.random.randn(len(time))
y = trend + signal + spike + dip + noise

# Scatter data for panel C
core = np.random.multivariate_normal([0, 0], [[0.25, 0.05], [0.05, 0.20]], 300)
outliers = np.random.multivariate_normal([3, 2], [[0.10, 0], [0, 0.10]], 40)
points = np.vstack([core, outliers])

fig = plt.figure(figsize=(dm.cm2in(16), dm.cm2in(12)), dpi=300)
gs = fig.add_gridspec(
    nrows=2,
    ncols=2,
    left=0.08,
    right=0.98,
    top=0.95,
    bottom=0.08,
    wspace=0.30,
    hspace=0.42,
)

# Panel A: Zoom on transient event
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(time, y, color='dm.blue6', lw=0.8)
ax1.set_xlabel('Time', fontsize=dm.fs(0))
ax1.set_ylabel('Signal', fontsize=dm.fs(0))
ax1.set_title('Zoom on Transient', fontsize=dm.fs(1))
axins1 = inset_axes(ax1, width="48%", height="48%", loc='upper right')
axins1.plot(time, y, color='dm.blue6', lw=0.6)
axins1.set_xlim(5.2, 6.8)
axins1.set_ylim(1.0, 3.2)
axins1.tick_params(labelsize=dm.fs(-2))
mark_inset(ax1, axins1, loc1=1, loc2=3, fc="none", ec="dm.gray7", lw=0.6)

# Panel B: Signal with spectrum inset
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(time, y, color='dm.red6', lw=0.8, alpha=0.9)
ax2.set_xlabel('Time', fontsize=dm.fs(0))
ax2.set_ylabel('Signal', fontsize=dm.fs(0))
ax2.set_title('Transient + Spectrum', fontsize=dm.fs(1))
axins2 = inset_axes(ax2, width="52%", height="52%", loc='upper right')
dt = time[1] - time[0]
freq = np.fft.rfftfreq(len(time), d=dt)
spec = np.abs(np.fft.rfft(y - np.mean(y)))
axins2.plot(freq, spec, color='dm.red6', lw=0.7)
axins2.set_xlim(0, 1.5)
axins2.set_ylim(0, spec[freq < 1.5].max() * 1.05)
axins2.set_xlabel('Hz', fontsize=dm.fs(-2))
axins2.set_ylabel('|F|', fontsize=dm.fs(-2))
axins2.tick_params(labelsize=dm.fs(-3))

# Panel C: Clustered scatter with zoomed core
ax3 = fig.add_subplot(gs[1, 0])
ax3.scatter(points[:, 0], points[:, 1], s=10, color='dm.green6', alpha=0.7, edgecolor='none')
ax3.set_xlabel('Feature 1', fontsize=dm.fs(0))
ax3.set_ylabel('Feature 2', fontsize=dm.fs(0))
ax3.set_title('Cluster Zoom', fontsize=dm.fs(1))
axins3 = inset_axes(ax3, width="44%", height="44%", loc='upper left')
axins3.scatter(points[:, 0], points[:, 1], s=8, color='dm.green6', alpha=0.7, edgecolor='none')
axins3.set_xlim(-1.2, 1.2)
axins3.set_ylim(-1.2, 1.2)
axins3.tick_params(labelsize=dm.fs(-3))
mark_inset(ax3, axins3, loc1=2, loc2=4, fc="none", ec="dm.gray7", lw=0.6)

# Panel D: Highlighted interval with distribution inset
ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(time, y, color='dm.purple6', lw=0.8, alpha=0.9)
ax4.axvspan(9, 12, color='dm.purple2', alpha=0.25, edgecolor='dm.purple6', lw=0.5)
ax4.set_xlabel('Time', fontsize=dm.fs(0))
ax4.set_ylabel('Signal', fontsize=dm.fs(0))
ax4.set_title('Window + Distribution', fontsize=dm.fs(1))
axins4 = inset_axes(ax4, width="48%", height="48%", loc='upper right')
window = (time >= 9) & (time <= 12)
axins4.hist(y[window], bins=18, color='dm.purple5', alpha=0.8, edgecolor='dm.purple7', linewidth=0.3)
axins4.set_xlabel('Value', fontsize=dm.fs(-2))
axins4.set_ylabel('Count', fontsize=dm.fs(-2))
axins4.tick_params(labelsize=dm.fs(-3))

dm.simple_layout(fig, gs=gs)
plt.show()
