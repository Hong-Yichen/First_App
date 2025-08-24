import streamlit as st
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
         f"""
         <style>
         [data-testid="stAppViewContainer"] {{
             background-image: url("data:image/png;base64,{encoded}");
             background-size: cover;
             background-attachment: fixed;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

st.write("Here is some **bold text** and some <span style='color: yellow;'>purple text</span>.",
         unsafe_allow_html=True)
add_bg_from_local("background.png")
st.title("Harry Potter App")
st.caption("Created by Yichen")
if st.button("Sign up"):
    st.switch_page("pages/sign_up_page.py")
if st.button("Log in"):
    st.switch_page("pages/login_page.py")