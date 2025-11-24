import os
import sys
from pathlib import Path

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

# Remove version from the sidebar title
html_title = f"{project} documentation"

# -- Shibuya theme options ---------------------------------------------------
html_theme_options = {
    "github_url": "https://github.com/dartwork-repo/dartwork-mpl",
    "accent_color": "teal",
    "globaltoc_expand_depth": 0,  # Start with collapsed sidebar items
    "dark_code": False,  # Use light code blocks (default Shibuya style)
    "nav_links": [
        {"title": "Installation", "url": "installation"},
        {"title": "Usage Guide", "url": "DARTWORK_MPL_USAGE_GUIDE"},
        {"title": "Color System", "url": "COLOR_SYSTEM"},
        {"title": "Examples Gallery", "url": "gallery/index"},
        {"title": "API Reference", "url": "api/index"},
    ]
}


# -- Sphinx Gallery configuration --------------------------------------------
sphinx_gallery_conf = {
     'examples_dirs': 'examples_source',   # path to your example scripts
     'gallery_dirs': 'gallery',  # path to where to save gallery generated output
     'filename_pattern': '/plot_',
}

# -- MyST Parser configuration -----------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
myst_heading_anchors = 3


_GALLERY_TOC_OLD = """.. toctree::
   :hidden:
   :includehidden:


   /gallery/01_basic_plots/index.rst
   /gallery/02_statistical_plots/index.rst
   /gallery/03_bar_charts/index.rst
   /gallery/04_scientific_plots/index.rst
   /gallery/05_time_series/index.rst
   /gallery/06_specialized_plots/index.rst
   /gallery/07_layout_styling/index.rst
   /gallery/08_colors_images/index.rst
"""

_GALLERY_TOC_NEW = """.. toctree::
   :maxdepth: 1
   :caption: Categories

   Basic Plots <gallery/01_basic_plots/index>
   Statistical Plots <gallery/02_statistical_plots/index>
   Bar Charts <gallery/03_bar_charts/index>
   Scientific Plots <gallery/04_scientific_plots/index>
   Time Series <gallery/05_time_series/index>
   Specialized Plots <gallery/06_specialized_plots/index>
   Layout & Styling <gallery/07_layout_styling/index>
   Colors & Images <gallery/08_colors_images/index>
"""


def _patch_gallery_toc(_app, docname, source):
    """Ensure sphinx-gallery output exposes the category toctree in nav."""
    if docname != "gallery/index":
        return

    current = source[0]
    if _GALLERY_TOC_NEW in current:
        return

    if _GALLERY_TOC_OLD in current:
        source[0] = current.replace(_GALLERY_TOC_OLD, _GALLERY_TOC_NEW)
    else:
        # Fall back to appending so nav still appears if template changes.
        source[0] = f"{current.strip()}\n\n{_GALLERY_TOC_NEW}"


def _generate_gallery_assets(_app):
    """Bake high-res color system images during the build."""
    from generate_gallery import build_gallery_assets

    build_gallery_assets(Path(__file__).parent)


def setup(app):
    app.connect("builder-inited", _generate_gallery_assets)
    app.connect("source-read", _patch_gallery_toc)
    return {"parallel_read_safe": True}
