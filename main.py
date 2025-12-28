import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
import textwrap

# Load environment variables from .env
load_dotenv()

def generate_idea(interests: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY in your .env file")

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

    Start directly with the first idea (no long introduction). Make them inspiring!
    """

    response = client.chat.completions.create(
        model="gemini-2.5-flash",  # Latest fast model as of Dec 2025
        messages=[
            {"role": "system", "content": "You are an expert AI project mentor. Be direct and list the 3 ideas clearly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=2000  # More space for full detailed ideas
    )

    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="AI Project Idea Generator (Powered by Gemini)")
    parser.add_argument("interests", type=str, nargs="?", default="natural language processing",
                        help="Your interests (e.g., 'natural language processing') - optional for interactive mode")
    args = parser.parse_args()
    
    interests = args.interests
    if not interests:
        interests = input("What topic are you interested in? (e.g., natural language processing): ").strip()
        if not interests:
            interests = "natural language processing"
    
    print("🤖 Generating awesome project ideas for you...\n")
    ideas = generate_idea(interests)
    
    # Clean, beautiful output
    print("✨ Here are your 3 sparkling project ideas! ✨\n")
    print(textwrap.fill(ideas, width=100))
    print("\n🎉 Happy building! 🚀")

if __name__ == "__main__":
    main()