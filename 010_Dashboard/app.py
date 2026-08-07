
import streamlit as st

from utils.style_loader import load_all_css
from views import (
    dashboard,
    analytics,
    prediction,
    storage_optimizer,
    data_explorer,
    reports,
    alerts,
    about,
)


# -----------------------------------------------------------------
# 1. PAGE CONFIG - must be the very first Streamlit command
# -----------------------------------------------------------------
st.set_page_config(
    page_title="DataTierAI Dashboard",
    page_icon="💠",
    layout="wide",
)

load_all_css()


# -----------------------------------------------------------------
# 2. SIDEBAR BRANDING (shown above the menu on every page)
# -----------------------------------------------------------------


st.sidebar.markdown("""
<div class="sidebar-logo">

<h2 class="sidebar-title">🚀 DataTierAI</h2>

<p class="sidebar-subtitle">
Intelligent Data Lifecycle<br>
Analytics Platform
</p>

</div>
""",unsafe_allow_html=True)

# -----------------------------------------------------------------
# 3. THE 8-ITEM SIDEBAR MENU
# The order in this list is the order they appear in the sidebar.
# Each st.Page needs its own url_path - without it, Streamlit tries
# to build the URL from the function name, and every view here is
# named "render", which would collide. Giving each one an explicit
# url_path avoids that.
# -----------------------------------------------------------------
navigation_pages = [
    st.Page(dashboard.render, title="Dashboard", icon="🏠", url_path="dashboard", default=True),
    st.Page(analytics.render, title="Analytics", icon="📊", url_path="analytics"),
    st.Page(prediction.render, title="Prediction", icon="🤖", url_path="prediction"),
    st.Page(storage_optimizer.render, title="Storage Optimizer", icon="💾", url_path="storage-optimizer"),
    st.Page(data_explorer.render, title="Data Explorer", icon="📁", url_path="data-explorer"),
    st.Page(reports.render, title="Reports", icon="📄", url_path="reports"),
    st.Page(alerts.render, title="Alerts", icon="🔔", url_path="alerts"),
    st.Page(about.render, title="About", icon="ℹ️", url_path="about"),
]

selected_page = st.navigation(navigation_pages)


# -----------------------------------------------------------------
# 4. RUN THE SELECTED PAGE
# -----------------------------------------------------------------
selected_page.run()
