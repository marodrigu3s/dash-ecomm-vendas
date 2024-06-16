import streamlit as st
import pandas as pd
from dataset import df
from utils import locale
import plotly.express as px
import plotly.graph_objects as go
from streamlit_card import card


#make it look nice from the start
st.set_page_config(
    layout='wide'
    ,initial_sidebar_state="collapsed"
    ,page_title='Detalhado'
)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=False,
)


