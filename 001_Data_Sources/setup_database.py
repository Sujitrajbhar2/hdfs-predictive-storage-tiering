import sqlite3
from pathlib import Path

# ==========================================
# Database Location
# ==========================================

DB_PATH = Path(__file__).resolve().parent / "database" / "company_metadata.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

print("=" * 60)
print("Creating Enterprise Database...")
print("=" * 60)

# =====================================================
# Employees Table
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(

employee_id TEXT PRIMARY KEY,
employee_name TEXT,
department TEXT,
designation TEXT

)
""")

# =====================================================
# Departments Table
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments(

department_id TEXT PRIMARY KEY,
department_name TEXT,
location TEXT

)
""")

# =====================================================
# Projects Table
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS projects(

project_id TEXT PRIMARY KEY,
project_name TEXT,
department TEXT,
priority TEXT

)
""")

# =====================================================
# Storage Policy Table
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS storage_policy(

extension TEXT,
storage_tier TEXT,
retention_years INTEGER

)
""")

print("Tables Created Successfully.")

# ==========================================
# Employees
# ==========================================

employees = [

("E001","Rahul Sharma","HR","Manager"),
("E002","Priya Singh","Finance","Analyst"),
("E003","Amit Kumar","Engineering","Developer"),
("E004","Sneha Patel","Marketing","Executive"),
("E005","Rohan Verma","IT","Administrator")

]

cursor.executemany(

"INSERT OR IGNORE INTO employees VALUES(?,?,?,?)",
employees

)

# ==========================================
# Departments
# ==========================================

departments = [

("D001","HR","Mumbai"),
("D002","Finance","Pune"),
("D003","Engineering","Bangalore"),
("D004","Marketing","Delhi"),
("D005","IT","Hyderabad")

]

cursor.executemany(

"INSERT OR IGNORE INTO departments VALUES(?,?,?)",
departments

)

# ==========================================
# Projects
# ==========================================

projects = [

("P001","DataTierAI","Engineering","High"),
("P002","ERP Upgrade","IT","Medium"),
("P003","Cloud Migration","Engineering","High"),
("P004","Marketing Campaign","Marketing","Low")

]

cursor.executemany(

"INSERT OR IGNORE INTO projects VALUES(?,?,?,?)",
projects

)

# ==========================================
# Storage Policies
# ==========================================

storage = [

("pdf","HOT",5),
("docx","HOT",5),
("xlsx","HOT",7),
("zip","COLD",10),
("log","ARCHIVE",2),
("csv","COLD",3),
("tar","ARCHIVE",5)

]

cursor.executemany(

"INSERT OR IGNORE INTO storage_policy VALUES(?,?,?)",
storage

)

conn.commit()

print("Sample Enterprise Data Inserted.")

conn.close()

print("=" * 60)
print("Enterprise Database Ready")
print("=" * 60)