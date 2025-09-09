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
def general_setup():
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
    #Make all questions white
    st.markdown("""
    <style>
    /* Make markdown question text white */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] div {
    color: #ffffff !important;
    }

    /* Make radio option labels and their text white */
    div[role="radiogroup"] label,
    div[role="radiogroup"] label span {
    color: #ffffff !important;
    }

    /* Ensure any other label text in the app is visible on dark background */
    section[data-testid="stApp"] label {
    color: #ffffff !important;
    }

    /* Optional: ensure paragraph wrapping behaves well on small screens */
    [data-testid="stMarkdownContainer"] p {
    overflow-wrap: break-word;
    word-break: normal;
    white-space: normal;
    }
    </style>
    """, unsafe_allow_html=True)