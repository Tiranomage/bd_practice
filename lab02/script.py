from pyspark.sql import SparkSession
# Создаем сессию Spark на локальном компьютере
spark = SparkSession.builder.master("local[*]").getOrCreate()

import collections
rdd = spark.sparkContext.textFile("/content/sample_data/ml-100k/u.data")

parsed_rdd = rdd.map(lambda line: line.split('\t'))
pair_rdd = parsed_rdd.map(lambda fields: (int(fields[1]), int(fields[2])))

aggPairRDD = pair_rdd.groupByKey()

def printStat(inp):
  ind, ratings_dict = inp
  marks = [0, 0, 0, 0, 0]
  for rating, count in ratings_dict.items():
    if 1 <= rating <= 5:
      marks[rating - 1] = count
  print(f'Marks for film {ind}: 1 -> {marks[0]}, 2 -> {marks[1]}, 3 -> {marks[2]}, 4 -> {marks[3]}, 5 -> {marks[4]}')

for i in aggPairRDD.mapValues(lambda x: dict(collections.Counter(x))).collect():
  printStat(i)

all_ratings = parsed_rdd.map(lambda fields: (int(fields[2]), 1)) 
all_ratings_counts = all_ratings.reduceByKey(lambda a, b: a + b).collectAsMap()

total_marks = [0, 0, 0, 0, 0]
for rating, count in all_ratings_counts.items():
  if 1 <= rating <= 5:
    total_marks[rating - 1] = count

print(f'Marks for films ALL: 1 -> {total_marks[0]}, 2 -> {total_marks[1]}, 3 -> {total_marks[2]}, 4 -> {total_marks[3]}, 5 -> {total_marks[4]}')