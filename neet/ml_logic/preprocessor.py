# Data preprocessing pipeline #
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer

from neet.ml_logic.utils import *
from neet.ml_logic.data import clean_data
from neet.ml_logic.feature_transform import (transform_time_features,
                                             transform_XYZ_features)

def preprocess_features(X: pd.DataFrame) -> pd.DataFrame:

    X_cleaned = clean_data(X)
    X_processed = # define pipeline using sklearn.pipeline module #

    return X_processed
