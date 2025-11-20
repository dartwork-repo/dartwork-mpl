"""
Polar Plots
===========

This example demonstrates polar coordinate plotting including basic polar plots,
polar scatter plots, and polar bar charts using dartwork-mpl.
"""

import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Apply scientific style preset
# Default: font.size=7.5, lines.linewidth=0.5, axes.linewidth=0.3
dm.style.use_preset('scientific')

# Generate sample data
theta = np.linspace(0, 2 * np.pi, 8, endpoint=False)
r1 = np.array([3, 5, 2, 4, 6, 3, 5, 4])
r2 = np.random.rand(20) * 5
theta2 = np.linspace(0, 2 * np.pi, 20, endpoint=False)

# Create figure
# Double column figure: 17cm width
fig = plt.figure(figsize=(dm.cm2in(17), dm.cm2in(6)), dpi=200)

# Create GridSpec for 3 subplots with polar projection
gs = fig.add_gridspec(
    nrows=1, ncols=3,
    left=0.08, right=0.98,
    top=0.92, bottom=0.15,
    wspace=0.3
)

# Panel A: Basic polar plot
ax1 = fig.add_subplot(gs[0, 0], projection='polar')
# Explicit parameters: lw=0.7, marker='o', markersize=4
ax1.plot(theta, r1, color='dm.blue5', lw=0.7, marker='o', markersize=4, label='Data')
ax1.fill(theta, r1, color='dm.blue2', alpha=0.3)
ax1.set_title('Basic Polar Plot', fontsize=dm.fs(1), pad=20)
ax1.set_theta_zero_location('N')
ax1.set_theta_direction(-1)
ax1.grid(True, linestyle='--', linewidth=0.3, alpha=0.5)

# Panel B: Polar scatter plot
ax2 = fig.add_subplot(gs[0, 1], projection='polar')
# Explicit parameters: s=20, alpha=0.6
ax2.scatter(theta2, r2, c='dm.red5', s=20, alpha=0.6, edgecolors='none')
ax2.set_title('Polar Scatter Plot', fontsize=dm.fs(1), pad=20)
ax2.set_theta_zero_location('N')
ax2.set_theta_direction(-1)
ax2.grid(True, linestyle='--', linewidth=0.3, alpha=0.5)

# Panel C: Polar bar chart
ax3 = fig.add_subplot(gs[0, 2], projection='polar')
# Explicit parameters: width=0.5, alpha=0.7, edgecolor, linewidth=0.3
width = 2 * np.pi / len(theta)
bars = ax3.bar(theta, r1, width=width, color='dm.green5', 
               alpha=0.7, edgecolor='dm.green7', linewidth=0.3)
ax3.set_title('Polar Bar Chart', fontsize=dm.fs(1), pad=20)
ax3.set_theta_zero_location('N')
ax3.set_theta_direction(-1)
ax3.grid(True, linestyle='--', linewidth=0.3, alpha=0.5)

# Optimize layout
dm.simple_layout(fig, gs=gs)

# Show plot
plt.show()

