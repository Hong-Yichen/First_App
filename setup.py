"""
Shared setup and utility functions used across all pages of the Harry Potter App.

Provides:
- Page background styling
- Global UI styling (buttons, inputs, text colours)
- Shared golden page header renderer
- Database read helpers
"""

import streamlit as st
import base64

# Path to the flat-file user database.
# Each line is a comma-separated record: email,password,first_name,last_name,house
# 'house' is "none" until the user completes the Hogwarts sorting quiz.
DATABASE_FILE = "users_information_database.txt"


def add_bg_from_local(image_file: str) -> None:
    """Encode a local image and inject it as the full-page background via CSS.

    Args:
        image_file: Path to the PNG/JPG background image (e.g. "background.png").
    """
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


def general_setup() -> None:
    """Apply global UI styling shared by every page.

    Sets button colours (blue background, white text, gold on hover),
    makes text input labels white, and ensures all markdown/radio text
    is white so it's readable on the dark background image.
    """
    # Style all buttons: blue background, white text, gold text and slight scale on hover
    st.markdown(
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
    # Make the first text input label white (visible on dark background)
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"]:nth-of-type(1) label {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Make all markdown text, radio option labels, and general labels white
    st.markdown(
        """
        <style>
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] div {
            color: #ffffff !important;
        }

        div[role="radiogroup"] label,
        div[role="radiogroup"] label span {
            color: #ffffff !important;
        }

        section[data-testid="stApp"] label {
            color: #ffffff !important;
        }

        /* Prevent text overflow on small screens */
        [data-testid="stMarkdownContainer"] p {
            overflow-wrap: break-word;
            word-break: normal;
            white-space: normal;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_page_header(title: str) -> None:
    """Render the golden Papyrus-font page title and 'Created by Yichen' caption.

    This is used on every page to provide a consistent branded header.

    Args:
        title: The heading text to display (e.g. "Harry Potter App").
    """
    # Golden glowing title in Papyrus fantasy font
    st.markdown(
        f"""
        <style>
        .magic-title {{
            font-family: 'Papyrus', fantasy;
            color: #FFD700;
            font-size: 60px;
            text-shadow: 0 0 10px #FFD700, 0 0 20px #FFA500, 0 0 30px #FFD700;
            text-align: center;
            letter-spacing: 3px;
        }}
        </style>

        <h1 class="magic-title">{title}</h1>
        """,
        unsafe_allow_html=True
    )
    # Subtitle attribution beneath the main title
    st.markdown(
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


def read_users() -> dict:
    """Read all user email/password pairs from the database.

    Returns:
        A dict mapping email -> password for every stored account.
        Returns an empty dict if the database file does not exist yet.
    """
    users = {}
    try:
        with open(DATABASE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:  # skip blank lines
                    uname, pwd, fname, lname, house = line.split(",", 4)
                    users[uname] = pwd
    except FileNotFoundError:
        pass
    return users


def read_specific_user_information(username: str):
    """Retrieve profile data for a single user from the database.

    Args:
        username: The email address used as the unique user identifier.

    Returns:
        [first_name, last_name, house] for the matching user, or None if not found.
    """
    users_information = {}
    try:
        with open(DATABASE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:  # skip blank lines
                    uname, pwd, fname, lname, house = line.split(",", 4)
                    users_information[uname] = [fname, lname, house]
    except FileNotFoundError:
        pass
    return users_information.get(username)
