# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import date
from os import path
from sphinx_kungfu_conf import version_info, download_info

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

root_dir = path.dirname(__file__)


# -- Project information -----------------------------------------------------

project = "功夫核心库"
author = "功夫量化"
copyright = f"2017 - {date.today().year}, {author}, Apache License 2.0"

needs_sphinx = "4.0"

language = "zh_CN"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "rinoh.frontend.sphinx",
    "rst2pdf.pdfbuilder",
    "sphinx_rtd_theme",
    "sphinx_rtd_dark_mode"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = [path.join(root_dir, "_templates")]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
default_dark_mode = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [path.join(root_dir, "_static")]
html_logo = path.join(root_dir, "_static", "images", "logo-sssss.png")

html_favicon = path.join(root_dir, "_static", "images", "icon.png")


# navigation_depth 目录最大深度设置,全局
html_theme_options = {
    "logo_only": True,
    "display_version": True,
    'navigation_depth': 6       
}

# The master toctree document.
master_doc = "index"

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
html_extra_path = [path.join(root_dir, "_static", "css")]

html_css_files = [path.join("css", "toggle.css")]
html_js_files = [path.join("js", "toggle.js")]

############################
# SETUP THE RTD LOWER-LEFT #
############################
try:
    html_context
except NameError:
    html_context = dict()
html_context["display_lower_left"] = True


# SET CURRENT_VERSION
current_version = version_info["current_version"]

# tell the theme which version we're currently on ('current_version' affects
# the lower-left rtd menu and 'version' affects the logo-area version)
html_context["current_version"] = current_version
html_context["version"] = current_version


# POPULATE LINKS TO OTHER VERSIONS
html_context["versions"] = version_info["versions"]
html_context["downloads"] = download_info["versions"]
html_context["has_prerelease"] = version_info["has_prerelease"]



# POPULATE LINKS TO OTHER FORMATS/DOWNLOADS

pdf_doc_name = f"kungfu-doc-v{current_version}"

# settings for creating PDF with rinoh
rinoh_documents = [
    dict(
        doc="index",
        target=pdf_doc_name,
    )
]
today_fmt = "%B %d, %Y"

# settings for rst2pdf
pdf_documents = [
    ("index", pdf_doc_name, "功夫核心库", f"v{current_version}"),
]

latex_pdf_name = f"kungfu-v{current_version}.tex"

pdf_name = f"kungfu-v{current_version}"

# 控制单面输出
latex_elements = {"extraclassoptions": "openany,oneside"}

latex_documents = [
    (master_doc, "index.tex", "功夫核心库", f"v{current_version}", "manual"),
]

man_pages = [(master_doc, pdf_name, "功夫核心库", [author], 1)]


# latex_show_urls = 'footnote'
# latex_use_xindy = True

# settings for EPUB
epub_basename = "target"

# html_context['downloads'] = list()
