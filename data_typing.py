from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, DoubleType
from pyspark.ml.feature import StandardScaler, VectorAssembler, StringIndexer, OneHotEncoder
from pyspark.ml import Pipeline

def transform_and_scale_data(df):
    df = df.withColumn('Loudness (db)',
                       F.regexp_replace(F.col('Loudness (db)'), '(?i)db', '').cast(DoubleType()))

    time_split = F.split(F.col('Length'), ':')
    df = df.withColumn('Length',
                       (time_split.getItem(0).cast(IntegerType()) * 60) +
                       (time_split.getItem(1).cast(IntegerType())))

    df = df.withColumn('Explicit', F.when(F.col('Explicit') == 'Yes', 1).otherwise(0))

    mapping = {'sadness': 1, 'joy': 2, 'love': 3, 'surprise': 4, 'anger': 5, 'fear': 6}
    mapping_expr = F.create_map([F.lit(x) for x in [val for pair in mapping.items() for val in pair]])
    df = df.withColumn('emotion', mapping_expr.getItem(F.col('emotion')))

    numeric_features = [
        'Length', 'Tempo', 'Loudness (db)', 'Energy', 'Danceability',
        'Positiveness', 'Speechiness', 'Liveness', 'Acousticness', 'Instrumentalness'
    ]
    categorical_columns = ['Genre', 'Key', 'Time signature']

    indexers = [StringIndexer(inputCol=c, outputCol=f"{c}_idx") for c in categorical_columns]
    encoders = [OneHotEncoder(inputCol=f"{c}_idx", outputCol=f"{c}_ohe") for c in categorical_columns]

    assembler = VectorAssembler(inputCols=numeric_features, outputCol="num_features")
    scaler = StandardScaler(inputCol="num_features", outputCol="scaled_features", withStd=True, withMean=True)

    pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler])
    df = pipeline.fit(df).transform(df)

    print(f"\nTransformation complete. Total columns in result: {len(df.columns)}")
    return df
