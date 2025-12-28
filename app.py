import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()

# Page config - cute and centered!
st.set_page_config(
    page_title="AI Project Idea Generator ✨",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
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
    /* Full width magic */
    .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    /* Pretty container styling */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-left: 8px solid #ff6bc2 !important;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(255, 105, 194, 0.15);
        background: white;
        padding: 30px;
    }
    /* Text visibility fix */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] {
        color: #333333 !important;
        font-weight: 500;
        line-height: 1.6;
        font-size: 16px;
    }
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] b {
        color: #ff6bc2 !important;
    }
</style>
""", unsafe_allow_html=True)

# === CUTE SIDEBAR ===
with st.sidebar:
    st.image("https://em-content.zobj.net/source/apple/391/robot_1f916.png", width=100)
    st.markdown("### ✨ Customize Your Magic!")
    
    num_ideas = st.slider("Number of ideas", 1, 10, 3)
    
    difficulty = st.selectbox(
        "Difficulty level",
        ["Any", "Beginner", "Intermediate", "Advanced"]
    )
    
    st.markdown("---")
    st.markdown("**Tips:**")
    st.caption("🌸 Try 'AI art', 'games', 'health', 'environment'")
    st.caption("🎀 Use the slider for more inspiration!")
    st.caption("Made with 💖 by Chacha")

# Title & subtitle
st.title("🤖 AI Project Idea Generator ✨")
st.markdown("<p style='text-align: center; color: #aa77aa;'>Your personal AI mentor for fun & creative project ideas!</p>", unsafe_allow_html=True)

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

                Jump straight to the ideas. Make them inspiring and exciting!{difficulty_prompt}
                """

                response = client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=[
                        {"role": "system", "content": "You are an enthusiastic AI project mentor. Jump straight into generating the ideas without long introductions."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9,
                    max_tokens=2000
                )

                ideas = response.choices[0].message.content

                st.success("Here are your sparkling project ideas! 🎉")

                # CUSTOM RAINBOW CONFETTI (Best & Reliable!)
                st.markdown("""
                <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
                <script>
                    confetti({
                        particleCount: 300,
                        spread: 100,
                        origin: { y: 0.6 },
                        colors: ['#ff6bc2', '#c5a3ff', '#ffeef8', '#ff9ecf', '#a8e6cf', '#ffd93d']
                    });
                </script>
                """, unsafe_allow_html=True)

                # Scrollable ideas box
                with st.container(height=1200, border=True):
                    st.markdown(ideas)

            except Exception as e:
                st.error(f"Oh no! Something went wrong: {str(e)}")
                st.info("Check your GEMINI_API_KEY and internet connection! 🌐")

# Footer
st.markdown("<p style='text-align: center; color: #cc99cc; margin-top: 80px;'>Made with 💖 by Chacha </p>", unsafe_allow_html=True)