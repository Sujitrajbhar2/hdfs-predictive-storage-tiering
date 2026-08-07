# DataTierAI Dashboard

A Streamlit dashboard for data lifecycle analytics, styled as a
compact enterprise dashboard (Power BI / Microsoft Fabric style).

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

`app.py` is the only entry point. It builds the sidebar menu (Dashboard,
Analytics, Prediction, Storage Optimizer, Data Explorer, Reports, Alerts,
About) and runs whichever page is selected. Best viewed on a normal desktop
monitor (designed around a 1920x1080 screen at 100% browser zoom).

## Folder structure

```
datatierai_dashboard/
├── app.py                    <- Entry point: page config, CSS, sidebar menu
├── views/                    <- One file per page, each with a render() function
│   ├── dashboard.py           <- Executive Summary: KPI rows, AI Insights, 4 charts,
│   │                              Top 10 Largest Files table, Recommendations
│   ├── analytics.py           <- Detailed charts (Department Risk Score, Storage Usage
│   │                              by Department, Enterprise/Activity Score Distribution,
│   │                              Correlation Matrix, Average File Age) + filters
│   ├── prediction.py          <- Storage tier prediction form
│   ├── storage_optimizer.py   <- File-level cleanup candidates
│   ├── data_explorer.py       <- Filter/browse/export the raw dataset
│   ├── reports.py             <- Department summary + CSV export
│   ├── alerts.py              <- Rule-based department alerts
│   └── about.py               <- About this project
├── utils/
│   ├── data_loader.py         <- All data calculations (edit column names here)
│   ├── style_loader.py        <- Loads every CSS file into the app
│   ├── components.py          <- Reusable card / table / chart-card renderers
│   ├── insights.py            <- Builds the AI Insights + Recommendations text
│   └── model.py                <- The Prediction page's ML model
├── assets/css/
│   ├── theme.css               <- ALL COLORS live here - change theme here first
│   ├── background.css          <- Page background
│   ├── layout.css              <- Page width, titles, spacing
│   ├── sidebar.css             <- Sidebar (locked ~220px) + 8-item menu, hover/active states
│   ├── cards.css               <- KPI rows, insight/recommendation cards, premium table,
│   │                              alert cards, predict button
│   ├── dashboard.css           <- Equal-height card alignment across chart/insight rows
│   ├── charts.css              <- Small Plotly chart container tweaks
│   ├── tables.css              <- st.dataframe styling (used on other pages)
│   ├── animations.css          <- Hover / fade animation timing
│   └── responsive.css          <- Collapses the KPI grid gracefully on narrow screens
└── data/
    └── feature_engineered_metadata.csv
```

## KPI layout (fixed, not auto-wrapping)

The Dashboard's KPI cards are deliberately laid out as two SEPARATE grids,
not one auto-wrapping grid, so the count per row never changes:

- **Row 1** - exactly 4 cards: Total Files, Total Storage, Hot Files, Warm Files
  (CSS class `.kpi-row-4`)
- **Row 2** - exactly 3 cards: Cold Files, Enterprise Score, Activity Score
  (CSS class `.kpi-row-3`)

Both are built by the same Python function - `render_kpi_row(cards, columns)`
in `utils/components.py` - just called twice with a different card list and
column count. `views/reports.py` reuses the same function for its 3-card row.

## How to make common changes

- **Change a color** -> open `assets/css/theme.css`, change the hex code, save. Every
  card/chart/button using that variable updates automatically.
- **Change the sidebar width / gap / page width** -> `assets/css/sidebar.css`
  (`[data-testid="stSidebar"]`) and `assets/css/layout.css` (`.block-container`).
- **Add/remove a sidebar menu item** -> open `app.py`, add or remove one
  `st.Page(...)` line in `navigation_pages`, and create/delete the matching
  file in `views/`.
- **Change what a KPI card shows** -> open `views/dashboard.py`, edit the
  matching dictionary inside `kpi_row_1` or `kpi_row_2`.
- **Change KPI card size** -> `assets/css/cards.css`, `.kpi-card` (size) and
  `.kpi-row-2/3/4` (`grid-template-columns`, currently fixed at 230px each).
- **Fix/adjust the sparkline inside a KPI card** -> `utils/components.py` ->
  `build_sparkline_svg()`. It's plain inline SVG built INSIDE the card's own
  HTML, so it can never overflow the card.
- **Change the Top 10 Largest Files table** (columns, badges) -> the row data
  comes from `utils/data_loader.py` -> `get_top_largest_files()`, and the HTML
  table itself is built by `utils/components.py` -> `render_premium_table()`.
- **Change a Recommendation card** (title, savings, priority) -> `utils/insights.py`
  -> `build_ai_recommendations()`.
- **Add/remove a chart on the Dashboard** -> `views/dashboard.py`, copy an
  existing `with chart_card(key="chartcard_...")` block and edit it, or delete one.
- **Add a filter on the Analytics page** -> `views/analytics.py`.
- **Change what the Predict button predicts on** -> `utils/model.py`
  (the `FEATURE_COLUMNS` list) and `views/prediction.py` (the input fields).

## A note on the HTML cards

Every card (KPI, insight, recommendation, alert, table) is built as a plain
HTML string and rendered with `st.markdown(..., unsafe_allow_html=True)`.
Streamlit/Markdown treats an INDENTED line as a code block (shown as literal
text) instead of HTML - so every HTML string in `utils/components.py` is run
through a small `_clean_html()` helper that flattens it to a single line with
zero line breaks before it's rendered. If you ever add a new card function,
copy that pattern (build the multi-line f-string, then call `_clean_html()`
on it) so this bug can't come back.

Every Python file is still written step-by-step with comments so you can find
and change things easily - only the final HTML output gets flattened to one line.
