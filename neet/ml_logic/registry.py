# Load and Save model to MLflow Registry #

from neet.ml_logic.params import LOCAL_REGISTRY_PATH

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

import os

def save_model(model: None,
               params: dict = None,
               metrics: dict = None) -> None:

    if os.environ.get("MODEL_TARGET") == "mlflow":

        print("Save model to mlflow..." )

        mlflow_tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
        mlflow_experiment = os.environ.get("MLFLOW_EXPERIMENT")
        mlflow_model_name = os.environ.get("MLFLOW_MODEL_NAME")

        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment(experiment_name=mlflow_experiment)

        with mlflow.start_run():

            if params is not None:
                mlflow.log_params(params)

            if metrics is not None:
                mlflow.log_metrics(metrics)

            if model is not None:

                mlflow.sklearn.log_model(sk_model=model,
                                       artifact_path="model",
                                       registered_model_name=mlflow_model_name)

        print("data saved to mlflow")

        return

def load_model(save_copy_locally=False) :
    """
    load the latest saved model, return None if no model found

    """

    if os.environ.get("MODEL_TARGET") == "mlflow":

        print(" Load model from mlflow...")

        # load model from mlflow
        mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))

        mlflow_model_name = os.environ.get("MLFLOW_MODEL_NAME")

        stage = "Production"

        model_uri = f"models:/{mlflow_model_name}/{stage}"
        print(f"- uri: {model_uri}")

        try:
            model = mlflow.sklearn.load_model(model_uri=model_uri)
            print(" model loaded from mlflow")
        except:
            print(f" no model in stage {stage} on mlflow")
            return None

        return model


def get_model_version(stage="Production"):
    """
    Retrieve the version number of the latest model in the given stage
    - stages: "None", "Production", "Staging", "Archived"

    """

    if os.environ.get("MODEL_TARGET") == "mlflow":

        mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))

        mlflow_model_name = os.environ.get("MLFLOW_MODEL_NAME")

        client = MlflowClient()

        try:
            version = client.get_latest_versions(name=mlflow_model_name, stages=[stage])
        except:
            return None

        # check whether a version of the model exists in the given stage
        if not version:
            return None

        return int(version[0].version)

    # model version not handled

    return None
