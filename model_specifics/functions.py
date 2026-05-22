import json
from typing import Callable, List, Mapping, NamedTuple, TypeAlias, TypeVar

from model_specifics.responses import ResponseType

RESPONSE = TypeVar('RESPONSE')
RESPONSE_TEXT = TypeVar('RESPONSE')

FUNC_INVOKATION_RESULT: TypeAlias = dict


class Function(NamedTuple):
    
    name: str
    
    args: Mapping[str, str]
    p_kwargs: Mapping[str, Mapping[str, str]]


# TODO split this to e.g. tool call and create
class FunctionToolCall:
    

    def __init__(self, 
                 name: str, 
                 args: Mapping[str, str], 
                 resp_type: ResponseType, 
                 _id: str, 
                 call_id: str) -> None:

        self.name = name
        self.args = args
        self.resp_type = resp_type

        self._id = _id
        self.call_id = call_id

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return 'NAME: %s - ARGS: %s - RESP TYPE: %s' % (self.name, self.args, self.resp_type, )


def gather_tool_calls(response_item: RESPONSE, 
                      verbosity: bool) -> List[FunctionToolCall]:
    
    func_calls = []

    for item in response_item.output:

        if item.type == 'function_call':
            
            function_tool_call = FunctionToolCall(name=item.name,
                                                  args=json.loads(item.arguments),
                                                  resp_type=ResponseType.TOOL_FUNCTION_CALL,
                                                  _id=item.id,
                                                  call_id=item.call_id)
           
            func_calls.append(function_tool_call)

        else:
            print('UNKWOWN TYPE: %s', (item.type, ))

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



