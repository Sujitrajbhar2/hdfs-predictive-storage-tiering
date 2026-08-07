"""
style_loader.py

One job only: read every .css file inside assets/css and inject
it into the Streamlit page. Every page (Home, Analytics, Prediction)
calls load_all_css() once at the top, so styling stays identical
across the whole app.

If you add a new .css file to assets/css, add its name to the
CSS_FILES list below and it will load automatically.
"""

import streamlit as st

# The order matters a little: theme.css must load first because
# every other file uses the color variables defined inside it.
CSS_FILES = [
    "theme.css",
    "background.css",
    "layout.css",
    "sidebar.css",
    "cards.css",
    "dashboard.css",
    "charts.css",
    "tables.css",
    "animations.css",
    "responsive.css",
]

CSS_FOLDER = "assets/css"


def load_all_css():
    """Read each file listed in CSS_FILES and inject it as one <style> block."""
    combined_css = ""

    for file_name in CSS_FILES:
        file_path = f"{CSS_FOLDER}/{file_name}"
        with open(file_path, "r") as css_file:
            combined_css += css_file.read()
            combined_css += "\n"

    st.markdown(f"<style>{combined_css}</style>", unsafe_allow_html=True)
