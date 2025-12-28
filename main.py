import os
from dotenv import load_dotenv
import argparse
from google import genai
from google.genai import types

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
response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)

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

print(response.text)
