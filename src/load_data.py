# importing the necessary libraries for this script
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType


# creating a SparkSession object to work with Spark
spark = SparkSession.builder \
        .appName("Load Data") \
        .config("spark.jars", "drivers/postgresql-42.7.12.jar") \
        .getOrCreate()

# defining the schema for the data to be loaded into the database
schema = StructType([
    StructField("show_id", StringType(), True),
    StructField("type", StringType(), True),
    StructField("title", StringType(), True),
    StructField("director", StringType(), True),
    StructField("cast", StringType(), True),
    StructField("country", StringType(), True),
    StructField("date_added", StringType(), True),
    StructField("release_year", IntegerType(), True),
    StructField("rating", StringType(), True),
    StructField("duration", StringType(), True),
    StructField("listed_in", StringType(), True),
    StructField("description", StringType(), True)
])

# reading the CSV file into a Spark DataFrame using the defined schema
df = spark.read.csv("data/raw/netflix_titles.csv", header=True, schema=schema)

# configuring the database connection properties and writing the DataFrame to the PostgreSQL database
DB_URL = "jdbc:postgresql://localhost:5432/bootcamp"
PROPS = {"user": "postgres", "password": "postgres", "driver": "org.postgresql.Driver"}

# writing the DataFrame to the staging_raw table in the database, overwriting any existing data
df.write.jdbc(url=DB_URL, table="staging_raw", mode="overwrite", properties=PROPS)
print(f"Loaded {df.count()} records into the staging_raw table in the database.")