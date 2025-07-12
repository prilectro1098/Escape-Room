import streamlit as st
import json
import os

PUZZLE_FILE = "puzzles.json"

# Load existing puzzles
def load_puzzles():
    if os.path.exists(PUZZLE_FILE):
        with open(PUZZLE_FILE, "r") as f:
            return json.load(f)
    return []

def save_puzzles(puzzles):
    with open(PUZZLE_FILE, "w") as f:
        json.dump(puzzles, f, indent=2)

st.set_page_config(page_title="🛠️ Admin Panel", layout="wide")
st.title("🧠 Puzzle Admin Panel")

puzzles = load_puzzles()

st.subheader("📋 Existing Puzzles")
for i, pz in enumerate(puzzles):
    with st.expander(f"{i+1}. {pz['title']}"):
        st.markdown(f"**Question:** {pz['question']}")
        st.markdown(f"**Answer:** {pz['answer']}")
        st.markdown(f"**Level:** {pz['level']}")
        st.markdown(f"**Hint:** {pz['hint']}")
        if st.button(f"❌ Delete Puzzle {i+1}", key=f"del{i}"):
            puzzles.pop(i)
            save_puzzles(puzzles)
            st.experimental_rerun()

st.subheader("➕ Add New Puzzle")
with st.form("add_puzzle_form"):
    title = st.text_input("Title")
    question = st.text_area("Question")
    answer = st.text_input("Answer")
    hint = st.text_input("Hint (optional)")
    level = st.selectbox("Level", ["easy", "medium", "hard"])
    submitted = st.form_submit_button("Add Puzzle")

    if submitted and title and question and answer:
        puzzles.append({
            "title": title,
            "question": question,
            "answer": answer,
            "hint": hint,
            "level": level
        })
        save_puzzles(puzzles)
        st.success("✅ Puzzle added!")
        st.experimental_rerun()
