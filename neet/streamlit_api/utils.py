import streamlit as st
import pandas as pd

def add_custom_css():
    ''' Outputs styling from CSS file on every page, e.g. to remove the "Made with Streamlit" message.'''

    with open('neet/streamlit_api/style.css', "r") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

@st.cache_data
def get_data():
    return pd.read_csv('neet/streamlit_api/train_singleUPN.csv')

@st.cache_data
def get_list_of_upns():

    data = get_data()
    
    return data['upn']

