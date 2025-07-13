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

    .adventure-card {{
        background: rgba(255,255,255,0.1);
        border: 2px solid {colors['fg']};
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
        text-align: center;
    }}

    .adventure-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
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

    .game-over-buttons {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 20px 0;
    }}

    .game-button {{
        background: linear-gradient(45deg, {colors['fg']}, {colors['bg']});
        color: {colors['bg']};
        border: none;
        padding: 15px 25px;
        border-radius: 10px;
        font-size: 1.1em;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }}

    .game-button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 20px {colors['fg']};
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

import random

def get_default_puzzles():
    """Return complete puzzle collection with all categories and difficulty levels"""
    puzzles = [
        # 🍛 DESI FOOD & CULTURE - Easy
        {"title": "The Golgappa Puzzle", "question": "I'm round and crunchy, I hold spicy water and khatta-meetha chaat. One bite and I'm gone. What am I?\n\nA) Samosa\nB) Dhokla\nC) Golgappa", "answer": "C", "hint": "Also called Pani Puri in Mumbai!", "level": "easy", "category": "Desi Food & Culture"},
        {"title": "Chai Time Mystery", "question": "I'm brown, hot, and sweet. Indians can't start their day without me. What am I?\n\nA) Coffee\nB) Chai\nC) Hot Chocolate", "answer": "B", "hint": "Milk, sugar, and tea leaves!", "level": "easy", "category": "Desi Food & Culture"},
        {"title": "Paani Puri Economics", "question": "What costs 5 rupees but gives unlimited happiness?\n\nA) Chocolate\nB) Paani Puri\nC) Candy", "answer": "B", "hint": "Teeka, meetha, khatta - perfect combo!", "level": "easy", "category": "Desi Food & Culture"},
        {"title": "Sweet Jalebi", "question": "I'm orange, circular, and dripping with sugar syrup. What am I?\n\nA) Gulab Jamun\nB) Jalebi\nC) Rasgulla", "answer": "B", "hint": "Crispy outside, syrupy inside!", "level": "easy", "category": "Desi Food & Culture"},
        
        # 🍛 DESI FOOD & CULTURE - Medium
        {"title": "Lassi Logic", "question": "I'm a cool Punjabi drink, white and thick, served in a steel glass with malai. What am I?\n\nA) Lassi\nB) Chaas\nC) Milk", "answer": "A", "hint": "Made from dahi and very popular in Punjab!", "level": "medium", "category": "Desi Food & Culture"},
        {"title": "Biryani Battle", "question": "I'm a royal dish with layers of rice and meat. Hyderabadi and Lucknowi fight over me. What am I?\n\nA) Pulao\nB) Biryani\nC) Fried Rice", "answer": "B", "hint": "Dum cooking method makes me special!", "level": "medium", "category": "Desi Food & Culture"},
        {"title": "Dosa Dilemma", "question": "I'm crispy, golden, and from South India. I come with coconut chutney and sambar. What am I?\n\nA) Idli\nB) Uttapam\nC) Dosa", "answer": "C", "hint": "Made from fermented rice and lentil batter!", "level": "medium", "category": "Desi Food & Culture"},
        {"title": "Rajma Chawal", "question": "Which combination is called 'Sunday ka khana' in North India?\n\nA) Dal Chawal\nB) Rajma Chawal\nC) Chole Bhature", "answer": "B", "hint": "Red kidney beans with rice!", "level": "medium", "category": "Desi Food & Culture"},
        
        # 🍛 DESI FOOD & CULTURE - Hard
        {"title": "Rogan Josh Recipe", "question": "I'm a Kashmiri dish, red in color, made with yogurt and spices. My name means 'red juice'. What am I?\n\nA) Rogan Josh\nB) Butter Chicken\nC) Tikka Masala", "answer": "A", "hint": "Kashmir's signature mutton dish!", "level": "hard", "category": "Desi Food & Culture"},
        {"title": "Modak Mystery", "question": "I'm Lord Ganesha's favorite sweet, steamed and filled with jaggery and coconut. What am I?\n\nA) Laddu\nB) Modak\nC) Barfi", "answer": "B", "hint": "Specially made during Ganesh Chaturthi!", "level": "hard", "category": "Desi Food & Culture"},
        {"title": "Dhokla Debate", "question": "I'm spongy, steamed, and from Gujarat. Made from gram flour and tempered with mustard seeds. What am I?\n\nA) Dhokla\nB) Khandvi\nC) Thepla", "answer": "A", "hint": "Yellow, fluffy, and perfect for breakfast!", "level": "hard", "category": "Desi Food & Culture"},
        {"title": "Mysore Pak Origin", "question": "Which sweet was first made in the kitchens of Mysore Palace?\n\nA) Rasgulla\nB) Mysore Pak\nC) Sandesh", "answer": "B", "hint": "Ghee, gram flour, and sugar - royal treat!", "level": "hard", "category": "Desi Food & Culture"},

        # 🎭 BOLLYWOOD & ENTERTAINMENT - Easy
        {"title": "King Khan Mystery", "question": "Who is known as the 'King of Bollywood'?\n\nA) Salman Khan\nB) Shah Rukh Khan\nC) Aamir Khan", "answer": "B", "hint": "Known for romantic movies and charm!", "level": "easy", "category": "Bollywood & Entertainment"},
        {"title": "Bollywood Physics", "question": "In Bollywood movies, what doesn't follow the laws of physics?\n\nA) Cars\nB) Bullets\nC) Both A and B", "answer": "C", "hint": "Cars can fly and bullets can be dodged!", "level": "easy", "category": "Bollywood & Entertainment"},
        {"title": "Item Number Queen", "question": "Who is known for the song 'Munni Badnaam Hui'?\n\nA) Katrina Kaif\nB) Malaika Arora\nC) Kareena Kapoor", "answer": "B", "hint": "She's the ultimate item song queen!", "level": "easy", "category": "Bollywood & Entertainment"},
        {"title": "Bhai's Signature", "question": "Which actor is known for removing his shirt in movies?\n\nA) Akshay Kumar\nB) Salman Khan\nC) John Abraham", "answer": "B", "hint": "Bhai ki shirtless entry!", "level": "easy", "category": "Bollywood & Entertainment"},

        # 🎭 BOLLYWOOD & ENTERTAINMENT - Medium
        {"title": "Lagaan Challenge", "question": "Which Bollywood movie was nominated for Oscar in 2002?\n\nA) Lagaan\nB) Taare Zameen Par\nC) 3 Idiots", "answer": "A", "hint": "Cricket and tax collection in British India!", "level": "medium", "category": "Bollywood & Entertainment"},
        {"title": "Sholay Dialogue", "question": "Complete the dialogue: 'Kitne aadmi the?' Response: '___'\n\nA) Do Sarkar\nB) Teen Sarkar\nC) Char Sarkar", "answer": "A", "hint": "Classic dialogue from Sholay!", "level": "medium", "category": "Bollywood & Entertainment"},
        {"title": "Dangal Dedication", "question": "Which actor gained and lost weight dramatically for the movie 'Dangal'?\n\nA) Aamir Khan\nB) Salman Khan\nC) Shah Rukh Khan", "answer": "A", "hint": "Mr. Perfectionist's dedication!", "level": "medium", "category": "Bollywood & Entertainment"},
        {"title": "Comedy King", "question": "Who is known as the 'Comedy King' of Bollywood?\n\nA) Johnny Lever\nB) Paresh Rawal\nC) Govinda", "answer": "C", "hint": "Hero No. 1 and coolie dance moves!", "level": "medium", "category": "Bollywood & Entertainment"},

        # 🎭 BOLLYWOOD & ENTERTAINMENT - Hard
        {"title": "Mughal-e-Azam Mystery", "question": "Which was the first Bollywood movie to be made in Technicolor?\n\nA) Mother India\nB) Mughal-e-Azam\nC) Pakeezah", "answer": "B", "hint": "Epic love story of Salim and Anarkali!", "level": "hard", "category": "Bollywood & Entertainment"},
        {"title": "Satyajit Ray's Trilogy", "question": "What is the name of Satyajit Ray's famous trilogy?\n\nA) Apu Trilogy\nB) Calcutta Trilogy\nC) Bengali Trilogy", "answer": "A", "hint": "Pather Panchali is the first film!", "level": "hard", "category": "Bollywood & Entertainment"},
        {"title": "Filmfare First", "question": "Which movie won the first Filmfare Award for Best Film?\n\nA) Awaara\nB) Do Bigha Zamin\nC) Shree 420", "answer": "B", "hint": "1954 film about a farmer's struggle!", "level": "hard", "category": "Bollywood & Entertainment"},
        {"title": "Parallel Cinema", "question": "Who is considered the father of Indian parallel cinema?\n\nA) Shyam Benegal\nB) Satyajit Ray\nC) Mrinal Sen", "answer": "B", "hint": "Bengali filmmaker who won numerous international awards!", "level": "hard", "category": "Bollywood & Entertainment"},

        # 🏏 SPORTS & CRICKET - Easy
        {"title": "Captain Cool", "question": "Who is known as 'Captain Cool' in Indian cricket?\n\nA) Virat Kohli\nB) MS Dhoni\nC) Rohit Sharma", "answer": "B", "hint": "Famous for helicopter shot!", "level": "easy", "category": "Sports & Cricket"},
        {"title": "God of Cricket", "question": "Who is called the 'God of Cricket'?\n\nA) Sachin Tendulkar\nB) Virat Kohli\nC) Kapil Dev", "answer": "A", "hint": "Master Blaster with 100 centuries!", "level": "easy", "category": "Sports & Cricket"},
        {"title": "IPL Mumbai", "question": "Which team has won the most IPL titles?\n\nA) Chennai Super Kings\nB) Mumbai Indians\nC) Kolkata Knight Riders", "answer": "B", "hint": "Blue and gold team from Mumbai!", "level": "easy", "category": "Sports & Cricket"},
        {"title": "Wicket Count", "question": "How many wickets are there on a cricket field?\n\nA) 2\nB) 3\nC) 4", "answer": "A", "hint": "One at each end of the pitch!", "level": "easy", "category": "Sports & Cricket"},

        # 🏏 SPORTS & CRICKET - Medium
        {"title": "1983 Glory", "question": "Who was India's captain in the 1983 World Cup final?\n\nA) Sunil Gavaskar\nB) Kapil Dev\nC) Ravi Shastri", "answer": "B", "hint": "He lifted the trophy at Lord's!", "level": "medium", "category": "Sports & Cricket"},
        {"title": "T20 Master", "question": "Which player holds the record for most T20I sixes for India?\n\nA) Virat Kohli\nB) Rohit Sharma\nC) Suryakumar Yadav", "answer": "B", "hint": "Also called the Hitman!", "level": "medium", "category": "Sports & Cricket"},
        {"title": "Test Match Trivia", "question": "How many players are there in a Test cricket team?\n\nA) 10\nB) 11\nC) 12", "answer": "B", "hint": "Same as in all cricket formats!", "level": "medium", "category": "Sports & Cricket"},
        {"title": "Boundary Rules", "question": "How many runs are scored for hitting the ball over the boundary?\n\nA) 4\nB) 6\nC) Depends on how it crosses", "answer": "C", "hint": "Bouncing = 4, direct = 6!", "level": "medium", "category": "Sports & Cricket"},

        # 🏏 SPORTS & CRICKET - Hard
        {"title": "Kumble's Ten", "question": "Which bowler took all 10 wickets in a Test innings against Pakistan?\n\nA) Harbhajan Singh\nB) Anil Kumble\nC) Ravindra Jadeja", "answer": "B", "hint": "Historic match in Delhi!", "level": "hard", "category": "Sports & Cricket"},
        {"title": "Fastest 100", "question": "Who scored the fastest ODI century for India?\n\nA) Virat Kohli\nB) KL Rahul\nC) Rohit Sharma", "answer": "A", "hint": "Took just 52 balls vs Australia!", "level": "hard", "category": "Sports & Cricket"},
        {"title": "World Cup Streak", "question": "India won the 2011 World Cup under whose captaincy?\n\nA) Sourav Ganguly\nB) MS Dhoni\nC) Rahul Dravid", "answer": "B", "hint": "Hit the winning six at Wankhede!", "level": "hard", "category": "Sports & Cricket"},
        {"title": "Eden Gardens", "question": "Which stadium is known as the 'Mecca of Cricket'?\n\nA) Wankhede Stadium\nB) Eden Gardens\nC) M. Chinnaswamy Stadium", "answer": "B", "hint": "Kolkata's iconic cricket ground!", "level": "hard", "category": "Sports & Cricket"},

        # 🎉 FESTIVALS & CELEBRATIONS - Easy
        {"title": "Festival of Colors", "question": "Which festival is known as the 'Festival of Colors'?\n\nA) Diwali\nB) Holi\nC) Dussehra", "answer": "B", "hint": "Bura na mano, Holi hai!", "level": "easy", "category": "Festivals & Celebrations"},
        {"title": "Diwali Lights", "question": "Diwali is the festival of what?\n\nA) Lights\nB) Colors\nC) Harvest", "answer": "A", "hint": "Deepavali means row of lights!", "level": "easy", "category": "Festivals & Celebrations"},
        {"title": "Ganesh Chaturthi", "question": "Which festival celebrates the birth of Lord Ganesha?\n\nA) Janmashtami\nB) Ganesh Chaturthi\nC) Navratri", "answer": "B", "hint": "Ganpati Bappa Morya!", "level": "easy", "category": "Festivals & Celebrations"},
        {"title": "Raksha Bandhan", "question": "On Raksha Bandhan, what do sisters tie on their brother's wrist?\n\nA) Bracelet\nB) Rakhi\nC) Watch", "answer": "B", "hint": "Thread of protection and love!", "level": "easy", "category": "Festivals & Celebrations"},

        # 🎉 FESTIVALS & CELEBRATIONS - Medium
        {"title": "Lohri Fire", "question": "Lohri is celebrated in which state?\n\nA) Punjab\nB) Gujarat\nC) Bihar", "answer": "A", "hint": "Bonfire and bhangra time!", "level": "medium", "category": "Festivals & Celebrations"},
        {"title": "Navratri Nights", "question": "Garba is a traditional dance during which festival?\n\nA) Diwali\nB) Holi\nC) Navratri", "answer": "C", "hint": "9 nights of devotion and dance!", "level": "medium", "category": "Festivals & Celebrations"},
        {"title": "Harvest Special", "question": "Pongal is mainly celebrated in which Indian state?\n\nA) Kerala\nB) Tamil Nadu\nC) Andhra Pradesh", "answer": "B", "hint": "Sakkarai Pongal is a must!", "level": "medium", "category": "Festivals & Celebrations"},
        {"title": "Onam Feast", "question": "Which festival is celebrated with the traditional Sadhya feast?\n\nA) Onam\nB) Vishu\nC) Thrissur Pooram", "answer": "A", "hint": "Kerala's biggest festival!", "level": "medium", "category": "Festivals & Celebrations"},

        # 🎉 FESTIVALS & CELEBRATIONS - Hard
        {"title": "Deepavali Meaning", "question": "What does the word 'Deepavali' mean?\n\nA) Row of flowers\nB) Row of lights\nC) Row of prayers", "answer": "B", "hint": "Deep = lamp, Avali = row", "level": "hard", "category": "Festivals & Celebrations"},
        {"title": "Makar Sankranti", "question": "Makar Sankranti is dedicated to which deity?\n\nA) Lord Vishnu\nB) Surya (Sun God)\nC) Lord Shiva", "answer": "B", "hint": "It marks the Sun's northward journey!", "level": "hard", "category": "Festivals & Celebrations"},
        {"title": "Ram Navami", "question": "Ram Navami marks the birth of whom?\n\nA) Krishna\nB) Rama\nC) Hanuman", "answer": "B", "hint": "Son of King Dasharatha!", "level": "hard", "category": "Festivals & Celebrations"},
        {"title": "Kumbh Mela", "question": "How often is the Purna Kumbh Mela held?\n\nA) Every 6 years\nB) Every 12 years\nC) Every 144 years", "answer": "B", "hint": "Largest religious gathering in the world!", "level": "hard", "category": "Festivals & Celebrations"},

        # 💼 OFFICE & WORK LIFE - Easy
        {"title": "Monday Blues", "question": "Which day of the week is universally hated by office workers?\n\nA) Monday\nB) Tuesday\nC) Wednesday", "answer": "A", "hint": "Weekend ka hangover!", "level": "easy", "category": "Office & Work Life"},
        {"title": "Chai Break", "question": "What's the most important meeting in any Indian office?\n\nA) Board Meeting\nB) Chai Break\nC) Review Meeting", "answer": "B", "hint": "No agenda, maximum discussion!", "level": "easy", "category": "Office & Work Life"},
        {"title": "Email CC", "question": "What does CC mean in emails?\n\nA) Carbon Copy\nB) Clear Copy\nC) Confidential Copy", "answer": "A", "hint": "Everyone gets a copy!", "level": "easy", "category": "Office & Work Life"},
        {"title": "TGIF", "question": "What does TGIF stand for?\n\nA) Time Goes In Flow\nB) Thank God It's Friday\nC) Today's Great In Fun", "answer": "B", "hint": "Weekend is coming!", "level": "easy", "category": "Office & Work Life"},

        # 💼 OFFICE & WORK LIFE - Medium
        {"title": "Deadline Pressure", "question": "When do most people actually start working on a project?\n\nA) As soon as assigned\nB) One day before deadline\nC) After the deadline", "answer": "B", "hint": "Procrastination is real!", "level": "medium", "category": "Office & Work Life"},
        {"title": "Meeting Bingo", "question": "What happens in most office meetings?\n\nA) Productive discussion\nB) Another meeting is scheduled\nC) Decisions are made", "answer": "B", "hint": "Let's take this offline!", "level": "medium", "category": "Office & Work Life"},
        {"title": "Wi-Fi Password", "question": "What's the most asked question in any office?\n\nA) What's for lunch?\nB) What's the Wi-Fi password?\nC) When is the holiday?", "answer": "B", "hint": "First thing new employees ask!", "level": "medium", "category": "Office & Work Life"},
        {"title": "Work From Home", "question": "What became the most popular work arrangement during 2020?\n\nA) Flexible hours\nB) Work from home\nC) Part-time work", "answer": "B", "hint": "Pajama professional life!", "level": "medium", "category": "Office & Work Life"},

        # 💼 OFFICE & WORK LIFE - Hard
        {"title": "Parkinson's Law", "question": "According to Parkinson's Law, work expands to fill what?\n\nA) The available time\nB) The available space\nC) The available resources", "answer": "A", "hint": "Time management principle!", "level": "hard", "category": "Office & Work Life"},
        {"title": "Agile Methodology", "question": "In Agile, what is a 'Sprint'?\n\nA) Running exercise\nB) Time-boxed iteration\nC) Meeting type", "answer": "B", "hint": "Usually 2-4 weeks long!", "level": "hard", "category": "Office & Work Life"},
        {"title": "KPI Meaning", "question": "What does KPI stand for?\n\nA) Key Performance Indicator\nB) Key Process Improvement\nC) Key Personnel Information", "answer": "A", "hint": "Measures performance!", "level": "hard", "category": "Office & Work Life"},
        {"title": "Peter Principle", "question": "The Peter Principle states that people rise to their level of what?\n\nA) Competence\nB) Incompetence\nC) Excellence", "answer": "B", "hint": "Promoted until they can't perform!", "level": "hard", "category": "Office & Work Life"},

        # 🎓 STUDENT & ACADEMIC LIFE - Easy
        {"title": "Maggi Magic", "question": "What's the most cooked item in student hostels?\n\nA) Rice\nB) Maggi\nC) Dal", "answer": "B", "hint": "2 minute mein ready!", "level": "easy", "category": "Student & Academic Life"},
        {"title": "Last Minute Study", "question": "When do most students start studying for exams?\n\nA) Beginning of semester\nB) Mid-semester\nC) Night before exam", "answer": "C", "hint": "All-nighter champions!", "level": "easy", "category": "Student & Academic Life"},
        {"title": "Library Excuse", "question": "Where do students say they're going but never actually go?\n\nA) Canteen\nB) Library\nC) Hostel", "answer": "B", "hint": "Books are waiting!", "level": "easy", "category": "Student & Academic Life"},
        {"title": "Assignment Deadline", "question": "When do most students submit their assignments?\n\nA) Early\nB) On time\nC) Last minute", "answer": "C", "hint": "Printer queue at 11:59 PM!", "level": "easy", "category": "Student & Academic Life"},

        # 🎓 STUDENT & ACADEMIC LIFE - Medium
        {"title": "Semester System", "question": "How many semesters are in a typical engineering course?\n\nA) 6\nB) 8\nC) 10", "answer": "B", "hint": "4 years = 8 semesters!", "level": "medium", "category": "Student & Academic Life"},
        {"title": "Attendance Shortage", "question": "What's the minimum attendance percentage in most colleges?\n\nA) 65%\nB) 75%\nC) 85%", "answer": "B", "hint": "Proxy attendance is common!", "level": "medium", "category": "Student & Academic Life"},
        {"title": "Scholarship Criteria", "question": "Merit scholarships are usually based on what?\n\nA) Family income\nB) Academic performance\nC) Sports achievements", "answer": "B", "hint": "Grade point average matters!", "level": "medium", "category": "Student & Academic Life"},
        {"title": "Group Project", "question": "In group projects, who usually does most of the work?\n\nA) Everyone equally\nB) One person\nC) The group leader", "answer": "B", "hint": "Free riders are everywhere!", "level": "medium", "category": "Student & Academic Life"},

        # 🎓 STUDENT & ACADEMIC LIFE - Hard
        {"title": "CGPA Calculation", "question": "What does CGPA stand for?\n\nA) Cumulative Grade Point Average\nB) Current Grade Point Average\nC) Complete Grade Point Assessment", "answer": "A", "hint": "Overall academic performance!", "level": "hard", "category": "Student & Academic Life"},
        {"title": "Thesis Defense", "question": "What is a viva voce examination?\n\nA) Written exam\nB) Oral examination\nC) Practical exam", "answer": "B", "hint": "Face-to-face with examiners!", "level": "hard", "category": "Student & Academic Life"},
        {"title": "Academic Calendar", "question": "What is the period between two academic sessions called?\n\nA) Vacation\nB) Semester break\nC) Intersession", "answer": "C", "hint": "Gap between sessions!", "level": "hard", "category": "Student & Academic Life"},
        {"title": "Dissertation vs Thesis", "question": "A dissertation is typically required for which degree?\n\nA) Bachelor's\nB) Master's\nC) PhD", "answer": "C", "hint": "Doctoral level research!", "level": "hard", "category": "Student & Academic Life"}
    ]
    
    return puzzles

