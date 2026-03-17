from schemas import get_data_schema
from load_data import extract_music_data
from validation_service import run_validation


def load_and_validate_music_data(spark, file_path: str):
    try:
        schema = get_data_schema()
        df = extract_music_data(spark, file_path, schema)
        run_validation(df)
        return df

    except Exception as e:
        raise RuntimeError(f"Failed to load and validate music data: {e}")