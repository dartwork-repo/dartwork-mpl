"""
Heatmap
=======

Heatmap visualization.
"""

import matplotlib.pyplot as plt
import numpy as np
import dartwork_mpl as dm

dm.style.use_preset('scientific')

# Generate data
data = np.random.rand(10, 10)

fig = plt.figure(figsize=(dm.cm2in(10), dm.cm2in(8)), dpi=200)
gs = fig.add_gridspec(
    1, 1,
    left=0.15, right=0.88,
    top=0.92, bottom=0.12
)
ax = fig.add_subplot(gs[0, 0])

# Use dartwork-mpl's spectral colormap
# You can access it via 'dm.Spectral' or 'dm.coolwarm' etc.
im = ax.imshow(data, cmap='dm.Spectral')

# Add colorbar
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('Intensity', fontsize=dm.fs(0))

ax.set_title('Random Heatmap with dm.spectral', fontsize=dm.fs(1))
ax.set_xlabel('X Axis', fontsize=dm.fs(0))
ax.set_ylabel('Y Axis', fontsize=dm.fs(0))

dm.simple_layout(fig, gs=gs)
plt.show()
