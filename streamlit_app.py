import streamlit as st
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    page_bg = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

add_bg_from_local("background.png")
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        div[data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <h1 style="
        color: #FFD700;
        text-shadow: 2px 2px 5px black;
        font-family: 'Papyrus', fantasy;
    ">
        ✨ Harry Potter App ✨
    </h1>
    """,
    unsafe_allow_html=True
)

add_bg_from_local("background.png")
st.title("Harry Potter App")
st.caption("Created by Yichen")
if st.button("Sign up"):
    st.switch_page("pages/sign_up_page.py")
if st.button("Log in"):
    st.switch_page("pages/login_page.py")