"""
views/storage_optimizer.py

Shows the concrete list of files behind each AI Recommendation on the
Dashboard - the files that could be archived, compressed, or deleted -
so a user can see exactly what the recommendation is based on.
"""

import streamlit as st

from utils.data_loader import (
    load_data,
    get_files_for_archive,
    get_large_files_for_compression,
    get_temp_files_for_deletion,
)
from utils.components import chart_card


def render():
    dataframe = load_data()

    st.markdown('<div class="page-title">Storage Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Files identified as candidates for cleanup</div>',
                unsafe_allow_html=True)

    with chart_card(key="chartcard_archive_candidates"):
        st.markdown('<div class="chart-card-title">📦 Files Ready to Archive (old + inactive)</div>',
                    unsafe_allow_html=True)
        archive_table = get_files_for_archive(dataframe)
        st.dataframe(archive_table, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

    with chart_card(key="chartcard_compress_candidates"):
        st.markdown('<div class="chart-card-title">📄 Large Files to Compress</div>', unsafe_allow_html=True)
        compress_table = get_large_files_for_compression(dataframe)
        st.dataframe(compress_table, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

    with chart_card(key="chartcard_delete_candidates"):
        st.markdown('<div class="chart-card-title">🗑️ Temporary Files to Delete</div>', unsafe_allow_html=True)
        temp_table = get_temp_files_for_deletion(dataframe)
        st.dataframe(temp_table, use_container_width=True, hide_index=True)
