import streamlit as st
import os
import logging
from firebase_admin import credentials, firestore, initialize_app
import Landingpage
import Signup
import Signin
import firebase_admin
import os

# Load Firebase credentials from environment variable
firebase_key = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
# Initialize Firebase
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_key)
        initialize_app(cred)
    db = firestore.client()
    logging.info("Firebase initialized successfully")
except Exception as e:
    logging.error(f"Error initializing Firebase: {e}")
    st.error("An error occurred while initializing the application. Please try again later.")

# Initialize session state if not already done
if 'page' not in st.session_state:
    st.session_state.page = 'sign_in'  # Default to Sign In page

def main():
    if st.session_state.page == 'sign_up':
        Signup.sign_up()
    elif st.session_state.page == 'sign_in':
        Signin.sign_in()
    elif st.session_state.page == 'landing_page':
         Landingpage.landing_page()
    
    # Navigation buttons
    st.sidebar.button("SignUp", on_click=lambda: setattr(st.session_state, 'page', 'sign_up'))
    st.sidebar.button("SignIn", on_click=lambda: setattr(st.session_state, 'page', 'sign_in'))

if __name__ == '__main__':
    main()

