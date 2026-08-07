"""
views/reports.py

A one-page executive report: per-department summary table plus a
CSV download, so results can be shared outside the dashboard.
"""

import streamlit as st

from utils.data_loader import load_data, get_kpi_summary, get_department_summary_table
from utils.components import render_kpi_row, chart_card


def render():
    dataframe = load_data()
    kpi = get_kpi_summary(dataframe)

    st.markdown('<div class="page-title">Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Department-level summary, ready to export</div>',
                unsafe_allow_html=True)

    summary_cards = [
        {
            "icon": "📁", "icon_color_class": "icon-blue", "label": "Total Files",
            "value": f"{kpi['total_files']:,}", "delta_text": "Across all departments", "delta_direction": "up",
        },
        {
            "icon": "🗄️", "icon_color_class": "icon-purple", "label": "Total Storage",
            "value": f"{kpi['total_storage_gb']:.2f} GB", "delta_text": "Across all departments", "delta_direction": "up",
        },
        {
            "icon": "🛡️", "icon_color_class": "icon-green", "label": "Avg Enterprise Score",
            "value": f"{kpi['enterprise_score']:.1f}", "delta_text": "Across all departments", "delta_direction": "up",
        },
    ]
    render_kpi_row(summary_cards, columns=3)

    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

    with chart_card(key="chartcard_department_summary"):
        st.markdown('<div class="chart-card-title">Department Summary</div>', unsafe_allow_html=True)
        summary_table = get_department_summary_table(dataframe)
        st.dataframe(summary_table, use_container_width=True, hide_index=True)

    csv_data = get_department_summary_table(dataframe).to_csv(index=False)
    st.download_button(
        label="⬇️ Download department report as CSV",
        data=csv_data,
        file_name="datatierai_department_report.csv",
        mime="text/csv",
    )
