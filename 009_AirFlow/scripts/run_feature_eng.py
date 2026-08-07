import subprocess

print("="*60)
print("Running Feature Engineering")
print("="*60)

subprocess.run(
    ["python","/opt/DataTierAI/004_Feature_Engineering/feature_eng.py"],
    check=True
)

print("\nFeature Engineering Completed")