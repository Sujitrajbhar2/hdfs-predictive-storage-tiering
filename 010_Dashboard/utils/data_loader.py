
import pandas as pd
import streamlit as st
from pathlib import Path

DATA_FILE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "enterprise_dataset.csv"
)


@st.cache_data
def load_data():
    """Load the CSV once and cache it so every page reuses the same data."""
    dataframe = pd.read_csv(DATA_FILE_PATH)
    return dataframe


def get_kpi_summary(dataframe):
    """
    Return the 7 headline numbers shown as KPI cards on the Home page:
    total files, total storage, hot/warm/cold split, enterprise score,
    activity score.
    """
    total_files = len(dataframe)

    total_storage_gb = dataframe["Size_KB"].sum() / (1024 * 1024)

    hot_count = (dataframe["Storage_Label"] == "HOT").sum()
    warm_count = (dataframe["Storage_Label"] == "WARM").sum()
    cold_count = (dataframe["Storage_Label"] == "COLD").sum()
    archive_count = (dataframe["Storage_Label"]=="ARCHIVE").sum()

    hot_pct = round((hot_count / total_files) * 100, 0)
    warm_pct = round((warm_count / total_files) * 100, 0)
    cold_pct = round((cold_count / total_files) * 100, 0)
    archive_pct = round(archive_count/total_files*100,0)

    average_enterprise_score = dataframe["Enterprise_Score"].mean()
    average_activity_score = dataframe["Activity_Score"].mean()

    summary = {
        "total_files": total_files,
        "total_storage_gb": total_storage_gb,
        "hot_count": hot_count,
        "hot_pct": hot_pct,
        "warm_count": warm_count,
        "warm_pct": warm_pct,
        "cold_count": cold_count,
        "cold_pct": cold_pct,
        "enterprise_score": average_enterprise_score,
        "activity_score": average_activity_score,
        "archive_count":archive_count,
        "archive_pct":archive_pct,
    }
    return summary


def get_storage_distribution(dataframe):
    """Return file count per storage tier (HOT / WARM / COLD) for the donut chart."""
    distribution = dataframe["Storage_Label"].value_counts().reset_index()
    distribution.columns = ["Storage_Tier", "File_Count"]
    return distribution


def get_top_departments_by_storage(dataframe, top_n=8):
    """Return the departments that consume the most storage, in TB, biggest first."""
    grouped = dataframe.groupby("Department")["Size_KB"].sum().reset_index()
    grouped["Storage_TB"] = grouped["Size_KB"] / (1024 * 1024 * 1024)
    grouped = grouped.sort_values("Storage_TB", ascending=False).head(top_n)
    return grouped[["Department", "Storage_TB"]]


def get_cold_files_by_department(dataframe, top_n=8):
    """Return the % of files that are COLD, for the top departments by file count."""
    top_departments = dataframe["Department"].value_counts().head(top_n).index

    result_rows = []
    for department_name in top_departments:
        department_data = dataframe[dataframe["Department"] == department_name]
        cold_files = (department_data["Storage_Label"] == "COLD").sum()
        total_files = len(department_data)
        cold_percentage = (cold_files / total_files) * 100
        result_rows.append({"Department": department_name, "Cold_Percentage": cold_percentage})

    result_df = pd.DataFrame(result_rows)
    return result_df


def get_storage_growth_trend(dataframe):
    """
    Build a cumulative storage growth line, one point per year,
    based on each file's Created_Date year.
    """
    dated_files = dataframe.dropna(subset=["Created_Date"]).copy()

    dated_files["Created_Date"] = pd.to_datetime(

        dated_files["Created_Date"],
        errors="coerce"
    )

    dated_files["Created_Year"] = dated_files["Created_Date"].dt.year


    yearly_storage = dated_files.groupby("Created_Year")["Size_KB"].sum().reset_index()
    yearly_storage = yearly_storage.sort_values("Created_Year")

    yearly_storage["Cumulative_KB"] = yearly_storage["Size_KB"].cumsum()
    yearly_storage["Cumulative_TB"] = yearly_storage["Cumulative_KB"] / (1024 * 1024 * 1024)

    return yearly_storage[["Created_Year", "Cumulative_TB"]]


