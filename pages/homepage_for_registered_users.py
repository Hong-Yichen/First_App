"""
Homepage for registered users of the Harry Potter App.

Displays the user's name and either:
- A button to start the Hogwarts sorting quiz (if house == "none"), or
- Their assigned house banner with crest and description (if already sorted).

session_state.user_information is a list: [first_name, last_name, house]
"""

import streamlit as st
import base64
import os
import setup
from typing import Optional, Dict

# --- House data ---
HOUSE_DESCS: Dict[str, str] = {
    "Gryffindor": "Bravery, daring, nerve and chivalry.",
    "Hufflepuff": "Hard work, patience, justice and loyalty.",
    "Ravenclaw": "Intelligence, learning, wisdom and wit.",
    "Slytherin": "Ambition, cunning, resourcefulness and leadership."
}

HOUSE_COLORS: Dict[str, str] = {
    "Gryffindor": "#7F0909",
    "Hufflepuff": "#ECB939",
    "Ravenclaw": "#0E1A40",
    "Slytherin": "#1A472A"
}

CREST_PATHS: Dict[str, str] = {
    "Gryffindor": "crests/gryffindor.png",
    "Hufflepuff": "crests/hufflepuff.png",
    "Ravenclaw": "crests/ravenclaw.png",
    "Slytherin": "crests/slytherin.png"
}


# --- Helpers ---

def _img_to_data_uri(path: str) -> Optional[str]:
    """Encode a local image file to a base64 data URI for embedding in HTML.

    Args:
        path: Relative path to the image file.

    Returns:
        A data URI string, or None if the file does not exist.
    """
    if not path or not os.path.exists(path):
        return None
    mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"


def _render_house_banner(chosen_house: str, crest_size_px: int = 160, tie_info: Optional[list] = None) -> None:
    """Render a coloured house banner with crest image and description.

    Args:
        chosen_house: Name of the Hogwarts house to display.
        crest_size_px: Width in pixels for the crest image column.
        tie_info: If a tie was broken, list of tied houses (currently unused in display).
    """
    if not chosen_house:
        st.warning("No house provided.")
        return

    color = HOUSE_COLORS.get(chosen_house, "#222")
    desc = HOUSE_DESCS.get(chosen_house, "")
    crest_data = _img_to_data_uri(CREST_PATHS.get(chosen_house, ""))

    img_html = ""
    if crest_data:
        img_html = (
            f"<div class='crest-wrap' style='display:flex;align-items:center;justify-content:center;'>"
            f"<img src='{crest_data}' style='max-width:{crest_size_px}px;height:auto;"
            f"border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,0.30);'/>"
            f"</div>"
        )

    # Two-column grid: text on the left, crest image on the right.
    # On narrow screens (≤720px) the columns stack vertically.
    banner_html = f"""
    <style>
      .sh-banner {{
        background:{color};
        padding:20px;
        border-radius:12px;
        display:grid;
        grid-template-columns: minmax(0, 1fr) {crest_size_px}px;
        gap:18px;
        align-items:center;
        color:#ffffff;
        max-width:100%;
      }}
      .sh-banner .text {{ min-width:0; }}
      .sh-banner h1 {{ margin:0 0 6px 0; font-family:Georgia, 'Times New Roman', serif; font-size:28px; }}
      .sh-banner p {{ margin:0; font-size:15px; line-height:1.45; overflow-wrap:break-word; }}
      @media (max-width:720px) {{
        .sh-banner {{ grid-template-columns: 1fr; text-align:center; }}
        .crest-wrap {{ margin-top:12px; }}
      }}
    </style>

    <div class="sh-banner">
      <div class="text">
        <h1>{chosen_house}</h1>
        <p>{desc}</p>
      </div>
      {img_html}
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)


# --- Per-house wrapper functions (convenience callers) ---

def render_gryffindor(crest_size_px: int = 160, tie_info: Optional[list] = None) -> None:
    """Render the Gryffindor house banner."""
    _render_house_banner("Gryffindor", crest_size_px=crest_size_px, tie_info=tie_info)

def render_hufflepuff(crest_size_px: int = 160, tie_info: Optional[list] = None) -> None:
    """Render the Hufflepuff house banner."""
    _render_house_banner("Hufflepuff", crest_size_px=crest_size_px, tie_info=tie_info)

def render_ravenclaw(crest_size_px: int = 160, tie_info: Optional[list] = None) -> None:
    """Render the Ravenclaw house banner."""
    _render_house_banner("Ravenclaw", crest_size_px=crest_size_px, tie_info=tie_info)

def render_slytherin(crest_size_px: int = 160, tie_info: Optional[list] = None) -> None:
    """Render the Slytherin house banner."""
    _render_house_banner("Slytherin", crest_size_px=crest_size_px, tie_info=tie_info)


# --- Page setup: background image and global styles ---
setup.general_setup()
setup.add_bg_from_local("background.png")

# --- Page header ---
setup.render_page_header("Harry Potter App")

# --- User greeting and content ---
# user_information = [first_name, last_name, house]
st.subheader(f"{st.session_state.user_information[0]} {st.session_state.user_information[1]}")

house = st.session_state.user_information[2]

if house == "none":
    # User hasn't been sorted yet — show the quiz entry button
    if st.button("🪄Hogwarts Sorting"):
        st.switch_page("pages/hogwarts_sorting.py")
elif house == "Gryffindor":
    render_gryffindor(crest_size_px=200)
elif house == "Hufflepuff":
    render_hufflepuff(crest_size_px=200)
elif house == "Ravenclaw":
    render_ravenclaw(crest_size_px=200)
elif house == "Slytherin":
    render_slytherin(crest_size_px=200)
