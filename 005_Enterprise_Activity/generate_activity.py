import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

print("="*70)
print("DataTierAI - Enterprise Activity Generator")
print("="*70)
INPUT_FILE = Path("/opt/DataTierAI/004_Feature_Engineering/output/feature_engineered_metadata.csv")

df = pd.read_csv(INPUT_FILE)

print(f"Records Loaded : {len(df)}")
print(f"Columns Loaded : {len(df.columns)}")

# =====================================================
# Access Count (Last 30 Days)
# =====================================================

def generate_access(row):

    if row["Storage_Label"] == "HOT":
        return np.random.randint(3000,7000)

    elif row["Storage_Label"] == "WARM":
        return np.random.randint(1000,3000)

    elif row["Storage_Label"] == "COLD":
        return np.random.randint(100,1000)

    else:
        return np.random.randint(0,100)

df["Access_Count_30D"] = df.apply(generate_access,axis=1)

# =====================================================
# Last Access Date
# =====================================================

today = datetime.today()

def last_access(row):

    if row["Storage_Label"]=="HOT":
        days=np.random.randint(0,7)

    elif row["Storage_Label"]=="WARM":
        days=np.random.randint(7,30)

    elif row["Storage_Label"]=="COLD":
        days=np.random.randint(30,180)

    else:
        days=np.random.randint(180,730)

    return (today-timedelta(days=days)).date()

df["Last_Access_Date"]=df.apply(last_access,axis=1)

# =====================================================
# Unique Users
# =====================================================

def user_count(row):

    if row["Priority"]=="High":
        return np.random.randint(20,100)

    elif row["Priority"]=="Medium":
        return np.random.randint(10,40)

    else:
        return np.random.randint(1,20)

df["Unique_Users"]=df.apply(user_count,axis=1)

# =====================================================
# Read / Write Count
# =====================================================

df["Read_Count"]=(df["Access_Count_30D"]*0.8).astype(int)

df["Write_Count"]=(df["Access_Count_30D"]*0.2).astype(int)

# =====================================================
# Compliance
# =====================================================

def compliance(row):

    dept=str(row["Department"]).lower()

    if "finance" in dept:
        return "SOX"

    elif "hr" in dept:
        return "GDPR"

    elif "medical" in dept:
        return "HIPAA"

    else:
        return "None"

df["Compliance"]=df.apply(compliance,axis=1)

# =====================================================
# Retention
# =====================================================

def retention(row):

    if row["Compliance"]=="SOX":
        return 7

    elif row["Compliance"]=="GDPR":
        return 10

    elif row["Compliance"]=="HIPAA":
        return 8

    else:
        return 2

df["Retention_Years"]=df.apply(retention,axis=1)

# =====================================================
# Storage Cost
# =====================================================

def storage_cost(row):

    size_mb=row["Size_KB"]/1024

    if row["Storage_Label"]=="HOT":
        rate=0.20

    elif row["Storage_Label"]=="WARM":
        rate=0.10

    elif row["Storage_Label"]=="COLD":
        rate=0.05

    else:
        rate=0.02

    return round(size_mb*rate,2)

df["Storage_Cost"]=df.apply(storage_cost,axis=1)

# =====================================================
# Backup Flag
# =====================================================

df["Backup_Flag"]=df["Object_Name"].str.lower().str.contains(
    "backup|archive",
    regex=True
)

df["Backup_Flag"]=df["Backup_Flag"].map({
    True:"YES",
    False:"NO"
})

# =====================================================
# Enterprise Expansion
# =====================================================

target_records = 100000

copies = int(target_records / len(df)) + 1

expanded = []

for i in range(copies):

    temp = df.copy()

    temp["Object_Name"] = (
        temp["Object_Name"].astype(str)
        + "_V"
        + str(i+1)
    )

    expanded.append(temp)

enterprise_df = pd.concat(expanded,ignore_index=True)

enterprise_df = enterprise_df.head(target_records)



# =====================================================
# Generate Balanced Storage Labels
# =====================================================

# Remove old label if present
if "Storage_Label" in enterprise_df.columns:
    enterprise_df.drop(columns=["Storage_Label"], inplace=True)

# Sort by Access Count (highest first)
enterprise_df = enterprise_df.sort_values(
    by="Access_Count_30D",
    ascending=False
).reset_index(drop=True)

total = len(enterprise_df)

hot_end = int(total * 0.15)
warm_end = int(total * 0.45)
cold_end = int(total * 0.80)

enterprise_df["Storage_Label"] = "ARCHIVE"

enterprise_df.loc[:hot_end-1, "Storage_Label"] = "HOT"
enterprise_df.loc[hot_end:warm_end-1, "Storage_Label"] = "WARM"
enterprise_df.loc[warm_end:cold_end-1, "Storage_Label"] = "COLD"
enterprise_df.loc[cold_end:, "Storage_Label"] = "ARCHIVE"


print("\nBalanced Storage Distribution\n")
print(enterprise_df["Storage_Label"].value_counts())

print("\nPercentage\n")
print(
    round(
        enterprise_df["Storage_Label"].value_counts(normalize=True) * 100,
        2
    )
)


# =====================================================
# Save Dataset
# =====================================================

OUTPUT_FOLDER = Path("/opt/DataTierAI/005_Enterprise_Activity/output")
OUTPUT_FOLDER.mkdir(parents=True,exist_ok=True)

OUTPUT_FILE=OUTPUT_FOLDER/"enterprise_activity_metadata.csv"

enterprise_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n"+"="*70)
print("Enterprise Activity Dataset Created Successfully")
print("="*70)

print(f"Final Records : {len(enterprise_df)}")
print(f"Final Columns : {len(enterprise_df.columns)}")

print("\nStorage Distribution\n")
print(enterprise_df["Storage_Label"].value_counts())

print(f"\nOutput : {OUTPUT_FILE}")
print("="*70)