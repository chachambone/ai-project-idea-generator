import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Page config - make it cute!
st.set_page_config(
    page_title="AI Project Idea Generator ✨",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for maximum cuteness + VISIBLE TEXT!
st.markdown("""
<style>
    .main { background-color: #fff5f8; }
    .stApp { background: linear-gradient(to bottom, #ffeef8, #f8f0ff); }
    h1 { color: #ff6bc2; font-family: 'Comic Sans MS', cursive, sans-serif; text-align: center; }
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
    .idea-box {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(255, 105, 194, 0.15);
        margin: 20px 0;
        border-left: 8px solid #ff6bc2;
    }
    /* THIS IS THE MAGIC FIX: Force all text inside ideas to be dark and readable */
    .idea-box, .idea-box * {
        color: #333333 !important;
        font-size: 16px;
        line-height: 1.6;
    }
    .idea-box h3, .idea-box strong {
        color: #ff6bc2 !important;
    }
</style>
""", unsafe_allow_html=True)

# Title with sparkles
st.title("🤖 AI Project Idea Generator ✨")
st.markdown("<p style='text-align: center; color: #aa77aa;'>Your personal AI mentor for fun & creative project ideas!</p>", unsafe_allow_html=True)

# Input
interests = st.text_input(
    "What are you interested in? 🌟",
    placeholder="e.g., natural language processing, computer vision, games, art...",
    key="interests_input"
)

if st.button("Generate Magical Ideas! 🎀"):
    if not interests.strip():
        st.warning("Please tell me what you're curious about! 💕")
    else:
        with st.spinner("Thinking of super cool ideas just for you... 🦄"):
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
                    max_tokens=1000
                )

                ideas = response.choices[0].message.content

                st.success("Here are your sparkling project ideas! 🎉")
                st.markdown(f"<div class='idea-box'>{ideas}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Oh no! Something went wrong: {str(e)}")
                st.info("Make sure your GEMINI_API_KEY is valid and you have internet! 🌐")

# Footer
st.markdown("<p style='text-align: center; color: #cc99cc; margin-top: 50px;'>Made with 💕 by Chacha & Grok</p>", unsafe_allow_html=True)