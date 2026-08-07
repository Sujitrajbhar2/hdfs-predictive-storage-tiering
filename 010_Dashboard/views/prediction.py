import streamlit as st
import pandas as pd

from utils.model import load_model, predict_storage


def render():

    model, feature_columns, target_encoder = load_model()

    st.markdown(
        '<div class="page-title">Storage Tier Prediction</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Enter File Details</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        size_gb = st.number_input(
            "File Size (GB)",
            min_value=0.0,
            value=1.0,
        )

        file_age_days = st.number_input(
            "File Age (Days)",
            min_value=0,
            value=365,
        )

    with col2:

        last_modified_days = st.number_input(
            "Days Since Last Modified",
            min_value=0,
            value=30,
        )

        activity_score = st.number_input(
            "Activity Score",
            min_value=0,
            value=50,
        )

    st.divider()

    if st.button(
        "🔮 Predict Storage Tier",
        use_container_width=True,
    ):

        input_df = pd.DataFrame({

            "Size_KB": [size_gb * 1024 * 1024],

            "File_Age_Days": [file_age_days],

            "Last_Modified_Days": [last_modified_days],

            "Activity_Score": [activity_score]

        })

        prediction, confidence = predict_storage(
            model,
            feature_columns,
            target_encoder,
            input_df,
        )

        st.success(
            f"Predicted Storage Tier : {prediction}"
        )

        st.info(
            f"Confidence : {confidence}%"
        )