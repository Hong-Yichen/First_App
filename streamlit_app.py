"""
Main entry point for the Harry Potter App.

Displays the landing page with navigation buttons for Sign Up and Login.
All styling and shared utilities are handled by setup.py.
"""

import streamlit as st
import setup

# --- Page setup: background image and global styles ---
setup.general_setup()
setup.add_bg_from_local("background.png")

# --- Page header ---
setup.render_page_header("Harry Potter App")

# --- Navigation buttons ---
if st.button("Sign up"):
    st.switch_page("pages/sign_up_page.py")
if st.button("Login"):
    st.switch_page("pages/login_page.py")
