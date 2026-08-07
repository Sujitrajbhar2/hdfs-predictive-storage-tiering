import joblib
import pandas as pd

print("=" * 70)
print("DataTierAI - Storage Prediction")
print("=" * 70)

# --------------------------------------------------
# Load Saved Files
# --------------------------------------------------

model = joblib.load("models/best_model.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")
target_encoder = joblib.load("models/target_encoder.pkl")

print("\nModel Loaded Successfully")

# --------------------------------------------------
# Sample Enterprise File
# --------------------------------------------------

sample = {
    "Category": "GitHub Repository",
    "Department": "IT",
    "Extension_Type": "Python",
    "Size_KB": 15000,
    "Priority": "High",
    "Stars": 500,
    "Forks": 120,
    "Open_Issues": 12,
    "Visibility": "public",
    "Default_Branch": "main",
    "File_Age_Days": 350,
    "Last_Modified_Days": 5,
    "Size_Category": "Large",
    "Activity_Score": 632,
    "Priority_Business_Score": 30,
    "Source_Business_Score": 5,
    "Department_Business_Score": 4,
    "Age_Score": 6,
    "Size_Score": 8,
    "Activity_Business_Score": 25,
    "Enterprise_Score": 78,
    "Access_Count_30D": 900,
    "Last_Access_Date": "2026-08-01",
    "Unique_Users": 18,
    "Read_Count": 700,
    "Write_Count": 150,
    "Retention_Years": 5,
    "Storage_Cost": 2.10,
    "Backup_Flag": "YES"
}

df = pd.DataFrame([sample])

# --------------------------------------------------
# Encode Categorical Columns
# --------------------------------------------------

for col in df.columns:

    if col in label_encoders:

        encoder = label_encoders[col]

        try:
            df[col] = encoder.transform(df[col])
        except:
            df[col] = 0

# --------------------------------------------------
# Arrange Columns
# --------------------------------------------------
'''
df = df.reindex(columns=feature_columns, fill_value=0)
print(label_encoders.keys())'''

# =====================================================
# Read One Real Record From Dataset
# =====================================================

dataset = pd.read_csv("enterprise_dataset.csv")

print("\nDataset Loaded Successfully")

# Select one record (change index if you want)
record = dataset.iloc[[0]].copy()

# Save Actual Label
actual_label = record["Storage_Label"].values[0]

# Remove Target Column
record = record.drop(columns=["Storage_Label"])

# --------------------------------------------------
# Encode Categorical Columns
# --------------------------------------------------

for col in record.columns:

    if col in label_encoders:

        try:
            record[col] = label_encoders[col].transform(record[col].astype(str))
        except:
            record[col] = 0

# Arrange columns exactly like training
record = record.reindex(columns=feature_columns, fill_value=0)

# --------------------------------------------------
# Prediction
# --------------------------------------------------

prediction = model.predict(record)

predicted_label = target_encoder.inverse_transform(prediction)[0]

print("\n" + "=" * 60)
print("Prediction Result")
print("=" * 60)

print(f"Actual Label      : {actual_label}")
print(f"Predicted Label   : {predicted_label}")

if actual_label == predicted_label:
    print("\nPrediction Status : CORRECT")
else:
    print("\nPrediction Status : INCORRECT")

print("=" * 60)