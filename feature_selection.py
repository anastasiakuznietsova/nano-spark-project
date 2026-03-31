from pyspark.sql import DataFrame

def select_and_split_data(df: DataFrame, seed: int = 42):
    cols = ['emotion', 'text', 'Explicit', 'Length', 'Genre', 'Key', 'Tempo',
            'Loudness (db)', 'Time signature', 'Energy', 'Danceability',
            'Positiveness', 'Speechiness', 'Liveness', 'Acousticness', 'Instrumentalness']

    df_selected = df.select(*cols)

    train_df, val_df, test_df = df_selected.randomSplit([0.7, 0.15, 0.15], seed=seed)

    num_cols = len(train_df.columns)
    print(f"Train shape: ({train_df.count()}, {num_cols})")
    print(f"Validation shape: ({val_df.count()}, {num_cols})")
    print(f"Test shape: ({test_df.count()}, {num_cols})")

    return train_df, val_df, test_df
