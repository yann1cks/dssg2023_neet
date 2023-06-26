import streamlit as st
import utils as ut

st.set_page_config(
    page_title="Indivdiual Students", 
    page_icon="🔮"
)

names = ("Select", "test", "test")
upns =  ut.get_list_of_upns()



def main():

    # Add global styles
    ut.add_custom_css()


    st.title("Information about individual students")
    st.markdown("Please select one student based on the filters below.")

    col1, col2 = st.columns(2)

    with col1:
        selected = st.selectbox("Select by Name", options=names, index=0)

    with col2:
        selected = st.selectbox("Select by ID", options=upns, index=0)

    st.write('You selected:', selected)

# Run the Streamlit app
if __name__ == '__main__':
    main()

