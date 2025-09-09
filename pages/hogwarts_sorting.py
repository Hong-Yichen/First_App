import streamlit as st
import random
import os
import base64
import setup

setup.general_setup()
setup.add_bg_from_local("background.png")

st.set_page_config(page_title="Hogwarts House Quiz", page_icon="🪄", layout="centered")
# -----------------------------
# Houses, colors, crest paths
# -----------------------------
HOUSES = {
    "Gryffindor": "Bravery, daring, nerve and chivalry.",
    "Hufflepuff": "Hard work, patience, justice and loyalty.",
    "Ravenclaw": "Intelligence, learning, wisdom and wit.",
    "Slytherin": "Ambition, cunning, resourcefulness and leadership."
}

HOUSE_COLORS = {
    "Gryffindor": "#7F0909",
    "Hufflepuff": "#ECB939",
    "Ravenclaw": "#0E1A40",
    "Slytherin": "#1A472A"
}

# Put PNG crest images in ./crests/ with these names (optional)
CREST_PATHS = {
    "Gryffindor": "crests/gryffindor.png",
    "Hufflepuff": "crests/hufflepuff.png",
    "Ravenclaw": "crests/ravenclaw.png",
    "Slytherin": "crests/slytherin.png"
}

# -----------------------------
# Full pool of 12 questions
# -----------------------------
QUESTION_POOL = [
    {
        "q": "It is dawn and you find yourself walking alone in the forest. You come across four paths. Which do you follow?",
        "options": {
            "A winding trail up toward the mountain peak.": {"Gryffindor": 2},
            "A sunny lane bordered with wildflowers.": {"Hufflepuff": 2},
            "A quiet path leading to an ancient library ruin.": {"Ravenclaw": 2},
            "A shadowy track that disappears into the mist.": {"Slytherin": 2},
        }
    },
    {
        "q": "Which artifact intrigues you the most?",
        "options": {
            "A tarnished sword said to have never lost a battle.": {"Gryffindor": 2},
            "A wooden cup that always refills with water.": {"Hufflepuff": 2},
            "A book that whispers its secrets when the moon is full.": {"Ravenclaw": 2},
            "A ring that grants influence over those who wear it.": {"Slytherin": 2},
        }
    },
    {
        "q": "One of your classmates has been wrongly accused of something. You would:",
        "options": {
            "Speak up loudly, even if no one else does.": {"Gryffindor": 2},
            "Stay by their side and quietly defend them.": {"Hufflepuff": 2},
            "Investigate the facts and prove their innocence.": {"Ravenclaw": 2},
            "Look for who benefits from the accusation and expose them.": {"Slytherin": 2},
        }
    },
    {
        "q": "You may choose a magical companion. Which draws you in?",
        "options": {
            "A phoenix that blazes brightly against the night sky.": {"Gryffindor": 2},
            "A loyal badger that never abandons you.": {"Hufflepuff": 2},
            "A raven that brings cryptic messages.": {"Ravenclaw": 2},
            "A serpent with eyes that gleam like emeralds.": {"Slytherin": 2},
        }
    },
    {
        "q": "A locked door stands before you. Behind it is something valuable. You:",
        "options": {
            "Kick it open, ready to face whatever’s inside.": {"Gryffindor": 2},
            "Wait patiently — the right key will appear eventually.": {"Hufflepuff": 2},
            "Examine the mechanism and solve the lock’s puzzle.": {"Ravenclaw": 2},
            "Pick the lock swiftly before anyone notices.": {"Slytherin": 2},
        }
    },
    {
        "q": "A traveler offers four maps. You pick:",
        "options": {
            "The map marked with daring routes and hidden wonders.": {"Gryffindor": 2},
            "The map that winds gently among peaceful villages.": {"Hufflepuff": 2},
            "The map annotated with riddles and scholarly notes.": {"Ravenclaw": 2},
            "The map with secret shortcuts and private paths.": {"Slytherin": 2},
        }
    },
    {
        "q": "When reading a story, you most enjoy:",
        "options": {
            "Scenes of bold heroics and dramatic triumphs.": {"Gryffindor": 2},
            "Warm passages about friendship and simple joys.": {"Hufflepuff": 2},
            "Intricate plots, clever puzzles and ideas.": {"Ravenclaw": 2},
            "Schemes, subtle rivalries and clever plans.": {"Slytherin": 2},
        }
    },
    {
        "q": "At a celebration you are most likely to:",
        "options": {
            "Leap into the centre and start the loudest toast.": {"Gryffindor": 2},
            "Make sure everyone has a seat and a plate.": {"Hufflepuff": 2},
            "Observe quietly and strike up thoughtful conversation.": {"Ravenclaw": 2},
            "Whisper to a few people and steer the evening’s course.": {"Slytherin": 2},
        }
    },
    {
        "q": "You discover a strange creature in need. You:",
        "options": {
            "Rush in bravely to save it from immediate danger.": {"Gryffindor": 2},
            "Tend to it kindly and patiently nurse it back.": {"Hufflepuff": 2},
            "Study it and learn how best to help.": {"Ravenclaw": 2},
            "Consider whether caring for it might give you an advantage.": {"Slytherin": 2},
        }
    },
    {
        "q": "A professor offers an optional challenge: high risk, high reward. You:",
        "options": {
            "Sign up immediately — risks are part of learning.": {"Gryffindor": 2},
            "Ask if you can help someone else take part instead.": {"Hufflepuff": 2},
            "Read all past examples before deciding to join.": {"Ravenclaw": 2},
            "Calculate how it improves your position and then decide.": {"Slytherin": 2},
        }
    },
    {
        "q": "If you could own one possession, you would choose:",
        "options": {
            "An heirloom sword with a storied past.": {"Gryffindor": 2},
            "A simple but enchanted charm that comforts you.": {"Hufflepuff": 2},
            "A curious instrument that reveals hidden patterns.": {"Ravenclaw": 2},
            "A signet that opens doors in quiet circles.": {"Slytherin": 2},
        }
    },
    {
        "q": "Late at night you prefer to:",
        "options": {
            "Go on an impromptu walk under the stars.": {"Gryffindor": 2},
            "Share tea and stories with a close friend.": {"Hufflepuff": 2},
            "Lose yourself in books and thoughtful study.": {"Ravenclaw": 2},
            "Work quietly on something that will matter later.": {"Slytherin": 2},
        }
    }
]

