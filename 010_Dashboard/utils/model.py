import joblib
import pandas as pd
import streamlit as st
from pathlib import Path


# ============================================================
# MODEL PATHS
# ============================================================

# Current file:
# DataTierAI/
# └── 010_Dashboard/
#     └── utils/
#         └── model.py
#
# parent.parent.parent = DataTierAI project root

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = PROJECT_ROOT / "008_Machine_Learning" / "models" / "best_model.pkl"
FEATURE_PATH = PROJECT_ROOT / "008_Machine_Learning" / "models" / "feature_columns.pkl"
TARGET_PATH = PROJECT_ROOT / "008_Machine_Learning" / "models" / "target_encoder.pkl"


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    model = joblib.load(MODEL_PATH)

    feature_columns = joblib.load(FEATURE_PATH)

    target_encoder = joblib.load(TARGET_PATH)

    return model, feature_columns, target_encoder


# ============================================================
# PREDICT STORAGE TIER
# ============================================================

def predict_storage(
    model,
    feature_columns,
    target_encoder,
    input_df
):

    # Convert categorical columns
    input_df = pd.get_dummies(input_df)

    # Match training columns
    input_df = input_df.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # Make prediction
    prediction = model.predict(input_df)

    # Convert encoded prediction back to label
    label = target_encoder.inverse_transform(prediction)[0]

    # Default confidence
    confidence = 0

    # Calculate prediction probability if model supports it
    if hasattr(model, "predict_proba"):

        confidence = round(
            model.predict_proba(input_df).max() * 100,
            2
        )

    return label, confidence