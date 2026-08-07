"""
views/analytics.py

The detailed / advanced charts live here instead of the main
Dashboard page, so the Dashboard stays simple and executive-focused.
app.py calls render() when the user picks "Analytics" in the sidebar.

Layout of this file:
    1. Load data
    2. Filter bar (Department, Storage Tier, Category, Date Range, Search)
    3. Apply filters
    4. Draw the 6 detailed charts
"""

import streamlit as st
import plotly.graph_objects as go

from utils.data_loader import (
    load_data,
    get_department_list,
    get_storage_tier_list,
    get_category_list,
    filter_dataframe,
    get_department_risk_score,
    get_storage_usage_by_department_full,
    get_enterprise_score_distribution,
    get_activity_score_distribution,
    get_correlation_matrix,
    get_average_file_age_by_department,
)
from utils.components import chart_card, get_base_plotly_layout


def render():
    dataframe = load_data()

    st.markdown('<div class="page-title">Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Detailed visualizations and filters</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # FILTER BAR
    # -------------------------------------------------------------
    filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)

    with filter_col1:
        selected_departments = st.multiselect("Department", options=get_department_list(dataframe))

    with filter_col2:
        selected_tiers = st.multiselect("Storage Tier", options=get_storage_tier_list(dataframe))

    with filter_col3:
        selected_categories = st.multiselect("Category", options=get_category_list(dataframe))

    with filter_col4:
        date_range = st.date_input("Date Range", value=(), key="date_range_filter")

    with filter_col5:
        search_text = st.text_input("Search File", placeholder="e.g. kibana")

    # date_input returns an empty tuple until the user picks both a start and end date
    start_date, end_date = (date_range[0], date_range[1]) if len(date_range) == 2 else (None, None)

    filtered_dataframe = filter_dataframe(
        dataframe,
        departments=selected_departments,
        tiers=selected_tiers,
        categories=selected_categories,
        start_date=start_date,
        end_date=end_date,
        search_text=search_text,
    )

    st.caption(f"Showing {len(filtered_dataframe):,} of {len(dataframe):,} files")
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # CHART ROW 1: Department Risk Score + Storage Usage by Department
    # -------------------------------------------------------------
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        with chart_card(key="chartcard_department_risk"):
            st.markdown('<div class="chart-card-title">Department Risk Score</div>', unsafe_allow_html=True)
            risk_data = get_department_risk_score(filtered_dataframe)
            figure = go.Figure(data=[go.Bar(
                x=risk_data["Department"], y=risk_data["Risk_Score"], marker=dict(color="#EF4444"),
            )])
            figure.update_layout(**get_base_plotly_layout())
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": False})

    with row1_col2:
        with chart_card(key="chartcard_storage_usage_full"):
            st.markdown('<div class="chart-card-title">Storage Usage by Department</div>', unsafe_allow_html=True)
            usage_data = get_storage_usage_by_department_full(filtered_dataframe)
            figure = go.Figure(data=[go.Bar(
                x=usage_data["Department"], y=usage_data["Storage_GB"], marker=dict(color="#2563EB"),
            )])
            figure.update_layout(**get_base_plotly_layout())
            figure.update_layout(yaxis_title="Storage (GB)")
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": False})

    # -------------------------------------------------------------
    # CHART ROW 2: Enterprise Score Distribution + Activity Score Distribution
    # -------------------------------------------------------------
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        with chart_card(key="chartcard_enterprise_score_dist"):
            st.markdown('<div class="chart-card-title">Enterprise Score Distribution</div>', unsafe_allow_html=True)
            scores = get_enterprise_score_distribution(filtered_dataframe)
            figure = go.Figure(data=[go.Histogram(x=scores, marker=dict(color="#16A34A"))])
            figure.update_layout(**get_base_plotly_layout())
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": False})

    with row2_col2:
        with chart_card(key="chartcard_activity_score_dist"):
            st.markdown('<div class="chart-card-title">Activity Score Distribution</div>', unsafe_allow_html=True)
            scores = get_activity_score_distribution(filtered_dataframe)
            figure = go.Figure(data=[go.Histogram(x=scores, marker=dict(color="#06B6D4"))])
            figure.update_layout(**get_base_plotly_layout())
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": False})

    # -------------------------------------------------------------
    # CHART ROW 3: Correlation Matrix + Average File Age by Department
    # -------------------------------------------------------------
    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        with chart_card(key="chartcard_correlation_matrix"):
            st.markdown('<div class="chart-card-title">Correlation Matrix</div>', unsafe_allow_html=True)
            correlation_matrix = get_correlation_matrix(filtered_dataframe)
            figure = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.columns,
                colorscale="Blues",
                colorbar=dict(
                    tickfont=dict(color="#334155"),
                    title=dict(
                        text="Correlation",
                        font=dict(color="#334155")
                    )
                )
            ))
            figure.update_layout(**get_base_plotly_layout())
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": False})

    with row3_col2:
        with chart_card(key="chartcard_avg_file_age"):
            st.markdown('<div class="chart-card-title">Average File Age by Department</div>', unsafe_allow_html=True)
            age_data = get_average_file_age_by_department(filtered_dataframe)
            figure = go.Figure(data=[go.Bar(
                x=age_data["Department"], y=age_data["Average_Age_Days"], marker=dict(color="#F59E0B"),
            )])
            figure.update_layout(**get_base_plotly_layout())
            figure.update_layout(yaxis_title="Average Age (Days)")
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": False})

    # -------------------------------------------------------------
    # FILTERED DATA TABLE
    # -------------------------------------------------------------
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Filtered File List</div>', unsafe_allow_html=True)
    st.dataframe(filtered_dataframe, use_container_width=True, hide_index=True)
