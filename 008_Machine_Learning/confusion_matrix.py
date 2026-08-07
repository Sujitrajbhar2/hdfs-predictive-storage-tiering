import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

print("=" * 70)
print("DataTierAI - Confusion Matrix")
print("=" * 70)

# =====================================================
# Load Dataset
# =====================================================

df = pd.read_csv("enterprise_dataset.csv",low_memory=False)

print("\nDataset Loaded Successfully")

# =====================================================
# Remove Unnecessary Columns
# =====================================================

drop_columns = [
    "Object_Name",
    "Owner",
    "Location",
    "Created_Date",
    "Modified_Date"
]

df.drop(columns=drop_columns, inplace=True, errors="ignore")

# =====================================================
# Missing Values
# =====================================================

for col in df.columns:

    if df[col].dtype in ["int64", "float64"]:

        df[col] = df[col].fillna(df[col].median())

    else:

        df[col] = df[col].fillna("Unknown")

# =====================================================
# Features & Target
# =====================================================

X = df.drop(columns=["Storage_Label"])
y = df["Storage_Label"]

# =====================================================
# Load Encoders
# =====================================================

label_encoders = joblib.load("models/label_encoders.pkl")
target_encoder = joblib.load("models/target_encoder.pkl")

for col in X.columns:

    if col in label_encoders:

        encoder = label_encoders[col]

        # Replace missing values with the first class seen during training
        X[col] = X[col].fillna(encoder.classes_[0]).astype(str)

        # Replace any unseen values with the first known class
        X[col] = X[col].apply(
            lambda x: x if x in encoder.classes_ else encoder.classes_[0]
        )

        X[col] = encoder.transform(X[col])

y = target_encoder.transform(y)

# =====================================================
# Load Training Feature Columns
# =====================================================

feature_columns = joblib.load("models/feature_columns.pkl")

# Keep exactly the same columns as training
X = X.reindex(columns=feature_columns, fill_value=0)

# =====================================================
# Train/Test Split
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# =====================================================
# Load Model
# =====================================================

model = joblib.load("models/best_model.pkl")

# =====================================================
# Prediction
# =====================================================

y_pred = model.predict(X_test)

# =====================================================
# Classification Report
# =====================================================

report = classification_report(
    y_test,
    y_pred,
    target_names=target_encoder.classes_
)

print("\nClassification Report\n")
print(report)

# =====================================================
# Save Report
# =====================================================

os.makedirs("output", exist_ok=True)

with open("output/classification_report.txt", "w") as f:
    f.write(report)

# =====================================================
# Confusion Matrix
# =====================================================

cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=target_encoder.classes_
)

plt.figure(figsize=(7,6))
disp.plot(cmap="Blues")

plt.title("Storage Tier Confusion Matrix")

plt.savefig(
    "output/confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nConfusion Matrix Saved Successfully")
print("Report : output/classification_report.txt")
print("Image  : output/confusion_matrix.png")