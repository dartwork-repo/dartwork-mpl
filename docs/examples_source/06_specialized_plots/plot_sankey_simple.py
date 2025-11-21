"""
Flow Diagrams
=============

Visualizing flows and connections between elements.
"""

import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

dm.style.use_preset('scientific')

fig = plt.figure(figsize=(dm.cm2in(17), dm.cm2in(10)), dpi=200)
gs = fig.add_gridspec(nrows=2, ncols=2, left=0.08, right=0.98,
                      top=0.95, bottom=0.08, wspace=0.3, hspace=0.4)

# Panel A: Simple flow diagram
ax1 = fig.add_subplot(gs[0, 0])
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
boxes = [('Input', 0.1, 0.5), ('Process', 0.5, 0.5), ('Output', 0.9, 0.5)]
for label, x, y in boxes:
    box = FancyBboxPatch((x-0.08, y-0.1), 0.16, 0.2, boxstyle="round,pad=0.01",
                         edgecolor='dm.blue5', facecolor='dm.blue2', linewidth=0.7)
    ax1.add_patch(box)
    ax1.text(x, y, label, ha='center', va='center', fontsize=dm.fs(0))
arrow1 = FancyArrowPatch((0.18, 0.5), (0.42, 0.5), arrowstyle='->', lw=0.7, color='dm.gray7')
arrow2 = FancyArrowPatch((0.58, 0.5), (0.82, 0.5), arrowstyle='->', lw=0.7, color='dm.gray7')
ax1.add_patch(arrow1)
ax1.add_patch(arrow2)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')
ax1.set_title('Simple Flow', fontsize=dm.fs(1))

# Panel B: Branch flow
ax2 = fig.add_subplot(gs[0, 1])
ax2.add_patch(FancyBboxPatch((0.05, 0.45), 0.15, 0.1, boxstyle="round,pad=0.01",
                            edgecolor='dm.green5', facecolor='dm.green2', lw=0.7))
ax2.text(0.125, 0.5, 'Start', ha='center', va='center', fontsize=dm.fs(-1))
for i, label in enumerate(['A', 'B', 'C']):
    y = 0.7 - i*0.2
    ax2.add_patch(FancyBboxPatch((0.4, y-0.05), 0.15, 0.1, boxstyle="round,pad=0.01",
                                edgecolor='dm.blue5', facecolor='dm.blue2', lw=0.7))
    ax2.text(0.475, y, label, ha='center', va='center', fontsize=dm.fs(-1))
    arrow = FancyArrowPatch((0.2, 0.5), (0.4, y), arrowstyle='->', lw=0.5, color='dm.gray7')
    ax2.add_patch(arrow)
ax2.set_xlim(0, 0.7)
ax2.set_ylim(0.1, 0.9)
ax2.axis('off')
ax2.set_title('Branching Flow', fontsize=dm.fs(1))

# Panel C: Circular flow
ax3 = fig.add_subplot(gs[1, 0])
angles = np.linspace(0, 2*np.pi, 5, endpoint=False)
radius = 0.3
labels = ['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4']
for i, (angle, label) in enumerate(zip(angles[:-1], labels)):
    x, y = 0.5 + radius*np.cos(angle), 0.5 + radius*np.sin(angle)
    ax3.add_patch(FancyBboxPatch((x-0.08, y-0.05), 0.16, 0.1, boxstyle="round,pad=0.01",
                                edgecolor='dm.orange5', facecolor='dm.orange2', lw=0.7))
    ax3.text(x, y, label, ha='center', va='center', fontsize=dm.fs(-2))
    # Arrow to next
    next_angle = angles[i+1]
    x2, y2 = 0.5 + radius*np.cos(next_angle), 0.5 + radius*np.sin(next_angle)
    ax3.annotate('', xy=(x2-0.08, y2), xytext=(x+0.08, y),
                arrowprops=dict(arrowstyle='->', lw=0.5, color='dm.gray7'))
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')
ax3.set_title('Circular Flow', fontsize=dm.fs(1))

# Panel D: Decision tree
ax4 = fig.add_subplot(gs[1, 1])
ax4.add_patch(FancyBboxPatch((0.4, 0.8), 0.2, 0.1, boxstyle="round,pad=0.01",
                            edgecolor='dm.purple5', facecolor='dm.purple2', lw=0.7))
ax4.text(0.5, 0.85, 'Decision', ha='center', va='center', fontsize=dm.fs(-1))
for i, (x, label) in enumerate([(0.25, 'Yes'), (0.75, 'No')]):
    ax4.add_patch(FancyBboxPatch((x-0.1, 0.5), 0.2, 0.1, boxstyle="round,pad=0.01",
                                edgecolor='dm.blue5', facecolor='dm.blue2', lw=0.7))
    ax4.text(x, 0.55, label, ha='center', va='center', fontsize=dm.fs(-1))
    arrow = FancyArrowPatch((0.5, 0.8), (x, 0.6), arrowstyle='->', lw=0.5, color='dm.gray7')
    ax4.add_patch(arrow)
ax4.set_xlim(0, 1)
ax4.set_ylim(0.3, 1)
ax4.axis('off')
ax4.set_title('Decision Tree', fontsize=dm.fs(1))

dm.simple_layout(fig, gs=gs)
dm.save_and_show(fig)
