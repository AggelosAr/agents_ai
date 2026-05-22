from enum import Enum
from typing import Mapping, NamedTuple


class ResponseType(Enum):
    FUNCTION_CALL = 1


class ResponseObject(NamedTuple):
    
    item_type: ResponseType
    call_id: str
