# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../../backend/app'))

project = 'SnapQR MVP'
copyright = '2025, JazzDataSolutions'
author = 'JazzDataSolutions'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints', 
    'recommonmark',
    'sphinxcontrib.plantuml', # para los .puml
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

plantuml = 'plantuml'  # o ruta absoluta a plantuml.jar

html_theme = 'sphinx_rtd_theme'

# Permitir Markdown
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
