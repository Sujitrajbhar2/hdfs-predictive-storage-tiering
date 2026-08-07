from pathlib import Path
import random

# ==============================
# Base Folder
# ==============================
BASE_DIR = Path("windows_server")

# Department -> Files
departments = {
    "HR": [
        "employee_salary.xlsx",
        "attendance.csv",
        "offer_letters.docx",
        "employee_master.xlsx",
        "leave_requests.xlsx"
    ],

    "Finance": [
        "budget_2026.xlsx",
        "invoices.pdf",
        "tax_report.xlsx",
        "payroll_summary.xlsx",
        "expense_report.csv"
    ],

    "Marketing": [
        "campaign_plan.pptx",
        "customer_feedback.csv",
        "social_media_report.xlsx",
        "marketing_budget.xlsx"
    ],

    "Engineering": [
        "project_specs.pdf",
        "source_code_backup.zip",
        "deployment_guide.docx",
        "architecture_diagram.vsdx",
        "release_notes.pdf"
    ]
}

print("=" * 60)
print("Creating Enterprise Windows Server...")
print("=" * 60)

for department, files in departments.items():

    folder = BASE_DIR / department
    folder.mkdir(parents=True, exist_ok=True)

    print(f"\nCreating Folder : {department}")

    for filename in files:

        filepath = folder / filename

        size_kb = random.randint(20, 500)

        with open(filepath, "wb") as f:
            f.write(b"0" * size_kb * 1024)

        print(f"   Created : {filename} ({size_kb} KB)")

print("\n" + "=" * 60)
print("Windows Enterprise File Server Ready")
print("=" * 60)