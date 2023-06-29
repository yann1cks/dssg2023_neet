import streamlit as st
import utils as ut
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="NEET Risk Dashboard", 
    page_icon="🔮", 
)

def main():
    '''Renders the contents of the streamlit page.'''

    # Add global styles and load state
    ut.add_custom_css()
    ut.initalize_global_state()


    st.title("Welcome to the Risko of NEET dashboard 👋", anchor=False)

    """
    This dashboard allows you to:
    * View descriptive statistics about NEET youth.
    * Analyse the NEET risk of individual youth and their risk factors.
    * Upload new data to enhance the model.
    * Get a spreadsheet with risk predication for every youth.
    """

# Run the Streamlit app
if __name__ == "__main__":
    main()


