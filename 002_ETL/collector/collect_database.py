import sqlite3
import pandas as pd
from pathlib import Path

# ==========================================
# Database Path
# ==========================================

DB_PATH = Path("/opt/DataTierAI/001_Data_Sources/database/company_metadata.db")

print("=" * 60)
print("Connecting to Enterprise Database...")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)

# ==========================================
# Read Tables
# ==========================================

employees = pd.read_sql("SELECT * FROM employees", conn)

departments = pd.read_sql("SELECT * FROM departments", conn)

projects = pd.read_sql("SELECT * FROM projects", conn)

storage = pd.read_sql("SELECT * FROM storage_policy", conn)

print("\nEmployees")
print(employees.head())

print("\nDepartments")
print(departments.head())

print("\nProjects")
print(projects.head())

print("\nStorage Policy")
print(storage.head())

conn.close()

employees["Source"] = "Database"
departments["Source"] = "Database"
projects["Source"] = "Database"
storage["Source"] = "Database"

database_metadata = pd.concat(
    [employees, departments, projects, storage],
    ignore_index=True,
    sort=False
)

database_metadata.to_csv(
    "database_metadata.csv",
    index=False
)

print("\nDatabase Metadata Saved Successfully.")