# -----------------------------
# App configuration and helpers
# -----------------------------
QUESTIONS_TO_SHOW = 7  # pick 7 of the 12 each session

def img_to_data_uri(path):
    """Return data URI for PNG/JPG crest (or None if not found)."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
    return f"data:{mime};base64,{b64}"

# -----------------------------
# Session state initialization
# -----------------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "result" not in st.session_state:
    st.session_state.result = None
if "tie_info" not in st.session_state:
    st.session_state.tie_info = None
if "shuffled_options" not in st.session_state:
    st.session_state.shuffled_options = {}
if "question_indices" not in st.session_state:
    # randomly choose QUESTIONS_TO_SHOW indices from pool once per session
    st.session_state.question_indices = random.sample(range(len(QUESTION_POOL)), QUESTIONS_TO_SHOW)

# -----------------------------
# UI: header (clean)
# -----------------------------
st.markdown(          #For text "🪄Hogwarts Sorting"
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

    <h1 class="magic-title">🪄Hogwarts Sorting</h1>
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

# -----------------------------
# Render the selected questions
# -----------------------------
for display_idx, q_idx in enumerate(st.session_state.question_indices, start=1):
    qdata = QUESTION_POOL[q_idx]
    key = f"q{display_idx}"

    # Shuffle options once per question key in the session
    if key not in st.session_state.shuffled_options:
        opts = list(qdata["options"].keys())
        random.shuffle(opts)
        st.session_state.shuffled_options[key] = opts

    opts_shuffled = st.session_state.shuffled_options[key]

    if not st.session_state.submitted:
        # placeholder prevents any default selection bias
        choices = ["-- select an option --"] + opts_shuffled
        selection = st.radio(f"**Q{display_idx}. {qdata['q']}**", choices, key=key)
        st.session_state.answers[key] = None if selection == "-- select an option --" else selection
    else:
        # Locked view after submission: plain text that can't be edited
        st.markdown(f"**Q{display_idx}. {qdata['q']}**")
        selected_text = st.session_state.answers.get(key, "No answer")
        st.markdown(f"> {selected_text}")

st.write("")  # spacing

# -----------------------------
# Compute result
# -----------------------------
def compute_result_and_lock():
    # Tally scores
    scores = {h: 0 for h in HOUSES}
    for display_idx, q_idx in enumerate(st.session_state.question_indices, start=1):
        key = f"q{display_idx}"
        chosen_text = st.session_state.answers.get(key)
        if not chosen_text:
            continue
        qmap = QUESTION_POOL[q_idx]["options"]
        mapping = qmap.get(chosen_text)
        if mapping:
            for house, pts in mapping.items():
                scores[house] += pts

    max_score = max(scores.values())
    top = [h for h, s in scores.items() if s == max_score]

    if len(top) == 1:
        chosen = top[0]
        st.session_state.tie_info = None
    else:
        concat = "|".join([str(st.session_state.answers.get(f"q{i}")) for i in range(1, QUESTIONS_TO_SHOW + 1)])
        seed = abs(hash(concat))
        chosen = random.Random(seed).choice(top)
        st.session_state.tie_info = top

    st.session_state.result = chosen
    st.session_state.submitted = True

# -----------------------------
# Submit button (disabled after submit)
# -----------------------------
if not st.session_state.submitted:
    if st.button("✨ Reveal My House"):
        # validate all questions answered
        missing = [k for k, v in st.session_state.answers.items() if not v]
        if missing:
            st.warning("Please answer all questions before submitting.")
        else:
            compute_result_and_lock()

# -----------------------------
# Display result banner (grid layout — responsive, prevents cramped text)
# -----------------------------
if st.session_state.submitted and st.session_state.result:
    chosen = st.session_state.result
    color = HOUSE_COLORS.get(chosen, "#222")
    desc = HOUSES[chosen]
    crest_path = CREST_PATHS.get(chosen)
    crest_data_uri = img_to_data_uri(crest_path) if crest_path else None

    # Use a grid with minmax(0,1fr) so text area can shrink properly without forcing tiny columns.
    # crest column set to 160px (adjust as desired). On narrow screens the grid stacks so text isn't cramped.
    img_html = ""
    if crest_data_uri:
        img_html = (
            f"<div class='crest-wrap' style='display:flex;align-items:center;justify-content:center;'>"
            f"<img src='{crest_data_uri}' class='crest-img' style='max-width:160px;height:auto;border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,0.30);'/>"
            f"</div>"
        )

    # CSS included in the same HTML block for isolation
    banner_html = f"""
    <style>
      /* Ensure the text container can shrink/grow without pushing layout into tiny columns */
      .sh-banner {{
        background:{color};
        padding:22px;
        border-radius:12px;
        display:grid;
        grid-template-columns: minmax(0, 1fr) 160px;
        gap:20px;
        align-items:center;
        color: white;
        max-width:100%;
      }}
      .sh-banner .text {{
        min-width:0; /* very important to allow proper flexing in grid */
      }}
      .sh-banner p {{
        margin:0;
        font-size:16px;
        line-height:1.5;
        opacity:0.98;
        overflow-wrap:break-word;
        word-break:normal;
        white-space:normal;
      }}
      /* Responsive: stack crest below text on small screens */
      @media (max-width:720px) {{
        .sh-banner {{
          grid-template-columns: 1fr;
          text-align:center;
        }}
        .sh-banner .text {{
          order:0;
        }}
        .crest-wrap {{
          order:1;
          margin-top:12px;
        }}
        .sh-banner p {{ text-align:center; }}
      }}
    </style>

    <div class="sh-banner">
      <div class="text">
        <h1 style="margin:0 0 8px 0;font-family:Georgia, 'Times New Roman', serif;font-size:30px;letter-spacing:0.6px;">
          🎉 {chosen}
        </h1>
        <p>{desc}</p>
      </div>
      {img_html}
    </div>
    """

    st.markdown(banner_html, unsafe_allow_html=True)