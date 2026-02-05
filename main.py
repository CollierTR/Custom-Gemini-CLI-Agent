import os
from dotenv import load_dotenv
import argparse
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("No api key found...")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)

if response.usage_metadata == None:
    raise RuntimeError("Some ill thing has befallen us...")

if args.verbose:
    print(" ")
    print("--------------------------------")
    print("User prompt: ", args.user_prompt)
    print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
    print("Response tokens: ", response.usage_metadata.candidates_token_count)
    print("--------------------------------")
    print(" ")

if response.function_calls:
    print("--------------------------------")

    function_results = []

    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
        function_call_result = call_function(function_call)

        # validation
        if not function_call_result.parts:
            raise Exception("Error: function_call_result does not have PARTS property")
        if not function_call_result.parts[0].function_response:
            raise Exception("Error: No function_response object found")
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Error: No function_response found")

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
        function_results.append(function_call_result.parts[0])

    print("--------------------------------")
    print(" ")
else:
    print(response.text)