def get_puzzles_by_category(category):
    """Get all puzzles for a specific category"""
    all_puzzles = get_default_puzzles()
    return [puzzle for puzzle in all_puzzles if puzzle['category'] == category]

def get_puzzles_by_level(level):
    """Get all puzzles for a specific difficulty level"""
    all_puzzles = get_default_puzzles()
    return [puzzle for puzzle in all_puzzles if puzzle['level'] == level]

def get_puzzles_by_category_and_level(category, level):
    """Get puzzles filtered by both category and level"""
    all_puzzles = get_default_puzzles()
    return [puzzle for puzzle in all_puzzles if puzzle['category'] == category and puzzle['level'] == level]

def get_random_puzzle_of_the_day():
    """Returns one random puzzle regardless of category or level"""
    puzzles = get_default_puzzles()
    return random.choice(puzzles)

def get_random_puzzle_by_category(category):
    """Returns one random puzzle from a specific category"""
    category_puzzles = get_puzzles_by_category(category)
    if category_puzzles:
        return random.choice(category_puzzles)
    return None

def get_random_puzzle_by_level(level):
    """Returns one random puzzle from a specific difficulty level"""
    level_puzzles = get_puzzles_by_level(level)
    if level_puzzles:
        return random.choice(level_puzzles)
    return None

