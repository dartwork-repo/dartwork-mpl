"""
Streamplot
==========

This example demonstrates how to create a streamplot to visualize vector fields.
"""

import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Apply scientific style
dm.style.use_preset('scientific')

# Generate vector field
Y, X = np.mgrid[-3:3:100j, -3:3:100j]
U = -1 - X**2 + Y
V = 1 + X - Y**2
speed = np.sqrt(U**2 + V**2)

fig = plt.figure(figsize=(dm.cm2in(10), dm.cm2in(8)))
gs = fig.add_gridspec(1, 1)
ax = fig.add_subplot(gs[0, 0])

# Streamplot
# Use dartwork-mpl's viridis colormap
strm = ax.streamplot(X, Y, U, V, color=speed, linewidth=2, cmap='dm.viridis')

# Add colorbar
cbar = fig.colorbar(strm.lines, ax=ax)
cbar.set_label('Speed')

ax.set_title('Vector Field Streamplot')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')

dm.simple_layout(fig, gs=gs)
plt.show()
