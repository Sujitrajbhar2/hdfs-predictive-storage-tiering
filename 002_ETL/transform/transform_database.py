import pandas as pd
from pathlib import Path

print("=" * 70)
print("DataTierAI - Database Metadata Transformer")
print("=" * 70)

# ======================================================
# Read Database Metadata
# ======================================================

INPUT_FILE = Path("/opt/DataTierAI/002_ETL/output/database_metadata.csv")

database_df = pd.read_csv(INPUT_FILE)

print(f"Records Loaded : {len(database_df)}")

# ======================================================
# Transform to Enterprise Schema
# ======================================================

enterprise_df = pd.DataFrame()

enterprise_df["Source"] = database_df["Source"]
enterprise_df["Object_Name"] = database_df["employee_name"]
enterprise_df["Category"] = "Database Record"
enterprise_df["Department"] = database_df["department_name"]
enterprise_df["Extension_Type"] = database_df["extension"]
enterprise_df["Size_KB"] = 0
enterprise_df["Created_Date"] = "N/A"
enterprise_df["Modified_Date"] = "N/A"
enterprise_df["Owner"] = database_df["employee_name"]
enterprise_df["Location"] = database_df["location"]
enterprise_df["Priority"] = database_df["priority"]
enterprise_df["Storage_Tier"] = database_df["storage_tier"]

# ======================================================
# Save Output
# ======================================================

OUTPUT_FILE = Path("/opt/DataTierAI/002_ETL/output/database_enterprise.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

enterprise_df.to_csv(
    OUTPUT_FILE,
    index=False
)
print("\nTransformation Completed Successfully")
print(f"Output File : {OUTPUT_FILE}")
print(f"Total Records : {len(enterprise_df)}")

print("\nPreview\n")
print(enterprise_df.head())