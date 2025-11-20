"""
Violin and Box Plots
====================

This example compares Box plots and Violin plots for visualizing distributions.
"""

import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Apply scientific style
dm.style.use_preset('scientific')

# Generate data
np.random.seed(10)
data = [np.random.normal(0, std, 100) for std in range(1, 5)]

fig = plt.figure(figsize=(dm.cm2in(15), dm.cm2in(8)))
gs = fig.add_gridspec(1, 2, wspace=0.3)

# Box Plot
ax1 = fig.add_subplot(gs[0])
ax1.boxplot(data, patch_artist=True, 
            boxprops=dict(facecolor='dm.blue3', color='dm.blue7'),
            medianprops=dict(color='white'),
            whiskerprops=dict(color='dm.gray7'),
            capprops=dict(color='dm.gray7'))
ax1.set_title('Box Plot')
ax1.set_xlabel('Category')
ax1.set_ylabel('Value')

# Violin Plot
ax2 = fig.add_subplot(gs[1])
parts = ax2.violinplot(data, showmeans=False, showmedians=True)

# Customize violin plot colors
for pc in parts['bodies']:
    pc.set_facecolor('dm.red5')
    pc.set_edgecolor('dm.red7')
    pc.set_alpha(0.7)

for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians'):
    vp = parts[partname]
    vp.set_edgecolor('dm.gray7')
    vp.set_linewidth(1)

ax2.set_title('Violin Plot')
ax2.set_xlabel('Category')
ax2.set_ylabel('Value')

dm.simple_layout(fig, gs=gs)
plt.show()
