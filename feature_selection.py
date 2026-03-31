from pyspark.sql import DataFrame

def select_columns(df: DataFrame):
    cols = ['emotion', 'text', 'Explicit', 'Length', 'Genre', 'Key', 'Tempo',
            'Loudness (db)', 'Time signature', 'Energy', 'Danceability',
            'Positiveness', 'Speechiness', 'Liveness', 'Acousticness', 'Instrumentalness']

    df_selected = df.select(*cols)

    num_cols = len(df_selected.columns)
    print(f"Dataframe columns: {num_cols}")

    return df_selected

def split_data(df: DataFrame, seed: int = 42):
    train_df, val_df, test_df = df.randomSplit([0.7, 0.15, 0.15], seed=seed)

    num_cols = len(train_df.columns)
    print(f"Train shape: ({train_df.count()}, {num_cols})")
    print(f"Validation shape: ({val_df.count()}, {num_cols})")
    print(f"Test shape: ({test_df.count()}, {num_cols})")

    return train_df, val_df, test_df