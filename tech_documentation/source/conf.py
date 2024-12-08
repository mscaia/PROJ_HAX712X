# Configuration file for the Sphinx documentation builder.
#

import os
import sys
import pandas as pd

# -- Path setup --------------------------------------------------------------
# Add project directory to sys.path
sys.path.insert(0, os.path.abspath('../../Cycle3'))
print("sys.path:", sys.path)

# -- Project information -----------------------------------------------------
project = 'CycleVision3'
copyright = '2024, ARMAND Charlotte, CONDAMY Fabian, SCAIA Matteo, STETSUN Kateryna'
author = 'ARMAND Charlotte, CONDAMY Fabian, SCAIA Matteo, STETSUN Kateryna'
release = '1.0.1'

# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and dirs to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The master document
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_baseurl = "https://mscaia.github.io/PROJ_HAX712X/"
language = 'fr'

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None)
}

# Autodoc settings
autodoc_mock_imports = [
    'osmnx', 'folium', 'networkx', 'pandas', 'numpy', 'matplotlib', 'seaborn',
    'cycler', 'pooch', 'plotly', 'kaleido', 'ipywidgets', 'memory_profiler'
]