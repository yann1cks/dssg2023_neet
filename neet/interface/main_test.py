
import numpy as np
import pandas as pd

# Example - to be changed! #

# from neet.ml_logic.data import clean_data
# from neet.ml_logic.model import initialize_model, compile_model, train_model, evaluate_model
# from neet.ml_logic.params import DATASET_SIZE, VALIDATION_DATASET_SIZE
# from neet.ml_logic.preprocessor import preprocess_features
# from neet.ml_logic.utils import get_dataset_timestamp
# from neet.ml_logic.registry import get_model_version, load_model, save_model


def preprocess(source_type = 'train'):
    """
    Preprocess the dataset (fitting in memory)
    parameters:
    - source_type: 'train' or 'val'
    """

    # Here our code -- to be done! #

    return None

def train():
    """
    Train a new model on the full (already pre-processed) dataset

    """

    model = None
    model = load_model()  # production model

    # Model params
    # to be defined here

    return # here some metric


def evaluate():
    """
    Evaluate the performance of the latest production model on new data

    """

    return # here some metric


def pred(X_pred: pd.DataFrame = None) -> np.ndarray:
    """
    Make a prediction using the latest trained model

    """

    # Here our code #

    return # y_pred

def package_name():
    print("The package name is neet!")



if __name__ == '__main__':
    # preprocess(source_type='train')
    # preprocess(source_type='val')
    # train()
    # pred()
    # evaluate()
    package_name() # just a working example!
