import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("DataTierAI - Enterprise Feature Engineering")
print("=" * 70)

# =====================================================
# Read Clean Enterprise Dataset
# =====================================================

INPUT_FILE = Path("/opt/DataTierAI/003_Preprocessing/output/clean_enterprise_metadata.csv")



df = pd.read_csv(INPUT_FILE)

print(f"Records Loaded : {len(df)}")
print(f"Columns Loaded : {len(df.columns)}")

print("\nDataset Columns\n")
print(df.columns.tolist())

# =====================================================
# Convert Date Columns
# =====================================================

date_columns = [
    "Created_Date",
    "Modified_Date"
]

for column in date_columns:

    if column in df.columns:

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce",
            utc=True
        ).dt.tz_localize(None)

today = datetime.now()

print("\nDate Conversion Completed")

# =====================================================
# Feature 1 : File Age (Days)
# =====================================================

df["File_Age_Days"] = (
    today - df["Created_Date"]
).dt.days

df["File_Age_Days"] = df["File_Age_Days"].fillna(0)

# =====================================================
# Feature 2 : Last Modified Days
# =====================================================

df["Last_Modified_Days"] = (
    today - df["Modified_Date"]
).dt.days

df["Last_Modified_Days"] = df["Last_Modified_Days"].fillna(0)

# =====================================================
# Feature 3 : Size Category
# =====================================================

def size_category(size):

    if size < 100:
        return "Small"

    elif size < 10000:
        return "Medium"

    else:
        return "Large"


df["Size_Category"] = df["Size_KB"].apply(size_category)

# =====================================================
# Feature 4 : Repository Activity
# =====================================================

if "Stars" in df.columns:

    df["Activity_Score"] = (
        df["Stars"] +
        df["Forks"] +
        df["Open_Issues"]
    )

else:

    df["Activity_Score"] = 0


# =====================================================
# Storage Tier Rule Engine
# =====================================================

PRIORITY_SCORE = {
    "High": 30,
    "Medium": 20,
    "Low": 10,
    "N/A": 5
}

SOURCE_SCORE = {
    "Database": 10,
    "GitHub": 8,
    "Windows": 6,
    "Linux": 6
}

DEPARTMENT_SCORE = {
    "Finance": 5,
    "IT": 5,
    "HR": 4,
    "Marketing": 3
}

# =====================================================
# Business Scores
# =====================================================

df["Priority_Business_Score"] = df["Priority"].map(PRIORITY_SCORE).fillna(5)

df["Source_Business_Score"] = df["Source"].map(SOURCE_SCORE).fillna(4)

df["Department_Business_Score"] = df["Department"].map(DEPARTMENT_SCORE).fillna(2)

# =====================================================
# Age Score
# =====================================================

def age_score(age):

    if age <= 30:
        return 20
    elif age <= 180:
        return 15
    elif age <= 365:
        return 10
    else:
        return 5


df["Age_Score"] = df["File_Age_Days"].apply(age_score)

# =====================================================
# Size Score
# =====================================================

def size_score(size):

    if size >= 100000:
        return 10
    elif size >= 10000:
        return 8
    elif size >= 1000:
        return 6
    else:
        return 4


df["Size_Score"] = df["Size_KB"].apply(size_score)

# =====================================================
# Activity Business Score
# =====================================================

def activity_score(score):

    if score >= 10000:
        return 25
    elif score >= 5000:
        return 20
    elif score >= 1000:
        return 15
    elif score >= 100:
        return 10
    else:
        return 5


df["Activity_Business_Score"] = df["Activity_Score"].apply(activity_score)

# =====================================================
# Enterprise Score
# =====================================================

df["Enterprise_Score"] = (

    df["Priority_Business_Score"]

    + df["Source_Business_Score"]

    + df["Department_Business_Score"]

    + df["Age_Score"]

    + df["Size_Score"]

    + df["Activity_Business_Score"]

)

# =====================================================
# Storage Tier Decision
# =====================================================

def assign_storage(score):

    if score >= 75:
        return "HOT"

    elif score >= 60:
        return "WARM"

    elif score >= 40:
        return "COLD"

    else:
        return "ARCHIVE"


df["Storage_Label"] = df["Enterprise_Score"].apply(assign_storage)

print("\nEnterprise Score Statistics\n")
print(df["Enterprise_Score"].describe())

print("\nStorage Tier Distribution\n")
print(df["Storage_Label"].value_counts())

print("\nStorage Tier Percentage\n")
print(round(df["Storage_Label"].value_counts(normalize=True) * 100, 2))


# =====================================================
# Save Feature Engineered Dataset
# =====================================================

OUTPUT_FOLDER = Path("/opt/DataTierAI/004_Feature_Engineering/output")
OUTPUT_FOLDER.mkdir(parents=True,exist_ok=True)

OUTPUT_FILE = OUTPUT_FOLDER / "feature_engineered_metadata.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("Feature Engineering Completed Successfully")
print("=" * 70)

print(f"Records : {len(df)}")
print(f"Columns : {len(df.columns)}")

print("\nStorage Label Distribution\n")

print(df["Storage_Label"].value_counts())

print(f"\nOutput File : {OUTPUT_FILE}")

print("=" * 70)