"""
Sign-up page for the Harry Potter App.

Collects a new user's details, stores them in the flat-file database with
house set to "none", and navigates directly to the registered-user homepage.
"""

import streamlit as st
import datetime
import setup
from setup import read_users, read_specific_user_information, DATABASE_FILE


def sign_up(username: str, password: str, fname: str, lname: str, users: dict) -> None:
    """Register a new user account and redirect to the homepage.

    If the email is already registered, an error is shown instead.
    New users are stored with house="none" until they complete the sorting quiz.

    Args:
        username: Email address to register.
        password: Chosen password.
        fname: User's first name.
        lname: User's last name.
        users: Dict of existing email -> password pairs from the database.
    """
    # Open the database in append mode; new record is written on its own line
    with open(DATABASE_FILE, "a") as f:
        if username in users:
            st.error("Looks like you already have a Harry Potter account with this email")
        else:
            # House is "none" — it will be set after the sorting quiz
            f.write(f"\n{username},{password},{fname},{lname},none")
    # Store the user's email and profile so other pages can access them.
    st.session_state.username = username
    st.session_state.user_information = read_specific_user_information(username)
    st.switch_page("pages/homepage_for_registered_users.py")


# --- Page setup: background image and global styles ---
setup.general_setup()
setup.add_bg_from_local("background.png")

# --- Page header ---
setup.render_page_header("Harry Potter App")

# --- Sign-up form ---
st.markdown("<h2 style='color: white;'>Sign up</h2>", unsafe_allow_html=True)

st.markdown(
    """
    <p style="color: white; font-size: 16px;">
    Enjoy magical features including the official sorting ceremony, portrait maker and more!
    </p>
    """,
    unsafe_allow_html=True
)

st.date_input(
    "Date of Birthday",
    min_value=datetime.date(2000, 1, 1),
    max_value=datetime.date.today()
)
email = st.text_input("Email Address")
password = st.text_input("Password")
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")

st.markdown(
    """
    <p style="color: white; font-size: 16px;">
    By proceeding you agree to our Terms of Use and acknowledge our Privacy Policy.
    </p>
    """,
    unsafe_allow_html=True
)

if st.button("Sign up"):
    sign_up(email, password, first_name, last_name, read_users())

# --- Divider ---
st.markdown('<hr style="border:0;border-top:2px solid grey;margin:1rem 0;">', unsafe_allow_html=True)

# --- Login redirect ---
st.markdown("<h2 style='color: white;'>Already have an account?</h2>", unsafe_allow_html=True)

if st.button("Login"):
    st.switch_page("pages/login_page.py")
