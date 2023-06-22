import streamlit as st
import pandas as pd
import plotly.express as px
import utils as ut

# Function to create a count plot
def create_count_plot(data):
    # Create a count plot using plotly
    fig = px.histogram(
        data, x="neet_ever", color="neet_ever", title="Number of Students by neet_ever"
    )
    fig.update_layout(showlegend=False)

    # Display the plot
    st.plotly_chart(fig)


# Function to create a table of absences for students with neet_ever = True
def create_absence_table(data):
    # Filter the data based on neet_ever == True
    filtered_data = data[data["neet_ever"] == True]

    # Select the desired columns for the table
    table_data = filtered_data[["upn", "total_absences"]]

    # Display the title
    st.subheader("Absence Details for Students with neet_ever = True")

    # Display the table with styled CSS
    st.dataframe(
        table_data.style.highlight_max(subset=["total_absences"], color="#FF6F61")
    )


# Main Streamlit app
def main():

    st.set_page_config(
        page_title="NEET Risk Dashboard", 
        page_icon="📚", 
        layout="wide"
    )

    # Add global styles
    ut.add_global_styles()

    # Initialize the session state if it doesn't exist
    if "data" not in st.session_state:
        st.session_state.data = []

    st.header("See the visualizations here")

    # Check if data is uploaded
    if st.session_state.data:
        # Combine all the uploaded data
        combined_data = pd.concat(st.session_state.data, ignore_index=True)

        create_count_plot(combined_data)
        create_absence_table(combined_data)
    else:
        st.warning("No data uploaded.")


# Run the Streamlit app
if __name__ == "__main__":
    main()