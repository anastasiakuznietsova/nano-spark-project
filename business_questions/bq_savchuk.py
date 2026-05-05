import os
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def run_all_transformations(df):
    if not os.path.exists("data_output"):
        os.makedirs("data_output")

    questions = [
        (1, "Які топ-5 найенергійніших Explicit рок-треків з темпом понад 120 BPM?", rock_explicit_energy),
        (2, "Середня енергійність та танцювальність у кожній тональності для non-explicit контенту?",
         key_metrics_non_explicit),
        (3, "Топ-3 найгучніші показники (Loudness) всередині кожного жанру?", loudness_rank_by_genre),
        (4, "Відхилення енергії кожного запису від середнього значення у його емоційній категорії?",
         energy_deviation_by_emotion),
        (5, "Середня кількість слів у розрізі музичного розміру для довгих треків (понад 3 хв)?",
         speechiness_long_tracks),
        (6, "Максимальна та мінімальна танцювальність для кожної емоції серед інструментальних треків?",
         danceability_range_instrumental)
    ]

    for num, text, func in questions:
        print("\n" + "=" * 90)
        print(f"ПИТАННЯ №{num}: {text}")
        print("=" * 90)
        func(df)


def save_result(df, name):
    output_path = f"data_output/{name}"
    columns_to_save = [c for c, t in df.dtypes if not (t.startswith("vector") or t.startswith("struct"))]
    df_to_save = df.select(columns_to_save)

    df_to_save.write.mode("overwrite").option("header", "true").csv(output_path)

    df_to_save.show(10)
    df_to_save.explain()
    print(f"\nРезультати збережено у: {output_path}")



def rock_explicit_energy(df):
    result = df.filter(
        (F.col("Genre") == "rock") &
        (F.col("Explicit") == 1) &
        (F.col("Tempo") > 120)
    ).orderBy(F.desc("Energy")).limit(5)
    save_result(result, "q1_rock_energy")


def key_metrics_non_explicit(df):
    result = df.filter(F.col("Explicit") == 0) \
        .groupBy("Key") \
        .agg(
        F.avg("Energy").alias("avg_energy"),
        F.avg("Danceability").alias("avg_danceability")
    ).orderBy(F.desc("avg_energy"))
    save_result(result, "q2_key_metrics")


def loudness_rank_by_genre(df):
    window_spec = Window.partitionBy("Genre").orderBy(F.desc("Loudness (db)"))

    result = df.withColumn("rank", F.rank().over(window_spec)) \
        .filter(F.col("rank") <= 3) \
        .select("Genre", "Loudness (db)", "Energy", "rank")
    save_result(result, "q3_loudness_ranking")


def energy_deviation_by_emotion(df):
    window_spec = Window.partitionBy("emotion")

    result = df.withColumn("avg_emo_energy", F.avg("Energy").over(window_spec)) \
        .withColumn("energy_diff", F.abs(F.col("Energy") - F.col("avg_emo_energy"))) \
        .select("emotion", "Energy", "avg_emo_energy", "energy_diff") \
        .orderBy(F.desc("energy_diff"))
    save_result(result, "q4_energy_deviation")


def speechiness_long_tracks(df):
    result = df.withColumn("word_count", F.size(F.split(F.col("text"), r"\s+"))) \
        .filter(F.col("Length") > 180) \
        .groupBy("Time signature") \
        .agg(
        F.avg("word_count").alias("avg_word_count"),
        F.count("*").alias("track_count")
    ).orderBy(F.desc("avg_word_count"))
    save_result(result, "q5_speechiness_analysis")


def danceability_range_instrumental(df):
    result = df.filter(F.col("Instrumentalness") > 0.5) \
        .groupBy("emotion") \
        .agg(
        F.max("Danceability").alias("max_dance"),
        F.min("Danceability").alias("min_dance")
    ).orderBy(F.desc("max_dance"))
    save_result(result, "q6_instrumental_dance")