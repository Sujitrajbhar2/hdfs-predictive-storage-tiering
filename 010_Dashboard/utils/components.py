"""
components.py

Small, reusable "building blocks" for the dashboard UI.
Every function here renders ONE piece of HTML using
st.markdown(unsafe_allow_html=True). The styling for every
class name used below (kpi-card, insight-card, etc.) lives
in assets/css/cards.css - change the look there, not here.

IMPORTANT: every HTML string built here is passed through
_clean_html(), which flattens it to a single line with no
line breaks at all. Markdown treats indented lines as a CODE
block (shown as literal text) instead of an HTML block - and
that can happen on ANY line inside a multi-line HTML string,
not just the first one. Flattening to one line removes every
line break, so this bug can't happen no matter how many nested
tags a card has.
"""

import streamlit as st
from contextlib import contextmanager


def _clean_html(html_text):
    """
    Flatten a multi-line HTML string into ONE single line with zero
    line breaks anywhere in it, so Markdown can never mistake any
    part of it for an indented code block.
    """
    lines = [line.strip() for line in html_text.strip().splitlines()]
    return " ".join(line for line in lines if line)


# ===================================================================
# 1. KPI CARDS
# ===================================================================

def build_sparkline_svg(values, color):
    """
    Build a small inline SVG sparkline (a line + soft fill under it).

    Because this returns a plain string that gets embedded INSIDE the
    kpi-card's own HTML, the sparkline is physically part of the card -
    it can never render outside the card's borders the way a separate
    Streamlit chart element could.

    A small amount of padding is left on all four sides INSIDE the
    SVG's own coordinate space (not just the card's CSS padding), so
    the line and its fill never touch even the sparkline's own edges.

    values -> a plain list of numbers, oldest first
    color  -> a hex color string, e.g. "#2563EB"
    """
    if not values or len(values) < 2:
        return ""

    width = 100
    height = 28
    padding_y = 4
    padding_x = 4

    min_value = min(values)
    max_value = max(values)
    value_range = max_value - min_value if max_value != min_value else 1

    usable_width = width - (2 * padding_x)
    step_x = usable_width / (len(values) - 1)

    line_points = []
    for index, value in enumerate(values):
        x = padding_x + (index * step_x)
        y = height - padding_y - ((value - min_value) / value_range) * (height - (2 * padding_y))
        line_points.append(f"{x:.1f},{y:.1f}")

    line_points_text = " ".join(line_points)

    # Same points, but closed at the bottom corners, used to draw the soft fill.
    fill_bottom = height - padding_y
    fill_points_text = f"{padding_x},{fill_bottom} " + line_points_text + f" {width - padding_x},{fill_bottom}"

    svg_markup = f"""
    <svg class="kpi-sparkline" viewBox="0 0 {width} {height}" preserveAspectRatio="none">
        <polyline points="{fill_points_text}" fill="{color}" fill-opacity="0.15" stroke="none"></polyline>
        <polyline points="{line_points_text}" fill="none" stroke="{color}" stroke-width="2"
                   stroke-linecap="round" stroke-linejoin="round"></polyline>
    </svg>
    """
    return _clean_html(svg_markup)


def build_kpi_card_html(icon, icon_color_class, label, value, delta_text, delta_direction,
                         sparkline_values=None, sparkline_color="#2563EB"):
    """Build (but do not render) the HTML for one compact KPI card."""
    sparkline_svg = ""
    if sparkline_values is not None:
        sparkline_svg = build_sparkline_svg(sparkline_values, sparkline_color)

    card_html = f"""
    <div class="kpi-card">
        <div class="kpi-card-top">
            <div class="kpi-top-row">
                <div class="kpi-icon-box {icon_color_class}">{icon}</div>
                <div class="kpi-label">{label}</div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta {delta_direction}">{delta_text}</div>
        </div>
        <div class="kpi-sparkline-wrap">{sparkline_svg}</div>
    </div>
    """
    return _clean_html(card_html)


def render_kpi_row(cards, columns):
    """
    Render one row of KPI cards as a fixed-column-count CSS Grid, so
    the row always shows EXACTLY `columns` cards per row - never more,
    never fewer, regardless of screen width (see assets/css/cards.css
    -> .kpi-row-2 / .kpi-row-3 / .kpi-row-4).

    cards   -> a list of dicts, each with the same keys as
               build_kpi_card_html's arguments, e.g.:
               [{"icon": "📁", "icon_color_class": "icon-blue",
                 "label": "Total Files", "value": "11.3K",
                 "delta_text": "+430.8%", "delta_direction": "up",
                 "sparkline_values": [...], "sparkline_color": "#2563EB"}, ...]
    columns -> 2, 3, or 4 - picks which .kpi-row-N CSS class to use.
    """
    all_cards_html = ""
    for card in cards:
        all_cards_html += build_kpi_card_html(
            icon=card["icon"],
            icon_color_class=card["icon_color_class"],
            label=card["label"],
            value=card["value"],
            delta_text=card["delta_text"],
            delta_direction=card["delta_direction"],
            sparkline_values=card.get("sparkline_values"),
            sparkline_color=card.get("sparkline_color", "#2563EB"),
        )

    row_html = f'<div class="kpi-row-{columns}">{all_cards_html}</div>'
    st.markdown(row_html, unsafe_allow_html=True)


# ===================================================================
# 2. AI INSIGHT CARDS
# ===================================================================

