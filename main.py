import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load .env variables

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_idea(interests: str) -> str:
    prompt = f"""
    Generate a creative, feasible AI/ML project idea based on the interests: '{interests}'.
    Make it suitable for a beginner to intermediate level.
    Include: 
    - A short title
    - 1-2 sentence description
    - Key technologies (e.g., Python, scikit-learn)
    - Why it's cool/ useful
    Keep it under 150 words.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Swap to gpt-4o for better results if you have access
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()

def main():
    parser = argparse.ArgumentParser(description="AI Project Idea Generator")
    parser.add_argument("interests", type=str, help="Your interests (e.g., 'computer vision beginner')")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="OpenAI model to use")
    args = parser.parse_args()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in .env file!")
        return
    
    idea = generate_idea(args.interests)
    print(f"Generated Idea:\n{idea}")

if __name__ == "__main__":
    main()