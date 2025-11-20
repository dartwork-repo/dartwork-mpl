"""
Heatmap Visualization
=====================

This example demonstrates how to create heatmaps using dartwork-mpl's custom colormaps.
"""

import matplotlib.pyplot as plt
import numpy as np
import dartwork_mpl as dm

dm.style.use_preset('scientific')

# Generate data
data = np.random.rand(10, 10)

fig = plt.figure(figsize=(dm.cm2in(10), dm.cm2in(8)))
gs = fig.add_gridspec(1, 1)
ax = fig.add_subplot(gs[0, 0])

# Use dartwork-mpl's spectral colormap
# You can access it via 'dm.Spectral' or 'dm.coolwarm' etc.
im = ax.imshow(data, cmap='dm.Spectral')

# Add colorbar
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('Intensity')

ax.set_title('Random Heatmap with dm.spectral')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')

dm.simple_layout(fig, gs=gs)
plt.show()
