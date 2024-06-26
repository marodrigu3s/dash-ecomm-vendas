# autenticacao
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader
from streamlit.components.v1 import html
from dataset import df, dfMetrica, dfMetricaTempoResp, dfVisita, dfPosVenda, dfPergunta, dfTop10
from pages.ResumoVendas import dashboard
import toml
from streamlit_javascript import st_javascript

st.set_page_config(page_title='Login', layout="centered", initial_sidebar_state="collapsed", menu_items=None)


metricaAtraso = ((dfMetrica['num_NotaAtrasoEnvio'].iloc[0] * 100) - 100) * -1

#st.set_page_config(
#            layout="centered"
#            ,page_title='AMS - Dashboard'
#            ,initial_sidebar_state="collapsed"
#        )





#st_autorefresh(interval=30000, limit=None, key="fizzbuzzcounter")


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)


col1,col2,col3 = st.columns((4,4,4))
with col1:
    pass
with col2:
    entrar = authenticator.login()
with col3:
    pass


if st.session_state["authentication_status"]:
    dashboard()
elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha is inválido')