def get_available_categories():
    """Get list of all available categories"""
    all_puzzles = get_default_puzzles()
    categories = list(set(puzzle['category'] for puzzle in all_puzzles))
    return sorted(categories)

def get_available_levels():
    """Get list of all available difficulty levels"""
    return ['easy', 'medium', 'hard']

def get_category_stats():
    """Get statistics for each category"""
    all_puzzles = get_default_puzzles()
    stats = {}
    
    for puzzle in all_puzzles:
        category = puzzle['category']
        level = puzzle['level']
        
        if category not in stats:
            stats[category] = {'easy': 0, 'medium': 0, 'hard': 0, 'total': 0}
        
        stats[category][level] += 1
        stats[category]['total'] += 1
    
    return stats

def create_custom_quiz(num_questions=10, category=None, level=None):
    """Create a custom quiz with specified parameters"""
    if category and level:
        available_puzzles = get_puzzles_by_category_and_level(category, level)
    elif category:
        available_puzzles = get_puzzles_by_category(category)
    elif level:
        available_puzzles = get_puzzles_by_level(level)
    else:
        available_puzzles = get_default_puzzles()
    
    if len(available_puzzles) < num_questions:
        num_questions = len(available_puzzles)
    
    return random.sample(available_puzzles, num_questions)

# Example usage and testing
if __name__ == "__main__":
    # Test the system
    print("=== QUIZ SYSTEM DEMO ===\n")
    
    # Show available categories
    print("Available Categories:")
    for i, category in enumerate(get_available_categories(), 1):
        print(f"{i}. {category}")
    
    print(f"\nAvailable Levels: {', '.join(get_available_levels())}")
    
    # Show category statistics
    print("\n=== Category Statistics ===")
    stats = get_category_stats()
    for category, counts in stats.items():
        print(f"{category}: {counts['total']} total (Easy: {counts['easy']}, Medium: {counts['medium']}, Hard: {counts['hard']})")
    
    # Random puzzle of the day
    print("\n=== Random Puzzle of the Day ===")
    daily_puzzle = get_random_puzzle_of_the_day()
    print(f"Title: {daily_puzzle['title']}")
    print(f"Category: {daily_puzzle['category']}")
    print(f"Level: {daily_puzzle['level'].capitalize()}")
    print(f"Question: {daily_puzzle['question']}")
    print(f"Answer: {daily_puzzle['answer']}")
    print(f"Hint: {daily_puzzle['hint']}")
    
    # Custom quiz example
    print("\n=== Custom Quiz Example (5 Medium Questions) ===")
    custom_quiz = create_custom_quiz(num_questions=5, level='medium')
    for i, puzzle in enumerate(custom_quiz, 1):
        print(f"{i}. {puzzle['title']} ({puzzle['category']})")
    
    print(f"\nTotal puzzles in system: {len(get_default_puzzles())}")

