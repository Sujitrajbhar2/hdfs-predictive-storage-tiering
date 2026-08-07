from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os 

print("=" * 70)
print("DataTierAI - Spark ETL Processing")
print("=" * 70)

# =====================================================
# Create Spark Session
# =====================================================

spark = (
    SparkSession.builder
    .appName("DataTierAI")
    .master("local[*]")
    .getOrCreate()
)

# =====================================================
# Read Dataset from HDFS
# =====================================================

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv("hdfs://namenode:9000/DataTierAI/raw/enterprise_activity_metadata.csv")
)

print("\nDataset Loaded Successfully")

# =====================================================
# Dataset Information
# =====================================================

print("\nTotal Records :", df.count())
print("Total Columns :", len(df.columns))

print("\nSchema")
df.printSchema()

# =====================================================
# Null Value Check
# =====================================================

print("\nNull Value Summary")

df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
]).show()

# =====================================================
# Department Summary
# =====================================================

print("\nDepartment-wise File Count")

df.groupBy("Department") \
    .count() \
    .orderBy(desc("count")) \
    .show()

# =====================================================
# Storage Tier Summary
# =====================================================

print("\nStorage Label Summary")

df.groupBy("Storage_Label") \
    .count() \
    .show()

# =====================================================
# Compliance Summary
# =====================================================

print("\nCompliance Summary")

df.groupBy("Compliance") \
    .count() \
    .show()

# =====================================================
# Top 10 Largest Files
# =====================================================

print("\nTop 10 Largest Files")

df.select(
    "Object_Name",
    "Department",
    "Size_KB"
).orderBy(
    desc("Size_KB")
).show(10, truncate=False)

# =====================================================
# Enterprise Score
# =====================================================

print("\nAverage Enterprise Score")

df.select(
    avg("Enterprise_Score")
).show()


# =====================================================
# Save Processed Dataset to HDFS
# =====================================================

HDFS_OUTPUT = "hdfs://namenode:9000/DataTierAI/processed/enterprise_dataset"

(
    df.coalesce(1)
      .write
      .mode("overwrite")
      .option("header", "true")
      .csv(HDFS_OUTPUT)
)

print("\nProcessed Dataset Saved to HDFS")
print(f"HDFS Path : {HDFS_OUTPUT}")

os.makedirs("/opt/DataTierAI/007_Spark_Processing/output", exist_ok=True)

# =====================================================
# Save Processed Dataset Locally (For Machine Learning)
# =====================================================

LOCAL_OUTPUT = "/opt/DataTierAI/007_Spark_Processing/output/enterprise_dataset"

(
    df.coalesce(1)
      .write
      .mode("overwrite")
      .option("header", "true")
      .csv(LOCAL_OUTPUT)
)

print("\nProcessed Dataset Saved Locally")
print(f"Local Path : {LOCAL_OUTPUT}")

# =====================================================
# Stop Spark
# =====================================================

spark.stop()

print("\nSpark ETL Completed Successfully")
print("=" * 70)
