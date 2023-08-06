from sklearn.model_selection import train_test_split

from xgboost_model.config import config
from xgboost_model.processing.data_management import load_dataset, save_pipeline
from xgboost_model.processing.preprocessing import DropNas
from xgboost_model import pipeline


def run_training():

    df = load_dataset(file_name=config.TRAINING_DATA_FILE)
    drop_nas = DropNas()
    df = drop_nas.transform(df)

    X_train, X_test, y_train, y_test = train_test_split(df
                                                    , df[config.target]
                                                    , test_size=config.test_size
                                                    , random_state=config.random_state)

    pipeline.price_pipe.fit(X_train, y_train)
    save_pipeline(pipeline=pipeline.price_pipe)


if __name__ == "__main__":
    model = run_training()
