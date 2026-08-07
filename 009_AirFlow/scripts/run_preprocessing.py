import subprocess

print("="*60)
print("Running Preprocessing")
print("="*60)

subprocess.run(
    ["python","/opt/DataTierAI/003_Preprocessing/preprocess.py"],
    check=True
)

print("\nPreprocessing Completed")