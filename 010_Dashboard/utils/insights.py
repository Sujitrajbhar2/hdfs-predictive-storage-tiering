"""
insights.py

Turns raw numbers from the dataset into short, readable sentences
for the "AI Insights" and "AI Recommendations" sections. Nothing
here is a real machine-learning model - it is simple rule-based
logic (e.g. "if this department has the most storage, mention it").
That keeps it easy to read and easy to change.

Each function returns a plain Python list of dictionaries, so the
page file can loop over the list and render one card per item.
"""

def build_ai_insights(dataframe):
    """Return a list of insight cards (icon + text) built from the current data."""
    insights = []

    total_storage_kb = dataframe["Size_KB"].sum()

    # Insight 1: department with the highest storage share
    storage_by_department = dataframe.groupby("Department")["Size_KB"].sum()
    top_department = storage_by_department.idxmax()
    top_department_share = round((storage_by_department.max() / total_storage_kb) * 100, 1)
    insights.append({
        "icon": "🏢",
        "text": f"<b>{top_department}</b> is the largest storage consumer in the enterprise, accounting for nearly ~{top_department_share}% of total storage."
    })

    # Insight 2: department with the highest share of old, inactive files
    old_file_cutoff_days = 365
    old_files = dataframe[dataframe["Last_Modified_Days"] > old_file_cutoff_days]
    if len(old_files) > 0:
        old_files_by_department = old_files["Department"].value_counts()
        top_stale_department = old_files_by_department.idxmax()
        stale_department_total = len(dataframe[dataframe["Department"] == top_stale_department])
        stale_share = round((old_files_by_department.max() / stale_department_total) * 100, 1)
        insights.append({
            "icon": "🕒",
            "text": f"<b>{top_stale_department}</b> has the highest share of old, inactive files "
                    f"(~{stale_share}%) untouched for {old_file_cutoff_days}+ days."
        })

    # Insight 3: single largest repository / department footprint
    largest_footprint_department = storage_by_department.idxmax()
    largest_footprint_gb = round(storage_by_department.max() / (1024 * 1024), 1)
    insights.append({
        "icon": "☁️",
        "text": f"<b>{largest_footprint_department}</b> occupies the largest storage footprint "
                f"({largest_footprint_gb} GB)."
    })

    # Insight 4: estimated savings from cold files (assume cold files can move to cheaper tier)
    cold_files = dataframe[dataframe["Storage_Label"].isin(["COLD", "ARCHIVE"])]
    cold_storage_gb = cold_files["Size_KB"].sum() / (1024 * 1024)
    estimated_savings_gb = round(cold_storage_gb * 0.55, 0)  # assume ~55% cost reduction on cold data
    insights.append({
        "icon": "🎯",
        "text": f"Estimated storage-saving opportunity: ~{estimated_savings_gb:.0f} GB across "
                f"identified optimization actions."
    })

    return insights


def build_ai_recommendations(dataframe):
    """
    Return a list of recommendation cards built from the current data.
    Each item has: icon, title, text (description), savings_text, and
    priority ("High" / "Medium" / "Low") - all shown on the card.
    """
    recommendations = []

    # 1. Move Inactive Files - files untouched for a long time
    old_file_cutoff_days = 365
    old_files = dataframe[dataframe["Last_Modified_Days"] > old_file_cutoff_days]
    old_files_count = len(old_files)
    old_files_savings_gb = round(old_files["Size_KB"].sum() * 0.4 / (1024 * 1024), 0)
    recommendations.append({
        "icon": "📦",
        "title": "Move Inactive Files",
        "text": f"{old_files_count:,} files haven't been touched in {old_file_cutoff_days}+ days.",
        "savings_gb": old_files_savings_gb,
        "priority": "High" if old_files_savings_gb > 50 else "Medium",
    })

    # 2. Compress Logs - larger log/temp-named files
    temp_pattern_files = dataframe[
        dataframe["Object_Name"].str.contains("log|temp|tmp", case=False, na=False)
    ]
    compress_cutoff_kb = 50 * 1024  # 50 MB
    logs_to_compress = temp_pattern_files[temp_pattern_files["Size_KB"] > compress_cutoff_kb]
    logs_to_compress_count = len(logs_to_compress)
    logs_savings_gb = round(logs_to_compress["Size_KB"].sum() * 0.3 / (1024 * 1024), 0)
    recommendations.append({
        "icon": "📄",
        "title": "Compress Logs",
        "text": f"{logs_to_compress_count:,} log-type files are large enough to benefit from compression.",
        "savings_gb": logs_savings_gb,
        "priority": "Medium",
    })

    # 3. Archive Files - files already sitting in the cold tier
    cold_files = dataframe[dataframe["Storage_Label"] == "COLD"]
    cold_file_count = len(cold_files)
    cold_storage_gb = round(cold_files["Size_KB"].sum() / (1024 * 1024), 0)
    archive_savings_gb = round(cold_storage_gb * 0.4, 0)
    recommendations.append({
        "icon": "🗄️",
        "title": "Optimize Cold Storage",
        "text": f"{cold_file_count:,} COLD/ARCHIVE files ({cold_storage_gb:.0f} GB) are cold and ready to archive.",
        "savings_gb": archive_savings_gb,
        "priority": "High" if archive_savings_gb > 50 else "Medium",
    })

    # 4. Delete Temporary Files - small log/temp-named files (low value to keep)
    temp_files_to_delete = temp_pattern_files[temp_pattern_files["Size_KB"] <= compress_cutoff_kb]
    temp_files_to_delete_count = len(temp_files_to_delete)
    temp_files_savings_gb = round(temp_files_to_delete["Size_KB"].sum() / (1024 * 1024), 0)
    recommendations.append({
        "icon": "🗑️",
        "title": "Delete Temporary Files",
        "text": f"{temp_files_to_delete_count:,} small temporary files can likely be deleted outright.",
        "savings_gb": temp_files_savings_gb,
        "priority": "Low",
    })

    # 5. Estimated Savings - summary card totalling the above
    total_savings_gb = old_files_savings_gb + logs_savings_gb + archive_savings_gb + temp_files_savings_gb
    recommendations.append({
        "icon": "💰",
        "title": "Estimated Savings",
        "text": "Combined potential savings across every recommendation above.",
        "savings_gb": total_savings_gb,
        "priority": "High",
    })

    # Turn the raw savings_gb number into the display string used on the card
    for recommendation in recommendations:
        recommendation["savings_text"] = f"💾 Estimated savings: ~{recommendation['savings_gb']:.0f} GB"

    return recommendations
