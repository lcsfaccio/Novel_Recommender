import streamlit as st
#import os
#from dotenv import load_dotenv
#import streamlit_google_oauth as oauth

#load_dotenv()
# os.environ["GOOGLE_CLIENT_ID"] ="186940062697-acgucff8i09gu24f5akkjnassgt7uceh.apps.googleusercontent.com"
# os.environ["GOOGLE_CLIENT_SECRET"] ="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"
# os.environ["GOOGLE_REDIRECT_URI"] ="http://localhost:8501"

client_id = st.secrets["GOOGLE_CLIENT_ID"]
client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"]


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
# streamlit run app.py --server.port 8080