def get_top_largest_files(dataframe, top_n=10):
    """
    Return the top N largest files as a plain list of dicts, ready for
    utils/components.py -> render_premium_table(). Each row also gets
    a simple, rule-based "Recommendation" based on its storage tier
    and how long it's been since it was last touched.
    """
    top_files = dataframe.sort_values("Size_KB", ascending=False).head(top_n).copy()

    rows = []
    for _, file_row in top_files.iterrows():
        size_gb = round(file_row["Size_KB"] / (1024 * 1024), 2)
        storage_tier = file_row["Storage_Label"] if pd.notna(file_row["Storage_Label"]) else "COLD"
        last_modified_days = file_row["Last_Modified_Days"]

        if storage_tier == "ARCHIVE" and last_modified_days > 365:
            recommendation = "Already Archived"
        elif storage_tier == "COLD":
            recommendation = "Archive"
        elif storage_tier == "WARM":
            recommendation = "Monitor"
        else:
            recommendation = "Keep Active"

        rows.append({
            "file_name": file_row["Object_Name"] if pd.notna(file_row["Object_Name"]) else "Unnamed File",
            "department": file_row["Department"] if pd.notna(file_row["Department"]) else "Unknown",
            "size_text": f"{size_gb} GB",
            "storage_tier": storage_tier,
            "last_access": str(file_row["Modified_Date"])[:10] if pd.notna(file_row["Modified_Date"]) else "Unknown",
            "recommendation": recommendation,
        })

    return rows


def get_department_list(dataframe):
    """Return a sorted list of unique departments, used for the Analytics page filter."""
    departments = dataframe["Department"].dropna().unique().tolist()
    departments.sort()
    return departments


def get_storage_tier_list(dataframe):
    """Return the unique storage tier labels, used for the Analytics page filter."""
    tiers = dataframe["Storage_Label"].dropna().unique().tolist()
    return tiers


def get_category_list(dataframe):
    """Return the unique file categories, used for the Analytics page filter."""
    categories = dataframe["Category"].dropna().unique().tolist()
    return categories


def get_department_risk_score(dataframe, top_n=10):
    """
    Return an average 'risk score' per department. The dataset already
    provides Department_Business_Score, so we simply average it per
    department - higher score means the department carries more risk
    from a storage/lifecycle standpoint.
    """
    grouped = dataframe.groupby("Department")["Department_Business_Score"].mean().reset_index()
    grouped = grouped.sort_values("Department_Business_Score", ascending=False).head(top_n)
    grouped.columns = ["Department", "Risk_Score"]
    return grouped


def get_storage_usage_by_department_full(dataframe):
    """Return storage usage (GB) for EVERY department, not just the top ones."""
    grouped = dataframe.groupby("Department")["Size_KB"].sum().reset_index()
    grouped["Storage_GB"] = grouped["Size_KB"] / (1024 * 1024)
    grouped = grouped.sort_values("Storage_GB", ascending=False)
    return grouped[["Department", "Storage_GB"]]


def get_enterprise_score_distribution(dataframe):
    """Return the raw Enterprise_Score column for a histogram."""
    return dataframe["Enterprise_Score"].dropna()


def get_activity_score_distribution(dataframe):
    """Return the raw Activity_Score column for a histogram."""
    return dataframe["Activity_Score"].dropna()


def get_correlation_matrix(dataframe):
    """Return a correlation matrix of the key numeric scoring columns."""
    numeric_columns = [
        "Size_KB", "File_Age_Days", "Last_Modified_Days",
        "Activity_Score", "Age_Score", "Size_Score",
        "Activity_Business_Score", "Enterprise_Score",
    ]
    correlation_matrix = dataframe[numeric_columns].corr()
    return correlation_matrix


def get_average_file_age_by_department(dataframe, top_n=10):
    """Return the average File_Age_Days per department."""
    grouped = dataframe.groupby("Department")["File_Age_Days"].mean().reset_index()
    grouped = grouped.sort_values("File_Age_Days", ascending=False).head(top_n)
    grouped.columns = ["Department", "Average_Age_Days"]
    return grouped


def get_files_for_archive(dataframe, age_cutoff_days=365, top_n=15):
    """Return the oldest, least recently modified files - candidates to archive."""
    old_files = dataframe[dataframe["Last_Modified_Days"] > age_cutoff_days].copy()
    old_files["File_Name"] = old_files["Object_Name"].fillna("Unnamed File")
    old_files["Size_GB"] = round(old_files["Size_KB"] / (1024 * 1024), 2)
    old_files = old_files.sort_values("Last_Modified_Days", ascending=False).head(top_n)
    return old_files[["File_Name", "Department", "Size_GB", "Last_Modified_Days", "Storage_Label"]].rename(
        columns={"Last_Modified_Days": "Days Since Modified", "Storage_Label": "Storage Tier"}
    )


