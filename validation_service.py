from pyspark.sql import functions as F

def run_validation(df):
    print("\n" + "=" * 50)
    print("STARTING DATA VALIDATION PROCESS")
    print("=" * 50)

    # 1. Перевірка кількості записів (Integrity Check)
    total_count = df.count()
    print(f"[CHECK 1] Загальна кількість записів: {total_count}")
    if total_count == 0:
        print("!!! WARNING: Датасет порожній!")
        return

    # 2. Перевірка на критичні NULL значення (Accuracy Check)
    # Перевіряємо колонки Artist(s) та song, бо без них запис не має сенсу
    critical_cols = ["Artist(s)", "song"]
    for col_name in critical_cols:
        null_count = df.filter(df[col_name].isNull() | (F.col(col_name) == "")).count()
        print(f"[CHECK 2] Порожні значення в '{col_name}': {null_count}")
        if null_count > 0:
            print(f"   -> Потрібна очистка: {null_count} рядків мають дефекти.")

    # 3. Валідація діапазонів (Range Check)
    # Наприклад, популярність та енергія мають бути в межах 0-100
    print("[CHECK 3] Перевірка діапазонів числових значень:")
    stats = df.select(
        F.min("Popularity").alias("min_pop"),
        F.max("Popularity").alias("max_pop"),
        F.min("Energy").alias("min_energy"),
        F.max("Energy").alias("max_energy")
    ).collect()[0]

    print(f"   -> Popularity: від {stats['min_pop']} до {stats['max_pop']}")
    print(f"   -> Energy: від {stats['min_energy']} до {stats['max_energy']}")

    # 4. Перевірка схеми (Schema Verification)
    print("[CHECK 4] Структура даних:")
    df.printSchema()

    print("=" * 50)
    print("VALIDATION COMPLETED")
    print("=" * 50 + "\n")


