# main.py

# imports
import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT
from available_fns import available_functions
from call_function import call_function

def main():
    # get api key
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
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

    # ai feedback loop
    for _ in range(20): # caps ai feedback loop at 20 cycles

        # get ai response
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=SYSTEM_PROMPT
                )
        )

        # add model response to conversation history (and raise exception if none)
        if not response.candidates:
            raise RuntimeError("Error: No response candidates.")
        for candidate in response.candidates:
            messages.append(candidate.content)

        # check for token metadata
        if not response.usage_metadata:
            raise RuntimeError("Error: No token metadata found.")

        # printout of verbose info
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # make and handle function calls
        if response.function_calls:
            print("Function calls:")
            function_results = []
            for call in response.function_calls:
                function_call_result = call_function(call, call.args)
                if not function_call_result.parts:
                    raise RuntimeError("Error: Function .parts list is None; supposed to have Part object.")
                if not function_call_result.parts[0].function_response.response:
                    raise RuntimeError("Error: Function result is None.")
                function_results.append(function_call_result)
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
    
            # show ai the results of function calls it makes
            messages.extend(function_results)

        # print response and end loop if no function calls
        else:
            print("Response:")
            print(response.text)
            return

    # handle loop cap being reached
    print("Error: maximum internal feedback loops reached, but model has no final response.")
    sys.exit(1)

if __name__ == "__main__":
    main()
