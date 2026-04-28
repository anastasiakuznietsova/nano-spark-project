from pyspark.sql.window import Window
from pyspark.sql import functions as F


#1
def check_avg_positiveness_with_high_energy(df):
    high_energy_df = df.filter(F.col("Energy") > 0.7)

    genre_stats = high_energy_df.groupBy("Genre").agg(
        F.avg("Positiveness").alias("avg_positiveness"),
        F.count("*").alias("track_count")
    )
    joined = df.select("Genre").distinct().join(genre_stats, on="Genre", how="left").orderBy(F.desc("avg_positiveness"))
    joined.show()
    joined.explain()

#2
def genre_loudness_outliers(df):
    window_spec = Window.partitionBy("Genre").orderBy(F.desc("Loudness (db)"))
    loudest_per_genre = (df.withColumn("rank", F.rank().over(window_spec))
                         .filter(F.col("rank") <= 3)
                         .select("Genre", "Loudness (db)", "emotion")
                         )
    loudest_per_genre.show()
    loudest_per_genre.explain()

#3
def unstable_emotions(df):
    emotional_stability_df = (df.groupBy("emotion").agg(
            F.stddev("Energy").alias("energy_var"),
            F.stddev("Loudness (db)").alias("loudness_var"),
            F.stddev("Positiveness").alias("positivity_var"),
            F.count("*").alias("sample_size"))
      .withColumn("total_avg_var",(F.col("energy_var")+F.col("loudness_var")+F.col("positivity_var"))/3)
      .orderBy(F.desc("total_avg_var")))

    emotional_stability_df.show()
    emotional_stability_df.explain()

#4
def genres_energy_outliers(df):
    genre_window = Window.partitionBy("Genre")
    vibe_deviation_df = (df.withColumn("genre_avg_energy", F.avg("Energy").over(genre_window))
                         .withColumn("energy_diff", F.abs(F.col("Energy") - F.col("genre_avg_energy")))
                         .select("Genre", "Energy", "genre_avg_energy", "energy_diff", "emotion")
                         .filter(F.col("energy_diff") > 0.3))

    vibe_deviation_df.show()
    vibe_deviation_df.explain()

#5
def emotions_lyrics_density(df):
    word_density_df = df.withColumn("word_count", F.size(F.split(F.col("text"), r"\s+")))

    emotion_stats = (word_density_df.groupBy("emotion").agg(
                        F.avg("word_count").alias("avg_words"),
                        F.stddev("word_count").alias("word_variation"),
                        F.count("*").alias("track_count"))
                     .orderBy(F.desc("avg_words")))
    emotion_stats.show()
    emotion_stats.explain()

#6
def high_energy_explicit_word_count(df):
    energy_summary = df.groupBy("emotion").agg(F.avg("Energy").alias("avg_energy"))
    high_energy_emotions = energy_summary.filter(F.col("avg_energy") > 0.8)

    comparison_df = (df.join(high_energy_emotions, on="emotion", how="inner")
        .filter(F.col("Energy") > 0.8)
        .groupBy("emotion")
        .agg(
            F.avg("explicit").alias("explicit_rate"),
            F.avg(F.size(F.split(F.col("text"), r"\s+"))).alias("avg_word_count")
        ))
    comparison_df.show()
    comparison_df.explain()
