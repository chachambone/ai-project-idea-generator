import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
import textwrap  # For nice wrapped output

# Load environment variables from .env
load_dotenv()

def generate_idea(interests: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY in your .env file")

    # Correct Gemini OpenAI-compatible endpoint (no trailing slash needed in latest examples)
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
        model="gemini-2.5-flash",  # Current stable fast model (Dec 2025)
        messages=[
            {"role": "system", "content": "You are a bubbly, enthusiastic AI project mentor who loves helping people build cool things!"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=1000
    )

    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="AI Project Idea Generator (Powered by Gemini)")
    parser.add_argument("interests", type=str, nargs="?", default="natural language processing",
                        help="Your interests (e.g., 'natural language processing') - optional if you want interactive mode")
    args = parser.parse_args()
    
    interests = args.interests
    if not interests:
        interests = input("What topic are you interested in? (e.g., natural language processing): ").strip()
        if not interests:
            interests = "natural language processing"  # fallback
    
    print("🤖 Generating awesome project ideas for you...\n")
    idea = generate_idea(interests)
    
    # Nice formatted output that won't get cut off weirdly
    print(textwrap.fill(idea, width=100))

if __name__ == "__main__":
    main()