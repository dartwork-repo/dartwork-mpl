"""
Probability Density Plot
========================

This example demonstrates how to visualize probability distributions using histograms and Kernel Density Estimation (KDE).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import dartwork_mpl as dm

# Apply scientific style
dm.style.use_preset('scientific')

# Generate synthetic data
np.random.seed(42)
data = np.concatenate([
    np.random.normal(0, 1, 1000),
    np.random.normal(4, 1.5, 500)
])

fig = plt.figure(figsize=(dm.cm2in(10), dm.cm2in(7)))
ax = fig.add_subplot(111)

# Histogram
# Use 'density=True' to normalize
n, bins, patches = ax.hist(data, bins=30, density=True, 
                           color='dm.gray3', alpha=0.6, 
                           edgecolor='white', label='Histogram')

# Kernel Density Estimation (KDE)
kde = stats.gaussian_kde(data)
x_grid = np.linspace(data.min() - 1, data.max() + 1, 200)
ax.plot(x_grid, kde(x_grid), color='dm.blue5', lw=2, label='KDE')

# Normal Distribution Fit (for comparison)
mu, std = stats.norm.fit(data)
p = stats.norm.pdf(x_grid, mu, std)
ax.plot(x_grid, p, color='dm.red5', lw=1.5, linestyle='--', label='Normal Fit')

ax.set_xlabel('Value')
ax.set_ylabel('Probability Density')
ax.set_title('Distribution Analysis')
ax.legend()

dm.simple_layout(fig)
plt.show()
