import streamlit as st
from firebase_admin import firestore
import bcrypt
import re
from time import time

def sign_in():
    st.title("Sign In")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if not email or not password:
            st.error("Please enter both email and password.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("Please enter a valid email address.")
        else:
            # Implement rate limiting
            if 'last_attempt' in st.session_state and time() - st.session_state.last_attempt < 3:
                st.error("Please wait a few seconds before trying again.")
            else:
                st.session_state.last_attempt = time()
                authenticate_user(email, password)

    if st.button("Don't have an account? Sign Up"):
        st.session_state.page = 'sign_up'

def authenticate_user(email, password):
    db = firestore.client()
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).limit(1)
    results = query.stream()

    user = next(results, None)

    if user:
        user_data = user.to_dict()
        if bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
            st.success(f"Welcome back, {user_data['username']}!")
            st.session_state.user = user_data
            st.session_state.page = 'landing_page'
        else:
            st.error("Incorrect password. Please try again.")
    else:
        st.error("No account found with this email. Please sign up.")

