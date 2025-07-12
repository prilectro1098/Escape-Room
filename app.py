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

    .escape-animation {{
        text-align: center;
        font-size: 2em;
        animation: glow 2s ease-in-out infinite alternate;
    }}

    @keyframes glow {{
        from {{ text-shadow: 0 0 10px {colors['fg']}; }}
        to {{ text-shadow: 0 0 20px {colors['fg']}, 0 0 30px {colors['fg']}; }}
    }}

    .door-container {{
        text-align: center;
        padding: 20px;
        border: 3px solid {colors['fg']};
        border-radius: 15px;
        margin: 20px 0;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }}

    .door-button {{
        background: linear-gradient(45deg, {colors['fg']}, {colors['bg']});
        color: {colors['bg']};
        border: none;
        padding: 15px 20px;
        border-radius: 10px;
        font-size: 1.2em;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin: 10px 0;
    }}

    .door-button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 20px {colors['fg']};
    }}

    .victory-message {{
        background: linear-gradient(45deg, {colors['fg']}, {colors['bg']});
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        animation: bounce 2s infinite;
    }}

    @keyframes bounce {{
        0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
        40% {{ transform: translateY(-10px); }}
        60% {{ transform: translateY(-5px); }}
    }}

    .category-card {{
        background: rgba(255,255,255,0.1);
        border: 2px solid {colors['fg']};
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }}

    .category-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }}
    </style>
