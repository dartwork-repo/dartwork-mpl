import os
import sys
from pathlib import Path

# Fix for PIL truncated image errors during sphinx-gallery generation
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, str(Path(__file__).parent.resolve()))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'dartwork-mpl'
copyright = '2025 Sangwon Lee & Wonjun Choi'
author = ' Sangwon Lee, Wonjun Choi'

version = '0.1.1'
release = '0.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'myst_parser',
    'sphinx_gallery.gen_gallery',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx_tabs.tabs',
]

templates_path = ['_templates']
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    # Helper READMEs inside example sources
    'examples_source/README.rst',
    'examples_source/*/README.rst',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'shibuya'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_js_files = ['custom.js']

# Prevent sections from gallery/index from appearing in the global toctree
toctree_object_entries = False

# Remove version from the sidebar title
html_title = f"{project} documentation"

# -- Shibuya theme options ---------------------------------------------------
html_theme_options = {
    "github_url": "https://github.com/dartwork-repo/dartwork-mpl",
    "accent_color": "teal",
    "globaltoc_expand_depth": 0,  # Start with collapsed sidebar items
    "dark_code": False,  # Use light code blocks (default Shibuya style)
    "nav_links": [
        {"title": "Installation", "url": "installation/index"},
        {"title": "Usage Guide", "url": "usage_guide/index"},
        {"title": "Color System", "url": "color_system/index"},
        {"title": "Examples Gallery", "url": "examples_gallery/index"},
        {"title": "API Reference", "url": "api/index"},
    ]
}


# -- Sphinx Gallery configuration --------------------------------------------
sphinx_gallery_conf = {
     'examples_dirs': 'examples_source',   # path to your example scripts
     'gallery_dirs': 'examples_gallery',  # path to where to save gallery generated output
     'filename_pattern': '/plot_',
     'nested_sections': False,  # Prevent nested sections in sidebar
     'within_subsection_order': 'FileNameSortKey',
     'backreferences_dir': None,  # Don't generate backreferences
     'show_signature': False,
     'remove_config_comments': True,
}

# -- MyST Parser configuration -----------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
myst_heading_anchors = 3


# -- Manual gallery index system ----------------------------------------------
# sphinx-gallery overwrites index files, so we write our manual indices
# AFTER sphinx-gallery runs but BEFORE Sphinx reads the rst files

_GALLERY_MAIN_INDEX = """Examples Gallery
================

This gallery contains examples demonstrating the features and capabilities
of dartwork-mpl. Browse the categories below for ready-to-use patterns
and techniques.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   Basic Plots <basic_plots/index>
   Statistical Plots <statistical_plots/index>
   Bar Charts <bar_charts/index>
   Scientific Plots <scientific_plots/index>
   Time Series <time_series/index>
   Specialized Plots <specialized_plots/index>
   Layout & Styling <layout_styling/index>
   Colors & Images <colors_images/index>
"""

_GALLERY_CATEGORY_INDICES = {
    'basic_plots': """Basic Plots
===========

Fundamental plotting examples demonstrating core dartwork-mpl features.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   plot_basic
   plot_reference_lines
   plot_area_plots
   plot_multiple_lines
   plot_markers
   plot_line_styles
   plot_scatter
   plot_line_advanced
""",
    'statistical_plots': """Statistical Plots
=================

Statistical visualization examples including histograms and distributions.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   plot_histogram
   plot_distribution
   plot_violin_box
   plot_errorbars
   plot_kde_plots
   plot_probability_density
   plot_regression
   plot_correlation_matrix
""",
    'bar_charts': """Bar Charts
==========

Various bar chart styles for categorical data visualization.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   plot_bar_chart
   plot_grouped_bar
   plot_stacked_bar
   plot_horizontal_bar
   plot_diverging_bar
   plot_waterfall
   plot_lollipop
""",
    'scientific_plots': """Scientific Plots
================

Advanced scientific visualizations for academic research.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   plot_3d_surface
   plot_contour
   plot_heatmap
   plot_phase_diagram
   plot_quiver
   plot_scientific_paper
   plot_spectral_analysis
   plot_streamplot
   plot_vector_field_advanced
""",
    'time_series': """Time Series
===========

Time-based data visualization examples.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   plot_autocorrelation
   plot_datetime
   plot_forecast
   plot_rolling_stats
   plot_stem
   plot_step
   plot_time_comparison
   plot_trend_analysis
""",
    'specialized_plots': """Specialized Plots
=================

Specialized visualization types for specific use cases.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   plot_3d
   plot_dual_axis
   plot_filled
   plot_pie
   plot_polar
   plot_radar_chart
   plot_ridgeline
   plot_sankey_simple
   plot_treemap_simple
""",
    'layout_styling': """Layout & Styling
================

Layout optimization and advanced styling techniques.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   plot_annotations
   plot_complex_grid
   plot_custom_ticks
   plot_inset_axes
   plot_layout
   plot_legend
   plot_mixed_subplots
   plot_shared_axes
   plot_subplots
""",
    'colors_images': """Colors & Images
===============

Color palette demonstrations and image display techniques.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   plot_color_cycles
   plot_color_perception
   plot_colors
   plot_custom_colormap
   plot_diverging_sequential
   plot_image
""",
}


def _write_manual_indices(app, env, docnames):
    """Write manual index files AFTER sphinx-gallery but BEFORE Sphinx reads docs."""
    gallery_dir = Path(app.srcdir) / 'examples_gallery'

    # Write main gallery index
    main_index = gallery_dir / 'index.rst'
    main_index.write_text(_GALLERY_MAIN_INDEX)
    print(f"Wrote manual index: examples_gallery/index.rst")

    # Write category indices
    for cat, content in _GALLERY_CATEGORY_INDICES.items():
        idx = gallery_dir / cat / 'index.rst'
        if idx.parent.exists():
            idx.write_text(content)
            print(f"Wrote manual index: examples_gallery/{cat}/index.rst")


def _generate_gallery_assets(_app):
    """Bake high-res color system images during the build."""
    from color_system.generate_assets import build_gallery_assets

    build_gallery_assets()  # Outputs to color_system/images/ by default


def setup(app):
    app.connect("builder-inited", _generate_gallery_assets)
    # Write manual indices AFTER sphinx-gallery runs but BEFORE docs are read
    app.connect("env-before-read-docs", _write_manual_indices)
    return {"parallel_read_safe": True}
