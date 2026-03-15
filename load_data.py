from pyspark.sql import SparkSession
from schemas import get_data_schema


def extract_music_data(spark, file_path, schema):
    """
    Function for reading a CSV file with music data
    """
    df = spark.read \
        .option("header", "true") \
        .option("multiline", "true") \
        .option("escape", '"') \
        .schema(schema) \
        .csv(file_path)

    return df


def main():
    # creating SparkSession
    spark = SparkSession.builder \
        .appName("MusicDataset") \
        .getOrCreate()

    # get schema
    schema = get_data_schema()

    file_path = "data/spotify_dataset.csv"

    # read data
    df = extract_music_data(spark, file_path, schema)


if __name__ == "__main__":
    main()