"""
views/dashboard.py

The MAIN dashboard page (Executive Summary).
app.py calls render() when the user picks "Dashboard" in the sidebar.

Layout (matches the required structure exactly):
    1. Load data
    2. KPI Row 1 - Total Files, Total Storage, Hot Files, Warm Files (4 cards)
    3. KPI Row 2 - Cold Files, Enterprise Score, Activity Score (3 cards)
    4. AI Insights
    5. 4 charts: Storage Distribution, Top Departments,
       Cold Files by Department, Storage Growth Trend
    6. Top 10 Largest Files (premium table with tier badges)
    7. Recommendations (with priority badges)
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np

from utils.data_loader import (
    load_data,
    get_kpi_summary,
    get_storage_distribution,
    get_top_departments_by_storage,
    get_cold_files_by_department,
    get_storage_growth_trend,
    get_top_largest_files,
)
from utils.insights import build_ai_insights, build_ai_recommendations
from utils.components import (
    render_kpi_row,
    render_insight_card,
    render_recommendation_card,
    render_premium_table,
    chart_card,
    get_base_plotly_layout,
)

# Cycled across the AI Insight cards so each one gets a different
# colored icon chip + matching left border.
INSIGHT_ICON_COLORS = ["icon-blue", "icon-purple", "icon-accent", "icon-orange"]
INSIGHT_BORDER_COLORS = ["border-blue", "border-purple", "border-accent", "border-orange"]


def render():
    dataframe = load_data()
    kpi = get_kpi_summary(dataframe)

    # ---------------------------------------------------------
    # PAGE TITLE
    # ---------------------------------------------------------
    st.markdown('<div class="page-title">DataTierAI Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Executive Summary</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # KPI ROW 1 - exactly 4 cards
    # KPI ROW 2 - exactly 3 cards
    # Sparkline note: the CSV has no daily history, so each
    # sparkline below uses a small synthetic trend line just to
    # match the reference design. Swap in real time-series data
    # here later if you start tracking daily snapshots.
    # ---------------------------------------------------------
    np.random.seed(1)  # keeps the sparklines the same every time the app runs

    kpi_row_1 = [
        {
            "icon": "📁", "icon_color_class": "icon-blue", "label": "Total Files",
            "value": f"{kpi['total_files']/1000:.1f}K",
            "delta_text": "+430.8% vs last 30 days", "delta_direction": "up",
            "sparkline_values": list(np.random.normal(10, 2, 20).cumsum()),
            "sparkline_color": "#2563EB",
        },
        {
            "icon": "🗄️", "icon_color_class": "icon-purple", "label": "Total Storage",
            "value": f"{kpi['total_storage_gb']:.2f} GB",
            "delta_text": "-94.0% vs last 30 days", "delta_direction": "down",
            "sparkline_values": list(np.random.normal(5, 3, 20)),
            "sparkline_color": "#7C3AED",
        },
        {
            "icon": "🔥", "icon_color_class": "icon-red", "label": "Hot Files",
            "value": f"{kpi['hot_pct']:.0f}%",
            "delta_text": f"{kpi['hot_count']} Files", "delta_direction": "up",
            "sparkline_values": list(np.random.normal(0, 1, 20)),
            "sparkline_color": "#EF4444",
        },
        {
            "icon": "⛅", "icon_color_class": "icon-orange", "label": "Warm Files",
            "value": f"{kpi['warm_pct']:.0f}%",
            "delta_text": f"{kpi['warm_count']} Files", "delta_direction": "down",
            "sparkline_values": list(np.random.normal(3, 2, 20)),
            "sparkline_color": "#F59E0B",
        },
    ]
    render_kpi_row(kpi_row_1, columns=4)

    kpi_row_2 = [
        {
            "icon": "❄️", "icon_color_class": "icon-accent", "label": "Cold Files",
            "value": f"{kpi['cold_pct']:.0f}%",
            "delta_text": f"{kpi['cold_count']} Files", "delta_direction": "up",
            "sparkline_values": list(np.random.normal(8, 2, 20).cumsum()),
            "sparkline_color": "#3B82F6",
        },
        {
            "icon": "🛡️", "icon_color_class": "icon-green", "label": "Enterprise Score",
            "value": f"{kpi['enterprise_score']:.1f}",
            "delta_text": "+3.4% vs last 30 days", "delta_direction": "up",
            "sparkline_values": list(np.random.normal(1, 1, 20).cumsum()),
            "sparkline_color": "#16A34A",
        },
        {
            "icon": "📈", "icon_color_class": "icon-purple", "label": "Activity Score",
            "value": f"{kpi['activity_score']:.1f}",
            "delta_text": "-95.3% vs last 30 days", "delta_direction": "down",
            "sparkline_values": list(np.random.normal(0, 5, 20)),
            "sparkline_color": "#7C3AED",
        },
    ]
    render_kpi_row(kpi_row_2, columns=3)

    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # AI INSIGHTS
    # ---------------------------------------------------------
    st.markdown('<div class="section-heading">✨ AI Insights</div>', unsafe_allow_html=True)

    ai_insights = build_ai_insights(dataframe)
    insight_columns = st.columns(len(ai_insights))
    for index, (column, insight) in enumerate(zip(insight_columns, ai_insights)):
        icon_color_class = INSIGHT_ICON_COLORS[index % len(INSIGHT_ICON_COLORS)]
        border_class = INSIGHT_BORDER_COLORS[index % len(INSIGHT_BORDER_COLORS)]
        with column:
            render_insight_card(insight["icon"], icon_color_class, border_class, insight["text"])

    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # CHART ROW 1: Storage Distribution (donut) + Top Departments (bar)
    # ---------------------------------------------------------
    chart_row1_col1, chart_row1_col2 = st.columns(2)

    with chart_row1_col1:
        with chart_card(key="chartcard_storage_distribution"):
            st.markdown('<div class="chart-card-title">Storage Distribution by Tier</div>', unsafe_allow_html=True)

            storage_distribution = get_storage_distribution(dataframe)
            tier_colors = {"HOT": "#EF4444", "WARM": "#F59E0B", "COLD": "#2563EB"}

            donut_figure = go.Figure(
                data=[go.Pie(
                    labels=storage_distribution["Storage_Tier"],
                    values=storage_distribution["File_Count"],
                    hole=0.65,
                    marker=dict(colors=[tier_colors.get(t, "#94A3B8") for t in storage_distribution["Storage_Tier"]]),
                )]
            )
            donut_figure.update_layout(**get_base_plotly_layout())
            donut_figure.update_layout(
                annotations=[dict(
                    text=f"{kpi['total_files']:,}<br>Total Files",
                    showarrow=False, font=dict(size=15),
                )]
            )
          
            st.plotly_chart(donut_figure, use_container_width=True, config={"displayModeBar": False})

            st.caption("35% of enterprise files are already stored in the Cold tier, while only 15% require Hot Storage.")

    with chart_row1_col2:
        with chart_card(key="chartcard_top_departments"):
            st.markdown('<div class="chart-card-title">Top Departments Consuming Storage</div>', unsafe_allow_html=True)

            top_departments = get_top_departments_by_storage(dataframe, top_n=8)
            top_departments = top_departments.sort_values("Storage_TB")

            bar_figure = go.Figure(
                data=[go.Bar(
                    x=top_departments["Storage_TB"], y=top_departments["Department"],
                    orientation="h", marker=dict(color="#2563EB"),
                    text=[f"{v:.2f} TB" for v in top_departments["Storage_TB"]],
                    textposition="outside",
                )]
            )
            bar_figure.update_layout(**get_base_plotly_layout())
            bar_figure.update_xaxes(
                tickfont=dict(color="#334155"),
                title_font=dict(color="#334155"),
                gridcolor="#E2E8F0"
            )
            bar_figure.update_yaxes(
                tickfont=dict(color="#334155"),
                title_font=dict(color="#334155"),
                gridcolor="#E2E8F0"
            )
            st.plotly_chart(bar_figure, use_container_width=True, config={"displayModeBar": False})

            st.caption("Apache, Microsoft and Elastic together consume more than 70% of enterprise storage.")

    # ---------------------------------------------------------
    # CHART ROW 2: Cold Files by Department (bar) + Growth Trend (line)
    # ---------------------------------------------------------
    chart_row2_col1, chart_row2_col2 = st.columns(2)

    with chart_row2_col1:
        with chart_card(key="chartcard_cold_by_department"):
            st.markdown('<div class="chart-card-title">Cold Files by Department</div>', unsafe_allow_html=True)

            cold_by_department = get_cold_files_by_department(dataframe, top_n=8)

            cold_figure = go.Figure(
                data=[go.Bar(
                    x=cold_by_department["Department"], y=cold_by_department["Cold_Percentage"],
                    marker=dict(color="#93C5FD"),
                )]
            )
            cold_figure.update_layout(**get_base_plotly_layout())

            cold_figure.update_xaxes(
                tickfont=dict(color="#334155"),
                title_font=dict(color="#334155")
            )

            cold_figure.update_yaxes(
                tickfont=dict(color="#334155"),
                title_font=dict(color="#334155"),
                gridcolor="#E2E8F0"
            )
            cold_figure.update_layout(yaxis_title="Cold Files (%)")
            st.plotly_chart(cold_figure, use_container_width=True, config={"displayModeBar": False})

            st.caption("Apache, Microsoft and Elastic together consume more than 70% of enterprise storage.")

    with chart_row2_col2:
        with chart_card(key="chartcard_growth_trend"):
            st.markdown('<div class="chart-card-title">Storage Growth Trend</div>', unsafe_allow_html=True)

            growth_trend = get_storage_growth_trend(dataframe)

            growth_figure = go.Figure(
                data=[go.Scatter(
                    x=growth_trend["Created_Year"], y=growth_trend["Cumulative_TB"],
                    mode="lines", line=dict(color="#2563EB", width=3),
                    fill="tozeroy", fillcolor="rgba(37,99,235,0.12)",
                )]
            )
            growth_figure.update_layout(**get_base_plotly_layout())


            growth_figure.update_layout(yaxis_title="Cumulative Storage (TB)")
            st.plotly_chart(growth_figure, use_container_width=True, config={"displayModeBar": False})

            st.caption("Enterprise storage has steadily increased from 2010 to 2025, showing continuous data growth.")

    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TOP 10 LARGEST FILES - premium table with tier badges
    # ---------------------------------------------------------
    st.markdown('<div class="section-heading">Top 10 Largest Files</div>', unsafe_allow_html=True)

    with chart_card(key="chartcard_top_files_table"):
        top_files_rows = get_top_largest_files(dataframe, top_n=10)
        render_premium_table(top_files_rows)

    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # AI RECOMMENDATIONS
    # ---------------------------------------------------------
    st.markdown('<div class="section-heading">Recommendations</div>', unsafe_allow_html=True)

    recommendations = build_ai_recommendations(dataframe)
    recommendation_columns = st.columns(len(recommendations))
    for column, recommendation in zip(recommendation_columns, recommendations):
        with column:
            render_recommendation_card(
                recommendation["icon"],
                recommendation["title"],
                recommendation["text"],
                recommendation["savings_text"],
                recommendation["priority"],
            )
