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
# toctree_object_entries = False  # Removed as it might interfere with sidebar

# Remove version from the sidebar title
html_title = f"{project} documentation"

# -- Shibuya theme options ---------------------------------------------------
html_theme_options = {
    "github_url": "https://github.com/dartwork-repo/dartwork-mpl",
    "accent_color": "teal",
    "globaltoc_expand_depth": 1,  # Allow expanding sidebar items
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
# -- Sphinx Gallery configuration --------------------------------------------

sphinx_gallery_conf = {
     'examples_dirs': [
         'examples_source/basic_plots',
         'examples_source/statistical_plots',
         'examples_source/bar_charts',
         'examples_source/scientific_plots',
         'examples_source/time_series',
         'examples_source/specialized_plots',
         'examples_source/layout_styling',
         'examples_source/colors_images',
     ],
     'gallery_dirs': [
         'examples_gallery/basic_plots',
         'examples_gallery/statistical_plots',
         'examples_gallery/bar_charts',
         'examples_gallery/scientific_plots',
         'examples_gallery/time_series',
         'examples_gallery/specialized_plots',
         'examples_gallery/layout_styling',
         'examples_gallery/colors_images',
     ],
     'filename_pattern': '/plot_',
     'nested_sections': False,
     'within_subsection_order': 'FileNameSortKey',
     'backreferences_dir': None,
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

.. grid:: 2 2 3 3
    :gutter: 2

    .. grid-item-card:: Basic Plots
        :link: basic_plots/index
        :link-type: doc

        Fundamental plotting examples demonstrating core dartwork-mpl features.

    .. grid-item-card:: Statistical Plots
        :link: statistical_plots/index
        :link-type: doc

        Statistical visualization examples including histograms and distributions.

    .. grid-item-card:: Bar Charts
        :link: bar_charts/index
        :link-type: doc

        Various bar chart styles for categorical data visualization.

    .. grid-item-card:: Scientific Plots
        :link: scientific_plots/index
        :link-type: doc

        Advanced scientific visualizations for academic research.

    .. grid-item-card:: Time Series
        :link: time_series/index
        :link-type: doc

        Time-based data visualization examples.

    .. grid-item-card:: Specialized Plots
        :link: specialized_plots/index
        :link-type: doc

        Specialized visualization types for specific use cases.

    .. grid-item-card:: Layout & Styling
        :link: layout_styling/index
        :link-type: doc

        Layout optimization and advanced styling techniques.

    .. grid-item-card:: Colors & Images
        :link: colors_images/index
        :link-type: doc

        Color palette demonstrations and image display techniques.

.. toctree::
   :hidden:

   Basic Plots <basic_plots/index>
   Statistical Plots <statistical_plots/index>
   Bar Charts <bar_charts/index>
   Scientific Plots <scientific_plots/index>
   Time Series <time_series/index>
   Specialized Plots <specialized_plots/index>
   Layout & Styling <layout_styling/index>
   Colors & Images <colors_images/index>
"""


def _write_manual_indices(app, env, docnames):
    """Write manual index files AFTER sphinx-gallery but BEFORE Sphinx reads docs."""
    gallery_dir = Path(app.srcdir) / 'examples_gallery'

    # Write main gallery index
    main_index = gallery_dir / 'index.rst'
    main_index.write_text(_GALLERY_MAIN_INDEX)
    print(f"Wrote manual index: examples_gallery/index.rst")


def _generate_gallery_assets(_app):
    """Bake high-res color system images during the build."""
    from color_system.generate_assets import build_gallery_assets

    build_gallery_assets()  # Outputs to color_system/images/ by default


def setup(app):
    app.connect("builder-inited", _generate_gallery_assets)
    # Write manual indices AFTER sphinx-gallery runs but BEFORE docs are read
    app.connect("env-before-read-docs", _write_manual_indices)
    return {"parallel_read_safe": True}
