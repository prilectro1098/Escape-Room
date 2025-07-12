import streamlit as st
import json
import random
import time
import os

# ✅ Must be first
st.set_page_config(page_title="Escape Room", layout="centered")

# 🎨 Theme Selector
theme = st.sidebar.selectbox("🎨 Choose Theme", [
    "Electric Neon",
    "Candy Pop",
    "Ocean Breeze",
    "Jungle Adventure",
    "Royal Velvet"
])

# Theme color mappings
theme_css = {
    "Electric Neon": {"bg": "#0f0f0f", "fg": "#39ff14"},
    "Candy Pop": {"bg": "#fff0f5", "fg": "#ff1493"},
    "Ocean Breeze": {"bg": "#e0f7fa", "fg": "#006064"},
    "Jungle Adventure": {"bg": "#f1f8e9", "fg": "#2e7d32"},
    "Royal Velvet": {"bg": "#4a148c", "fg": "#ffd700"},
}
colors = theme_css.get(theme, theme_css["Candy Pop"])

# 💅 Apply theme styling
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {colors['bg']};
        color: {colors['fg']};
    }}
    label, .stRadio label, .stRadio div, .stSelectbox div {{
        color: {colors['fg']} !important;
        font-weight: 600;
    }}
    .stSidebar > div {{
        background-color: {colors['bg']};
        color: {colors['fg']} !important;
    }}
    .stSelectbox label, .stTextInput label {{
        color: {colors['fg']} !important;
        font-weight: 600;
    }}
    </style>
