"""
Dual Axis Plot
==============

This example demonstrates how to create a plot with two y-axes, a common requirement in scientific visualization.
"""

import matplotlib.pyplot as plt
import numpy as np
import dartwork_mpl as dm

dm.style.use_preset('scientific')

x = np.arange(0, 10, 0.1)
y1 = np.exp(x / 3)
y2 = np.sin(x)

fig = plt.figure(figsize=(dm.cm2in(10), dm.cm2in(7)))
ax1 = fig.add_subplot(111)

# Plot on primary axis
color1 = 'dm.red5'
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Exponential', color=color1)
ax1.plot(x, y1, color=color1, label='Exp')
ax1.tick_params(axis='y', labelcolor=color1)

# Create secondary axis
ax2 = ax1.twinx()
color2 = 'dm.blue5'
ax2.set_ylabel('Sine', color=color2)
ax2.plot(x, y2, color=color2, label='Sin')
ax2.tick_params(axis='y', labelcolor=color2)

ax1.set_title('Dual Axis Example')

# Combine legends (Optional)
# lines1, labels1 = ax1.get_legend_handles_labels()
# lines2, labels2 = ax2.get_legend_handles_labels()
# ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

dm.simple_layout(fig)
plt.show()
