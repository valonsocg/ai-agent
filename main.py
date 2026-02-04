import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function



def main():
    parser = argparse.ArgumentParser(description="AIbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Api key not found")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    
    for _ in range(20):
        response, function_results = generate_content(client, messages, args.verbose)  
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if function_results:
            messages.append(types.Content(role="user", parts=function_results))   
        if response.function_calls == None:
            return
    print("Agent did not finish within max iterations")
    sys.exit(1)

def generate_content(client, messages, verbose):    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages, 
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt, 
            temperature=0)
    )
    if response.usage_metadata == None:
        raise RuntimeError("Failed Api Request")
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    function_results = []    
    function_calls = response.function_calls   
    if function_calls != None:
        for function_call in function_calls:
            function_call_result = call_function(function_call)
            if not function_call_result.parts:
                raise Exception("no parts in function")
            if function_call_result.parts[0].function_response == None:
                raise Exception("no function response")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("no actual function response")
            function_results.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
           
    else:
        print("Response:")
        print(response.text)
        
    return response, function_results 
    
  

if __name__ == "__main__":
    main()