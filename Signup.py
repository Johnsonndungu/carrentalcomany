import streamlit as st
from firebase_admin import firestore
import re
import bcrypt

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    return len(password) >= 8 and re.search(r"\d", password) and re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

def is_username_available(username):
    db = firestore.client()
    user_ref = db.collection('users').where('username', '==', username).limit(1).get()
    return len(user_ref) == 0

def sign_up():
    st.title("Sign Up")

    Firstname = st.text_input("Firstname", max_chars=25)
    Lastname = st.text_input("Lastname", max_chars=25)
    username = st.text_input("Username",max_chars=20)
    email = st.text_input("Email")
    phone_number = st.text_input("Phone number")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if not Firstname or not Lastname or not email or not phone_number or not password or not confirm_password:
            st.error("All fields are required.")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")
        elif not is_strong_password(password):
            st.error("Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif not is_username_available(username):
            st.error("Username is already taken. Please choose another.")
        else:
            try:
                db = firestore.client()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                db.collection('users').add({
                    'username': username,
                    'email': email,
                    'password': hashed_password.decode('utf-8')  # Store the hash as a string
                })
                st.success(f"Welcome {username}, your account has been created!")
                st.session_state.page = 'landing_page'
            except Exception as e:
                st.error(f"An error occurred: {e}")

    if st.button("Already have an account? Sign In"):
        st.session_state.page = 'sign_in'

