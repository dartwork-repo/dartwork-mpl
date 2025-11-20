"""
Annotations
===========

This example demonstrates various annotation techniques including text annotations,
arrow annotations, and custom markers with labels.
"""

import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Apply scientific style preset
# Default: font.size=7.5, lines.linewidth=0.5, axes.linewidth=0.3
dm.style.use_preset('scientific')

# Generate sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

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

# Panel A: Text annotations
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(x, y, color='dm.blue5', lw=0.7, alpha=0.8)
# Text annotation: fontsize=dm.fs(-1), bbox with explicit parameters
ax1.text(2, 0.5, 'Peak', fontsize=dm.fs(-1), 
         bbox=dict(boxstyle='round', facecolor='dm.blue2', alpha=0.5, 
                   edgecolor='dm.blue7', linewidth=0.3),
         ha='center', va='center')
ax1.text(8, -0.5, 'Valley', fontsize=dm.fs(-1),
         bbox=dict(boxstyle='round', facecolor='dm.red2', alpha=0.5,
                   edgecolor='dm.red7', linewidth=0.3),
         ha='center', va='center')
ax1.set_xlabel('Time [s]', fontsize=dm.fs(0))
ax1.set_ylabel('Amplitude', fontsize=dm.fs(0))
ax1.set_title('Text Annotations', fontsize=dm.fs(1))
ax1.set_xticks([0, 2, 4, 6, 8, 10])
ax1.set_yticks([-1, -0.5, 0, 0.5, 1])

# Panel B: Arrow annotations
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(x, y, color='dm.red5', lw=0.7, alpha=0.8)
# Arrow annotation: arrowprops with explicit parameters
ax2.annotate('Maximum', xy=(np.pi/2, 1), xytext=(4, 0.5),
             arrowprops=dict(arrowstyle='->', color='dm.red7', 
                           lw=0.7, connectionstyle='arc3,rad=0.3'),
             fontsize=dm.fs(-1), ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='white', 
                      alpha=0.8, edgecolor='dm.red7', linewidth=0.3))
ax2.annotate('Minimum', xy=(3*np.pi/2, -1), xytext=(7, -0.5),
             arrowprops=dict(arrowstyle='->', color='dm.red7',
                           lw=0.7, connectionstyle='arc3,rad=-0.3'),
             fontsize=dm.fs(-1), ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='white',
                      alpha=0.8, edgecolor='dm.red7', linewidth=0.3))
ax2.set_xlabel('Time [s]', fontsize=dm.fs(0))
ax2.set_ylabel('Amplitude', fontsize=dm.fs(0))
ax2.set_title('Arrow Annotations', fontsize=dm.fs(1))
ax2.set_xticks([0, 2, 4, 6, 8, 10])
ax2.set_yticks([-1, -0.5, 0, 0.5, 1])

# Panel C: Custom markers with labels
ax3 = fig.add_subplot(gs[0, 2])
ax3.plot(x, y, color='dm.green5', lw=0.7, alpha=0.8)
# Mark specific points: markersize=6, markeredgewidth=0.5
peak_idx = np.argmax(y)
valley_idx = np.argmin(y)
ax3.plot(x[peak_idx], y[peak_idx], 'o', color='dm.green7', 
         markersize=6, markeredgewidth=0.5, markeredgecolor='white',
         label='Peak', zorder=5)
ax3.plot(x[valley_idx], y[valley_idx], 's', color='dm.red7',
         markersize=6, markeredgewidth=0.5, markeredgecolor='white',
         label='Valley', zorder=5)
# Add labels next to markers: fontsize=dm.fs(-1)
ax3.text(x[peak_idx] + 0.5, y[peak_idx] + 0.2, 'Peak', 
         fontsize=dm.fs(-1), ha='left', va='bottom',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8,
                  edgecolor='dm.green7', linewidth=0.3))
ax3.text(x[valley_idx] + 0.5, y[valley_idx] - 0.2, 'Valley',
         fontsize=dm.fs(-1), ha='left', va='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8,
                  edgecolor='dm.red7', linewidth=0.3))
ax3.set_xlabel('Time [s]', fontsize=dm.fs(0))
ax3.set_ylabel('Amplitude', fontsize=dm.fs(0))
ax3.set_title('Custom Markers', fontsize=dm.fs(1))
ax3.legend(loc='upper right', fontsize=dm.fs(-1), ncol=1)
ax3.set_xticks([0, 2, 4, 6, 8, 10])
ax3.set_yticks([-1, -0.5, 0, 0.5, 1])

# Optimize layout
dm.simple_layout(fig, gs=gs)

# Show plot
plt.show()

