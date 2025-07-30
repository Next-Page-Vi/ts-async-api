"""pydantic"""

from typing import Annotated, Any

from pydantic import BeforeValidator, TypeAdapter

__INT_LIST_TA = TypeAdapter[list[int]](list[int])


def __parse_bytes_int_list(v: Any) -> Any:
    if not isinstance(v, bytes):
        return v
    v_list = v.split(b",")
    return __INT_LIST_TA.validate_python(v_list)


BytesIntList = Annotated[list[int], BeforeValidator(__parse_bytes_int_list)]
