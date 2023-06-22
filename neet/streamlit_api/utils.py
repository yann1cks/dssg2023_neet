import streamlit as st


def add_above_navigation():
    st.sidebar.markdown(
        "My Logo (sidebar) should be on top of the Navigation within the sidebar"
    )

def add_global_styles():
    ''' Outputs global CSS styles on every page, e.g. to remove the "Made with Streamlit" message.'''
    st.markdown("""<style>

        footer {visibility: hidden;}

        </style>""", 
        unsafe_allow_html=True) 
