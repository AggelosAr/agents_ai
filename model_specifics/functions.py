import json
from typing import Mapping, NamedTuple

from model_specifics.open_ai.response_objects import (ResponseObject,
                                                      ResponseType)


class Function(NamedTuple):
    
    name: str
    
    args: Mapping[str, str]
    p_kwargs: Mapping[str, Mapping[str, str]]


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
        return ('\n -> NAME: %s\n -> ARGS: %s\n -> RESP TYPE: %s\n -> ID: %s\n -> CALL ID: %s' 
                % (self.name, self.args, self.resp_type, self._id, self.call_id, ))


def gather_tool_calls(response: ResponseObject, 
                      verbosity: bool) -> list[FunctionToolCall]:
    
    func_calls = [] # type: ignore[var-annotated]

    for item in response.output:

        if item.type == 'function_call':

            print('\n\n\t[*] AI Response')
            print('\t[*] AI Response is a function call')

            function_tool_call = FunctionToolCall(name=item.name,
                                                  args=json.loads(item.arguments),
                                                  resp_type=ResponseType.TOOL_FUNCTION_CALL,
                                                  _id=item.id,
                                                  call_id=item.call_id)
           
            print(function_tool_call)
            func_calls.append(function_tool_call)

        if item.type == 'message':

            print('\n\n\t[*] AI Response')
            print('\t[*] AI Response is a message')
            print(response.output[0].content[0].text)

            print()

    return func_calls

