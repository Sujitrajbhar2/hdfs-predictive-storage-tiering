"""
views/data_explorer.py

A free-form way to browse the raw dataset: filter it, pick which
columns to see, and download the result as a CSV.
"""

import streamlit as st

from utils.data_loader import (
    load_data,
    get_department_list,
    get_storage_tier_list,
    filter_dataframe,
)


def render():
    dataframe = load_data()

    st.markdown('<div class="page-title">Data Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Browse, filter, and export the raw file metadata</div>',
                unsafe_allow_html=True)

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        selected_departments = st.multiselect("Department", options=get_department_list(dataframe))

    with filter_col2:
        selected_tiers = st.multiselect("Storage Tier", options=get_storage_tier_list(dataframe))

    with filter_col3:
        search_text = st.text_input("Search File Name", placeholder="e.g. kibana")

    filtered_dataframe = filter_dataframe(
        dataframe,
        departments=selected_departments,
        tiers=selected_tiers,
        search_text=search_text,
    )

    all_columns = dataframe.columns.tolist()
    default_columns = [
        "Object_Name", "Department", "Storage_Label", "Size_KB",
        "Category", "Last_Modified_Days", "Enterprise_Score",
    ]
    default_columns = [c for c in default_columns if c in all_columns]

    selected_columns = st.multiselect("Columns to show", options=all_columns, default=default_columns)

    st.caption(f"Showing {len(filtered_dataframe):,} of {len(dataframe):,} files")

    display_columns = selected_columns if selected_columns else all_columns
    st.dataframe(filtered_dataframe[display_columns], use_container_width=True, hide_index=True)

    csv_data = filtered_dataframe[display_columns].to_csv(index=False)
    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=csv_data,
        file_name="datatierai_filtered_export.csv",
        mime="text/csv",
    )
