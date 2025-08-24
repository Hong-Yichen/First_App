import streamlit as st

def sign_up(username, password, users):
    with open("usernames_and_passwords.txt", "a") as f:  # append mode
        if username in users:
             print("user already exist")
        else:
            f.write(f"\n{username},{password}")
            print(f"User {username} saved.")

def read_users():
        usernames = {}
        try:
            with open("usernames_and_passwords.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line: 
                        uname, pwd = line.split(",", 1)
                        usernames[uname] = pwd
                        return usernames
        except FileNotFoundError:
            pass 


st.title("Harry Potter App")
st.caption("Created by Yichen")
st.subheader("Sign up")
st.caption("Enjoy magical features including the official sorting ceremony, portrait maker and more!")
birthday = st.date_input("Date of Birthday")
email = st.text_input("Email Address")
password = st.text_input("Password")
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
st.caption("By proceeding you agree to our Terms of Use and acknowledge our Privacy Policy.")
if st.button("Sign up"):
    sign_up(email, password, read_users())
st.divider()
st.subheader("Already have an account?")
if st.button("Login"):
    st.switch_page("pages/login_page.py")