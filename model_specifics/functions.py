import json
from typing import Callable, List, Mapping, NamedTuple, TypeAlias, TypeVar

RESPONSE = TypeVar('RESPONSE')
RESPONSE_TEXT = TypeVar('RESPONSE')

FUNC_INVOKATION_RESULT: TypeAlias = dict


class Function(NamedTuple):
    
    name: str
    
    args: Mapping[str, str]
    p_kwargs: Mapping[str, Mapping[str, str]]


class ModelFunction(NamedTuple):
    
    name: str
    args: Mapping[str, str]


def gather_function_calls(response_item: RESPONSE, 
                          verbosity: bool) -> List[ModelFunction]:
    
    func_calls = []


    for item in response_item.output:

        if item.type == 'function_call':
            
            if item.name == "get_horoscope":
                sign = json.loads(item.arguments)["sign"]
            
        else:
            ...

    return func_calls


def run_functions(funcs: list[Callable], *args, **kwargs) -> FUNC_INVOKATION_RESULT:

    # file_path = json.loads(item.arguments)['file_path']
    # (err, status, msg), files_info = get_files_info(file_path=file_path)
    # return {
    #     'type': 'function_call_output',
    #     'call_id': item.call_id,
    #     'output': files_info,
    # }
    ...



