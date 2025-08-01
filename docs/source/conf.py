import os
import sys

# In order to get the module's version
sys.path.insert(0, os.path.abspath('../../'))
import idml2docbook

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'IDML Pandoc reader'
copyright = '2025, Yann Trividic'
author = 'Yann Trividic'
release = idml2docbook.__version__
print("Detected idml2docbook version: " + release)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx_rtd_theme',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.graphviz',
    'notfound.extension'
]

templates_path = ['_templates']
exclude_patterns = []

notfound_urls_prefix = "/fr/"

language = 'fr'

# Internationalisation
language = os.environ.get('LOCALE', 'fr')
languages = os.environ.get('LANGUAGES', 'fr').split(' ')
locale_dirs = ['locale/']
gettext_compact = False
gettext_last_translator = "Yann Trividic"
last_translator = "Yann Trividic <bonjour@yanntrividic.fr>"
language_team = "English <>"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

myst_heading_anchors = 6

html_theme_options = {
    'language_selector': True,
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

html_context = {
    'languages': [(lang, f'../{lang}/') for lang in languages],
}


# These folders are copied to the documentation's HTML output
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'custom.css',
]

graphviz_output_format="svg"