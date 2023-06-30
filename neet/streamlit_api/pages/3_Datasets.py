from pathlib import Path
from typing import Literal, BinaryIO
import pandas as pd
import streamlit as st
import utils as ut

st.set_page_config(
    page_title="Upload Data",
    page_icon="🔮",
)

# Define a streamlit folder
STREAMLIT_FOLDER = Path("neet/streamlit_api/")

# Define dict that contains every dataset as key-value-pairs. (Cannot be used for Literals.)
DATASET_TYPES = {
    "attendance": "Attendance",
    "ks2": "KS2",
    "ks4": "KS4",
    "nccis": "NCCIS",
    "census": "School Census",
}


def render_file_upload_form() -> None:
    """
    Render the file upload form and contains nested functions for valdiation.
    """

    # Can I use theses somehow for the options as well?
    possible_response_types = Literal["success", "error"]
    possible_dataset_types = Literal["attendance", "nccis", "ks2", "ks4", "census"]

    def set_form_response_state(
        response_type: possible_response_types,
        message: str = "An unexpected error occured",
    ) -> None:
        """
        Sets a "form_response" session state based on the passed values. To be used with validation.
        The response type is either "success" or "error".

        Args:
            response_type: Either "success" or "error.
            message: A message that is shown for the selected response type.
        Returns:
            None
        """
        response = {
            "type": response_type,
            "message": message,
        }

        if "form_response" not in st.session_state:
            st.session_state.form_response = response

    def validate_form_submission(
        dataset_type: possible_dataset_types, year: str, file: BinaryIO
    ) -> bool:
        """
        Validate if all fields are filed and if the file was updated. Also sets an error message

        Args:
            dataset_type: The type of the dataset, e. g. NCCIS
            year: Year of the dataset
            file: Uploaded csv file. Uses streamlits UploadedFile object.
        Returns:
            bool: The return value. True if is submission is valid. False otherwise.

        TODO: I also have the check if the file was already uploaded.
        """

        # Get already uploaded forms from state
        # data_raw = st.session_state.data_raw

        if None not in (dataset_type, year, file) and "Select" not in (year, file):
            return True
        else:
            set_form_response_state(
                "error", "An error occurred. Please fill all fields and try again."
            )
            return False

    def validate_file_content(df: pd.DataFrame) -> bool:
        """
        Validates the file content of an uploaded .csv file

        Args:
            df: Pandas dataframe of the file content.
        Returns:
            bool: The return value. True for success, False otherwise.

        TODO: Use pandas schema valdiation.
        """

        if "upn" not in df.columns:
            set_form_response_state(
                "error", "The columns are incorrect for this dataset."
            )
            return

        return True

    def save_uploaded_file(
        dataset_type: possible_dataset_types,
        year: str,
        file: BinaryIO,
    ) -> None:
        """
        Saves the uploaded file to disk.
        The streamlit UploadedFile argument is passed to save am addtional pd.to_csv

        Args:
            dataset_type: The type of the dataset, e. g. NCCIS
            year: Year of the dataset
            file: Uploaded csv file. Uses streamlits UploadedFile object.
            df: Pandas dataframe of the file content.

        TODO: Update the filename based on the metadata. Do not allow overwriting.
        """
        file_name = ut.get_file_name(dataset_type, year)
        fullpath = STREAMLIT_FOLDER / "uploads" / file_name

        with open(fullpath, "wb") as f:
            f.write(file.getbuffer())

    def process_file_upload() -> None:
        """
        Wrapper function for the different steps of processing a form submission.
        """

        # Reset the form error state
        if "form_response" in st.session_state:
            del st.session_state.form_response

        # Set session state as variables
        year = st.session_state.form_year
        dataset_type = st.session_state.form_dataset_type
        file = st.session_state.form_file

        # Validate the form submission.
        if not validate_form_submission(dataset_type, year, file):
            return

        # Read csv and valid the content.
        df = pd.read_csv(st.session_state.form_file)

        if not validate_file_content(df):
            return

        # Save the uploaded files to disk and set the state.
        save_uploaded_file(dataset_type, year, file)
        ut.add_uploaded_file_to_state(dataset_type, year, df)

        # Lets rename add the information to the global state, rename it and save the file
        set_form_response_state("success", "The upload of XYZ was successfull.")

    # Create variables for form responses in state
    options_datasets = list(DATASET_TYPES.keys())
    options_years = [
        "2023",
        "2022",
        "2021",
        "2020",
        "2019",
        "2018",
        "2017",
        "2016",
        "2015",
    ]

    with st.form(key="file_upload", clear_on_submit=True):
        st.header("Upload datasets")
        st.markdown(
            "You can upload one dataset for each year. The datasets must conform with the requiered schema."
        )

        # Slighty more complicated to return key from DATASET_TYPES not the values
        st.selectbox(
            "Dataset Type",
            key="form_dataset_type",
            options=["Select"] + options_datasets,
            format_func=lambda x: "Select" if x == "Select" else DATASET_TYPES[x],
            index=0,
        )

        st.selectbox(
            "Year",
            key="form_year",
            options=["Select"] + options_years,
            index=0,
        )

        st.file_uploader(
            "Upload Attendance data",
            key="form_file",
            accept_multiple_files=False,
            help="Please upload on file per year.",
            type="csv",
        )

        st.form_submit_button(
            "Upload File",
            on_click=process_file_upload,
            type="primary",
            use_container_width=True,
        )

        if "form_response" in st.session_state:
            response = st.session_state.form_response

            if response["type"] == "error":
                st.error(response["message"], icon="🚨")
            elif response["type"] == "success":
                st.success(response["message"], icon="✅")


