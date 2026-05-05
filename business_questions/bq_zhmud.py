from pyspark.sql import functions as F


# =====================================================
# SAVE RESULTS
# =====================================================
def save_result(df, path):
    df.coalesce(1) \
      .write \
      .mode("overwrite") \
      .option("header", True) \
      .csv(path)


# =====================================================
# Q1: Як рівень енергійності впливає на популярність треку?
# =====================================================
def q1(df):
    data = df.withColumn(
        "energy_level",
        F.when(F.col("energy") < 0.33, "low")
         .when(F.col("energy") < 0.66, "medium")
         .otherwise("high")
    )

    result = data.groupBy("energy_level").agg(
        F.round(F.avg("popularity"), 2).alias("avg_popularity"),
        F.count("*").alias("track_count")
    ).orderBy("energy_level")

    save_result(result, "results/q1_energy_vs_popularity")
    return result


# =====================================================
# Q2: Яка комбінація темпу та танцювальності дає найвищу популярність?
# =====================================================
def q2(df):
    data = df.withColumn(
        "tempo_bucket",
        F.when(F.col("tempo") < 90, "slow")
         .when(F.col("tempo") < 130, "medium")
         .otherwise("fast")
    ).withColumn(
        "dance_bucket",
        F.when(F.col("danceability") < 0.33, "low")
         .when(F.col("danceability") < 0.66, "medium")
         .otherwise("high")
    )

    result = data.groupBy("tempo_bucket", "dance_bucket").agg(
        F.round(F.avg("popularity"), 2).alias("avg_popularity"),
        F.count("*").alias("track_count")
    ).orderBy(F.desc("avg_popularity"))

    save_result(result, "results/q2_tempo_dance_popularity")
    return result


# =====================================================
# Q3: Яка тривалість треків є оптимальною для популярності?
# =====================================================
def q3(df):
    data = df.withColumn(
        "length_bucket",
        F.when(F.col("length") < 180, "short")
         .when(F.col("length") < 300, "medium")
         .otherwise("long")
    )

    result = data.groupBy("length_bucket").agg(
        F.round(F.avg("popularity"), 2).alias("avg_popularity"),
        F.count("*").alias("track_count")
    ).orderBy(F.desc("avg_popularity"))

    save_result(result, "results/q3_length_vs_popularity")
    return result


# =====================================================
# Q4: Який рівень емоційної позитивності найкраще сприймається аудиторією?
# =====================================================
def q4(df):
    data = df.withColumn(
        "positiveness_level",
        F.when(F.col("positiveness") < 0.33, "low")
         .when(F.col("positiveness") < 0.66, "medium")
         .otherwise("high")
    )

    result = data.groupBy("positiveness_level").agg(
        F.round(F.avg("popularity"), 2).alias("avg_popularity"),
        F.count("*").alias("track_count")
    ).orderBy(F.desc("avg_popularity"))

    save_result(result, "results/q4_positiveness_vs_popularity")
    return result


# =====================================================
# Q5: Який сегмент треків має найбільший потенціал хіта?
# =====================================================
def q5(df):
    data = df.withColumn(
        "hit_score",
        F.round(
            F.col("energy") * 0.4 +
            F.col("danceability") * 0.4 +
            F.col("positiveness") * 0.2, 2
        )
    ).withColumn(
        "hit_segment",
        F.when(F.col("hit_score") < 0.33, "low")
         .when(F.col("hit_score") < 0.66, "medium")
         .otherwise("high")
    )

    result = data.groupBy("hit_segment").agg(
        F.round(F.avg("popularity"), 2).alias("avg_popularity"),
        F.count("*").alias("track_count")
    ).orderBy(F.desc("avg_popularity"))

    save_result(result, "results/q5_hit_potential")
    return result


# =====================================================
# Q6: Які жанри мають найбільший потенціал успіху серед малопопулярних треків?
# =====================================================
def q6(df):
    low_pop = df.filter(F.col("popularity") < 40)

    result = low_pop.groupBy("genre").agg(
        F.round(
            F.avg(
                F.col("energy") * 0.4 +
                F.col("danceability") * 0.4 +
                F.col("positiveness") * 0.2
            ), 2
        ).alias("avg_hit_potential"),
        F.count("*").alias("track_count")
    ).filter(F.col("track_count") >= 10) \
     .orderBy(F.desc("avg_hit_potential")) \
     .limit(10)

    save_result(result, "results/q6_hidden_genre_potential")
    return result


# =====================================================
# RUN ALL QUESTIONS + CONSOLE OUTPUT
# =====================================================
def run_business_questions_zhmud(df):
    results = {}

    print("\n================ Q1: Energy vs Popularity ================")
    results["q1"] = q1(df)
    results["q1"].show(truncate=False)

    print("\n================ Q2: Tempo + Danceability ================")
    results["q2"] = q2(df)
    results["q2"].show(truncate=False)

    print("\n================ Q3: Length vs Popularity ================")
    results["q3"] = q3(df)
    results["q3"].show(truncate=False)

    print("\n================ Q4: Positiveness vs Popularity ================")
    results["q4"] = q4(df)
    results["q4"].show(truncate=False)

    print("\n================ Q5: Hit Potential ================")
    results["q5"] = q5(df)
    results["q5"].show(truncate=False)

    print("\n================ Q6: Hidden Genre Potential ================")
    results["q6"] = q6(df)
    results["q6"].show(truncate=False)

    return results