from enum import Enum
from typing import NamedTuple


class ResponseType(Enum):
    TOOL_FUNCTION_CALL = 1


class ResponseObject(NamedTuple):
    
    item_type: ResponseType
    call_id: str
