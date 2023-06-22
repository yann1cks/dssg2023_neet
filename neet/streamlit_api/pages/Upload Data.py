import streamlit as st
import utils as ut

import pandas as pd

st.set_page_config(
    page_title="Upload Data",
    page_icon="📈",
)


# Main Streamlit app
def main():
    
    # Add global styles
    ut.add_global_styles()

    # Initialize the session state if it doesn't exist
    if 'data' not in st.session_state:
        st.session_state.data = []
    
    st.header("This is where you upload")
    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Read the uploaded CSV file
            data = pd.read_csv(uploaded_file)
            
            # Display the uploaded data
            st.subheader("Uploaded Data")
            st.write(data)
            
            # Append the new data to the existing data
            st.session_state.data.append(data)

# Run the Streamlit app
if __name__ == '__main__':
    main()