def render_list_of_files() -> None:
    """
    Renders a list of files that were uploaded and are available in the state 'data_raw'
    """

    def remove_uploaded_file(file_info: dict) -> None:
        """
        Removes a file form the filesystem and the state.
        Assumes that the file names match the onces created on upload and no
        duplicates exist. Does not check for the existence of a file.

        Args:
            file_info: Dictionary with year, dataset_type and pandas dataframe.
        """

        dataset_type = file_info["dataset_type"]
        year = file_info["year"]

        ## Remove from disk by rebulding the filename form file_info
        file_name = ut.get_file_name(dataset_type, year)
        file_path = STREAMLIT_FOLDER / "uploads" / file_name
        file_path.unlink()

        ## Remove from state
        data_raw = st.session_state.data_raw

        for item in data_raw.copy():
            if item.get("year") == year and item.get("dataset_type") == dataset_type:
                data_raw.remove(item)
                break

        st.session_state.data_raw = data_raw

    if not st.session_state.data_raw:
        st.warning("Please upload files.")
        return

    for type in DATASET_TYPES:
        files = list(
            filter(lambda d: d["dataset_type"] in [type], st.session_state.data_raw)
        )

        # Bail early if no files are available
        if not files:
            continue

        # Print a heading for each dataset type
        st.subheader(DATASET_TYPES[type], anchor=False)

        for f in files:
            title = DATASET_TYPES[f["dataset_type"]] + " " + f["year"]

            with st.expander(title):
                # st.dataframe(
                #    f["data"],
                #    use_container_width=True,
                #    hide_index=True,
                # )
                st.button(
                    "Remove file",
                    key=title,
                    help="You cannot undo this action!",
                    on_click=remove_uploaded_file,
                    args=(f,),
                )


# Main Streamlit app
def main():
    """Renders the contents of the streamlit page."""

    # Add global styles and load state
    ut.add_custom_css()
    ut.initalize_global_state()

    st.title("Datasets", anchor=False)

    render_file_upload_form()

    st.header("Uploaded files")
    st.markdown(
        "Add explanation. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo."
    )
    render_list_of_files()

    st.button("Process data & calculate risk", type="primary", on_click=ut.run_pipeline)

    # TODO:If the final dataset is saved to disk we have to review this.
    st.download_button(
        label="Download processed data",
        data=st.session_state.data_final_csv,
        file_name="NEET_Rist_Predictions.csv",
        mime="text/csv",
    )

    st.header("About the data schemas")

    with st.expander("CCIS"):
        st.markdown(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )
    with st.expander("School Census"):
        st.markdown(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )
    with st.expander("Attainment (KS2 and KS4)"):
        st.markdown(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )
    with st.expander("Attendance"):
        st.markdown(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )


# Run the Streamlit app
if __name__ == "__main__":
    main()
