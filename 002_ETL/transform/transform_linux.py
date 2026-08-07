import pandas as pd
from pathlib import Path

print("=" * 70)
print("DataTierAI - Linux Metadata Transformer")
print("=" * 70)

# ======================================================
# Read Linux Metadata
# ======================================================

INPUT_FILE = Path("/opt/DataTierAI/002_ETL/output/linux_metadata.csv")

linux_df = pd.read_csv(INPUT_FILE)

print(f"Records Loaded : {len(linux_df)}")

# ======================================================
# Transform to Enterprise Schema
# ======================================================

enterprise_df = pd.DataFrame()

enterprise_df["Source"] = linux_df["Source"]
enterprise_df["Object_Name"] = linux_df["File_Name"]
enterprise_df["Category"] = "Linux File"
enterprise_df["Department"] = linux_df["Folder"]
enterprise_df["Extension_Type"] = linux_df["Extension"]
enterprise_df["Size_KB"] = linux_df["Size_KB"]
enterprise_df["Created_Date"] = linux_df["Created_Time"]
enterprise_df["Modified_Date"] = linux_df["Modified_Time"]
enterprise_df["Owner"] = "Linux System"
enterprise_df["Location"] = linux_df["Folder"]
enterprise_df["Priority"] = "Medium"
enterprise_df["Storage_Tier"] = "Unknown"

# ======================================================
# Save Output
# ======================================================

OUTPUT_FILE = Path("/opt/DataTierAI/002_ETL/output/linux_enterprise.csv")

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