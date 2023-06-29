from pathlib import Path
from typing import Literal, BinaryIO
import pandas as pd
import streamlit as st


# Define a streamlit folder
STREAMLIT_FOLDER = Path("neet/streamlit_api/")


def add_custom_css() -> None:
    """Outputs styling from CSS file on every page, e.g. to remove the "Made with Streamlit" message."""

    path = STREAMLIT_FOLDER / "style.css"

    with open(path, "r") as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


def add_uploaded_file_to_state(
    dataset_type,
    year: str,
    df: pd.DataFrame,
) -> None:
    """
    Adds a file to the global "data_raw" state.

    Args:
        dataset_type: The type of the dataset, e. g. NCCIS
        year: Year of the dataset
        df: Pandas dataframe of the file content.

    TODO: Update the filename based on the metadata. Do not allow overwriting.
    """

    file_info = {
        "dataset_type": dataset_type,
        "year": year,
        "data": df,
    }

    # Add the uploaded file to the raw data state with relevant information
    st.session_state.data_raw.append(file_info)

def get_file_name(dataset_type, year) -> str:
    """
    Creates the filename.
    Moved to a function in case we have adapt the naming.

    Args:
        dataset_type: The type of the dataset, e. g. NCCIS
        year: Year of the dataset
    Return:
        filename: String of the filename
    """
    return dataset_type + "_" + year + ".csv"

def initalize_global_state() -> None:
    """
    Loads data from disk into the state

    TODO: Saved to disk files need to be loaded into the state as well.
    """

    # Load and initalize raw data
    # Initialize "data" as an empty set if it does not exists already.
    if "data_raw" not in st.session_state:
        # We always have to initalize the state.
        st.session_state.data_raw = []

        path = STREAMLIT_FOLDER / "uploads"

        uploads = path.glob("*.csv")  # get all csvs in your dir.

        for file in uploads:
            file_name = file.stem
            dataset_type, year = file_name.split("_", 1)
            df = pd.read_csv(file, index_col=0)

            add_uploaded_file_to_state(dataset_type, year, df)

    # Initialize final data
    if "data_final" not in st.session_state:
        st.session_state.data_final = pd.read_csv(
            "neet/streamlit_api/train_singleUPN.csv"
        )


def run_pipeline() -> None:
    """
    Simple wrapper function to run our pipeline

    TODO: Add checks if all needed data is available
    """

    st.success("Predictions done")
