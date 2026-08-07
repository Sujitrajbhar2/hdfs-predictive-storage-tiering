import pandas as pd
from pathlib import Path

print("=" * 70)
print("DataTierAI - Enterprise ETL Merge Engine")
print("=" * 70)

# ======================================================
# Output Folder
# ======================================================

OUTPUT_FOLDER = Path("/opt/DataTierAI/002_ETL/output")

# ======================================================
# Read Enterprise Files
# ======================================================

windows_df = pd.read_csv(OUTPUT_FOLDER / "windows_enterprise.csv")
linux_df = pd.read_csv(OUTPUT_FOLDER / "linux_enterprise.csv")
database_df = pd.read_csv(OUTPUT_FOLDER / "database_enterprise.csv")
github_df = pd.read_csv(OUTPUT_FOLDER / "github_enterprise.csv")

print(f"Windows Records   : {len(windows_df)}")
print(f"Linux Records     : {len(linux_df)}")
print(f"Database Records  : {len(database_df)}")
print(f"GitHub Records    : {len(github_df)}")

# ======================================================
# Merge All Data
# ======================================================

enterprise_df = pd.concat(
    [
        windows_df,
        linux_df,
        database_df,
        github_df
    ],
    ignore_index=True,
    sort=False
)

# ======================================================
# Remove Duplicate Records
# ======================================================

before = len(enterprise_df)

enterprise_df.drop_duplicates(inplace=True)

after = len(enterprise_df)

print("\nDuplicate Records Removed :", before - after)

# ======================================================
# Fill Missing Values
# ======================================================

# Fill text columns
text_columns = enterprise_df.select_dtypes(include=["object"]).columns
enterprise_df[text_columns] = enterprise_df[text_columns].fillna("N/A")

# Fill numeric columns
numeric_columns = enterprise_df.select_dtypes(include=["number"]).columns
enterprise_df[numeric_columns] = enterprise_df[numeric_columns].fillna(0)

# ======================================================
# Sort Data
# ======================================================

enterprise_df.sort_values(
    by=["Source", "Object_Name"],
    inplace=True
)

enterprise_df.reset_index(
    drop=True,
    inplace=True
)

# ======================================================
# Save Enterprise Dataset
# ======================================================

OUTPUT_FILE = OUTPUT_FOLDER / "enterprise_metadata.csv"

enterprise_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ======================================================
# Dataset Information
# ======================================================

print("\n" + "=" * 70)
print("Enterprise Dataset Summary")
print("=" * 70)

print()

print(enterprise_df.head())

print()

print(enterprise_df.info())

print()

print(enterprise_df.describe(include="all"))

# ======================================================
# Final Output
# ======================================================

print("\n" + "=" * 70)
print("Enterprise ETL Merge Completed Successfully")
print("=" * 70)

print(f"Total Records : {len(enterprise_df)}")
print(f"Total Columns : {len(enterprise_df.columns)}")
print(f"Output File   : {OUTPUT_FILE}")

print("=" * 70)