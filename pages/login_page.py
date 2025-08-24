import streamlit as st

def login(username, password, users):
    if username in users:
        if users[username] == password:
            print("user logged in successfully")            
        else:
            print("password doesn't match")
    else:
        print("user isn't in the system")

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
st.subheader("Login")
email = st.text_input("Email Address")
password = st.text_input("password")
if st.button("Login"):
    login(email, password, read_users())
st.divider()
st.subheader("Don't have an account?")
if st.button("Sign up"):
    st.switch_page("pages/sign_up_page.py")



