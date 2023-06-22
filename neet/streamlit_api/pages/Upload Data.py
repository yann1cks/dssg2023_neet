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
    
    # Check if the file "train_singleUPN.csv" exists
    if 'train_singleUPN.csv' not in st.session_state:
        # Read the CSV file
        data = pd.read_csv('train_singleUPN.csv')
        
        # Display the data from the file
        st.subheader("Existing Data")
        st.write(data)
        
        # Append the data to the session state
        st.session_state.data.append(data)
        
        # Save the file reference in session state
        st.session_state['train_singleUPN.csv'] = True
    else:
        # If the file already exists, directly use the data
        data = pd.read_csv('train_singleUPN.csv')
        
        # Display the existing data
        st.subheader("Existing Data")
        st.write(data)
        
        # Append the existing data to the session state
        st.session_state.data.append(data)


# Run the Streamlit app
if __name__ == '__main__':
    main()
