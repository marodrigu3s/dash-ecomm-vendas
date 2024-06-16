import dash
import streamlit as st
import pandas as pd
import pyodbc
from streamlit_extras.grid import grid
import numpy as np


sqlOptions = (
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=75.101.154.23;'
            'DATABASE=amz_ams;'
            'UID=sa;'
            'PWD=wU#DjES!I3k@j?ZW9ZJ;'
            'TrustedServerCertificate=yes;'
            'Encrypt=no'
        )

sqlConn = pyodbc.connect(sqlOptions)
sqlCursor = sqlConn.cursor()

query = '''
    select 
        *
    from 
        fato_Venda
    '''

df = pd.read_sql(query, sqlConn)

def example():
    random_df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    my_grid = grid(2, [2, 4, 1], 1, 4, vertical_align="bottom")

    # Row 1:
    my_grid.dataframe(random_df, use_container_width=True)
    my_grid.line_chart(random_df, use_container_width=True)
    # Row 2:
    my_grid.selectbox("Select Country", ["Germany", "Italy", "Japan", "USA"])
    my_grid.text_input("Your name")
    my_grid.button("Send", use_container_width=True)
    # Row 3:
    my_grid.text_area("Your message", height=40)
    # Row 4:
    my_grid.button("Example 1", use_container_width=True)
    my_grid.button("Example 2", use_container_width=True)
    my_grid.button("Example 3", use_container_width=True)
    my_grid.button("Example 4", use_container_width=True)
    # Row 5 (uses the spec from row 1):
    with my_grid.expander("Show Filters", expanded=True):
        st.slider("Filter by Age", 0, 100, 50)
        st.slider("Filter by Height", 0.0, 2.0, 1.0)
        st.slider("Filter by Weight", 0.0, 100.0, 50.0)
    my_grid.dataframe(random_df, use_container_width=True)

example()

