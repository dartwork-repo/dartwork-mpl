"""
Basic Usage
===========

This example demonstrates the basic usage of dartwork-mpl, including applying style presets and creating a simple plot.
"""

import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Apply scientific style preset
dm.style.use_preset('scientific')

# Generate sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create figure
# Use dm.cm2in to convert centimeters to inches for precise sizing
fig = plt.figure(figsize=(dm.cm2in(9), dm.cm2in(7)))

# Create axes using GridSpec
gs = fig.add_gridspec(nrows=1, ncols=1)
ax = fig.add_subplot(gs[0, 0])

# Plot data
# Use dartwork-mpl custom colors (dm.red5, dm.blue5)
ax.plot(x, y1, label='Sin', color='dm.red5')
ax.plot(x, y2, label='Cos', color='dm.blue5')

# Set labels and title
ax.set_xlabel('Time [s]')
ax.set_ylabel('Amplitude')
ax.set_title('Basic Sine/Cosine Plot')

# Add legend
ax.legend()

# Optimize layout
dm.simple_layout(fig)

# Show plot
plt.show()
