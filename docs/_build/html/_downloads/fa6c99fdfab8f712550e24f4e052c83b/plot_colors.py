"""
Colors
======

Color palette visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

# Apply style
dm.style.use_preset('scientific')

# Create figure
fig = plt.figure(figsize=(dm.cm2in(12), dm.cm2in(8)), dpi=300)
gs = fig.add_gridspec(
    1, 1,
    left=0.12, right=0.95,
    top=0.88, bottom=0.17
)
ax = fig.add_subplot(gs[0, 0])

x = np.linspace(0, 10, 100)

# 1. dartwork-mpl custom colors (dm.*)
ax.plot(x, np.sin(x), color='dm.red5', lw=2, label='dm.red5')
ax.plot(x, np.cos(x), color='dm.blue5', lw=2, label='dm.blue5')

# 2. Tailwind CSS colors (tw.* or tailwind.*)
ax.plot(x, np.sin(x) + 2, color='tw.green:500', lw=2, label='tw.green:500')
ax.plot(x, np.cos(x) + 2, color='tw.purple:500', lw=2, label='tw.purple:500')

# 3. Color mixing
# Mix red and blue
mixed_color = dm.mix_colors('dm.red5', 'dm.blue5', alpha=0.5)
ax.plot(x, np.sin(x) + 4, color=mixed_color, lw=2, label='Mixed (Red+Blue)')

# 4. Pseudo-transparency
# Create a lighter version of red by mixing with white
transparent_red = dm.pseudo_alpha('dm.red5', alpha=0.3, background='white')
ax.fill_between(x, np.sin(x) + 4, 5.5, color=transparent_red, label='Pseudo-alpha Red')

ax.set_ylim(-1.5, 6)
ax.set_xlabel('X', fontsize=dm.fs(0))
ax.set_ylabel('Y', fontsize=dm.fs(0))
ax.set_title('dartwork-mpl Color System', fontsize=dm.fs(1))
ax.legend(ncol=2, loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize=dm.fs(-1))

dm.simple_layout(fig, gs=gs)
plt.show()
