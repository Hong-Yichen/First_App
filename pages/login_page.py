import streamlit as st
import base64
import setup

def login(username, password, users):
    if username in users:
        if users[username] == password:
            st.session_state.user_information = read_specific_user_information(username)
            st.switch_page("pages/homepage_for_registered_users.py")
        else:
            st.error("We can't find this email and password combination. Have you been Confunded? Try again.")
    else:
        st.error("We can't find this email. Have you been Confunded? Try again.")
def read_users():
    users = {}
    try:
        with open("users_information_database.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:  # skip empty lines
                    uname, pwd, fname, lname, house = line.split(",", 5)
                    users[uname] = pwd
    except FileNotFoundError:
        pass  # if file doesn’t exist yet
    return users
def read_specific_user_information(username):
    users_information = {}
    try:
        with open("users_information_database.txt", "r") as f:
           for line in f:                
                line = line.strip()
                if line:  # skip empty lines
                    uname, pwd, fname, lname, house = line.split(",", 4)
                    users_information[uname] = [fname, lname, house]
    except FileNotFoundError:
        pass  # if file doesn’t exist yet
    return users_information.get(username)

setup.general_setup()
setup.add_bg_from_local("background.png")
st.markdown(          #For text "Harry Potter App"
    """
    <style>
    .magic-title {
        font-family: 'Papyrus', fantasy;   /* mystical vibe */
        color: #FFD700;                   /* golden yellow */
        font-size: 60px;
        text-shadow: 0 0 10px #FFD700, 0 0 20px #FFA500, 0 0 30px #FFD700;
        text-align: center;
        letter-spacing: 3px;
    }
    </style>

    <h1 class="magic-title">Harry Potter App</h1>
    """,
    unsafe_allow_html=True
)
st.markdown(                 #For text "Created by Yichen"
    """
    <style>
    .harry-caption {
        font-family: Papyrus, fantasy;
        color: #FFD700;
        font-size: 20px;
        text-align: center;
        text-shadow: 
            1px 1px 3px #000000,
            0 0 8px #FFD700;
    }
    </style>

    <p class="harry-caption">Created by Yichen</p>
    """,
    unsafe_allow_html=True
)
st.markdown(           #For text "Login"
    "<h2 style='color: white;'>Login</h2>",
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* Only the first text input's label */
    div[data-testid="stTextInput"]:nth-of-type(1) label {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
email = st.text_input("Email Address")
password = st.text_input("Password")
if st.button("Login"):
    login(email, password, read_users())
st.markdown(        #Make divider grey
    '<hr style="border:0;border-top:2px solid grey;margin:1rem 0;">',
    unsafe_allow_html=True
)
st.markdown(         #For text "Don't have an account?"
    "<h2 style='color: white;'>Don't have an account?</h2>",
    unsafe_allow_html=True
)
if st.button("Sign up"):
    st.switch_page("pages/sign_up_page.py")



