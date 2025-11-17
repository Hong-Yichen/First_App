import streamlit as st
import base64
import datetime
import setup

def sign_up(username, password, fname, lname, users):
    with open("users_information_database.txt", "a") as f:  # append mode
        if username in users:
            st.error("Looks like you already have a Harry Potter account with this email")
        else:
            f.write(f"\n{username},{password},{fname},{lname},none")
    st.session_state.user_information = read_specific_user_information(username)
    st.switch_page("pages/homepage_for_registered_users.py")

def read_users():
        usernames = {}
        try:
            with open("users_information_database.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line: 
                        uname, pwd, fname, lname, house = line.split(",", 4)
                        usernames[uname] = pwd
                return usernames
        except FileNotFoundError:
            pass 
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
    print(users_information)
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
st.markdown(           #For text "Sign up"
    "<h2 style='color: white;'>Sign up</h2>",
    unsafe_allow_html=True
)

st.markdown(           #For text "Enjoy magical features including the official sorting ceremony, portrait maker and more!"
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
st.markdown(           #For text "By proceeding you agree to our Terms of Use and acknowledge our Privacy Policy."
    """
    <p style="color: white; font-size: 16px;">
    By proceeding you agree to our Terms of Use and acknowledge our Privacy Policy.
    </p>
    """,
    unsafe_allow_html=True
)
if st.button("Sign up"):
    sign_up(email, password, first_name, last_name, read_users())
st.markdown(        #Make divider grey
    '<hr style="border:0;border-top:2px solid grey;margin:1rem 0;">',
    unsafe_allow_html=True
)
st.markdown(         #For text "Already have an account?"
    "<h2 style='color: white;'>Already have an account?</h2>",
    unsafe_allow_html=True
)
if st.button("Login"):
    st.switch_page("pages/login_page.py")