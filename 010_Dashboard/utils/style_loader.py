"""
style_loader.py

Loads every CSS file from:

010_Dashboard/assets/css/

and injects the combined CSS into the Streamlit application.

The path is calculated relative to this Python file, so the
application works correctly even when Streamlit is started
from the DataTierAI project root.
"""

import streamlit as st
from pathlib import Path


# ============================================================
# CSS FILE ORDER
# ============================================================
# theme.css should load first because other CSS files use
# variables defined inside theme.css.
# ============================================================

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


# ============================================================
# FIND THE CSS DIRECTORY
# ============================================================
#
# Current file:
#
# DataTierAI/
# └── 010_Dashboard/
#     └── utils/
#         └── style_loader.py
#
# parent        -> utils
# parent.parent -> 010_Dashboard
#
# Therefore:
#
# 010_Dashboard/assets/css
#
# ============================================================

DASHBOARD_DIR = Path(__file__).resolve().parent.parent

CSS_FOLDER = DASHBOARD_DIR / "assets" / "css"


# ============================================================
# LOAD ALL CSS
# ============================================================

def load_all_css():
    """
    Read every CSS file listed in CSS_FILES and inject
    the combined CSS into the Streamlit page.
    """

    combined_css = ""

    # --------------------------------------------------------
    # Check CSS directory
    # --------------------------------------------------------

    if not CSS_FOLDER.exists():

        st.error(
            f"CSS folder not found:\n\n{CSS_FOLDER}"
        )

        return

    # --------------------------------------------------------
    # Load CSS files
    # --------------------------------------------------------

    for file_name in CSS_FILES:

        file_path = CSS_FOLDER / file_name

        # ----------------------------------------------------
        # Check individual CSS file
        # ----------------------------------------------------

        if not file_path.exists():

            st.warning(
                f"CSS file not found: {file_path}"
            )

            continue

        # ----------------------------------------------------
        # Read CSS
        # ----------------------------------------------------

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as css_file:

                combined_css += css_file.read()
                combined_css += "\n\n"

        except Exception as error:

            st.warning(
                f"Unable to load {file_name}: {error}"
            )

    # --------------------------------------------------------
    # Inject CSS into Streamlit
    # --------------------------------------------------------

    if combined_css:

        st.markdown(
            f"""
            <style>
            {combined_css}
            </style>
            """,
            unsafe_allow_html=True,
        )