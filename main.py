from io import StringIO
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='CSV Plotter', page_icon=':bar_chart:', layout="wide")

# Define the first page
def page1():
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.read()
        df = pd.read_csv(uploaded_file)
        st.session_state['df'] = df
        st.success('File uploaded successfully!')

def page2():
    df = st.session_state.get('df')
    int_cols = df.select_dtypes(include=['int']).columns.tolist()
    float_cols = df.select_dtypes(include=['float']).columns.tolist()

    col1, col2 = st.columns(2)
    with col1:
        # Create the dropdown menus
        x_col = st.selectbox('Select an X-axis column', int_cols + float_cols)
        y_col = st.selectbox('Select a Y-axis column', int_cols + float_cols)
        graph_type = st.selectbox('Select a graph type', ['scatter', 'line', 'bar'])
    with col2:

        # Plot the graph
        if graph_type == 'scatter':
            fig = px.scatter(df, x=x_col, y=y_col)
        elif graph_type == 'line':
            fig = px.line(df, x=x_col, y=y_col)
        else:
            fig = px.bar(df, x=x_col, y=y_col)
        st.plotly_chart(fig)

# Create the app
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Upload CSV', 'Plot Data'])
if page == 'Upload CSV':
    page1()
else:
    page2()


