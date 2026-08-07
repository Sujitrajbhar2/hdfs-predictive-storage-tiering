import subprocess

print("="*60)
print("Running Machine Learning Pipeline")
print("="*60)

subprocess.run(
    [
        "python",
        "/opt/DataTierAI/008_Machine_Learning/train_model.py"
    ],
    check=True
)

print("="*60)
print("ML Training Completed")
print("="*60)