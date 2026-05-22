from enum import Enum
from typing import Any


class ResponseType(Enum):
    TOOL_FUNCTION_CALL = 1
    AI_MESSAGE = 2


# trick type checker for now
class ResponseContentObject:
    text: str


class ResponseOutputObject:

    #
    type: ResponseType

    name: str
    arguments: Any
    
    #
    id: str

    call_id: str

    content: list[ResponseContentObject]


class UsageObject:

    input_tokens: str | int | float
    output_tokens: str | int | float


class ResponseObject:
    
    item_type: ResponseType
    call_id: str

    output: list[ResponseOutputObject]

    usage: UsageObject
    