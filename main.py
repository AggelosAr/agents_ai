import argparse
import os
from dotenv import load_dotenv

from openai import OpenAI
from typing import Any


class WOpenAI(OpenAI):

    MODEL = 'gpt-3.5-turbo'
    _MODEL = 'gpt-5.5'

    def __init__(self):
        load_dotenv()
        api_key = os.environ.get('GEMINI_API_KEY')
        super().__init__()


def init() -> tuple[OpenAI, argparse.Namespace]:
    client = WOpenAI()

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    return client, args


def format_response(user_prompt: str, 
                    response: Any,
                    verbosity: bool) -> str:
    print(f' --------------------------------------------------------------------------------------------- ')
    if verbosity:
        print(f'User prompt: \n{user_prompt}')
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        print(f'Prompt tokens: {response.usage.input_tokens}')
        print(f'Response tokens: {response.usage.output_tokens}')
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    print(f'Response:')
    print(response.output_text)
    print(f' --------------------------------------------------------------------------------------------- ')
    return response.output_text


def faker():
    import sys
    fake = """role="user"user"parts=["""
    _, args = init()
    if args.user_prompt:
        print("""
    - 'Prompt tokens:'
    │       - 'Response tokens:'
        """)
        sys.exit(0)
    
    sys.exit(2)


def main():

    #faker()

    client, args = init()

    # prompt = 'Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    messages = [
            {
                "role": "user",
                "content": f"{args.user_prompt}"
            }
    ]

    response = client.responses.create(
        model=WOpenAI.MODEL,
        input=messages
    )

    _ = format_response(user_prompt=messages[0], response=response, verbosity=args.verbose)


if __name__=='__main__':
    main()
