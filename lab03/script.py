from pyspark.sql.functions import col, count
from pyspark.sql.types import StructType, StructField, StringType, LongType

schema = StructType([
    StructField("name", StringType(), True),
    StructField("country", StringType(), True),
    StructField("subcountry", StringType(), True),
    StructField("geonameid", LongType(), True)
])

df = spark.read.csv("world-cities.csv", header=True, schema=schema)

df.printSchema()

result = df.groupBy("country", "subcountry").agg(count("*").alias("cnt"))

result = result.orderBy(col("cnt").desc())

result.show()