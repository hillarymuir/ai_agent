# imports
import os, argparse
from dotenv import load_dotenv
from google import genai

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
    args = parser.parse_args()

    # ask ai
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt
    )

    # check for token metadata
    if response.usage_metadata == None:
        raise RuntimeError("No token metadata found.")

    # print token metadata and response
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)



if __name__ == "__main__":
    main()
