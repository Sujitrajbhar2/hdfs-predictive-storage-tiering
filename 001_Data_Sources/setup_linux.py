from pathlib import Path
import random

# ==========================================
# Linux Server Base Directory
# ==========================================

BASE_DIR = Path(__file__).resolve().parent / "linux_server"

linux_folders = {

    "logs": [
        "system.log",
        "access.log",
        "error.log",
        "auth.log"
    ],

    "backup": [
        "backup_2026_01.tar",
        "backup_2026_02.tar"
    ],

    "configs": [
        "app.conf",
        "nginx.conf",
        "database.conf"
    ],

    "projects": [
        "project_alpha.zip",
        "project_beta.zip",
        "analytics_engine.tar.gz"
    ]
}

print("="*60)
print("Creating Enterprise Linux Server...")
print("="*60)

for folder, files in linux_folders.items():

    path = BASE_DIR / folder
    path.mkdir(parents=True, exist_ok=True)

    print(f"\nCreating Folder : {folder}")

    for file in files:

        file_path = path / file

        size = random.randint(50,700)

        with open(file_path,"wb") as f:
            f.write(b"0"*1024*size)

        print(f"   Created : {file} ({size} KB)")

print("\nLinux Enterprise Server Ready")