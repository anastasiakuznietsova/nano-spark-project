from pyspark.sql import SparkSession
import os
import sys

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

spark = SparkSession.builder \
    .appName("TestApp") \
    .getOrCreate()

data = [(1,"Test Set 1"), (2,"Test Set 2"), (3,"Test Set 3")]    # create fake test data
columns = ["ID","Name"]    # column names
df = spark.createDataFrame(data, schema=columns)

df.show()
df.write.csv("result.csv")

spark.stop()