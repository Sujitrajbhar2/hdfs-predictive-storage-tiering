from pyspark.sql import SparkSession

print("=" * 70)
print("DataTierAI - Spark Environment Setup")
print("=" * 70)

# Create Spark Session
spark = (
    SparkSession.builder
    .appName("DataTierAI")
    .master("local[*]")
    .getOrCreate()
)

print("\nSpark Session Started Successfully")

# Spark Version
print(f"\nSpark Version : {spark.version}")

# Application Name
print(f"Application Name : {spark.sparkContext.appName}")

# Master
print(f"Spark Master : {spark.sparkContext.master}")

# Default Parallelism
print(f"Default Parallelism : {spark.sparkContext.defaultParallelism}")

print("\nSpark Environment Verified Successfully")

spark.stop()

print("\nSpark Session Stopped Successfully")
print("=" * 70)