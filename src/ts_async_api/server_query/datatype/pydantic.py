"""pydantic helper"""

from collections import defaultdict
from typing import Annotated, Any, Optional, cast

from pydantic import BaseModel, BeforeValidator, StrictBytes, StrictStr, TypeAdapter, ValidationError, model_validator

from ..utils import unescape

__INT_LIST_TA = TypeAdapter[list[int]](list[int])


def __parse_bytes_int_list(v: Any) -> Any:
    if not isinstance(v, bytes):
        return v
    v_list = v.split(b",")
    return __INT_LIST_TA.validate_python(v_list)


BytesIntList = Annotated[list[int], BeforeValidator(__parse_bytes_int_list)]


class FlattenInfo:
    """flatten model info"""

    prefix: str

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix


StrDictTA = TypeAdapter[dict[str, Optional[bytes]]](dict[StrictStr, Optional[StrictBytes]])


class FlattenMixin:
    """flatten validator mixin"""

    @model_validator(mode="before")
    @classmethod
    def __collect_flatten(cls, data: Any) -> Any:
        typed_cls = cast("type[BaseModel]", cls)  # make mypy happy

        # 遍历所有 field, 收集 FlattenInfo
        # flatten_prefix -> key
        flatten_map: dict[str, str] = {}
        for k, v in typed_cls.model_fields.items():
            for o in v.metadata:
                if isinstance(o, FlattenInfo):
                    assert o.prefix not in flatten_map
                    flatten_map[o.prefix] = k
        if len(flatten_map) == 0:
            return data

        # 检查 data 的类型, 不为 dict 则直接跳过
        try:
            typed_data = StrDictTA.validate_python(data)
            data.clear()
        except ValidationError:
            return data

        ret: dict[str, Optional[bytes | dict[str, Optional[bytes]]]] = data
        flatten_data: dict[str, dict[str, Optional[bytes]]] = defaultdict(dict)
        # 从 typed_data 中收集 Flatten 的字段并去除 prefix
        for k, value in typed_data.items():
            for flatten_prefix, nest_key in flatten_map.items():
                if k.startswith(flatten_prefix):
                    suffix = k[len(flatten_prefix) :]
                    if suffix:
                        flatten_data[nest_key][suffix] = value
                        break
            else:
                ret[k] = value
        ret.update(flatten_data)
        return data


class UnescapeMixin:
    """flatten validator mixin"""

    @model_validator(mode="before")
    @classmethod
    def __unescape_value(cls, data: Any) -> Any:
        typed_cls = cast("type[BaseModel]", cls)  # make mypy happy

        unescape_key_set: set[str] = set()
        for k, v in typed_cls.model_fields.items():
            if v.annotation in (str, Optional[str]):
                unescape_key_set.add(k)

        # 检查 data 的类型, 不为 dict 则直接跳过
        try:
            typed_data = StrDictTA.validate_python(data)
            data.clear()
        except ValidationError:
            return data

        ret: dict[str, Optional[bytes]] = data
        # unescape
        for k, value in typed_data.items():
            if value is not None and k in unescape_key_set:
                ret[k] = unescape(value)
            else:
                ret[k] = value
        return ret


__INT_TA = TypeAdapter[int](int)


def __parse_bytes_int(v: Any) -> int:
    return __INT_TA.validate_python(v)


BytesInt = BeforeValidator(__parse_bytes_int)
