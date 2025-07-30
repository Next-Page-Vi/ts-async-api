"""utils"""

import logging
import os
from collections import defaultdict
from typing import Any, Literal, Optional, cast

from pydantic import BaseModel, BeforeValidator, StrictBytes, StrictStr, TypeAdapter, ValidationError, model_validator

__ESCAPE_MAP: dict[int, bytes] = {
    b"\\"[0]: rb"\\",
    b"/"[0]: rb"\/",
    b" "[0]: rb"\s",
    b"|"[0]: rb"\p",
    b"\a"[0]: rb"\a",
    b"\b"[0]: rb"\b",
    b"\f"[0]: rb"\f",
    b"\n"[0]: rb"\n",
    b"\r"[0]: rb"\r",
    b"\t"[0]: rb"\t",
    b"\v"[0]: rb"\v",
}
__UNESCAPE_MAP: dict[bytes, int] = {v: k for k, v in __ESCAPE_MAP.items()}
__MAX_ESCAPE_LEN = max(len(k) for k in __UNESCAPE_MAP)


def escape(data: bytes) -> bytes:
    """Escapes characters that need escaping according to __ESCAPE_MAP"""
    return b"".join(__ESCAPE_MAP.get(b, bytes([b])) for b in data)


def unescape(data: bytes) -> bytes:
    """Undo escaping of characters according to __ESCAPE_MAP"""
    result = bytearray()
    i = 0
    while i < len(data):
        if data[i : i + 1] == b"\\":
            for match_len in range(2, __MAX_ESCAPE_LEN + 1):  # 尝试匹配 \x 这样的
                part = data[i : i + match_len]
                res = __UNESCAPE_MAP.get(part)
                if res is not None:
                    result.append(res)
                    i += match_len
                    continue
        result.append(data[i])
        i += 1
    return bytes(result)


def init_logger(
    log_level: Literal["CRITICAL", "FATAL", "ERROR", "WARN", "INFO", "DEBUG"] = "DEBUG",
) -> None:
    """初始化日志"""
    logging.root.setLevel(level=log_level)
    if "PYTEST_VERSION" not in os.environ:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        formatter = logging.Formatter(log_format)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logging.root.addHandler(stream_handler)


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