""", unsafe_allow_html=True)

# 📁 Puzzle File
PUZZLE_FILE = "puzzles.json"

def load_puzzles():
    if os.path.exists(PUZZLE_FILE):
        with open(PUZZLE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_puzzles(puzzles):
    with open(PUZZLE_FILE, "w", encoding="utf-8") as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

def get_unique_categories(puzzles):
    return sorted(list(set(p["category"] for p in puzzles if "category" in p)))

# ⏱️ Timer
def start_timer():
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

def get_time_left(max_seconds):
    elapsed = time.time() - st.session_state.start_time
    return max(0, int(max_seconds - elapsed))

def cpu_guess(correct_answer):
    return correct_answer if random.random() > 0.5 else "wrong"

# 👥 Player avatars with titles
emoji_options = {
    "😎 Cool Hacker": "😎",
    "👩‍💻 Code Queen": "👩‍💻",
    "🧙‍♂️ Puzzle Wizard": "🧙‍♂️",
    "👸 Royal Solver": "👸",
    "🧞‍♂️ Genie Master": "🧞‍♂️",
    "🤠 Cowboy Coder": "🤠",
    "🧟 Brain Eater": "🧟",
    "🚀 Space Solver": "🚀"
}

# 🎮 Game Modes
st.title("🧙 Escape Room: Puzzle Game")
mode = st.radio("Select Mode", ["Single Player", "Multiplayer", "Play vs CPU", "Admin Panel"])

if mode == "Admin Panel":
    st.subheader("🔐 Admin Login")
    password = st.text_input("Enter admin password:", type="password")
    if password == "admin123":
        st.success("Logged in as Admin ✅")

        puzzles = load_puzzles()

        st.subheader("📋 All Puzzles")
        for i, pz in enumerate(puzzles):
            st.markdown(f"{i+1}. **{pz['title']}** — *{pz['level']}*, 🧠 *{pz['category']}*")

        st.markdown("---")
        st.subheader("➕ Add New Puzzle")
        new_title = st.text_input("Title")
        new_q = st.text_area("Question")
        new_ans = st.text_input("Answer")
        new_hint = st.text_input("Hint (optional)")
        new_level = st.selectbox("Level", ["easy", "medium", "hard"])
        existing_categories = get_unique_categories(puzzles)
        new_category = st.selectbox("Category", existing_categories + ["Other"])
        if new_category == "Other":
            new_category = st.text_input("Enter new category")

        if st.button("Add Puzzle"):
            if new_title and new_q and new_ans and new_category:
                puzzles.append({
                    "title": new_title,
                    "question": new_q,
                    "answer": new_ans,
                    "hint": new_hint,
                    "level": new_level,
                    "category": new_category
                })
                save_puzzles(puzzles)
                st.success("✅ Puzzle added!")
                st.experimental_rerun()
            else:
                st.error("Please fill all fields")

        st.markdown("---")
        st.subheader("❌ Delete Puzzle")
        del_title = st.text_input("Enter title to delete")
        if st.button("Delete"):
            new_puzzles = [pz for pz in puzzles if pz['title'] != del_title]
            if len(new_puzzles) < len(puzzles):
                save_puzzles(new_puzzles)
                st.success("Puzzle deleted.")
                st.experimental_rerun()
            else:
                st.warning("Title not found.")

    else:
        st.warning("Enter correct admin password to access.")

else:
    p1 = st.text_input("Player 1 Name")
    avatar1_choice = st.selectbox("Choose Avatar for Player 1", list(emoji_options.keys()), key="avatar1")
    avatar1 = emoji_options[avatar1_choice]

    if mode == "Multiplayer":
        p2 = st.text_input("Player 2 Name")
        avatar2_choice = st.selectbox("Choose Avatar for Player 2", list(emoji_options.keys()), key="avatar2")
        avatar2 = emoji_options[avatar2_choice]
    elif mode == "Play vs CPU":
        p2 = "CPU"
        avatar2 = "🤖"
    else:
        p2 = None
        avatar2 = None

    if p1 and (mode == "Single Player" or (p2 and mode != "Single Player")):
        puzzles = load_puzzles()
        all_categories = get_unique_categories(puzzles)
        level = st.selectbox("🎯 Select Level", ["easy", "medium", "hard"])
        category = st.selectbox("🧠 Select Category", all_categories)

        filtered = [pz for pz in puzzles if pz["level"] == level and pz["category"] == category]
        if not filtered:
            st.warning("No puzzles found for this selection.")
        else:
            puzzles = random.sample(filtered, min(3, len(filtered)))
            scores = {p1: 0}
            if p2: scores[p2] = 0
            current_player = p1
            current_avatar = avatar1
            result_log = []

            start_timer()
            max_time = 90

            for i, pz in enumerate(puzzles):
                time_left = get_time_left(max_time)
                if time_left == 0:
                    st.error("⏰ Time’s up! Game Over!")
                    break

                st.markdown(f"⏱ Time Left: {time_left}s")
                st.subheader(f"Puzzle {i+1}: {pz['title']}")
                st.markdown(pz["question"])

                if st.button(f"💡 Hint for Puzzle {i+1}", key=f"hint{i}"):
                    st.info(pz.get("hint", "No hint"))

                if current_player == "CPU":
                    cpu_ans = cpu_guess(pz["answer"])
                    st.markdown(f"🤖 CPU guesses: **{cpu_ans}**")
                    correct = cpu_ans.lower() == pz["answer"].lower()
                    result_log.append((pz["title"], f"{avatar2} {p2}", correct))
                    if correct: scores[p2] += 1
                else:
                    ans = st.text_input(f"{current_avatar} {current_player}, your answer:", key=f"{i}-{current_player}")
                    if ans:
                        correct = ans.strip().lower() == pz["answer"].lower()
                        result_log.append((pz["title"], f"{current_avatar} {current_player}", correct))
                        if correct:
                            st.success("✅ Correct!")
                            scores[current_player] += 1
                        else:
                            st.error("❌ Incorrect.")

                if mode in ["Multiplayer", "Play vs CPU"]:
                    if current_player == p1:
                        current_player, current_avatar = p2, avatar2
                    else:
                        current_player, current_avatar = p1, avatar1

            st.subheader("🏉 Final Scores")
            for name, scr in scores.items():
                st.markdown(f"**{name}** — {scr} / {len(puzzles)}")

            st.subheader("🗾️ Puzzle Summary")
            for title, player, correct in result_log:
                icon = "✅" if correct else "❌"
                st.markdown(f"{icon} {title} — by **{player}**")

            # 🎉 Final Escape Message
            if all([correct for _, _, correct in result_log]):
                st.success("🎉 Congratulations! You've cracked all the puzzles and escaped the room! 🔓🚪")
                st.markdown("""
                    <div style='font-size:22px; font-weight:bold; color:lime;'>You are a true Puzzle Master 🧠💥</div>
                    <div style='font-size:18px; margin-top:10px;'>🏃‍♂️🏃‍♀️ You ran past lasers, dodged traps, and nailed riddles like a boss!</div>
                    <div style='margin-top:10px;'>🔥 Want to challenge yourself again? Choose a harder level next time!</div>
                """, unsafe_allow_html=True)
            else:
                st.warning("🚪 You solved some, but the final door stayed shut! Try again to escape completely!")

            st.balloons()
