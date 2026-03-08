from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType


def get_data_schema():
    """
    Creates and returns the full schema for the dataset
    """
    schema = StructType([
        StructField("Artist(s)", StringType(), True),
        StructField("song", StringType(), True),
        StructField("text", StringType(), True),
        StructField("Length", StringType(), True),
        StructField("emotion", StringType(), True),
        StructField("Genre", StringType(), True),
        StructField("Album", StringType(), True),
        StructField("Release Date", StringType(), True),
        StructField("Key", StringType(), True),

        StructField("Tempo", DoubleType(), True),
        StructField("Loudness (db)", StringType(), True),
        StructField("Time signature", StringType(), True),

        StructField("Explicit", StringType(), True),

        StructField("Popularity", IntegerType(), True),
        StructField("Energy", IntegerType(), True),
        StructField("Danceability", IntegerType(), True),
        StructField("Positiveness", IntegerType(), True),
        StructField("Speechiness", IntegerType(), True),
        StructField("Liveness", IntegerType(), True),
        StructField("Acousticness", IntegerType(), True),
        StructField("Instrumentalness", IntegerType(), True),

        StructField("Good for Party", IntegerType(), True),
        StructField("Good for Work/Study", IntegerType(), True),
        StructField("Good for Relaxation/Meditation", IntegerType(), True),
        StructField("Good for Exercise", IntegerType(), True),
        StructField("Good for Running", IntegerType(), True),
        StructField("Good for Yoga/Stretching", IntegerType(), True),
        StructField("Good for Driving", IntegerType(), True),
        StructField("Good for Social Gatherings", IntegerType(), True),
        StructField("Good for Morning Routine", IntegerType(), True),

        StructField("Similar Artist 1", StringType(), True),
        StructField("Similar Song 1", StringType(), True),
        StructField("Similarity Score 1", DoubleType(), True),

        StructField("Similar Artist 2", StringType(), True),
        StructField("Similar Song 2", StringType(), True),
        StructField("Similarity Score 2", DoubleType(), True),

        StructField("Similar Artist 3", StringType(), True),
        StructField("Similar Song 3", StringType(), True),
        StructField("Similarity Score 3", DoubleType(), True)
    ])

    return schema