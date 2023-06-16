import streamlit as st

# https://docs.streamlit.io/library/cheatsheet #

import numpy as np
import pandas as pd

# Example

st.markdown("""# This is a header
## This is a sub header
This is text""")

df = pd.DataFrame({
    'first column': list(range(1, 11)),
    'second column': np.arange(10, 101, 10)
})

# this slider allows the user to select a number of lines
# to display in the dataframe
# the selected value is returned by st.slider
line_count = st.slider('Select a line count', 1, 10, 3)

# and used to select the displayed lines
head_df = df.head(line_count)

head_df

##############################

st.markdown(""" <style> .font {

    font-size:20px ; font-weight: bold; font-family: 'Courier'; color: #FF9633;}

    </style> """, unsafe_allow_html=True)

st.markdown('<p class="font">Upload your csv file </p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose your csv file", type=['csv'], key="2", label_visibility='hidden')


if uploaded_file is not None:

    # Validation rule #

    csv_data = pd.read_csv(uploaded_file)

    csv_data
