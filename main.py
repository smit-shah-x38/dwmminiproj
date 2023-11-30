import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import io

st.set_page_config(
    page_title="DWM Mini Project", page_icon=":bar_chart:", layout="wide"
)


# Define the first page
def page1():
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state["df"] = df
        st.success("File uploaded successfully!")


def page2():
    df = st.session_state.get("df")
    col1, col2 = st.columns(2)
    with col1:
        # Create the dropdown menus
        cols = df.columns
        graph_types = ["scatter", "line", "bar"]
        x_col = st.selectbox("Select an X-axis column", cols)
        y_col = st.selectbox("Select a Y-axis column", cols)
        graph_type = st.selectbox("Select a graph type", graph_types)
    with col2:
        # Plot the graph
        if graph_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col)
        elif graph_type == "line":
            fig = px.line(df, x=x_col, y=y_col)
        else:
            fig = px.bar(df, x=x_col, y=y_col)
        st.plotly_chart(fig)


def page3():
    df = st.session_state.get("df")
    cols = df.columns

    df2 = df[cols]

    lowerplots = ["kde", "line"]

    lower_selected = st.selectbox("Select the lower plot", lowerplots)
    if st.button("Generate"):
        fig = sns.pairplot(df2)
        if lower_selected == "kde":
            fig.map_lower(sns.kdeplot)
        else:
            fig.map_lower(sns.lineplot)

        st.pyplot(fig)


def page4():
    st.write("Database Cleaning")
    df2 = st.session_state.get("df")
    cols = df2.columns
    col5, col7, col8 = st.columns([1, 1, 1])

    with col5:
        options = ["drop", "fill", "global_const"]

        option_selected = st.selectbox("Select an option", options)
        column_selected = st.selectbox("Select column", cols)

        if option_selected == "drop":
            df2 = df2.drop(column_selected, axis=1)
        elif option_selected == "fill":
            df2 = df2.fillna(inplace=True, value=1)
        else:
            val = st.text_input("Enter Global Const")
            df2 = df2.fillna(value=val)

    with col7:
        df = st.session_state.get("df")
        st.write("Old database:")
        st.write(df)

    with col8:
        st.write("New database:")
        st.write(df2)


def page5():
    df3 = st.session_state.get("df")
    col55, col56 = st.columns([1, 1])
    buffer = io.StringIO()
    df3.info(buf=buffer)
    s = buffer.getvalue()

    with col55:
        st.write(df3.describe())

    with col56:
        st.text(s)


# Create the app
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Functionalities",
    [
        "Upload CSV",
        "Plot Data",
        "Generated Plots",
        "Database Manipulation",
        "Database Description",
    ],
)
if page == "Upload CSV":
    page1()
elif page == "Plot Data":
    page2()
elif page == "Generated Plots":
    page3()
elif page == "Database Manipulation":
    page4()
elif page == "Database Description":
    page5()
