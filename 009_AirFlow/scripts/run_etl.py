import subprocess
import os

BASE = "/opt/DataTierAI/002_ETL"

print("=" * 60)
print("Running ETL")
print("=" * 60)

subprocess.run([
    "python",
    os.path.join(BASE, "collector", "collect_windows.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE, "collector", "collect_linux.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE, "collector", "collect_database.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE, "collector", "collect_github.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE, "transform", "transform_windows.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE, "transform", "transform_linux.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE, "transform", "transform_database.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE, "transform", "transform_github.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE, "transform", "merge_metadata.py")
], check=True)

print("ETL Completed")