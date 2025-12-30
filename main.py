# main.py

# imports
import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    # get api key
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("No API key found.")
    
    # create Gemini client
    client = genai.Client(api_key=api_key)

    # parse user prompt
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # remember user prompt
    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)]
        )]

    # ask ai
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )

    # check for token metadata
    if response.usage_metadata == None:
        raise RuntimeError("No token metadata found.")

    # printout
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)



if __name__ == "__main__":
    main()
