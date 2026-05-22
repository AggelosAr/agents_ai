import argparse
import json
from typing import Callable, Mapping

from functions.get_file_contents import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_files_info import ResultObject, get_files_info

from model_specifics.functions import gather_tool_calls
from model_specifics.logs import show_response, show_usage, show_user_message
from model_specifics.open_ai.client import _OpenAI
from model_specifics.open_ai.prompts import \
    SYSTEM_PROMPT as OPEN_AI_SYSTEM_PROMPT
from model_specifics.open_ai.tools import TOOLS as OPEN_AI_TOOLS


FUNCTIONS: Mapping[str, Callable] = {
    'get_file_content': get_file_content,
    'write_file': write_file,
    'run_python_file': run_python_file,
    'get_files_info': get_files_info
}


def init() -> tuple[_OpenAI, argparse.Namespace]:
    client = _OpenAI()

    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument('user_prompt', type=str, help='User prompt')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    print('----------------------------')
    print('args ->>>>>>> ', args)
    print('----------------------------')

    return client, args


def main():

    client, args = init()
    verbosity = args.verbose or True

    # prompt = 'Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    messages = [
            {
                'role': 'system',
                'content': OPEN_AI_SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': f'{args.user_prompt}'
            }
    ]

    response = True
    MAX_ITERATIONS = 3
    iterations = 0

    while response and iterations < MAX_ITERATIONS:
        
        iterations += 1

        # 1. Get response from the last message
        response = client.responses.create(
            model=client.my_default_model,
            input=messages,
            tools=OPEN_AI_TOOLS,
            temperature=0
        )

        # 2. Print the user query and the response in a user-friendly manner
        _ = show_user_message(user_prompt=messages[-1], verbosity=verbosity)

        # 3. Update messages with the response output
        messages.extend(response.output)

        # 4. Find function calls and collect them if any
        # 5. Show the tool calls.
        tool_calls = gather_tool_calls(response_item=response,
                                       verbosity=verbosity)

        if not tool_calls:
            print('\n\n\t[*] AI NO TOOL CALLS BREAK [*]')
            break

        # Keep 1 tool call for now 
        tool_call = tool_calls[0]

        # 6. Show usage
        _ = show_usage(response=response, verbosity=verbosity)
        
        # 7. Call functions if you found any
        function_to_call = FUNCTIONS.get(tool_call.name)

        try: 
            called_function_result = function_to_call(**tool_call.args)
        except Exception as e:
            print('Exception: %s' % (str(e), )) 
            break

        # 8. Update the messages with the results of the functions calls
        messages.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(called_function_result),
            }
        )
        print('\n\n\t[*] ADDED FUNCTION CALL RESULT AT MESSAGES')
        print(str(called_function_result))



        # messages.extend(resp)
        # messages.extend(func_calls)

        print('\n\n\t\t-----------------------------------------------------------------')



if __name__=='__main__':
    main()
