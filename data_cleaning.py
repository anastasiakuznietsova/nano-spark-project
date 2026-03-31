from pyspark.sql import DataFrame
from pyspark.sql.functions import col, trim, lower, when, sum as spark_sum


def clean_music_data(df: DataFrame) -> DataFrame:
    text_cols = ["Artist(s)", "song", "text", "emotion"]
    existing_text_cols = [c for c in text_cols if c in df.columns]

    print("\n========== DATA CLEANING ==========")

    total_rows_before = df.count()
    unique_rows_before = df.dropDuplicates().count()
    duplicate_rows_before = total_rows_before - unique_rows_before

    null_exprs = [
        spark_sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
        for c in df.columns
    ]
    null_counts = df.select(*null_exprs).first().asDict()

    if existing_text_cols:
        empty_exprs = [
            spark_sum(
                when(col(c).isNotNull() & (trim(col(c)) == ""), 1).otherwise(0)
            ).alias(c)
            for c in existing_text_cols
        ]
        empty_counts = df.select(*empty_exprs).first().asDict()
    else:
        empty_counts = {}

    print(f"Rows total before cleaning     : {total_rows_before}")
    print(f"Duplicate rows before cleaning : {duplicate_rows_before}")

    print("\nNULL VALUES")
    for k, v in sorted(null_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{k:<25} {v}")

    print("\nEMPTY STRINGS")
    for k, v in empty_counts.items():
        print(f"{k:<25} {v}")

    love_fixed = 0
    angry_fixed = 0
    true_rows = 0
    bad_class_rows = 0

    if "emotion" in df.columns:
        love_fixed = df.filter(trim(col("emotion")) == "Love").count()
        angry_fixed = df.filter(lower(trim(col("emotion"))) == "angry").count()
        true_rows = df.filter(lower(trim(col("emotion"))) == "true").count()

        emotions_to_keep = ["sadness", "joy", "love", "surprise", "anger", "fear"]

        bad_class_rows = (
            df.withColumn("emotion_tmp", lower(trim(col("emotion"))))
            .withColumn(
                "emotion_tmp",
                when(col("emotion_tmp") == "angry", "anger")
                .otherwise(col("emotion_tmp"))
            )
            .filter(
                col("emotion_tmp").isNotNull()
                & (col("emotion_tmp") != "true")
                & (~col("emotion_tmp").isin(emotions_to_keep))
            )
            .count()
        )

        print("\nEMOTION ISSUES BEFORE CLEANING")
        print(f"{'Love -> love':<25} {love_fixed}")
        print(f"{'angry -> anger':<25} {angry_fixed}")
        print(f"{'emotion = true':<25} {true_rows}")
        print(f"{'bad emotion classes':<25} {bad_class_rows}")

    for c in existing_text_cols:
        df = df.withColumn(c, trim(col(c)))

    rows_before_dedup = df.count()
    df = df.dropDuplicates()
    rows_after_dedup = df.count()
    removed_duplicates = rows_before_dedup - rows_after_dedup

    print("\nDUPLICATES REMOVAL")
    print(f"Rows before dropDuplicates()   : {rows_before_dedup}")
    print(f"Rows after dropDuplicates()    : {rows_after_dedup}")
    print(f"Duplicates removed             : {removed_duplicates}")

    removed_true = 0
    removed_bad_classes = 0

    if "emotion" in df.columns:
        df = df.withColumn("emotion", trim(col("emotion")))
        df = df.withColumn("emotion", lower(col("emotion")))
        df = df.withColumn(
            "emotion",
            when(col("emotion") == "angry", "anger")
            .when(col("emotion") == "love", "love")
            .otherwise(col("emotion"))
        )

        removed_true = df.filter(col("emotion") == "true").count()

        emotions_to_keep = ["sadness", "joy", "love", "surprise", "anger", "fear"]

        removed_bad_classes = df.filter(
            col("emotion").isNotNull()
            & (col("emotion") != "true")
            & (~col("emotion").isin(emotions_to_keep))
        ).count()

        df = df.filter(col("emotion") != "true")
        df = df.filter(col("emotion").isin(emotions_to_keep))

        print("\nREMOVED ROWS")
        print(f"{'Removed true rows':<25} {removed_true}")
        print(f"{'Removed bad classes':<25} {removed_bad_classes}")

    total_rows_after = df.count()
    unique_rows_after = df.dropDuplicates().count()
    duplicate_rows_after = total_rows_after - unique_rows_after

    print("\nFINAL DATASET INFO")
    print(f"Rows total after cleaning      : {total_rows_after}")
    print(f"Duplicate rows after cleaning  : {duplicate_rows_after}")
    print(f"Total removed rows             : {total_rows_before - total_rows_after}")

    if "emotion" in df.columns:
        print("\nEmotion distribution:")
        emotion_counts = df.groupBy("emotion").count().orderBy(col("count").desc())
        emotion_counts.show(truncate=False)

    return df