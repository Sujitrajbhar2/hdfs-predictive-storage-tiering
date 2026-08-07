import os
import shutil

BASE_DIR = "/opt/DataTierAI"

MODEL_SOURCE = f"{BASE_DIR}/008_Machine_Learning/models"

MODEL_DEST = f"{BASE_DIR}/010_Dashboard/models"

os.makedirs(MODEL_DEST, exist_ok=True)

print("="*60)
print("Deploying Latest ML Model")
print("="*60)

for file in os.listdir(MODEL_SOURCE):

    if file.endswith(".pkl"):

        shutil.copy(
            os.path.join(MODEL_SOURCE,file),
            MODEL_DEST
        )

        print(f"Copied : {file}")

print("="*60)
print("Deployment Finished")
print("="*60)