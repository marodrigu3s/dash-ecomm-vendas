import streamlit as st
import pandas as pd
from dataset import df
from utils import locale
import plotly.express as px
import plotly.graph_objects as go
from streamlit_card import card
import hydralit_components as hc
import hydralit as hy

#make it look nice from the start
st.set_page_config(
    layout='wide'
    ,initial_sidebar_state="collapsed"
)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)


app = hy.HydraApp(title='outro gato')

@app.addapp(icon="📈")
def Dashboard():
    st.switch_page('pages/ResumoVendas.py')
@app.addapp(icon="📄")
def Detalhado():
    st.switch_page('Detalhado.py')
@app.addapp(icon="🔺")
def Logout():
    st.switch_page('pages/Login.py')

app.run()