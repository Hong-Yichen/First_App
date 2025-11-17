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
        "q": "A single, unlabelled bottle sits on a windowsill. What catches your eye?",
        "options": {
            "A faded smear where a thumb often rested.": {"Hufflepuff": 2},
            "A tiny stamped sigil, almost worn away.": {"Slytherin": 2},
            "The way a sliver of moonlight floods its shadow.": {"Ravenclaw": 2},
            "A cork scored by a bold, impatient twist.": {"Gryffindor": 2},
        }
    },
    {
        "q": "You hear a rumor of a midnight duel. What thought crosses your mind first?",
        "options": {
            "Who will be left out — can someone be kept safe?": {"Hufflepuff": 2},
            "Which angle promises the cleverest surprise?": {"Slytherin": 2},
            "I should see it — the spectacle will teach me something.": {"Gryffindor": 2},
            "What are the facts behind the whispers; note them.": {"Ravenclaw": 2},
        }
    },
    {
        "q": "A dusty book falls open to a page with four drawings. Which draws you?",
        "options": {
            "A map full of tiny notations and marginalia.": {"Ravenclaw": 2},
            "A hearth where three figures share a covered pot.": {"Hufflepuff": 2},
            "A lone figure climbing toward a banner.": {"Gryffindor": 2},
            "A hand sliding a sealed note into a sleeve.": {"Slytherin": 2},
        }
    },
    {
        "q": "You are given a single candle and told to keep watch. You:",
        "options": {
            "Place it where a friend might read by its light.": {"Hufflepuff": 2},
            "Set it high so its glow meets the horizon.": {"Gryffindor": 2},
            "Mark its burn pattern as if it were a message.": {"Ravenclaw": 2},
            "Shift it so the shadows hide what you need hidden.": {"Slytherin": 2},
        }
    },
    {
        "q": "You find four scarves in a chest. Which texture do you note first?",
        "options": {
            "The soft, worn weave that smells faintly of home.": {"Hufflepuff": 2},
            "A thread stitched through the edge, almost like a code.": {"Ravenclaw": 2},
            "A bold, frayed edge where the wind met it many times.": {"Gryffindor": 2},
            "A hidden pocket sewn into the seam.": {"Slytherin": 2},
        }
    },
    {
        "q": "A street performer offers you a choice: a trick that dazzles, a tune that soothes, a riddle, or a bargain. You choose:",
        "options": {
            "The tune — there is solace in small sounds.": {"Hufflepuff": 2},
            "The riddle — clear thinking is its own reward.": {"Ravenclaw": 2},
            "The dazzling trick — life needs a brave spark.": {"Gryffindor": 2},
            "The bargain — a small trade now can shape later.": {"Slytherin": 2},
        }
    },
    {
        "q": "On a note left under your door is only one word. Which would please you most?",
        "options": {
            "‘Stay’ — company matters when night is long.": {"Hufflepuff": 2},
            "‘Look’ — there is something to be deciphered.": {"Ravenclaw": 2},
            "‘Now’ — the moment asks for action.": {"Gryffindor": 2},
            "‘Remember’ — secrets may be currency.": {"Slytherin": 2},
        }
    },
    {
        "q": "A sudden storm blows through. What do you secure first?",
        "options": {
            "The windows so a neighbour’s cat won’t be exposed.": {"Hufflepuff": 2},
            "A small journal that holds neat lists and sketches.": {"Ravenclaw": 2},
            "The flagpole — it feels wrong to leave it loose.": {"Gryffindor": 2},
            "The trunks with locks you can later use for leverage.": {"Slytherin": 2},
        }
    },
    {
        "q": "You are shown an old portrait with eyes that seem almost alive. What do you do?",
        "options": {
            "Leave a gentle bow; manners matter to so many frames.": {"Hufflepuff": 2},
            "Stand back and read the plate beneath with care.": {"Ravenclaw": 2},
            "Step forward and challenge the stare — testing is honest.": {"Gryffindor": 2},
            "Watch how servants move past that portrait; small cues matter.": {"Slytherin": 2},
        }
    },
    {
        "q": "Four lanterns mark four gates. Which light would you follow?",
        "options": {
            "The nearest lantern where the road smells of baking.": {"Hufflepuff": 2},
            "The one with the faintest ink marks — someone notes the way.": {"Ravenclaw": 2},
            "The lantern on the cliff path where horizons open.": {"Gryffindor": 2},
            "The low lamp nearest a narrow door, half-hidden.": {"Slytherin": 2},
        }
    },
    {
        "q": "You stumble on a chessboard mid-game. Which piece do you move if you must?",
        "options": {
            "A loyal pawn that keeps the line steady.": {"Hufflepuff": 2},
            "A piece that will reveal the pattern of play.": {"Ravenclaw": 2},
            "A knight that charges into new space.": {"Gryffindor": 2},
            "A quiet piece that shifts control subtly.": {"Slytherin": 2},
        }
    },
    {
        "q": "There is a bonfire and four tales offered. Which kind of tale do you want to hear?",
        "options": {
            "A little story of generosity that made a small life better.": {"Hufflepuff": 2},
            "A curious anecdote with a lesson hidden between lines.": {"Ravenclaw": 2},
            "An account of a bold, foolish triumph.": {"Gryffindor": 2},
            "A recollection of a cunning plan that turned the game.": {"Slytherin": 2},
        }
    },
    {
        "q": "A sealed parcel contains either a charm, a map, a badge, or a note. Which possibility excites you most?",
        "options": {
            "A badge; you like to carry a small story visibly.": {"Gryffindor": 2},
            "A charm that comforts quietly in a pocket.": {"Hufflepuff": 2},
            "A map that asks questions rather than answers them.": {"Ravenclaw": 2},
            "A note that hints at a prefered beneficiary.": {"Slytherin": 2},
        }
    },
    {
        "q": "In a quiet hour, you prefer to occupy a corner with:",
        "options": {
            "A woven blanket and someone’s warm laughter.": {"Hufflepuff": 2},
            "A tall stack of slim volumes with dusty spines.": {"Ravenclaw": 2},
            "An open window where the first bird calls in the morning.": {"Gryffindor": 2},
            "A locked chest that opens only after you return.": {"Slytherin": 2},
        }
    },
    {
        "q": "Four footprints lead away from a gate. Which path would you follow quietly?",
        "options": {
            "The shallow, careful prints that stop at thresholds.": {"Hufflepuff": 2},
            "The prints that cut straight for a skylit courtyard.": {"Gryffindor": 2},
            "The tiny, detailed trod that seems to pause and change pace.": {"Ravenclaw": 2},
            "The narrowing set of tracks that turn into an alley.": {"Slytherin": 2},
        }
    },
    {
        "q": "Someone offers to teach you a little trick. You prefer it to be:",
        "options": {
            "A comfort trick that warms small troubles.": {"Hufflepuff": 2},
            "A practical method that works reliably every time.": {"Ravenclaw": 2},
            "A spectacle that makes onlookers clap.": {"Gryffindor": 2},
            "A clever sleight that helps you later in quiet rooms.": {"Slytherin": 2},
        }
    },
    {
        "q": "A narrow letter arrives: one line, one sentence. Which would you hope it says?",
        "options": {
            "‘Come, there’s room at the table.’": {"Hufflepuff": 2},
            "‘Look here — the margin contains the surprising part.’": {"Ravenclaw": 2},
            "‘Bring your courage; it will be needed.’": {"Gryffindor": 2},
            "‘Meet me where the shutters close after dusk.’": {"Slytherin": 2},
        }
    },
    {
        "q": "A piece of music plays faintly in the hall. Which strand do you catch?",
        "options": {
            "A slow, steady rhythm like a heart at rest.": {"Hufflepuff": 2},
            "A sequence that repeats with intricate variation.": {"Ravenclaw": 2},
            "A rising fanfare that asks to be answered at once.": {"Gryffindor": 2},
            "A thin, secretive passage that slips between bars.": {"Slytherin": 2},
        }
    },
    {
        "q": "Before dawn you must set an extra place at table. Who do you think of?",
        "options": {
            "Someone who always needed warmth and was shy to ask.": {"Hufflepuff": 2},
            "The scholar who left notes half-finished in margins.": {"Ravenclaw": 2},
            "The bold young thing who would take the next dawn.": {"Gryffindor": 2},
            "A quiet ally whose help will be worth remembering.": {"Slytherin": 2},
        }
    },
    {
        "q": "At journey's end you are richest in one small thing. Which would you hope it is?",
        "options": {
            "A pocket of returned kindnesses and small friends.": {"Hufflepuff": 2},
            "A book with pages that still make you think anew.": {"Ravenclaw": 2},
            "A scar earned from a moment you would do again.": {"Gryffindor": 2},
            "A sealed agreement whose terms favour your plans.": {"Slytherin": 2},
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