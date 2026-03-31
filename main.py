from pyspark.sql import SparkSession
from data_pipeline import load_and_validate_music_data
from data_cleaning import clean_music_data
from statistical_analysis import perform_statistical_analysis
from feature_selection import select_columns, split_data
from data_typing import transform_and_scale_data

def main():
    spark = SparkSession.builder \
        .appName("MusicPipeline") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    file_path = "raw_data/spotify_dataset.csv"

    try:
        df = load_and_validate_music_data(spark, file_path)
        df.show(5)

        df = clean_music_data(df)
        perform_statistical_analysis(df)
        df = select_columns(df)
        df = transform_and_scale_data(df)
        train_df, val_df, test_df = split_data(df)

    except Exception as e:
        print(f"Pipeline execution error: {e}")


if __name__ == "__main__":
    main()
