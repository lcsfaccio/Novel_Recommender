import streamlit as st
import pandas as pd
import numpy as np
import os
import asyncio
#------------------------------------------------------------------------------------------
from session_state import *
login_info = oauth.login(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        login_button_text="Continue with Google",
        logout_button_text="Logout",
    )

if login_info:
        user_id, user_email = login_info
        st.write(f"Welcome {user_email}")
else:
        st.write("Please login")
#------------------------------------------------------------------------------------------
df = pd.read_csv("algoritmo - Base.csv")
st.title('Bem vindo ao recomendador de livros')

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")