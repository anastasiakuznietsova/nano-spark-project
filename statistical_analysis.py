import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, DoubleType

def perform_statistical_analysis(df):
    print("--- Статистичний аналіз ---")

    print("--- Загальна інформація про набір даних ---")
    print(f"Кількість записів: {df.count()}")
    print(f"Кількість колонок: {len(df.columns)}")

    df.show(5)

    before = df.count()
    df = df.dropDuplicates()
    after = df.count()

    print(f"Було виявлено стільки дублікатів: {before - after}")

    cat_cols = ['Explicit', 'Genre', 'Key', 'Time signature']
    unique_counts = df.select([F.countDistinct(c).alias(c) for c in cat_cols])
    print("Кількість унікальних значень у категоріальних колонках:")
    unique_counts.show()

    df = df.withColumn("emotion", F.when(F.col("emotion") == "Love", "love").otherwise(F.col("emotion")))
    emotions_to_keep = ['sadness', 'joy', 'love', 'surprise', 'anger', 'fear']
    df = df.filter(F.col("emotion").isin(emotions_to_keep))

    df = df.withColumn("Loudness (db)", F.regexp_replace(F.col("Loudness (db)"), "db", "").cast(DoubleType()))
    df = df.withColumn("Length_Split", F.split(F.col("Length"), ":"))
    df = df.withColumn("Length",
        (F.col("Length_Split").getItem(0).cast(IntegerType()) * 60) +
        (F.col("Length_Split").getItem(1).cast(IntegerType()))
    ).drop("Length_Split")

    print("--- Статистика числових ознак ---")

    num_cols = ['Length', 'Tempo', 'Loudness (db)', 'Energy', 'Danceability', 'Positiveness', 'Speechiness', 'Liveness',
        'Acousticness', 'Instrumentalness', 'Similarity Score 1', 'Similarity Score 2', 'Similarity Score 3']
    df.select(num_cols).describe().show()

    print("--- Візуалізація ---")
    pdf = df.toPandas()
    sns.set_theme(style="whitegrid")


    print("--- Візуалізація категоріальних ознак ---")
    cat_cols = ['Explicit', 'Key', 'Time signature']
    for col in cat_cols:
        plt.figure(figsize=(12, 6))
        order = pdf[col].value_counts().index
        ax = sns.countplot(x=col, data=pdf, palette='magma', order=order)

        for container in ax.containers:
            ax.bar_label(container, fmt='%d', padding=3)

        plt.title(f'Розподіл за категорією: {col}')
        plt.xlabel(col)
        plt.ylabel('Кількість пісень')

        if len(order) > 5:
            plt.xticks(rotation=45)

        plt.show()

    print("--- Виведено графіки для категоріальних ознак ---")

    for col in ['Tempo', 'Loudness (db)', 'Energy', 'Length', 'Danceability', 'Positiveness', 'Speechiness', 'Liveness', 'Acousticness', 'Instrumentalness',  'Similarity Score 1', 'Similarity Score 2', 'Similarity Score 3']:
        fig, axes = plt.subplots(1, 2, figsize=(15, 4))
        sns.histplot(pdf[col], bins=30, kde=True, ax=axes[0], color='skyblue')
        sns.boxplot(x=pdf[col], ax=axes[1], color='lightgreen')
        plt.suptitle(f'Аналіз розподілу для {col}')
        plt.show()

    print("--- Виведено гістограми та боксплоти ---")


    plt.figure(figsize=(12, 8))
    correlation_matrix = pdf[num_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Кореляція числових ознак')
    plt.show()

    print("--- Виведено кореляційну матрицю ---")


    plt.figure(figsize=(10, 5))
    ax = sns.countplot(x='emotion', data=pdf, palette='viridis')
    for container in ax.containers:
        ax.bar_label(container)
    plt.title('Кількість пісень за емоціями')
    plt.show()

    print("--- Виведено графік розподілу пісень за емоціями ---")


    pdf_subset = pdf.sample(n=20000, random_state=42) if len(pdf) > 50000 else pdf
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Tempo', y='Loudness (db)', hue='emotion', data=pdf_subset, alpha=0.5, edgecolor=None, s=10)
    plt.title('Темп vs Гучність')
    plt.xlabel('Темп')
    plt.ylabel('Гучність (дб)')
    plt.show()

    print("--- Виведено графік Темп vs Гучність ---")


    plt.figure(figsize=(10, 6))
    emotion_means = pdf.groupby('emotion')[['Danceability', 'Popularity']].mean()
    sns.heatmap(emotion_means, annot=True, cmap='mako')
    plt.title('Середні характеристики для кожної емоції')
    plt.show()

    print("--- Виведено графік середніх характеристики для кожної емоції ---")


    energy_data = df.groupBy("emotion").agg(F.avg("Energy").alias("Average_Energy")).toPandas()
    order = ['sadness', 'joy', 'love', 'surprise', 'anger', 'fear']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='emotion',y='Average_Energy',data=energy_data,order=order,palette='coolwarm')
    plt.title('Середній рівень енергійності для кожної емоції')
    plt.xlabel('Емоція')
    plt.ylabel('Energy')
    plt.xticks(rotation=45)
    plt.show()

    print("--- Виведено графік середнього рівня енергійності для кожної емоції ---")

    heatmap_data = df.groupBy("emotion").agg(F.avg("Tempo").alias("Tempo"),F.avg("Loudness (db)").alias("Loudness (db)")).toPandas()
    heatmap_data = heatmap_data.set_index('emotion')

    plt.figure(figsize=(8, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap='coolwarm', cbar=True )
    plt.title('Середні значення Темпу та Гучності для кожної емоції')
    plt.ylabel('emotion')
    plt.show()

    print("--- Виведено графік середніх значень Темпу та Гучності для кожної емоції ---")