def render_insight_card(icon, icon_color_class, border_class, html_text):
    """
    Render one AI Insight card - a premium "notification card" with a
    colored icon chip and a matching colored left border.

    icon_color_class -> one of the icon-* classes (icon-blue, icon-purple, ...)
    border_class      -> one of the insight-card border-* classes
                         (border-blue, border-accent, border-purple, border-orange)
    html_text can include <b> tags for bold words.
    """
    card_html = f"""
    <div class="insight-card {border_class}">
        <div class="insight-icon-box {icon_color_class}">{icon}</div>
        <div class="insight-text">{html_text}</div>
    </div>
    """
    st.markdown(_clean_html(card_html), unsafe_allow_html=True)


# ===================================================================
# 3. RECOMMENDATION CARDS
# ===================================================================

def render_recommendation_card(icon, title, text, savings_text, priority):
    """
    Render one AI Recommendation card: icon, title, description,
    a savings line, and a priority badge (High / Medium / Low).
    """
    priority_class = f"priority-{priority.lower()}"
    card_html = f"""
    <div class="recommendation-card">
        <div class="recommendation-top-row">
            <div class="recommendation-icon">{icon}</div>
            <div class="priority-badge {priority_class}">{priority}</div>
        </div>
        <div class="recommendation-title">{title}</div>
        <div class="recommendation-text">{text}</div>
        <div class="recommendation-savings">{savings_text}</div>
    </div>
    """
    st.markdown(_clean_html(card_html), unsafe_allow_html=True)


# ===================================================================
# 4. PREMIUM TABLE (Top 10 Largest Files)
# ===================================================================

def _build_tier_badge(storage_tier):
    """Return a small colored pill for HOT / WARM / COLD."""
    tier_class_map = {"HOT": "tier-hot", "WARM": "tier-warm", "COLD": "tier-cold","ARCHIVE": "tier-archive"}


    tier_class = tier_class_map.get(storage_tier, "tier-archive")
    return f'<span class="tier-badge {tier_class}">{storage_tier}</span>'


def render_premium_table(rows):
    """
    Render the Top 10 Largest Files table as plain HTML (not
    st.dataframe), so the Storage Tier column can show a colored
    badge instead of plain text.

    rows -> a list of dicts, each with keys:
            "file_name", "department", "size_text", "storage_tier",
            "last_access", "recommendation"
    """
    header_html = (
        "<thead><tr>"
        "<th>File Name</th><th>Department</th><th>Size</th>"
        "<th>Storage Tier</th><th>Last Access</th><th>Recommendation</th>"
        "</tr></thead>"
    )

    body_rows_html = ""
    for row in rows:
        tier_badge = _build_tier_badge(row["storage_tier"])
        body_rows_html += (
            "<tr>"
            f'<td>{row["file_name"]}</td>'
            f'<td>{row["department"]}</td>'
            f'<td>{row["size_text"]}</td>'
            f'<td>{tier_badge}</td>'
            f'<td>{row["last_access"]}</td>'
            f'<td>{row["recommendation"]}</td>'
            "</tr>"
        )

    table_html = (
        '<div class="premium-table-wrap"><table class="premium-table">'
        f"{header_html}<tbody>{body_rows_html}</tbody>"
        "</table></div>"
    )
    st.markdown(_clean_html(table_html), unsafe_allow_html=True)


# ===================================================================
# 5. ALERT CARDS (Alerts page)
# ===================================================================

def render_alert_card(severity, department, message):
    """
    Render one alert row on the Alerts page.
    severity -> "High" or "Medium", controls the left border / badge color.
    """
    severity_class = "alert-high" if severity == "High" else "alert-medium"
    card_html = f"""
    <div class="alert-card {severity_class}">
        <div class="alert-badge {severity_class}">{severity}</div>
        <div class="alert-department">{department}</div>
        <div class="alert-message">{message}</div>
    </div>
    """
    st.markdown(_clean_html(card_html), unsafe_allow_html=True)


# ===================================================================
# 6. CHART CONTAINER CARD + SHARED PLOTLY LAYOUT
# ===================================================================

@contextmanager
def chart_card(key):
    """
    Use this to wrap any Plotly chart so it appears inside a white
    card with a border and shadow, matching the rest of the dashboard.

    Example:
        with chart_card(key="chartcard_storage_dist"):
            st.markdown('<div class="chart-card-title">Storage Distribution</div>', unsafe_allow_html=True)
            st.plotly_chart(my_figure, use_container_width=True)

    IMPORTANT: the key you pass in must start with "chartcard_" -
    that prefix is what the CSS rule in cards.css looks for.
    """
    container = st.container(key=key)
    with container:
        yield container

def get_base_plotly_layout():
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",

        "font": {
            "family": "Arial",
            "color": "#334155",
            "size": 13,
        },

        "margin": {
            "l": 45,
            "r": 25,
            "t": 45,
            "b": 45,
        },

        "xaxis": {
            "color": "#334155",
            "tickfont": {
                "color": "#334155",
                "size": 12,
            },
            "title_font": {
                "color": "#334155",
                "size": 13,
            },
            "gridcolor": "#E2E8F0",
            "zerolinecolor": "#CBD5E1",
        },

        "yaxis": {
            "color": "#334155",
            "tickfont": {
                "color": "#334155",
                "size": 12,
            },
            "title_font": {
                "color": "#334155",
                "size": 13,
            },
            "gridcolor": "#E2E8F0",
            "zerolinecolor": "#CBD5E1",
        },

        "hoverlabel": {
            "font": {
                "color": "#172033",
                "size": 13,
            }
        },
    }