def save_puzzles(puzzles):
    with open(PUZZLE_FILE, "w", encoding="utf-8") as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

def get_unique_categories(puzzles):
    return sorted(list(set(p["category"] for p in puzzles if "category" in p)))

# Adventure Categories with emojis
# Adventure Categories with emojis - Updated to match puzzle content
ADVENTURE_CATEGORIES = {
    "🍛 Desi Food & Culture": {
        "description": "Explore India's rich culinary heritage and cultural traditions",
        "category": "Desi Food & Culture",
        "icon": "🍛"
    },
    "🎭 Bollywood & Entertainment": {
        "description": "Test your knowledge of Indian cinema and entertainment",
        "category": "Bollywood & Entertainment", 
        "icon": "🎭"
    },
    "🏏 Sports & Cricket": {
        "description": "Challenge yourself with Indian sports trivia and cricket knowledge",
        "category": "Sports & Cricket",
        "icon": "🏏"
    },
    "🎉 Festivals & Celebrations": {
        "description": "Discover India's vibrant festivals and traditional celebrations",
        "category": "Festivals & Celebrations",
        "icon": "🎉"
    },
    "💼 Office & Work Life": {
        "description": "Navigate the funny and relatable world of Indian office culture",
        "category": "Office & Work Life",
        "icon": "💼"
    },
    "🎓 Student & Academic Life": {
        "description": "Relive the memorable moments of student life and academic experiences",
        "category": "Student & Academic Life",
        "icon": "🎓"
    }
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

# 🚪 Adventure Selection Screen
def show_adventure_selection():
    st.markdown('<div class="door-container">', unsafe_allow_html=True)
    st.markdown("## 🎮 Choose Your Next Adventure!")
    st.markdown("Select a category to begin your escape room challenge!")
    
    # Create a 2x2 grid for adventure categories
    cols = st.columns(2)
    
    for i, (adventure_name, details) in enumerate(ADVENTURE_CATEGORIES.items()):
        col_idx = i % 2
        with cols[col_idx]:
            st.markdown(f'<div class="adventure-card">', unsafe_allow_html=True)
            st.markdown(f"# {details['icon']}")
            st.markdown(f"### {adventure_name}")
            st.markdown(f"*{details['description']}*")
            
            if st.button(f"Start Adventure", key=f"adventure_{i}"):
                st.session_state.selected_adventure = details['category']
                st.session_state.adventure_selected = True
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 🎮 Game Over Screen
def show_game_over_screen(title, message, score, total, time_left):
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
    
    st.markdown("---")
    
    # Game over options
    st.markdown("## What would you like to do next?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚪 Choose Next Adventure", key="next_adventure"):
            # Reset game state but keep showing adventure selection
            st.session_state.game_completed = False
            st.session_state.show_adventure_selection = True
            st.session_state.adventure_selected = False
            st.session_state.selected_adventure = None
            if "start_time" in st.session_state:
                del st.session_state.start_time
            if "game_started" in st.session_state:
                del st.session_state.game_started
            st.rerun()
    
    with col2:
        if st.button("🚪 Exit Game", key="exit_game"):
            # Reset all session state
            for key in list(st.session_state.keys()):
                if key not in ['theme']:  # Keep theme preference
                    del st.session_state[key]
            st.success("Thanks for playing! Refresh the page to start a new game.")
            st.rerun()

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
if "show_adventure_selection" not in st.session_state:
    st.session_state.show_adventure_selection = False
if "adventure_selected" not in st.session_state:
    st.session_state.adventure_selected = False
if "selected_adventure" not in st.session_state:
    st.session_state.selected_adventure = None

# 🎮 Main Game
st.title("🧙 Escape Room: Indian Adventure")

# Show adventure selection if requested
if st.session_state.show_adventure_selection and not st.session_state.adventure_selected:
    show_adventure_selection()
    st.stop()

# Show selected adventure info
if st.session_state.adventure_selected and st.session_state.selected_adventure:
    st.info(f"🎯 Selected Adventure: {st.session_state.selected_adventure}")
    if st.button("🔄 Choose Different Adventure"):
        st.session_state.adventure_selected = False
        st.session_state.selected_adventure = None
        st.session_state.show_adventure_selection = True
        st.rerun()

mode = st.radio("Select Mode", ["Single Player", "Multiplayer", "Play vs CPU", "Admin Panel"])

if mode == "Admin Panel":
    st.subheader("🔐 Admin Panel")
    password = st.text_input("Enter admin password:", type="password")
    if password == "admin123":
        st.success("Logged in as Admin ✅")

        puzzles = load_puzzles()
        save_puzzles(puzzles)

        st.subheader("📊 Puzzle Statistics")
        categories = get_unique_categories(puzzles)
        for category in categories:
            st.markdown(f"### {category}")
            easy_count = len([p for p in puzzles if p["category"] == category and p["level"] == "easy"])
            medium_count = len([p for p in puzzles if p["category"] == category and p["level"] == "medium"])
            hard_count = len([p for p in puzzles if p["category"] == category and p["level"] == "hard"])
            st.markdown(f"- Easy: {easy_count} | Medium: {medium_count} | Hard: {hard_count}")

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
            
            # Use selected adventure category or show selection
            if st.session_state.selected_adventure:
                current_category = st.session_state.selected_adventure
                st.success(f"🎯 Adventure: {current_category}")
            else:
                available_categories = get_unique_categories(puzzles)
                current_category = st.selectbox("🧠 Select Category", available_categories)
                if current_category:
                    st.session_state.selected_adventure = current_category
            
            # Only show level selection if category is selected
            if current_category:
                level = st.selectbox("🎯 Select Level", ["easy", "medium", "hard"])
                
                # Filter puzzles based on selection
                filtered = [pz for pz in puzzles if pz["level"] == level and pz["category"] == current_category]
                
                if not filtered:
                    st.warning("No puzzles found for this selection.")
                    st.info("Try selecting a different level!")
                else:
                    st.success(f"Found {len(filtered)} puzzles for your selection!")
                    
                    if st.button("🚀 Start Escape Room Challenge!"):
                        st.session_state.game_started = True
                        st.session_state.start_time = time.time()

                    if st.session_state.get("game_started", False):
                        selected_puzzles = random.sample(filtered, min(5, len(filtered)))
                        scores = {p1: 0}
                        if p2: scores[p2] = 0
                        current_player = p1
                        current_avatar = avatar1
                        result_log = []

                        max_time = 120
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
                                if mode == "Single Player":
                                    final_score = scores[p1]
                                    total_puzzles = len(selected_puzzles)
                                else:
                                    final_score = scores[p1]
                                    total_puzzles = len(selected_puzzles)
                                
                                # Store game results for display
                                st.session_state.final_score = final_score
                                st.session_state.total_puzzles = total_puzzles
                                st.session_state.time_remaining = time_left
                                st.session_state.result_log = result_log
                                st.session_state.player_scores = scores
                                
                                st.rerun()
                        
                        else:
                            # Time's up!
                            st.session_state.game_completed = True
                            st.session_state.final_score = sum(scores.values()) if mode != "Single Player" else scores[p1]
                            st.session_state.total_puzzles = len(selected_puzzles)
                            st.session_state.time_remaining = 0
                            st.session_state.result_log = result_log
                            st.session_state.player_scores = scores
                            st.rerun()
                            
                    else:
                        st.markdown("---")
                        if st.button("🚪 Choose Adventure Category", key="choose_adventure"):
                            st.session_state.show_adventure_selection = True
                            st.rerun()
            else:
                st.markdown("---")
                if st.button("🚪 Browse Adventure Categories", key="browse_adventures"):
                    st.session_state.show_adventure_selection = True
                    st.rerun()
        else:
            st.info("Please enter player name(s) to continue")
            st.markdown("---")
            if st.button("🚪 Browse Adventure Categories", key="browse_adventures"):
                st.session_state.show_adventure_selection = True
                st.rerun()

    else:
        final_score = st.session_state.get("final_score", 0)
        total_puzzles = st.session_state.get("total_puzzles", 5)
        time_remaining = st.session_state.get("time_remaining", 0)
        result_log = st.session_state.get("result_log", [])
        player_scores = st.session_state.get("player_scores", {})
        
        title, message = get_victory_message(final_score, total_puzzles, time_remaining)
        show_game_over_screen(title, message, final_score, total_puzzles, time_remaining)
        
        st.markdown("---")
        st.subheader("📊 Detailed Results")
        
        if mode in ["Multiplayer", "Play vs CPU"]:
            st.markdown("### 🏆 Final Scores")
            for player, score in player_scores.items():
                if player == "CPU":
                    st.markdown(f"🤖 **{player}**: {score}/{total_puzzles}")
                else:
                    st.markdown(f"👤 **{player}**: {score}/{total_puzzles}")
            if len(player_scores) > 1:
                winner = max(player_scores, key=player_scores.get)
                if list(player_scores.values()).count(max(player_scores.values())) > 1:
                    st.markdown("🤝 **It's a tie!**")
                else:
                    st.markdown(f"🏆 **Winner: {winner}!**")
        
        if result_log:
            st.markdown("### 🧩 Puzzle Results")
            for puzzle_title, player, correct in result_log:
                status = "✅" if correct else "❌"
                st.markdown(f"{status} **{puzzle_title}** - {player}")
        
        st.markdown("---")
        st.subheader("📈 Performance Analysis")
        
        if final_score == total_puzzles:
            st.success("🎯 Perfect Score! You're a master puzzle solver!")
        elif final_score >= total_puzzles * 0.8:
            st.success("🌟 Excellent Performance! You're really good at this!")
        elif final_score >= total_puzzles * 0.6:
            st.info("👍 Good Job! You solved most puzzles correctly!")
        elif final_score >= total_puzzles * 0.4:
            st.warning("💪 Not bad! Keep practicing to improve!")
        else:
            st.error("🎯 Challenge yourself! Try an easier level or different category!")
        
        if time_remaining > 60:
            st.success(f"⚡ Lightning Fast! You finished with {time_remaining} seconds to spare!")
        elif time_remaining > 30:
            st.info(f"⏱️ Good Timing! You had {time_remaining} seconds left!")
        elif time_remaining > 0:
            st.warning(f"⏰ Close Call! Only {time_remaining} seconds remaining!")
        else:
            st.error("⏰ Time's Up! You ran out of time!")

st.markdown("---")
st.markdown("### 🎮 Game Features")
st.markdown("""
- **4 Adventure Categories**: Food & Culture, Bollywood, History & Geography, Science & Technology
- **3 Difficulty Levels**: Easy, Medium, Hard
- **Multiple Game Modes**: Single Player, Multiplayer, Play vs CPU
- **Themed Interface**: Choose from 5 beautiful themes
- **Timed Challenges**: 120-second escape room experience
- **Performance Analytics**: Detailed results and statistics
""")

st.markdown("---")
st.markdown("*Made with ❤️ for puzzle enthusiasts | Escape Room: Indian Adventure*")
