from model_specifics.responses import ResponseObject


def show_user_message(*, user_prompt: dict, verbosity: bool) -> None:

    if verbosity:
        print('\n\n\t[*] User prompt\n\n\t\t\t%s\n\n\t\t\t%s'
              % (user_prompt.get('role'), user_prompt.get('content'), ))
        

def show_response(*, response: ResponseObject, verbosity: bool) -> None:
    
    if verbosity:

        for item in response.output:
            
            if item.type == 'function_call':
                
                print('\n\n\t[*] Response: \n\n\t\t\t%s', (item, ))
                print()
                
            if item.type == 'message':

                print('\n\n\t[*] Response: Function Call:\n\n\t\t\t%s', (item, ))
                print()


def show_usage(*, response: ResponseObject, verbosity: bool) -> None:

    if verbosity:
        print()
        print()
        print()
        print('\t\t-------------------------------')
        print('\t\t| -> Prompt tokens: %s' % (response.usage.input_tokens, ))
        print('\t\t| -> Response tokens: %s' % (response.usage.output_tokens, ))
        print('\t\t-------------------------------')
        print()
        print()
        print()

