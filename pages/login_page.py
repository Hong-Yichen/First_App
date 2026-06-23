"""
Login page for the Harry Potter App.

Accepts an email and password, authenticates against the flat-file database,
and navigates authenticated users to the registered-user homepage.
"""

import streamlit as st
import setup
from setup import read_users, read_specific_user_information


def login(username: str, password: str, users: dict) -> None:
    """Authenticate the user and redirect to the homepage on success.

    Args:
        username: Email address entered by the user.
        password: Password entered by the user.
        users: Dict of email -> password loaded from the database.
    """
    if username in users:
        if users[username] == password:
            # Store the user's profile so other pages can access it via session state.
            # user_information = [first_name, last_name, house]
            st.session_state.user_information = read_specific_user_information(username)
            st.switch_page("pages/homepage_for_registered_users.py")
        else:
            st.error("We can't find this email and password combination. Have you been Confunded? Try again.")
    else:
        st.error("We can't find this email. Have you been Confunded? Try again.")


# --- Page setup: background image and global styles ---
setup.general_setup()
setup.add_bg_from_local("background.png")

# --- Page header ---
setup.render_page_header("Harry Potter App")

# --- Login form ---
st.markdown("<h2 style='color: white;'>Login</h2>", unsafe_allow_html=True)

email = st.text_input("Email Address")
password = st.text_input("Password")

if st.button("Login"):
    login(email, password, read_users())

# --- Divider ---
st.markdown('<hr style="border:0;border-top:2px solid grey;margin:1rem 0;">', unsafe_allow_html=True)

# --- Sign-up redirect ---
st.markdown("<h2 style='color: white;'>Don't have an account?</h2>", unsafe_allow_html=True)

if st.button("Sign up"):
    st.switch_page("pages/sign_up_page.py")
