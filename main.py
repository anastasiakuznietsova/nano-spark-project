from pyspark.sql import SparkSession
from data_pipeline import load_and_validate_music_data

def main():
    spark = SparkSession.builder \
        .appName("MusicPipeline") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    file_path = "raw_data/spotify_dataset.csv"

    try:
        df = load_and_validate_music_data(spark, file_path)
        df.show(5)
    except Exception as e:
        print(f"Pipeline execution error: {e}")


if __name__ == "__main__":
    main()
