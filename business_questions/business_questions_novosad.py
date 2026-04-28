from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import os


def save_result(df: DataFrame, name: str):
    output_path = f"results/{name}"
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_path)
    print(f"Результат збережено у: {output_path}")

def run_business_questions_novosad(df: DataFrame):

    if not os.path.exists('results'):
        os.makedirs('results')

    print("\n--- Запуск бізнес-аналізу та збереження результатів ---")


    print("\nПитання 1: Топ-3 найпопулярніші пісні для кожної емоції")

    window_emotion_popularity = Window.partitionBy("emotion").orderBy(F.col("Popularity").desc())

    q1_top_popular_songs_by_emotion = df \
        .filter(F.col("emotion").isNotNull()) \
        .filter(F.col("Popularity").isNotNull()) \
        .withColumn("pop_rank", F.row_number().over(window_emotion_popularity)) \
        .filter(F.col("pop_rank") <= 3) \
        .select(
        "emotion",
        "song",
        "Genre",
        "Popularity",
        "Positiveness",
        "pop_rank"
    )

    q1_top_popular_songs_by_emotion.show(20, truncate=False)
    q1_top_popular_songs_by_emotion.explain()

    save_result(q1_top_popular_songs_by_emotion,"q1_top3_popular_songs_by_emotion")

    print("\nПитання 2: Жанри, у яких explicit-треки мають вищу середню енергійність, ніж non-explicit-треки")

    explicit_energy = df.filter(F.col("Explicit") == 1) \
        .groupBy("Genre") \
        .agg(F.avg("Energy").alias("avg_explicit_energy"))

    non_explicit_energy = df \
        .filter(F.col("Explicit") == 0) \
        .groupBy("Genre") \
        .agg(F.avg("Energy").alias("avg_non_explicit_energy"))

    q2_explicit_energy_genres = explicit_energy.join(non_explicit_energy, on="Genre", how="inner") \
        .filter(F.col("avg_explicit_energy") > F.col("avg_non_explicit_energy")) \
        .orderBy(F.col("avg_explicit_energy").desc())

    q2_explicit_energy_genres.show(20, truncate=False)
    q2_explicit_energy_genres.explain()
    save_result(q2_explicit_energy_genres, "q2_explicit_energy_comparison")


    print("\nПитання 3: Найдовший акустичний трек у кожній тональності")

    df_acoustic = df.filter(F.col("Acousticness") > 80) \
        .withColumn("Length", F.col("Length").cast("int"))

    window_key = Window.partitionBy("Key").orderBy(F.col("Length").desc())

    q3_longest_acoustic_by_key = df_acoustic.withColumn("rank_in_key", F.row_number().over(window_key)) \
        .filter(F.col("rank_in_key") == 1) \
        .select(
            "Key",
            "song",
            "Length",
            "Acousticness",
            "rank_in_key"
        )

    q3_longest_acoustic_by_key.show(20, truncate=False)
    q3_longest_acoustic_by_key.explain()
    save_result(q3_longest_acoustic_by_key, "q3_longest_acoustic_per_key")

    print("\nПитання 4: Топ-3 емоції за середнім показником Liveness для кожного музичного розміру серед акустичних пісень")

    df_acoustic_for_liveness = df.filter(F.col("Acousticness") > 80)

    grouped_liveness = df_acoustic_for_liveness.groupBy("Time signature", "emotion").agg(F.avg("Liveness").alias("avg_liveness"))

    window_time_signature = Window.partitionBy("Time signature").orderBy(F.col("avg_liveness").desc())

    q4_top_emotions_by_liveness = grouped_liveness.withColumn("rank_in_time_signature", F.row_number().over(window_time_signature)) \
        .filter(F.col("rank_in_time_signature") <= 3) \
        .orderBy("Time signature", "rank_in_time_signature")

    q4_top_emotions_by_liveness.show(20, truncate=False)
    q4_top_emotions_by_liveness.explain()
    save_result(q4_top_emotions_by_liveness, "q4_top_emotions_liveness")


    print("\nПитання 5: Жанри, які найкраще підходять для тренувальних плейлистів")

    q5_workout_genres = df.filter(F.col("Energy") > 70) \
        .filter(F.col("Danceability") > 60) \
        .filter(F.col("Tempo") > 120) \
        .groupBy("Genre") \
        .agg(
            F.count("*").alias("tracks_count"),
            F.avg("Energy").alias("avg_energy"),
            F.avg("Danceability").alias("avg_danceability"),
            F.avg("Tempo").alias("avg_tempo")
        ) \
        .orderBy(
            F.col("tracks_count").desc(),
            F.col("avg_energy").desc()
        )

    q5_workout_genres.show(20, truncate=False)
    q5_workout_genres.explain()
    save_result(q5_workout_genres, "q5_workout_genres")


    print("Питання 6: Еталонні треки для кожної емоції")

    df_emotion_profiles = df.groupBy("emotion").agg(
        F.avg("Energy").alias("avg_energy"),
        F.avg("Danceability").alias("avg_dance")
    )
    df_q6 = df.join(df_emotion_profiles, on="emotion") \
        .withColumn("deviation",
                    F.abs(F.col("Energy") - F.col("avg_energy")) + F.abs(F.col("Danceability") - F.col("avg_dance")))

    window_spec = Window.partitionBy("emotion").orderBy(F.col("deviation").asc())
    q6_ideal_emotion_tracks = df_q6.withColumn("rank", F.row_number().over(window_spec)).filter(F.col("rank") <= 5)

    q6_result = q6_ideal_emotion_tracks.select(
        "emotion",
        "song",
        "Genre",
        "Energy",
        "Danceability",
        F.round("avg_energy", 2).alias("avg_emotion_energy"),
        F.round("avg_dance", 2).alias("avg_emotion_danceability"),
        F.round("deviation", 4).alias("deviation"),
        "rank"
    )

    q6_result.show(20, truncate=False)
    q6_result.explain()
    save_result(q6_result, "q6_ideal_emotion_tracks")

    return {
        "q1_top_popular_songs_by_emotion": q1_top_popular_songs_by_emotion,
        "q2_explicit_energy_genres": q2_explicit_energy_genres,
        "q3_longest_acoustic_by_key": q3_longest_acoustic_by_key,
        "q4_top_emotions_by_liveness": q4_top_emotions_by_liveness,
        "q5_workout_genres": q5_workout_genres,
        "q6_ideal_emotion_tracks": q6_ideal_emotion_tracks,
    }