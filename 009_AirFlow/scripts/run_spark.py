import subprocess

print("="*60)
print("Running Spark Processing")
print("="*60)

subprocess.run([
    "docker",
    "exec",
    "spark-master",
    "spark-submit",
    "/opt/DataTierAI/007_Spark_Processing/spark_read_hdfs.py"
], check=True)

print("\nSpark Completed")