import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

def generate_idea(interests: str):
    # Load your Gemini key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY in your .env file")

    # Point to Gemini's OpenAI-compatible endpoint
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # A better prompt for cool AI project ideas
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
        model="gemini-1.5-flash",  # Fast, free-tier friendly, and smart! (You can try gemini-1.5-pro later)
        messages=[
            {"role": "system", "content": "You are an expert AI project mentor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
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