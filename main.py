import argparse

from model_specifics.functions import gather_tool_calls
from model_specifics.logs import show_response, show_usage, show_user_message
from model_specifics.open_ai.client import _OpenAI
from model_specifics.open_ai.prompts import \
    SYSTEM_PROMPT as OPEN_AI_SYSTEM_PROMPT
from model_specifics.open_ai.tools import TOOLS as OPEN_AI_TOOLS


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
    verbosity = args.verbose

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

    while response:

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
        tool_calls = gather_tool_calls(response_item=response,
                                       verbosity=verbosity)

        # 5. Show the tool calls.
        # _ = show_response(response=response, verbosity=verbosity) ?
        for tool_call in tool_calls:
            print(tool_call)

        # 6. Show usage
        _ = show_usage(response=response, verbosity=verbosity)
        
        # 7. Call functions if you found any
        ...

        # 8. Update the messages with the results of the functions calls
        ...
        

        # messages.extend(resp)
        # messages.extend(func_calls)

        print('\n\n\t\t-----------------------------------------------------------------')

        break
        # input()


if __name__=='__main__':
    main()
