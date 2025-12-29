import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize session state for saved ideas
if "saved_ideas" not in st.session_state:
    st.session_state.saved_ideas = []

# Page config
st.set_page_config(
    page_title="AI Project Idea Generator",
    page_icon="robot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Ocean Blue Gradient + HIGH VISIBILITY TEXT
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #e0f2fe, #bae6fd, #7dd3fc, #0ea5e9);
    }
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 40px;
        margin-top: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    }
    h1 {
        color: #0c4a6e !important;
        text-align: center;
        font-weight: 700;
        font-size: 2.8rem !important;
    }
    h4 {
        color: #0369a1;
        text-align: center;
        margin-bottom: 40px;
    }
    /* HIGH VISIBILITY - DARK TEXT EVERYWHERE */
    .stMarkdown, p, div, label, .stTextInput label {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    .stTextInput > div > div > input {
        border-radius: 16px;
        padding: 16px;
        font-size: 1.1rem;
        border: 2px solid #7dd3fc;
        color: #1e293b !important;
    }
    /* Placeholder text dark */
    ::placeholder {
        color: #475569 !important;
        opacity: 1;
    }
    .stButton > button {
        background: linear-gradient(to right, #0ea5e9, #0284c7);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 16px 40px;
        font-weight: bold;
        font-size: 1.2rem;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.3);
        width: 100%;
        margin-top: 20px;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(14, 165, 233, 0.4);
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: white;
        border-radius: 16px;
        padding: 30px;
        border: none;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #1e293b !important;
        font-size: 17px !important;
        line-height: 1.8;
        font-weight: 500;
    }
    [data-testid="stMarkdownContainer"] strong {
        color: #0369a1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Settings")

    num_ideas = st.slider("Number of ideas", 1, 10, 3)

    difficulty = st.selectbox(
        "Difficulty level",
        ["Any", "Beginner", "Intermediate", "Advanced"]
    )

    st.divider()

    st.subheader("Saved Ideas")

    if st.session_state.saved_ideas:
        for i, saved in enumerate(st.session_state.saved_ideas):
            with st.expander(f"{saved['topic']} (Set {i + 1})"):
                st.markdown(saved['ideas'])

        if st.button("Clear all saved ideas"):
            st.session_state.saved_ideas = []
            st.success("All saved ideas cleared!")
            st.rerun()
    else:
        st.info("No saved ideas yet.")

    st.divider()
    st.caption("Example topics: computer vision, robotics, games, health tech, sustainability")

# Main content
st.title("AI Project Idea Generator")
st.markdown("#### Generate practical and creative AI/ML project ideas")

st.markdown("### What topic are you interested in?")
interests = st.text_input(
    label="Topic",
    placeholder="e.g., computer vision, machine learning, robotics, games, health tech",
    label_visibility="collapsed"
)

if st.button("Generate Ideas", type="primary"):
    if not interests.strip():
        st.warning("Please enter a topic to generate ideas.")
    else:
        difficulty_prompt = ""
        if difficulty != "Any":
            difficulty_prompt = f" Prioritize {difficulty.lower()} difficulty projects."

        with st.spinner("Generating ideas..."):
            try:
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    st.error("GEMINI_API_KEY not found in .env file.")
                    st.stop()

                client = OpenAI(
                    api_key=api_key,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )

                prompt = f"""
                Generate {num_ideas} practical AI/ML project ideas based on: "{interests}".
                For each idea, include:
                - A catchy title
                - Short description
                - Difficulty level (Beginner/Intermediate/Advanced)
                - Key technologies/libraries
                - Why it's valuable or fun

                Be clear and direct. Jump straight to the ideas.{difficulty_prompt}
                """

                response = client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=[
                        {"role": "system", "content": "You are a professional and helpful AI project mentor."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9,
                    max_tokens=2000
                )

                ideas = response.choices[0].message.content

                st.success("Your project ideas are ready!")

                # Ocean confetti
                st.markdown("""
                <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
                <script>
                    confetti({
                        particleCount: 200,
                        spread: 80,
                        origin: { y: 0.6 },
                        colors: ['#0ea5e9', '#0284c7', '#7dd3fc', '#bae6fd', '#e0f2fe']
                    });
                </script>
                """, unsafe_allow_html=True)

                with st.container(border=True):
                    st.markdown("#### Generated Ideas")
                    st.markdown(ideas)

                # FIXED SAVE BUTTON - Reliable feedback
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Save These Ideas", type="secondary"):
                        st.session_state.saved_ideas.append({
                            "topic": interests.capitalize(),
                            "ideas": ideas
                        })
                        st.success(f"\"{interests.capitalize()}\" ideas saved! Check the sidebar.")
                        st.rerun()

            except Exception as e:
                st.error("Request failed.")
                st.info("Daily free quota may be reached. Try again tomorrow or create a new API key.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #475569; font-size: 14px;'>Built by Chacha • Powered by Google Gemini</p>", unsafe_allow_html=True)