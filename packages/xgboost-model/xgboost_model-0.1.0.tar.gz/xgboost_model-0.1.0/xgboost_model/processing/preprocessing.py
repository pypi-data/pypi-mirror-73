from xgboost_model.config import config

from sklearn.base import BaseEstimator, TransformerMixin


class DropNas(BaseEstimator, TransformerMixin):
    def fit(self, X, y):
        """Fit statement to accomodate the sklearn pipeline."""
        return self

    def transform(self, df):
        df = df.copy()
        df.dropna(subset=['price'], inplace=True)
        df[config.target] = df.price.str.replace(r'\D+', '').astype(int)
        return df


class RenameCols(BaseEstimator, TransformerMixin):
    def fit(self, X, y):
        """Fit statement to accomodate the sklearn pipeline."""
        return self

    def transform(self, df):
        df = df.copy()
        df.rename(columns=config.var_rename_dict, inplace=True)
        return df


class LabelEncoding(BaseEstimator, TransformerMixin):

    def fit(self, X, y):
        """Fit statement to accomodate the sklearn pipeline."""
        return self

    def transform(self, df):
        df = df.copy()

        df[config.categorical_vars] = df[config.categorical_vars].astype('category')
        for var in config.categorical_vars:
            df[var] = df[var].cat.codes

        return df


class KeepFeatures(BaseEstimator, TransformerMixin):

    def fit(self, X, y):
        """Fit statement to accomodate the sklearn pipeline."""
        return self

    def transform(self, df):
        df = df.copy()
        df = df[config.KEEP_FEATURES]
        return df
