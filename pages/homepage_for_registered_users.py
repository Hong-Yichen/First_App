import streamlit as st
import base64
import setup
import os
from typing import Optional, Dict

# --- House data (edit paths/colors/descriptions if you want) ---
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
    if not path or not os.path.exists(path):
        return None
    mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"

def _render_house_banner(chosen_house: str, crest_size_px: int = 160, tie_info: Optional[list] = None) -> None:
    """Internal renderer used by the per-house functions."""
    if not chosen_house:
        st.warning("No house provided.")
        return

    color = HOUSE_COLORS.get(chosen_house, "#222")
    desc = HOUSE_DESCS.get(chosen_house, "")
    crest_path = CREST_PATHS.get(chosen_house)
    crest_data = _img_to_data_uri(crest_path)

    img_html = ""
    if crest_data:
        img_html = (
            f"<div class='crest-wrap' style='display:flex;align-items:center;justify-content:center;'>"
            f"<img src='{crest_data}' style='max-width:{crest_size_px}px;height:auto;border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,0.30);'/>"
            f"</div>"
        )

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

# --- Per-house wrapper functions ---
def render_gryffindor(crest_size_px: int = 160, tie_info: Optional[list] = None) -> None:
    _render_house_banner("Gryffindor", crest_size_px=crest_size_px, tie_info=tie_info)

def render_hufflepuff(crest_size_px: int = 160, tie_info: Optional[list] = None) -> None:
    _render_house_banner("Hufflepuff", crest_size_px=crest_size_px, tie_info=tie_info)

def render_ravenclaw(crest_size_px: int = 160, tie_info: Optional[list] = None) -> None:
    _render_house_banner("Ravenclaw", crest_size_px=crest_size_px, tie_info=tie_info)

def render_slytherin(crest_size_px: int = 160, tie_info: Optional[list] = None) -> None:
    _render_house_banner("Slytherin", crest_size_px=crest_size_px, tie_info=tie_info)

# --- Example usage ---
# Call one of these after you determine which house to show:
# render_gryffindor(crest_size_px=200)
# render_ravenclaw(crest_size_px=180, tie_info=['Ravenclaw','Slytherin'])
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
st.subheader(f"{st.session_state.user_information[0]} {st.session_state.user_information[1]}")
if st.session_state.user_information[2] == "none":
    if st.button("🪄Hogwarts Sorting"):
        st.switch_page("pages/hogwarts_sorting.py")
elif st.session_state.user_information[2] == "Gryffindor":
    render_gryffindor(crest_size_px=200)
elif st.session_state.user_information == "Hufflepuff":
    render_hufflepuff(crest_size_px=200)
elif st.session_state.user_information == "Ravenclaw":
    render_ravenclaw(crest_size_px=200)
elif st.session_state.user_information == "Slytherin":
    render_slytherin(crest_size_px=200)