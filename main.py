from io import StringIO
from os import write
from matplotlib.pyplot import hist
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

st.set_page_config(page_title='DWM Mini Project', page_icon=':bar_chart:', layout="wide")

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
    col1, col2 = st.columns(2)
    with col1:
        # Create the dropdown menus
        cols = df.columns
        x_col = st.selectbox('Select an X-axis column', cols)
        y_col = st.selectbox('Select a Y-axis column', cols)
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

def page3():
    df = st.session_state.get('df')
    cols = df.columns

    df2 = df[cols]
    fig = sns.pairplot(df2)
    fig.map_lower(sns.lineplot)

    st.pyplot(fig)

def page4():
    st.write("Database Cleaning")
    df2 = st.session_state.get('df')
    cols = df2.columns
    col5, col7, col8 = st.columns([1,1,1])

    with col5:
        options = ['drop', 'fill', 'global_const']

        option_selected = st.selectbox('Select an option', options)
        column_selected = st.selectbox('Select column', cols)

        if option_selected == 'drop':
            df2 = df2.drop(column_selected, axis=1)
        elif option_selected == 'fill':
            df2 = df2.fillna(inplace=True)
        else:
            val = st.text_input("Enter Global Const")
            df2 = df2.fillna(value=val)

    with col7:
        df = st.session_state.get('df')
        st.write("Old database:")
        st.write(df)

    with col8:
        st.write("New database:")
        st.write(df2)

# Create the app
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Upload CSV', 'Plot Data', 'Generated Plots', 'Database Manipulation'])
if page == 'Upload CSV':
    page1()
elif page == 'Plot Data':
    page2()
elif page == 'Generated Plots':
    page3()
elif page == 'Database Manipulation':
    page4()

