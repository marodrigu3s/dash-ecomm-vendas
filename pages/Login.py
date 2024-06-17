# autenticacao
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader

# conteudo
from pages.ResumoVendas import dashboard

st.set_page_config(
            layout="wide"
            ,page_title='AMS - Dashboard'
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

entrar = authenticator.login()

if st.session_state["authentication_status"]:
    dashboard()
elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha is inválido')


