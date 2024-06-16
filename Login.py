import streamlit as st
from pages import Home
import pandas as pd
from dataset import df
from utils import locale
import plotly.express as px
import streamlit_authenticator as stauth
#from streamlit_extras.metric_cards import style_metric_cards
import yaml
from yaml import SafeLoader
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go

st.set_page_config(
            layout="wide"
            ,page_title='AMS - Login'
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

#st_autorefresh(interval=30000, limit=None, key="fizzbuzzcounter")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

authenticator.login()

if st.session_state["authentication_status"]:
    with st.sidebar:
        st.write(f'Bem Vindo *{st.session_state["name"]}*')


    #st.switch_page('pages/Home.py')
elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha is inválido')

