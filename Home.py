import streamlit as st
from pages import ResumoVendas
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
            ,page_title='AMS - Bem Vindo'
        )

st.write('Clique abaixo para fazer login: ')
st.page_link('pages/Login.py')

