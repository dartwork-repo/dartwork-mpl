"""
3D Surface Plot
===============

This example demonstrates that dartwork-mpl styles also work well with 3D plots.
"""

import matplotlib.pyplot as plt
import numpy as np
import dartwork_mpl as dm

dm.style.use_preset('presentation')

fig = plt.figure(figsize=(dm.cm2in(12), dm.cm2in(10)))
ax = fig.add_subplot(111, projection='3d')

# Make data
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap='dm.Spectral',
                       linewidth=0, antialiased=False)

# Customize axis labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_title('3D Surface Plot')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

# Note: dm.simple_layout might not work perfectly with 3D axes in all cases,
# but standard tight_layout usually works fine or manual adjustment.
plt.tight_layout()
plt.show()
