"""
Script to generate color and colormap gallery images.

This script generates PNG images from plot_colormaps() and plot_colors() functions
and saves them to docs/images/ directory for use in COLOR_GALLERY.md documentation.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import dartwork_mpl as dm

# Create images directory if it doesn't exist
images_dir = Path(__file__).parent / 'images'
images_dir.mkdir(exist_ok=True)

print("Generating colormap images...")

# Generate colormap images
# We need to modify plot_colormaps behavior to save figures instead of showing them
# Since plot_colormaps calls plt.show() internally, we'll create a custom version
# that saves figures instead

def save_colormaps_by_category():
    """Generate and save colormap images by category."""
    import matplotlib.colors as mcolors
    import matplotlib as mpl
    
    # Get all colormaps (excluding reversed versions)
    cmap_list = list(mpl.colormaps.keys())
    cmap_list = [c for c in cmap_list if not c.endswith('_r')]
    cmap_list = [mpl.cm.get_cmap(c) if isinstance(c, str) else c for c in cmap_list]
    
    # Category order
    category_order = [
        "Sequential Single-Hue",
        "Sequential Multi-Hue",
        "Diverging",
        "Cyclical",
        "Categorical"
    ]
    
    # Classify colormaps by type
    categories = {category: [] for category in category_order}
    for cmap in cmap_list:
        category = dm.classify_colormap(cmap)
        if category in categories:
            categories[category].append(cmap)
    
    # Remove empty categories
    categories = {k: v for k, v in categories.items() if v}
    
    # Create gradient for colormap display
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    
    # Sort categories according to the defined order
    sorted_categories = [cat for cat in category_order if cat in categories]
    
    ncols = 3
    
    # Create and save a figure for each category
    for category in sorted_categories:
        cmaps = categories[category]
        
        # Sort colormaps: dm prefix first, then alphabetical order
        cmaps.sort(key=lambda cmap: (0 if cmap.name.startswith('dm.') else 1, cmap.name.lower()))
        
        # Calculate number of rows needed for this category
        nrows = (len(cmaps) + ncols - 1) // ncols
        
        # Create figure with appropriate size for this category
        figw = 6.4 * ncols / 1.5
        figh = 0.35 + 0.15 + (nrows + 1 + (nrows + 1 - 1) * 0.1) * 0.44
        
        # Create a new figure for this category
        fig = plt.figure(figsize=(figw, figh))
        
        # Create GridSpec with one extra row for the title
        gs = plt.GridSpec(nrows + 1, ncols, figure=fig, height_ratios=[0.3] + [1] * nrows)
        
        # Add category title
        title_ax = fig.add_subplot(gs[0, :])
        title_ax.text(0.5, 0.5, category, fontsize=14, fontweight='bold',
                     ha='center', va='center', transform=title_ax.transAxes)
        title_ax.set_axis_off()
        
        # Add colormaps for this category (column-major order: top to bottom)
        for i, cmap in enumerate(cmaps):
            row = i % nrows
            col = i // nrows
            ax = fig.add_subplot(gs[row + 1, col])
            ax.imshow(gradient, aspect='auto', cmap=cmap)
            ax.text(-0.01, 0.5, cmap.name, va='center', ha='right', fontsize=10,
                   transform=ax.transAxes)
            ax.set_axis_off()
        
        # Hide unused subplots
        total_subplots = (nrows + 1) * ncols
        used_subplots = 1 + len(cmaps)  # 1 for title + number of colormaps
        for i in range(used_subplots, total_subplots):
            row = i // ncols
            col = i % ncols
            if row < nrows + 1 and col < ncols:
                ax = fig.add_subplot(gs[row, col])
                ax.set_visible(False)
        
        plt.tight_layout()
        
        # Save figure
        filename = f"colormaps_{category.lower().replace(' ', '_')}.png"
        filepath = images_dir / filename
        fig.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"  Saved: {filename}")

print("Generating color images...")

# Generate color images
# plot_colors() returns a list of figures, one per library
figs = dm.plot_colors(ncols=6, sort_colors=True)

# Library order matches what plot_colors uses
library_order = ['opencolor', 'tw', 'md', 'ant', 'chakra', 'primer', 'other', 'xkcd']

# Save each figure
for i, fig in enumerate(figs):
    if i < len(library_order):
        library_name = library_order[i]
        filename = f"colors_{library_name}.png"
        filepath = images_dir / filename
        fig.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"  Saved: {filename}")

print("\nGallery images generated successfully!")
print(f"Images saved to: {images_dir}")