""", unsafe_allow_html=True)

# 📁 Puzzle File
PUZZLE_FILE = "puzzles.json"

def load_puzzles():
    if os.path.exists(PUZZLE_FILE):
        with open(PUZZLE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return get_default_puzzles()

def get_default_puzzles():
    """Return default puzzles with expanded Indian humor categories"""
    return [
        # Original puzzles from your file
        {
            "title": "The Golgappa Puzzle",
            "question": "I'm round and crunchy, I hold spicy water and khatta-meetha chaat. One bite and I'm gone. What am I?\n\nA) Samosa\nB) Dhokla\nC) Golgappa",
            "answer": "C",
            "hint": "Also called Pani Puri in Mumbai!",
            "level": "easy",
            "category": "Desi Food Riddles"
        },
        {
            "title": "Rickshaw Race",
            "question": "I have three wheels and make a lot of noise, painted with funny slogans, and I zig-zag through traffic. Who am I?\n\nA) Auto Rickshaw\nB) Tractor\nC) Bullet Bike",
            "answer": "A",
            "hint": "Yellow and black or green sometimes!",
            "level": "easy",
            "category": "Desi Transport"
        },
        {
            "title": "Lassi Logic",
            "question": "I'm a cool Punjabi drink, white and thick, served in a big steel glass with malai. What am I?\n\nA) Lassi\nB) Chaas\nC) Cold Coffee",
            "answer": "A",
            "hint": "Dahi se banta hai!",
            "level": "medium",
            "category": "Desi Food Riddles"
        },
        # New Indian Office/Student Life puzzles
        {
            "title": "Chai Time Mystery",
            "question": "Office mein sabse important meeting kaun si hoti hai jo bina agenda ke hoti hai?\n\nA) Board Meeting\nB) Chai Break\nC) Team Meeting",
            "answer": "B",
            "hint": "Gossip aur discussion ka perfect time!",
            "level": "easy",
            "category": "Desi Office Life"
        },
        {
            "title": "Jugaad Master",
            "question": "Desi innovation ka naam kya hai jo kaam bhi kare aur dekh ke hassi bhi aaye?\n\nA) Technology\nB) Jugaad\nC) Engineering",
            "answer": "B",
            "hint": "Indian way of problem solving!",
            "level": "easy",
            "category": "Desi Comedy"
        },
        {
            "title": "Sharma Ji Ka Beta",
            "question": "Har Indian parent ka favorite example kaun hai?\n\nA) Sachin Tendulkar\nB) Sharma Ji ka Beta\nC) APJ Abdul Kalam",
            "answer": "B",
            "hint": "Topper hai, engineer hai, doctor hai!",
            "level": "medium",
            "category": "Desi Family Drama"
        },
        {
            "title": "Aam Aadmi Problem",
            "question": "Kya cheez hai jo free mein milti hai par sabse jyada valuable hai?\n\nA) Wi-Fi Password\nB) Advice\nC) Parking Space",
            "answer": "B",
            "hint": "Sabke paas hai dene ke liye!",
            "level": "easy",
            "category": "Desi Life Hacks"
        },
        {
            "title": "Local Train Logic",
            "question": "Mumbai mein kya cheez hai jo time pe nahi aati par phir bhi sabka bharosa hai?\n\nA) Local Train\nB) Bus\nC) Auto",
            "answer": "A",
            "hint": "Mumbai ki lifeline!",
            "level": "medium",
            "category": "Desi Transport"
        },
        {
            "title": "Mummy Magic",
            "question": "Kya cheez hai jo mummy ke paas unlimited quantity mein hai?\n\nA) Paisa\nB) Pyaar\nC) Lecture",
            "answer": "C",
            "hint": "Subah se raat tak available!",
            "level": "easy",
            "category": "Desi Family Drama"
        },
        {
            "title": "Dhobi Ghat Mystery",
            "question": "Kahan pe kapde saaf hote hain par paani ganda hota hai?\n\nA) Washing Machine\nB) Dhobi Ghat\nC) River",
            "answer": "B",
            "hint": "Mumbai famous hai iske liye!",
            "level": "medium",
            "category": "Desi Life Hacks"
        },
        {
            "title": "Bollywood Logic",
            "question": "Kya cheez hai jo physics ke rules nahi manti?\n\nA) Bollywood Fight Scene\nB) Magic\nC) Dreams",
            "answer": "A",
            "hint": "Cars fly, heroes don't die!",
            "level": "easy",
            "category": "Bollywood Masala"
        },
        {
            "title": "Paani Puri Economics",
            "question": "Kya cheez hai jo 5 rupee mein khushi de deti hai?\n\nA) Chocolate\nB) Paani Puri\nC) Smile",
            "answer": "B",
            "hint": "Teeka, meetha, khatta - sabka mix!",
            "level": "easy",
            "category": "Desi Food Riddles"
        },
        {
            "title": "Cooler vs AC",
            "question": "Summer mein kya cheez hai jo gareeb ka AC hai?\n\nA) Fan\nB) Cooler\nC) Ice",
            "answer": "B",
            "hint": "Hawaa with water spray!",
            "level": "medium",
            "category": "Desi Life Hacks"
        },
        {
            "title": "Hostel Life",
            "question": "Kya cheez hai jo hostel mein sharing ki jaati hai par sharing nahi karni chahiye?\n\nA) Clothes\nB) Toothbrush\nC) Food",
            "answer": "B",
            "hint": "Personal hygiene item!",
            "level": "easy",
            "category": "Student Life"
        },
        {
            "title": "Maggi Magic",
            "question": "Student life mein kya cheez hai jo 2 minute mein banti hai par happiness lifetime ki deti hai?\n\nA) Tea\nB) Maggi\nC) Friendship",
            "answer": "B",
            "hint": "Har flavor mein available!",
            "level": "easy",
            "category": "Student Life"
        },
        {
            "title": "Barber Shop Philosophy",
            "question": "Kahan pe sabse deep conversations hote hain?\n\nA) Coffee Shop\nB) Barber Shop\nC) Library",
            "answer": "B",
            "hint": "Baal katwate time!",
            "level": "medium",
            "category": "Desi Comedy"
        },
        {
            "title": "Aunty Network",
            "question": "Kya cheez hai jo Facebook se bhi fast news spread karti hai?\n\nA) TV News\nB) Aunty Network\nC) WhatsApp",
            "answer": "B",
            "hint": "Society ki secret service!",
            "level": "easy",
            "category": "Desi Family Drama"
        },
        {
            "title": "Exam Fever",
            "question": "Kya cheez hai jo exams ke time pe sabse jyada important ho jaati hai?\n\nA) Books\nB) Last Day Notes\nC) Bhagwan",
            "answer": "B",
            "hint": "One night before exam!",
            "level": "medium",
            "category": "Student Life"
        },
        # Add more festival and cricket puzzles from original
        {
            "title": "Festival of Colors",
            "question": "Which festival makes everyone look like a rainbow?\n\nA) Diwali\nB) Holi\nC) Eid",
            "answer": "B",
            "hint": "Bura na mano, Holi hai!",
            "level": "easy",
            "category": "Festive Specials"
        },
        {
            "title": "Cricket Captain Cool",
            "question": "Who is known as Captain Cool in Indian cricket?\n\nA) Virat Kohli\nB) MS Dhoni\nC) Rohit Sharma",
            "answer": "B",
            "hint": "Helicopter shot master!",
            "level": "easy",
            "category": "Cricket Trivia"
        }
    ]

def save_puzzles(puzzles):
    with open(PUZZLE_FILE, "w", encoding="utf-8") as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

def get_unique_categories(puzzles):
    return sorted(list(set(p["category"] for p in puzzles if "category" in p)))

# Door to Category Mapping
DOOR_CATEGORIES = {
    "🍛 Desi Food Adventure": ["Desi Food Riddles"],
    "🎭 Bollywood Masala": ["Bollywood Masala"],
    "🏏 Cricket Champion": ["Cricket Trivia"],
    "🎉 Festival Fun": ["Festive Specials"],
    "💼 Office Comedy": ["Desi Office Life"],
    "👨‍👩‍👧‍👦 Family Drama": ["Desi Family Drama"],
    "🎓 Student Life": ["Student Life"],
    "😂 Comedy Central": ["Desi Comedy"],
    "🚗 Transport Tales": ["Desi Transport"],
    "🧠 Life Hacks": ["Desi Life Hacks"],
    "🎲 Mixed Masala": ["Desi Food Riddles", "Bollywood Masala", "Cricket Trivia", "Festive Specials"]
}

# ⏱️ Timer functions
def start_timer():
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

def get_time_left(max_seconds):
    elapsed = time.time() - st.session_state.start_time
    return max(0, int(max_seconds - elapsed))

def cpu_guess(correct_answer):
    return correct_answer if random.random() > 0.5 else "wrong"

# 🏆 Victory messages
def get_victory_message(score, total, time_left):
    if score == total:
        return "🎉 PERFECT ESCAPE! 🎉", "You solved ALL puzzles! You're a true escape room master!"
    elif score >= total * 0.8:
        return "🔓 GREAT ESCAPE! 🔓", "You escaped with flying colors! Well done!"
    elif score >= total * 0.6:
        return "🚪 NARROW ESCAPE! 🚪", "You made it out just in time! That was close!"
    elif score >= total * 0.4:
        return "🗝️ LUCKY ESCAPE! 🗝️", "You barely made it out! Better luck next time!"
    else:
        return "🔒 TRAPPED! 🔒", "You couldn't escape this time... Try again!"

# 🚪 Enhanced Door Selection
def show_door_selection():
    st.markdown('<div class="door-container">', unsafe_allow_html=True)
    st.markdown("## 🚪 Choose Your Next Adventure!")
    st.markdown("Each door leads to a different category of puzzles!")
    
    # Create a grid layout for doors
    cols = st.columns(2)
    door_keys = list(DOOR_CATEGORIES.keys())
    
    for i, (door_name, categories) in enumerate(DOOR_CATEGORIES.items()):
        col_idx = i % 2
        with cols[col_idx]:
            st.markdown(f'<div class="category-card">', unsafe_allow_html=True)
            st.markdown(f"### {door_name}")
            st.markdown(f"**Categories:** {', '.join(categories)}")
            
            if st.button(f"Enter {door_name}", key=f"door_{i}"):
                st.session_state.selected_door = door_name
                st.session_state.selected_categories = categories
                st.session_state.door_opened = True
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 🎮 Escape Sequence
def show_escape_sequence(title, message, score, total, time_left):
    st.markdown(f'<div class="victory-message">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="escape-animation">{message}</div>', unsafe_allow_html=True)
    
    # Show stats
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧩 Puzzles Solved", f"{score}/{total}")
    with col2:
        st.metric("⏱️ Time Remaining", f"{time_left}s")
    with col3:
        accuracy = int((score/total) * 100) if total > 0 else 0
        st.metric("🎯 Accuracy", f"{accuracy}%")
    
    st.markdown("---")
    
    # Victory effects
    if score == total:
        st.balloons()
        st.success("🏆 CONGRATULATIONS! You're a true escape room champion!")
    elif score >= total * 0.6:
        st.balloons()
        st.success("🎉 Well done! You successfully escaped!")
    else:
        st.warning("💪 Don't give up! Try again to improve your escape skills!")

# 👥 Player avatars
emoji_options = {
    "😎 Cool Hacker": "😎",
    "👩‍💻 Code Queen": "👩‍💻",
    "🧙‍♂️ Puzzle Wizard": "🧙‍♂️",
    "👸 Royal Solver": "👸",
    "🧞‍♂️ Genie Master": "🧞‍♂️",
    "🤠 Cowboy Coder": "🤠",
    "🧟 Brain Eater": "🧟",
    "🚀 Space Solver": "🚀",
    "🎭 Drama Queen": "🎭",
    "🍕 Foodie": "🍕",
    "🏏 Cricket Fan": "🏏",
    "🎨 Artist": "🎨"
}

# Initialize session state
if "game_completed" not in st.session_state:
    st.session_state.game_completed = False
if "door_opened" not in st.session_state:
    st.session_state.door_opened = False
if "selected_door" not in st.session_state:
    st.session_state.selected_door = None
if "selected_categories" not in st.session_state:
    st.session_state.selected_categories = []

# 🎮 Main Game
st.title("🧙 Escape Room: Desi Puzzle Adventure")

# Show door selection if game completed
if st.session_state.game_completed and not st.session_state.door_opened:
    show_door_selection()
elif st.session_state.door_opened:
    st.info(f"🚪 You entered the {st.session_state.selected_door}! Ready for {', '.join(st.session_state.selected_categories)} challenges?")
    if st.button("🔄 Start New Adventure"):
        # Reset game state but keep door selection
        for key in list(st.session_state.keys()):
            if key.startswith(('start_time', 'game_completed', 'door_opened', 'game_started')):
                del st.session_state[key]
        st.rerun()

mode = st.radio("Select Mode", ["Single Player", "Multiplayer", "Play vs CPU", "Admin Panel"])

if mode == "Admin Panel":
    st.subheader("🔐 Admin Panel")
    password = st.text_input("Enter admin password:", type="password")
    if password == "admin123":
        st.success("Logged in as Admin ✅")

        puzzles = load_puzzles()
        save_puzzles(puzzles)  # Save default puzzles if file doesn't exist

        st.subheader("📊 Puzzle Statistics")
        categories = get_unique_categories(puzzles)
        for category in categories:
            count = len([p for p in puzzles if p["category"] == category])
            st.markdown(f"**{category}**: {count} puzzles")

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
                st.rerun()
            else:
                st.error("Please fill all fields")

    else:
        st.warning("Enter correct admin password to access.")

else:
    if not st.session_state.game_completed:
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
            
            # Use selected categories from door choice or show all categories
            if st.session_state.selected_categories:
                available_categories = st.session_state.selected_categories
                st.info(f"🚪 Playing in {st.session_state.selected_door} mode!")
            else:
                available_categories = get_unique_categories(puzzles)
            
            level = st.selectbox("🎯 Select Level", ["easy", "medium", "hard"])
            
            if len(available_categories) > 1:
                category = st.selectbox("🧠 Select Category", available_categories)
            else:
                category = available_categories[0]
                st.info(f"🧠 Category: {category}")

            # Filter puzzles based on selection
            if st.session_state.selected_categories:
                filtered = [pz for pz in puzzles if pz["level"] == level and pz["category"] in st.session_state.selected_categories]
            else:
                filtered = [pz for pz in puzzles if pz["level"] == level and pz["category"] == category]
            
            if not filtered:
                st.warning("No puzzles found for this selection.")
                st.info("Try selecting a different level or category!")
            else:
                st.success(f"Found {len(filtered)} puzzles for your selection!")
                
                if st.button("🚀 Start Escape Room Challenge!"):
                    st.session_state.game_started = True
                    st.session_state.start_time = time.time()

                if st.session_state.get("game_started", False):
                    selected_puzzles = random.sample(filtered, min(5, len(filtered)))  # Increased to 5 puzzles
                    scores = {p1: 0}
                    if p2: scores[p2] = 0
                    current_player = p1
                    current_avatar = avatar1
                    result_log = []

                    max_time = 120  # Increased time for more puzzles
                    time_left = get_time_left(max_time)
                    
                    if time_left > 0:
                        st.markdown(f"⏱ Time Left: {time_left}s")
                        st.progress((max_time - time_left) / max_time)
                        
                        for i, pz in enumerate(selected_puzzles):
                            st.markdown("---")
                            st.subheader(f"🧩 Puzzle {i+1}: {pz['title']}")
                            st.markdown(pz["question"])

                            if st.button(f"💡 Hint for Puzzle {i+1}", key=f"hint{i}"):
                                st.info(pz.get("hint", "No hint available"))

                            if current_player == "CPU":
                                with st.spinner("🤖 CPU is thinking..."):
                                    time.sleep(1)
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
                                        st.success("✅ Correct! The door creaks open...")
                                        scores[current_player] += 1
                                    else:
                                        st.error("❌ Incorrect. The door remains locked...")

                            if mode in ["Multiplayer", "Play vs CPU"]:
                                if current_player == p1:
                                    current_player, current_avatar = p2, avatar2
                                else:
                                    current_player, current_avatar = p1, avatar1

                        # Game completion check
                        if len(result_log) >= len(selected_puzzles) or time_left <= 0:
                            st.session_state.game_completed = True
                            
                            # Calculate final scores
                            total_score = sum(scores.values()) if mode != "Single Player" else scores[p1]
                            title, message = get_victory_message(total_score, len(selected_puzzles), time_left)
                            
                            show_escape_sequence(title, message, total_score, len(selected_puzzles), time_left)
                            
                            st.subheader("🏆 Final Scores")
                            for name, scr in scores.items():
                                st.markdown(f"**{name}** — {scr} / {len(selected_puzzles)}")

                            st.subheader("📊 Puzzle Summary")
                            for puzzle_title, player, correct in result_log:
                                icon = "✅" if correct else "❌"
                                st.markdown(f"{icon} {puzzle_title} — by **{player}**")

                    else:
                        st.error("⏰ Time's up! The escape room locks you in!")
                        st.session_state.game_completed = True
                        show_escape_sequence("🔒 TIME'S UP!", "You ran out of time! Better luck next time!", 0, len(selected_puzzles), 0)
