import pandas as pd
from pathlib import Path

print("=" * 70)
print("DataTierAI - Windows Metadata Transformer")
print("=" * 70)

# ======================================================
# Read Windows Metadata
# ======================================================


INPUT_FILE = Path("/opt/DataTierAI/002_ETL/output/windows_metadata.csv")

windows_df = pd.read_csv(INPUT_FILE)

print(f"Records Loaded : {len(windows_df)}")

# ======================================================
# Transform to Enterprise Schema
# ======================================================

enterprise_df = pd.DataFrame()

enterprise_df["Source"] = windows_df["Source"]
enterprise_df["Object_Name"] = windows_df["File_Name"]
enterprise_df["Category"] = "Windows File"
enterprise_df["Department"] = windows_df["Department"]
enterprise_df["Extension_Type"] = windows_df["Extension"]
enterprise_df["Size_KB"] = windows_df["Size_KB"]
enterprise_df["Created_Date"] = windows_df["Created_Time"]
enterprise_df["Modified_Date"] = windows_df["Modified_Time"]
enterprise_df["Owner"] = windows_df["Department"]
enterprise_df["Location"] = windows_df["Department"]
enterprise_df["Priority"] = "Medium"
enterprise_df["Storage_Tier"] = "Unknown"

# ======================================================
# Save Output
# ======================================================

OUTPUT_FILE = Path("/opt/DataTierAI/002_ETL/output/windows_enterprise.csv")

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