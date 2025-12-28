# imports
import os
from dotenv import load_dotenv
from google import genai

def main():
    # get api key
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("No API key found.")
    
    # create Gemini client

    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
