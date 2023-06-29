import streamlit as st
import utils as ut
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Council information", page_icon="🔮")

# Function to create a count plot
def create_count_plot(data):
    # Create a count plot using plotly
    fig = px.histogram(
        data,
        x="neet_ever",
        color="neet_ever",
        title="Number of Students by neet_ever",
        color_discrete_map={True: "green", False: "orange"},
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
    st.subheader("Absence Details for NEET Students")

    # Display the table with styled CSS
    st.dataframe(
        table_data.style.highlight_max(subset=["total_absences"], color="#FF6F61")
    )


# Function to display a pie chart to show the percentage of each gender enrolled
def display_gender_enrollment_pie_chart(data):
    # Get the count of each gender category
    gender_counts = data[["gender__f", "gender__m", "gender__w", "gender__u"]].sum()

    # Create a pie chart using plotly
    fig = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        title="Gender Enrollment Pie Chart",
        color=gender_counts.index,
    )

    # Display the pie chart
    st.plotly_chart(fig)


# Function to create a bar graph for ethnicity columns
def plot_ethnicity_columns(data):
    # Filter the columns starting with "ethnicity"
    ethnicity_columns = [col for col in data.columns if col.startswith("ethnicity")]

    # Calculate the count of each ethnicity
    ethnicity_counts = data[ethnicity_columns].sum().sort_values(ascending=False)

    # Create a bar graph using plotly
    fig = px.bar(
        x=ethnicity_counts.values,
        y=ethnicity_counts.index,
        orientation="h",
        title="Ethnicity Counts",
        labels={"x": "Count", "y": "Ethnicity"},
    )

    # Display the bar graph
    st.plotly_chart(fig)


def plot_language_graph(data):
    # Filter the columns starting with "ethnicity"
    lang_graph = [col for col in data.columns if col.startswith("language")]

    # Calculate the count of each ethnicity
    language_counts = data[lang_graph].sum().sort_values(ascending=False)

    # Create a bar graph using plotly
    fig = px.bar(
        x=language_counts.values,
        y=language_counts.index,
        orientation="h",
        title="Language Counts",
        labels={"x": "Count", "y": "Languages"},
    )

    # Change the color of the bars to green
    fig.update_traces(marker_color="green")

    # Display the bar graph
    st.plotly_chart(fig)


# to display summary cards
def show_summary_card(data):
    # Get the total number of students
    total_students = len(data)

    # Display the number of students in a box
    st.info(f"Total Students: {total_students}")


def plot_birth_columns(data):
    # Filter the columns starting with "birth"
    birth_columns = [col for col in data.columns if col.startswith("birth")]

    # Create a DataFrame with the count of entries in each birth column
    counts = pd.DataFrame(data[birth_columns].sum(), columns=["Count"]).reset_index()
    counts.rename(columns={"index": "Year"}, inplace=True)

    # Create a line chart using plotly
    fig = px.line(
        counts,
        x="Year",
        y="Count",
        title="Number of students who are born in each month",
    )

    # Display the line chart
    st.plotly_chart(fig)


# Main Streamlit app
def main():
    """Renders the contents of the streamlit page."""

    # Add global styles and load state
    ut.add_custom_css()
    ut.initalize_global_state()

    # Get the data from state
    data = st.session_state.data_final

    st.title("Overview of local NEET risk")

    show_summary_card(data)

    # Create two columns for the graphs
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        #create_count_plot(data)
        st.bar_chart(
            data["neet_ever"].value_counts(),
            use_container_width=True
        )

    with col2:
        display_gender_enrollment_pie_chart(data)

    with col3:
        plot_ethnicity_columns(data)

    with col4:
        st.write("test")

    
    plot_language_graph(data)

    plot_birth_columns(data)
    create_absence_table(data)


# Run the Streamlit app
if __name__ == "__main__":
    main()