def get_large_files_for_compression(dataframe, size_cutoff_gb=5, top_n=15):
    """Return the largest files - candidates to compress."""
    size_cutoff_kb = size_cutoff_gb * 1024 * 1024
    large_files = dataframe[dataframe["Size_KB"] > size_cutoff_kb].copy()
    large_files["File_Name"] = large_files["Object_Name"].fillna("Unnamed File")
    large_files["Size_GB"] = round(large_files["Size_KB"] / (1024 * 1024), 2)
    large_files = large_files.sort_values("Size_GB", ascending=False).head(top_n)
    return large_files[["File_Name", "Department", "Size_GB", "Storage_Label"]].rename(
        columns={"Storage_Label": "Storage Tier"}
    )


def get_temp_files_for_deletion(dataframe, top_n=15):
    """Return files whose name suggests they are temporary/log files - candidates to delete."""
    temp_files = dataframe[
        dataframe["Object_Name"].str.contains("log|temp|tmp", case=False, na=False)
    ].copy()
    temp_files["File_Name"] = temp_files["Object_Name"]
    temp_files["Size_GB"] = round(temp_files["Size_KB"] / (1024 * 1024), 2)
    temp_files = temp_files.sort_values("Size_GB", ascending=False).head(top_n)
    return temp_files[["File_Name", "Department", "Size_GB", "Storage_Label"]].rename(
        columns={"Storage_Label": "Storage Tier"}
    )


def get_department_summary_table(dataframe):
    """Return one row per department with file count, storage, and average scores - used for Reports."""
    grouped = dataframe.groupby("Department").agg(
        File_Count=("Size_KB", "size"),
        Storage_KB=("Size_KB", "sum"),
        Avg_Enterprise_Score=("Enterprise_Score", "mean"),
        Avg_Activity_Score=("Activity_Score", "mean"),
    ).reset_index()
    grouped["Storage_GB"] = round(grouped["Storage_KB"] / (1024 * 1024), 2)
    grouped["Avg_Enterprise_Score"] = round(grouped["Avg_Enterprise_Score"], 1)
    grouped["Avg_Activity_Score"] = round(grouped["Avg_Activity_Score"], 1)
    grouped = grouped.sort_values("Storage_GB", ascending=False)
    return grouped[["Department", "File_Count", "Storage_GB", "Avg_Enterprise_Score", "Avg_Activity_Score"]]


def get_department_alerts(dataframe, risk_threshold=4, cold_threshold_pct=90):
    """
    Build a simple rule-based alert list: any department whose average
    risk score OR cold-file percentage crosses a threshold gets flagged.
    This is plain if/else logic, not a real anomaly-detection model.
    """
    department_names = dataframe["Department"].dropna().unique()
    alerts = []

    for department_name in department_names:
        department_data = dataframe[dataframe["Department"] == department_name]
        if len(department_data) == 0:
            continue

        avg_risk_score = department_data["Department_Business_Score"].mean()
        cold_percentage = (department_data["Storage_Label"] == "COLD").sum() / len(department_data) * 100

        if avg_risk_score >= risk_threshold:
            alerts.append({
                "severity": "High",
                "department": department_name,
                "message": f"Risk score is {avg_risk_score:.1f}, above the {risk_threshold} threshold.",
            })

        if cold_percentage >= cold_threshold_pct:
            alerts.append({
                "severity": "Medium",
                "department": department_name,
                "message": f"{cold_percentage:.0f}% of files are cold and may be safe to archive.",
            })

    return alerts


def filter_dataframe(dataframe, departments=None, tiers=None, categories=None,
                      start_date=None, end_date=None, search_text=None):
    """
    Apply the Analytics page filters one at a time. Every argument is
    optional - pass None (or an empty list) to skip that filter.
    """
    filtered = dataframe.copy()

    if departments:
        filtered = filtered[filtered["Department"].isin(departments)]

    if tiers:
        filtered = filtered[filtered["Storage_Label"].isin(tiers)]

    if categories:
        filtered = filtered[filtered["Category"].isin(categories)]

    if start_date is not None and end_date is not None:
        filtered["Created_Date_Parsed"] = pd.to_datetime(filtered["Created_Date"], errors="coerce")
        filtered = filtered[
            (filtered["Created_Date_Parsed"].dt.date >= start_date) &
            (filtered["Created_Date_Parsed"].dt.date <= end_date)
        ]

    if search_text:
        filtered = filtered[
            filtered["Object_Name"].str.contains(search_text, case=False, na=False)
        ]

    return filtered
