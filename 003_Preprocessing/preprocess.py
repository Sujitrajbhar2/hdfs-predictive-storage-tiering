import pandas as pd
from pathlib import Path

print("=" * 70)
print("DataTierAI - Enterprise Data Preprocessing")
print("=" * 70)

# =====================================================
# Read Enterprise Dataset
# =====================================================

INPUT_FILE = Path("/opt/DataTierAI/002_ETL/output/enterprise_metadata.csv")

df = pd.read_csv(INPUT_FILE)

print(f"Records Loaded : {len(df)}")
print(f"Columns Loaded : {len(df.columns)}")

# =====================================================
# Remove Duplicate Records
# =====================================================

before = len(df)

df.drop_duplicates(inplace=True)

after = len(df)

print(f"Duplicate Records Removed : {before-after}")

# =====================================================
# Fill Missing Values
# =====================================================

text_columns = df.select_dtypes(include=["object", "string"]).columns
df[text_columns] = df[text_columns].fillna("N/A")

numeric_columns = df.select_dtypes(include="number").columns
df[numeric_columns] = df[numeric_columns].fillna(0)

# =====================================================
# Remove Extra Spaces
# =====================================================

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()

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
        )

        # Remove timezone information
        df[column] = df[column].dt.tz_localize(None)


# =====================================================
# Save Clean Dataset
# =====================================================

OUTPUT_FOLDER = Path("/opt/DataTierAI/003_Preprocessing/output")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_FOLDER / "clean_enterprise_metadata.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nPreprocessing Completed Successfully")

print(f"Total Records : {len(df)}")

print(f"Output File : {OUTPUT_FILE}")

print("=" * 70)