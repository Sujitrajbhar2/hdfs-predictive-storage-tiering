from pyspark.sql import SparkSession

print("=" * 70)
print("DataTierAI - Spark HDFS Reader")
print("=" * 70)

# Create Spark Session
spark = (
    SparkSession.builder
    .appName("DataTierAI")
    .master("local[*]")
    .getOrCreate()
)

print("Spark Session Started Successfully\n")

# Read CSV from HDFS
df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv("hdfs://namenode:9000/DataTierAI/raw/enterprise_activity_metadata.csv")
)

print("=" * 70)
print("Dataset Loaded Successfully")
print("=" * 70)

print(f"Total Records : {df.count()}")
print(f"Total Columns : {len(df.columns)}")

print("\nColumns\n")
print(df.columns)

print("\nFirst 10 Records\n")
df.show(10, truncate=False)

spark.stop()

print("\nSpark Session Stopped")