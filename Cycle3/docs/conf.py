# Configuration file for the Sphinx documentation builder

import os
import sys
import pandas as pd

# -- Path setup --------------------------------------------------------------
# Add project directory to sys.path
sys.path.insert(0, os.path.abspath('../../Cycle3'))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Cycle3', 'analyse_donnee')))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Cycle3', 'map')))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Cycle3', 'video')))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Cycle3', 'data')))

# -- Project information -----------------------------------------------------
project = 'CycleVision3'
copyright = '2024, ARMAND Charlotte, CONDAMY Fabian, SCAIA Matteo, STETSUN Kateryna'
author = 'ARMAND Charlotte, CONDAMY Fabian, SCAIA Matteo, STETSUN Kateryna'
release = '1.0.0'

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
# autodoc_mock_imports = [ 'osmnx', 'folium', 'networkx', 'pandas', 'numpy', 'matplotlib', 'seaborn','cycler', 'pooch', 'plotly', 'kaleido', 'ipywidgets', 'memory_profiler'
autodoc_mock_imports = ["map, video, analyse-donnee"]  # Si certains modules ne sont pas installés]

autodoc_member_order = 'bysource'
autodoc_inherit_docstrings = True

todo_include_todos = True

def setup(app):
    app.add_css_file('custom.css')  # Add custom CSS if needed