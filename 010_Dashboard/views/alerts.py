"""
views/alerts.py

Simple rule-based alerts: departments whose risk score or cold-file
percentage crosses a threshold get flagged. See
utils/data_loader.py -> get_department_alerts() for the actual rules.
"""

import streamlit as st

from utils.data_loader import load_data, get_department_alerts
from utils.components import render_alert_card


def render():
    dataframe = load_data()

    st.markdown('<div class="page-title">Alerts</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Departments that need attention</div>', unsafe_allow_html=True)

    alerts = get_department_alerts(dataframe)

    if not alerts:
        st.info("No alerts right now - every department is within the normal range.")
        return

    high_priority = [a for a in alerts if a["severity"] == "High"]
    medium_priority = [a for a in alerts if a["severity"] == "Medium"]

    if high_priority:
        st.markdown('<div class="section-heading">🔴 High Priority</div>', unsafe_allow_html=True)
        for alert in high_priority:
            render_alert_card(alert["severity"], alert["department"], alert["message"])

    if medium_priority:
        st.markdown('<div class="section-heading">🟠 Medium Priority</div>', unsafe_allow_html=True)
        for alert in medium_priority:
            render_alert_card(alert["severity"], alert["department"], alert["message"])
