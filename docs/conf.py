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
        {"title": "Colors", "url": "COLORS"},
        {"title": "Colormaps", "url": "COLORMAPS"},
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


def _generate_gallery_assets(_app):
    """Bake high-res color system images during the build."""
    from generate_gallery import build_gallery_assets

    build_gallery_assets(Path(__file__).parent)


def setup(app):
    app.connect("builder-inited", _generate_gallery_assets)
    return {"parallel_read_safe": True}
