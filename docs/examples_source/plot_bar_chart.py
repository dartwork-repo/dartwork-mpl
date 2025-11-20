"""
Bar Chart Styling
=================

This example demonstrates how to create stylish bar charts using dartwork-mpl and Tailwind CSS colors.
"""

import matplotlib.pyplot as plt
import numpy as np
import dartwork_mpl as dm

# Apply presentation style for bolder look
dm.style.use_preset('presentation')

# Data
labels = ['Q1', 'Q2', 'Q3', 'Q4']
men_means = [20, 34, 30, 35]
women_means = [25, 32, 34, 20]

x = np.arange(len(labels))
width = 0.35

fig = plt.figure(figsize=(dm.cm2in(12), dm.cm2in(8)))
ax = fig.add_subplot(111)

# Plotting with Tailwind colors
rects1 = ax.bar(x - width/2, men_means, width, label='Men', color='tw.sky:500')
rects2 = ax.bar(x + width/2, women_means, width, label='Women', color='tw.rose:500')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Add value labels
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

ax.set_ylim(0, 45)

dm.simple_layout(fig)

plt.show()
