"""
Hierarchical Visualization
==========================

Visualizing hierarchical and nested data structures.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import dartwork_mpl as dm

dm.style.use_preset('scientific')

fig = plt.figure(figsize=(dm.cm2in(17), dm.cm2in(10)), dpi=200)
gs = fig.add_gridspec(nrows=2, ncols=2, left=0.05, right=0.98,
                      top=0.95, bottom=0.05, wspace=0.15, hspace=0.2)

# Panel A: Simple rectangles (treemap-like)
ax1 = fig.add_subplot(gs[0, 0])
sizes = [30, 25, 20, 15, 10]
colors = ['dm.red5', 'dm.blue5', 'dm.green5', 'dm.orange5', 'dm.purple5']
labels = ['A', 'B', 'C', 'D', 'E']
x, y = 0, 0
for size, color, label in zip(sizes, colors, labels):
    width = size / 100
    rect = Rectangle((x, 0), width, 1, facecolor=color, edgecolor='white', linewidth=2)
    ax1.add_patch(rect)
    ax1.text(x + width/2, 0.5, f'{label}\n{size}%', ha='center', va='center', fontsize=dm.fs(0), color='white', weight='bold')
    x += width
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')
ax1.set_title('Proportional Rectangles', fontsize=dm.fs(1))

# Panel B: Nested rectangles
ax2 = fig.add_subplot(gs[0, 1])
# Outer rectangle
ax2.add_patch(Rectangle((0, 0), 1, 1, facecolor='dm.blue2', edgecolor='dm.blue7', linewidth=1))
ax2.text(0.5, 0.93, 'Category A', ha='center', fontsize=dm.fs(0), weight='bold')
# Inner rectangles
inner_sizes = [0.4, 0.3, 0.3]
inner_colors = ['dm.blue4', 'dm.blue5', 'dm.blue6']
x_inner = 0.05
for size, color in zip(inner_sizes, inner_colors):
    ax2.add_patch(Rectangle((x_inner, 0.05), size-0.02, 0.8, facecolor=color, edgecolor='white', linewidth=1))
    x_inner += size
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')
ax2.set_title('Nested Structure', fontsize=dm.fs(1))

# Panel C: Grid layout
ax3 = fig.add_subplot(gs[1, 0])
grid_data = np.array([[30, 20, 15], [10, 8, 7], [5, 3, 2]])
colors_grid = ['dm.red5', 'dm.red4', 'dm.red3',
               'dm.blue5', 'dm.blue4', 'dm.blue3',
               'dm.green5', 'dm.green4', 'dm.green3']
idx = 0
for i in range(3):
    for j in range(3):
        size = grid_data[i, j]
        rect = Rectangle((j*0.33, 1-(i+1)*0.33), 0.32, 0.32,
                        facecolor=colors_grid[idx], edgecolor='white', linewidth=1.5)
        ax3.add_patch(rect)
        ax3.text(j*0.33 + 0.16, 1-(i+0.5)*0.33, f'{size}',
                ha='center', va='center', fontsize=dm.fs(0), color='white', weight='bold')
        idx += 1
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')
ax3.set_title('Grid Layout', fontsize=dm.fs(1))

# Panel D: Circular segments
ax4 = fig.add_subplot(gs[1, 1])
from matplotlib.patches import Wedge
values = [35, 25, 20, 12, 8]
colors_circ = ['dm.red5', 'dm.blue5', 'dm.green5', 'dm.orange5', 'dm.purple5']
start_angle = 0
for val, color in zip(values, colors_circ):
    angle = val * 3.6  # Convert percentage to degrees
    wedge = Wedge((0.5, 0.5), 0.4, start_angle, start_angle + angle,
                 facecolor=color, edgecolor='white', linewidth=2)
    ax4.add_patch(wedge)
    # Add label
    mid_angle = start_angle + angle/2
    rad = np.deg2rad(mid_angle)
    x = 0.5 + 0.25 * np.cos(rad)
    y = 0.5 + 0.25 * np.sin(rad)
    ax4.text(x, y, f'{val}%', ha='center', va='center', fontsize=dm.fs(-1), color='white', weight='bold')
    start_angle += angle
ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.axis('off')
ax4.set_title('Circular Partition', fontsize=dm.fs(1))

dm.simple_layout(fig, gs=gs)
dm.save_and_show(fig)
