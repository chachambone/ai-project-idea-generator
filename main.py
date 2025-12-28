import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

def generate_idea(interests: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY in your .env file")

    # Official Gemini OpenAI-compatible endpoint
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
    
    Make them inspiring for someone learning AI!
    """

    response = client.chat.completions.create(
        model="gemini-1.5-flash-latest",  # Latest fast model (free tier friendly)
        # Try "gemini-1.5-pro-latest" if you want smarter ideas (might hit limits faster)
        messages=[
            {"role": "system", "content": "You are an expert AI project mentor full of enthusiasm."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=1000
    )

    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="AI Project Idea Generator (Powered by Gemini)")
    parser.add_argument("interests", type=str, help="Your interests (e.g., 'natural language processing')")
    args = parser.parse_args()
    
    print("🤖 Generating awesome project ideas for you...")
    idea = generate_idea(args.interests)
    print("\n" + idea)

if __name__ == "__main__":
    main()