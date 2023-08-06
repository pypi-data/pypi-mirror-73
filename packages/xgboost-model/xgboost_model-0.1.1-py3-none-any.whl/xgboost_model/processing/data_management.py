import pandas as pd
import joblib

from xgboost_model.config import config
from xgboost_model import __version__ as _version


def load_dataset(file_name):
    df = pd.read_csv(f"{config.DATASET_DIR}/{file_name}")
    return df


def save_pipeline(pipeline):
    save_file_name = f"{config.PIPELINE_SAVE_FILE}{_version}.pkl"
    save_path = config.TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=save_file_name)
    joblib.dump(pipeline, save_path)


def load_pipeline(file_name):
    """Load a persisted pipeline."""

    file_path = config.TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_pipelines(files_to_keep):
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """

    for model_file in config.TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in [files_to_keep, "__init__.py"]:
            model_file.unlink()
