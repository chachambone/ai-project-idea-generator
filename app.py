import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit_confetti as confetti  # Make sure you have: pip install streamlit-confetti

# Load environment variables
load_dotenv()

# Page config - cute and centered!
st.set_page_config(
    page_title="AI Project Idea Generator ✨",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ultimate cuteness
st.markdown("""
<style>
    .main { background-color: #fff5f8; }
    .stApp { background: linear-gradient(to bottom, #ffeef8, #f8f0ff); }
    h1 { 
        color: #ff6bc2; 
        font-family: 'Comic Sans MS', cursive, sans-serif; 
        text-align: center; 
    }
    .stTextInput > div > div > input { 
        border-radius: 20px; 
        padding: 12px; 
        background-color: white;
    }
    .stButton > button {
        background: linear-gradient(to right, #ff9ecf, #c5a3ff);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 12px 30px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 105, 194, 0.3);
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 105, 194, 0.5);
    }
    /* Pretty border for the scrollable container */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-left: 8px solid #ff6bc2 !important;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(255, 105, 194, 0.15);
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# Title & subtitle
st.title("🤖 AI Project Idea Generator ✨")
st.markdown("<p style='text-align: center; color: #aa77aa;'>Your personal AI mentor for fun & creative project ideas!</p>", unsafe_allow_html=True)

# User input
interests = st.text_input(
    "What are you interested in? 🌟",
    placeholder="e.g., business ideas, restaurant tech, games, art, robots...",
    key="interests_input"
)

if st.button("Generate Magical Ideas! 🎀", use_container_width=True):
    if not interests.strip():
        st.warning("Please tell me what you're curious about! 💕")
    else:
        with st.spinner("Sprinkling AI magic... 🪄"):
            try:
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    st.error("Oops! GEMINI_API_KEY not found in .env file 😢")
                    st.stop()

                client = OpenAI(
                    api_key=api_key,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )

                prompt = f"""
                Generate 3 creative and doable AI/ML project ideas based on the interest: "{interests}".
                For each idea, include:
                - A catchy title
                - Short description
                - Difficulty level (Beginner/Intermediate/Advanced)
                - Key technologies/libraries to use
                - Why it's fun or useful

                Make them super inspiring and exciting for someone learning AI!
                """

                response = client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=[
                        {"role": "system", "content": "You are a bubbly, enthusiastic AI project mentor who loves helping people build cool things!"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9,
                    max_tokens=1200
                )

                ideas = response.choices[0].message.content

                st.success("Here are your sparkling project ideas! 🎉")

                # CONFETTI EXPLOSION!!!
                confetti.cannon(
                    particleCount=200,
                    spread=70,
                    startVelocity=45,
                    colors=['#ff6bc2', '#c5a3ff', '#ffeef8', '#ff9ecf']
                )

                # PERFECT SCROLLABLE BOX - this is the magic fix!
                with st.container(height=700, border=True):
                    st.markdown(ideas)

            except Exception as e:
                st.error(f"Oh no! Something went wrong: {str(e)}")
                st.info("Check your GEMINI_API_KEY and internet connection! 🌐")

# Footer
st.markdown("<p style='text-align: center; color: #cc99cc; margin-top: 80px;'>Made with 💕 by Chacha & Grok</p>", unsafe_allow_html=True)