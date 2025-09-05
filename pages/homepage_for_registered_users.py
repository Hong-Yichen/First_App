import streamlit as st
import base64

def add_bg_from_local(image_file):          #For backgroung image
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
st.markdown(                  #Make buttons' background blue and text white
    """
    <style>
    div.stButton > button {
        color: white !important;
        background-color: #0073e6;
        border-radius: 8px;
        padding: 8px 20px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color: #005bb5;
        color: #ffcc00 !important; /* text turns gold on hover */
        transform: scale(1.05); /* button grows slightly */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(              #Make text inputs white
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

add_bg_from_local("background.png")
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