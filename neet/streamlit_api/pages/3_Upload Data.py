import streamlit as st
import utils as ut
import pandas as pd

st.set_page_config(
    page_title="Upload Data",
    page_icon="🔮",
)

help_text="Please upload on file per year. The filename must contain the year in digits."

# Now add a submit button to the form:

def render_file_upload_form():

    def set_form_response_state (response_type: str, message='An unexpected error occured') -> None:
        '''
        Sets a "form_response" session state based on the passed values. To be used with validation. 
        The response type is either "success" or "error".
        '''
        dict = {
            "type": response_type,
            "message": message,
        }

        if 'form_response' not in st.session_state:
            st.session_state.form_response = dict
    
    def process_file_upload() -> None:
        '''
        Wrapper function form the different steps of processing a form submission.
        '''
        dataset_type = st.session_state.form_dataset_type
        year = st.session_state.form_year
        file = st.session_state.form_file
        
        # Simple check for column existance
        if dataset_type and year and file:

            set_form_response_state("success", "Test message")
            
            df = pd.read_csv(file)

            if 'UPN' in df.columns:
                st.write("SUCCESS")
            else:
                st.write("DAMN")

        else:
            set_form_response_state("error", "An error occurred. Please fill all fields and try again.")




    options_datasets = ["Select", "Attendance", "KS2", "KS4", "NCCIS", "School Census"]
    options_year = ["Select", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"]

    with st.form(key="file_upload", clear_on_submit=True):

        st.selectbox("Dataset Type", key="form_dataset_type", options=options_datasets, index=0, disabled=False)
        st.selectbox("Year", key="form_year", options=options_year, index=0, disabled=False)
        st.file_uploader("Upload Attendance data", key="form_file", accept_multiple_files=False, help=help_text, type="csv")

        st.form_submit_button("Upload File", on_click=process_file_upload, type="primary", use_container_width=True, disabled=False)

        if 'form_response' in st.session_state:
            dict = st.session_state.form_response

            if dict["type"] == "error":
                st.error(dict["message"], icon="🚨")
            elif dict["type"] =="success":
                st.success(dict["message"], icon="✅")

def render_list_of_files():
    if 'file_upload_year' in st.session_state:
        st.write("File uploaded")
        with st.container():
            st.write("Filename")
            st.button('Remove')
    else:
        st.warning("Please upload files.")


# Main Streamlit app
def main():
    
    # Add global styles
    ut.add_custom_css()

    st.title("File Uploads", anchor=False)

    st.markdown("Please upload your datasets. You can upload one dataset for each year. The datasets must conform with the requiered schema.")

    st.header("Upload files")

    render_file_upload_form()

    st.header("Uploaded files")
    st.markdown("Add explanation. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.")
    render_list_of_files()


    with st.expander("Data schema explanations"):
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

# Run the Streamlit app
if __name__ == '__main__':
    main()
