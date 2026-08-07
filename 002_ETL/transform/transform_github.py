import pandas as pd
from pathlib import Path

print("=" * 70)
print("DataTierAI - GitHub Metadata Transformer")
print("=" * 70)

# ======================================================
# Read GitHub Metadata
# ======================================================

INPUT_FILE = Path("/opt/DataTierAI/002_ETL/output/github_metadata.csv")

github_df = pd.read_csv(INPUT_FILE)

print(f"Records Loaded : {len(github_df)}")

# ======================================================
# Transform to Enterprise Schema
# ======================================================

enterprise_df = pd.DataFrame()

enterprise_df["Source"] = "GitHub"
enterprise_df["Object_Name"] = github_df["Repository_Name"]
enterprise_df["Category"] = "GitHub Repository"
enterprise_df["Department"] = github_df["Organization"]
enterprise_df["Extension_Type"] = github_df["Language"]
enterprise_df["Size_KB"] = github_df["Repository_Size_KB"]
enterprise_df["Created_Date"] = github_df["Created_Date"]
enterprise_df["Modified_Date"] = github_df["Updated_Date"]
enterprise_df["Owner"] = github_df["Organization"]
enterprise_df["Location"] = github_df["Repository_URL"]
enterprise_df["Priority"] = "Medium"
enterprise_df["Storage_Tier"] = "Unknown"

# ======================================================
# Additional GitHub Information
# ======================================================

enterprise_df["Stars"] = github_df["Stars"]
enterprise_df["Forks"] = github_df["Forks"]
enterprise_df["Open_Issues"] = github_df["Open_Issues"]
enterprise_df["Visibility"] = github_df["Visibility"]
enterprise_df["Default_Branch"] = github_df["Default_Branch"]

# ======================================================
# Save Output
# ======================================================
OUTPUT_FILE = Path("/opt/DataTierAI/002_ETL/output/github_enterprise.csv")

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