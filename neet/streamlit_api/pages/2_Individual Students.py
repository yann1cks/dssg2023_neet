import streamlit as st
import utils as ut

st.set_page_config(page_title="Indivdiual Students", page_icon="🔮")

names = ("Select", "test", "test")


def main():
    """Renders the contents of the streamlit page."""

    # Add global styles and load state
    ut.add_custom_css()
    ut.initalize_global_state()

    # Get the data from state
    data = st.session_state.data_final
    upns = data["upn"]

    st.title("Information about individual students")
    st.markdown("Please select one student based on the filters below.")

    col1, col2 = st.columns(2)

    with col1:
        selected = st.selectbox("Select by Name", options=names, index=0)

    with col2:
        selected = st.selectbox("Select by ID", options=upns, index=0)

    st.write("You selected:", selected)


# Run the Streamlit app
if __name__ == "__main__":
    main()
