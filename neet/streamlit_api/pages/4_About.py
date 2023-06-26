import streamlit as st
import utils as ut

st.set_page_config(
    page_title="About the project", 
    page_icon="🔮"
)

def main():

    # Add global styles
    ut.add_custom_css()

    st.title('About the project')

    st.header('Overview')

    st.markdown('This project was a collaboration between Buckinghamshire Council, the EY Foundation and Data Science for Social Good UK.')

    st.markdown('The goal of the project was to build a model for predicting which pupils in Buckinghamshire are at high risk of becoming NEET (Not in Education, Employment or Training) in the future, using a range of different datasets such as the School Census and National Client Caseload Information System (NCCIS) database.')
    
    st.header('Challenge')

    st.markdown('Between 2018 and 2020, Buckinghamshire county had a NEET rate of above 2% and Unknown destination rate of above 5% for young people aged 17 to 18.')

    st.markdown('Studies have shown that time spent NEET can have a detrimental effect on physical and mental health, increasing the likelihood of unemployment, low wages, or low quality of work later on in life. Buckinghamshire Council wanted to identify students’ risk of becoming NEET in years 12 or 13 (ages 17-18), by the end of years 10 or 11 (ages 14-16) so that they could target the right pupils with early intervention programmes. It is hoped that doing so will improve the life chances of those young people who receive intervention that they otherwise may not have done.')
    
# Run the Streamlit app
if __name__ == '__main__':
    main()
