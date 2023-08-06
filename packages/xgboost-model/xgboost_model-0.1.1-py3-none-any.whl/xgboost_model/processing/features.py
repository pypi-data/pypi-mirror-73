from sklearn.base import BaseEstimator, TransformerMixin


class CreateTypeVar(BaseEstimator, TransformerMixin):
    def fit(self, X, y):
        """Fit statement to accomodate the sklearn pipeline."""
        return self

    def transform(self, df):
        df = df.copy()

        df['type'] = 'Other'
        df.loc[df['title'] == 'Apartment for sale', 'type'] = 'Apartment'
        df.loc[df['title'] == 'House for sale', 'type'] = 'House'
        df.loc[df['title'] == 'Condo for sale', 'type'] = 'Condo'
        df.loc[df['title'] == 'Townhouse for sale', 'type'] = 'Townhouse'

        return df


class CreateAdditionalVars(BaseEstimator, TransformerMixin):
    def fit(self, X, y):
        """Fit statement to accomodate the sklearn pipeline."""
        return self

    def transform(self, df):
        df = df.copy()

        df['bed_count'] = df['facts and features'].str.split(',', expand=True)[0].str.replace(r'[^0-9^.]', '')
        df['bath_count'] = df['facts and features'].str.split(',', expand=True)[1].str.replace(r'[^0-9^.]', '')
        df['sqft'] = df['facts and features'].str.split(',', expand=True)[2].str.replace(r'[^0-9^.]', '')

        df.loc[df['bed_count'] == '', 'bed_count'] = None
        df.loc[df['bath_count'] == '', 'bath_count'] = None
        df.loc[df['sqft'] == '', 'sqft'] = None

        df['bed_count'] = df['bed_count'].astype(float)
        df['bath_count'] = df['bath_count'].astype(float)
        df['sqft'] = df['sqft'].astype(float)

        return df
