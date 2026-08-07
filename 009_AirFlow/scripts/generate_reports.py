import os
import shutil

BASE_DIR = "/opt/DataTierAI"

SOURCE = f"{BASE_DIR}/008_Machine_Learning/output"

DESTINATION = f"{BASE_DIR}/010_Dashboard/assets/ml_reports"

os.makedirs(DESTINATION, exist_ok=True)

files = [
    "classification_report.txt",
    "confusion_matrix.png",
    "feature_importance.png",
    "feature_importance.csv",
    "model_metrics.csv"
]

print("="*60)
print("Copying ML Reports...")
print("="*60)

for file in files:
    src = os.path.join(SOURCE, file)

    if os.path.exists(src):
        shutil.copy(src, DESTINATION)
        print(f"Copied : {file}")

print("="*60)
print("ML Reports Copied Successfully")
print("="*60)