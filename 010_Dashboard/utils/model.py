import joblib
import pandas as pd
import streamlit as st

MODEL_PATH = "models/best_model.pkl"
FEATURE_PATH = "models/feature_columns.pkl"
TARGET_PATH = "models/target_encoder.pkl"


@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURE_PATH)
    target_encoder = joblib.load(TARGET_PATH)

    return model, feature_columns, target_encoder


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

    prediction = model.predict(input_df)

    label = target_encoder.inverse_transform(prediction)[0]

    confidence = 0

    if hasattr(model, "predict_proba"):
        confidence = round(
            model.predict_proba(input_df).max() * 100,
            2
        )

    return label, confidence