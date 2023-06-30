import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import utils as ut


st.set_page_config(page_title="Indivdiual Students", page_icon="🔮")

names = ("Select", "test", "test")


def get_uid() -> str | None:
    """
    Helper function, because state can have the value 'Select'.
    To make it failsafe the state gets checked against set of all uids.

    Return:
        uid or None, if it is no valid uid.

    TODO: Might make sense to move set of uids into the state as part of initalize_global_state()
    """

    uid = st.session_state.selected_uid
    uids = st.session_state.data_final_uids

    if uid in uids:
        return uid

    return None


def render_chart_risk(indiv_data):
    # Source for simulation: https://stackoverflow.com/questions/60649486/line-chart-with-custom-confidence-interval-in-altair
    x = np.random.normal(70, 17, 5)

    epsilon = [33, 17, 21, 10, 5.5]

    data = pd.DataFrame(
        {
            "x": x,
            "lower": x - epsilon,
            "upper": x + epsilon,
            "year": ["2019", "2020", "2021", "2022", "2023"],
        }
    ).reset_index()

    line = alt.Chart(data).mark_line().encode(x="year", y="x")

    band = (
        alt.Chart(data)
        .mark_area(opacity=0.5)
        .encode(
            x="year",
            y=alt.Y("lower", title="Risk score (in percentage points)"),
            y2="upper",
        )
    )

    return st.altair_chart((band + line).interactive(), use_container_width=True)


def render_chart_explanations(indiv_data):
    chart_data = pd.DataFrame(
        np.random.randint(-10, 10, size=(5, 2)),
        index=["2019", "2020", "2021", "2022", "2023"],
        columns=["Authorised", "Unauthorised"],
    )
    return st.bar_chart(chart_data, use_container_width=True)


def render_chart_abscence(indiv_data):
    chart_data = pd.DataFrame(
        np.random.randint(0, 100, size=(5, 2)),
        index=["2019", "2020", "2021", "2022", "2023"],
        columns=["Authorised", "Unauthorised"],
    )
    return st.line_chart(chart_data, use_container_width=True)

def render_chart_attainment(indiv_data):

    chart_data= pd.DataFrame([['KS2', 5, 'Math'], 
                    ['KS4', 10, 'Math'], 
                    ['KS4', 3, 'Science'], 
                    ['KS2', 9, 'Science']], 
                    columns=['Stage', 'Grade', 'Subject'])

    return st.dataframe(chart_data, use_container_width=True)


def main():
    """Renders the contents of the streamlit page."""

    # Add global styles and load state
    ut.add_custom_css()
    ut.initalize_global_state()

    # Get the data from state
    data = st.session_state.data_final
    uids = st.session_state.data_final_uids

    st.title("Information about individual students")

    st.selectbox(
        "Select person",
        options=["Select"] + list(uids),
        key="selected_uid",
        format_func=lambda x: "Select"
        if x == "Select"
        else "Name (" + x + ")",  # + data.at[x, 'upn']
    )

    uid = get_uid()

    # Bail early if no uid is selected
    if uid is None:
        st.warning("Please select a student")
        return

    indiv_data = data.loc[uid]

    st.header(f"About John Doe")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Name: " + "John Doe")
        st.write("School: " + "Doe School")
        st.write("Post Code: " + "123456")
        st.write("UID: " + uid)

    with col2:
        st.metric(
            "Risk of NEET",
            value="76%",
            delta="-3%",
            delta_color="inverse",
            help="Risk score calculated by out prediction model.",
        )
    st.header("Risk prediciton over time")
    st.markdown("Shows the development of the predicted risk score over time.")
    render_chart_risk(indiv_data)

    st.header("Factors driving the risk score")
    render_chart_explanations(indiv_data)

    st.header("Absence")
    render_chart_abscence(indiv_data)

    st.header("Attainment")
    st.markdown("Attainment is reported relative to peer performance.")
    render_chart_attainment(indiv_data)

    st.header("View raw data")
    st.dataframe(indiv_data, use_container_width=True)


# Run the Streamlit app
if __name__ == "__main__":
    main()
