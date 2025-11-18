from pyspark.sql.functions import col, lag, avg
from pyspark.sql.window import Window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

schema = StructType([
    StructField("Country Name", StringType(), True),
    StructField("Year", StringType(), True),
    StructField("Population", DoubleType(), True)
])

df = spark.read.csv("population.csv", header=True, schema=schema)

window_spec = Window.partitionBy("Country Name").orderBy("Year")

df_with_growth = df.withColumn("previous_population", lag("Population").over(window_spec)) \
                  .withColumn("population_growth", col("Population") - col("previous_population"))

df_filtered = df_with_growth.filter((col("Year") >= "1990") & (col("Year") <= "2018"))

avg_growth = df_filtered.groupBy("Country Name").agg(avg("population_growth").alias("trend"))

declining_population = avg_growth.filter(col("trend") < 0)

declining_population.show()