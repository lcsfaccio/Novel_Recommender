import streamlit as st
import pandas as pd
import numpy as np
#------------------------------------------------------------------------------------------
client_id = st.secrets["GOOGLE_CLIENT_ID"]
client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"]
import streamlit_google_oauth as oauth

if __name__ == "__main__":
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

# filtros para a tabela
st.sidebar.markdown('## Selecione o seu nome')

nomes = list(df['name'].unique())
nome = st.sidebar.selectbox('Selecione seu perfil', options = nomes)
codigo = df.query('name == @nome')['name_cod'].unique()[0]

st.markdown('## Qual perfil de livro esta buscando?')

q1 = st.selectbox('Sobre as personagens do livro, elas são', options=['simples (tradicionalmente, são livros mais tranquilos de se ler, sem tantos detalhes)', 'complexas (normalmente, têm mais detalhes e exigem mais atenção na leitura)'])
q2 = st.selectbox('Sobre a personagem principal, ela seria classificada como', options=['herói (são livros mais associados com o gênero romance ou fantasia)', 'anti-herói (mais frequentes em livros antigos e ficções históricas)'])
q3 = st.selectbox('Sobre o enredo vivido pela personagem principal, qual fluxo é o que mais se aproxima', options=['boa para ruim', 'ruim para boa'])
q4 = st.selectbox('Sobre a construção da narrativa, qual é o tipo dela', options=['Vários focos de narração (tradicionalmente, são livros em terceira pessoa que desviam o rumo da narrativa)', 'Um único foco de narração (normalmente, têm perspectiva em primeira pessoa)'])
q5 = st.selectbox('Sobre a quantidade de páginas da história, prefere', options=['Tanto faz', 'Poucas páginas'])

mapper = {'simples (tradicionalmente, são livros mais tranquilos de se ler, sem tantos detalhes)':0,
         'complexas (normalmente, têm mais detalhes e exigem mais atenção na leitura)':1,
         'herói (são livros mais associados com o gênero romance ou fantasia)':0,
         'anti-herói (mais frequentes em livros antigos e ficções históricas)':1,
         'boa para ruim':0,
         'ruim para boa':1,
         'Vários focos de narração (tradicionalmente, são livros em terceira pessoa que desviam o rumo da narrativa)':0,
         'Um único foco de narração (normalmente, têm perspectiva em primeira pessoa)':1,
         'Poucas páginas':0,
          'Tanto faz':1
         }

context = [mapper[q1], mapper[q2], mapper[q3], mapper[q4], mapper[q5]]

#-------------------------------------------------------------------------------
from recommender import *
st.table(reccomendation_list(codigo, context))
