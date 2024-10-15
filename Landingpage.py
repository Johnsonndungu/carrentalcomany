import streamlit as st

def landing_page():
    if 'user' not in st.session_state:
        st.error("Please sign in to access this page.")
        st.session_state.page = 'sign_in'
        return

    st.title("Welcome to the Car Rental Dashboard")
    st.write(f"Hello, {st.session_state.user['username']}!")
    
    # Add more dashboard content here

    if st.button("Log Out"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    st.session_state.page = 'sign_in'
