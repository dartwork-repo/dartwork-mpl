"""
Scatter Plots
=============

This example demonstrates various scatter plot techniques using dartwork-mpl,
including basic scatter plots, color mapping, and size mapping.
"""

import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Apply scientific style preset
# Default: font.size=7.5, lines.linewidth=0.5, axes.linewidth=0.3
dm.style.use_preset('scientific')

# Generate sample data
np.random.seed(42)
n = 100
x1 = np.random.randn(n)
y1 = np.random.randn(n)
x2 = np.random.randn(n)
y2 = np.random.randn(n)
x3 = np.random.randn(n)
y3 = np.random.randn(n)

# Color mapping data
colors = np.random.rand(n)
# Size mapping data
sizes = 100 * np.random.rand(n)

# Create figure
# Single column figure: 9cm width
fig = plt.figure(figsize=(dm.cm2in(17), dm.cm2in(6)), dpi=200)

# Create GridSpec for 3 subplots
gs = fig.add_gridspec(
    nrows=1, ncols=3,
    left=0.08, right=0.98,
    top=0.92, bottom=0.15,
    wspace=0.3
)

# Panel A: Basic scatter with different markers
ax1 = fig.add_subplot(gs[0, 0])
# Explicit parameters: markersize=4, lw=0 (no edge), alpha=0.6
ax1.scatter(x1, y1, c='dm.blue5', s=20, marker='o', 
            edgecolors='none', alpha=0.6, label='Group A')
ax1.scatter(x2, y2, c='dm.red5', s=20, marker='s', 
            edgecolors='none', alpha=0.6, label='Group B')
ax1.set_xlabel('X value', fontsize=dm.fs(0))
ax1.set_ylabel('Y value', fontsize=dm.fs(0))
ax1.set_title('Basic Scatter Plot', fontsize=dm.fs(1))
ax1.legend(loc='upper right', fontsize=dm.fs(-1), ncol=1)
# Set explicit ticks
ax1.set_xticks([-3, -1, 1, 3])
ax1.set_yticks([-3, -1, 1, 3])

# Panel B: Scatter with color mapping
ax2 = fig.add_subplot(gs[0, 1])
# Color mapping: c=colors, cmap='dm.Spectral', s=20 (size), alpha=0.7
scatter2 = ax2.scatter(x1, y1, c=colors, s=20, cmap='dm.Spectral', 
                       edgecolors='none', alpha=0.7)
ax2.set_xlabel('X value', fontsize=dm.fs(0))
ax2.set_ylabel('Y value', fontsize=dm.fs(0))
ax2.set_title('Color Mapping', fontsize=dm.fs(1))
# Add colorbar with explicit fontsize
cbar2 = fig.colorbar(scatter2, ax=ax2)
cbar2.set_label('Intensity', fontsize=dm.fs(-1))
cbar2.ax.tick_params(labelsize=dm.fs(-1))
# Set explicit ticks
ax2.set_xticks([-3, -1, 1, 3])
ax2.set_yticks([-3, -1, 1, 3])

# Panel C: Scatter with size mapping
ax3 = fig.add_subplot(gs[0, 2])
# Size mapping: s=sizes, c='dm.green5', alpha=0.6
scatter3 = ax3.scatter(x1, y1, s=sizes, c='dm.green5', 
                       edgecolors='dm.green7', linewidths=0.3, alpha=0.6)
ax3.set_xlabel('X value', fontsize=dm.fs(0))
ax3.set_ylabel('Y value', fontsize=dm.fs(0))
ax3.set_title('Size Mapping', fontsize=dm.fs(1))
# Set explicit ticks
ax3.set_xticks([-3, -1, 1, 3])
ax3.set_yticks([-3, -1, 1, 3])

# Optimize layout
dm.simple_layout(fig, gs=gs)

# Show plot
plt.show()

