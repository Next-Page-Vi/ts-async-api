"""ts3 msg"""

import re
from abc import ABC
from typing import Optional, Self

from pydantic import BaseModel

from .exception import ParseException
from .utils import FlattenMixin, unescape

__MSG_PATTERN: re.Pattern[bytes] = re.compile(rb"^((\w+)=(\S+))( (\w+)=(\S+))*$")
__MSG_KV_PATTERN: re.Pattern[bytes] = re.compile(rb"(\w+)=(\S+)")


def parse_msg(msg_data: bytes) -> Optional[dict[str, bytes]]:
    """解析消息"""
    matches = __MSG_PATTERN.fullmatch(msg_data)
    if not matches:
        return None
    ret: dict[str, bytes] = {}
    for m in __MSG_KV_PATTERN.finditer(msg_data):
        k, v = m.groups()
        assert k not in ret
        ret[k.decode()] = unescape(v)
    return ret


class ResBase(BaseModel, FlattenMixin, ABC, extra="forbid"):
    """命令的执行结果"""

    @classmethod
    def from_payload(cls, payload: bytes) -> Self:
        """从 payload 中反序列化出 Res"""
        res = parse_msg(payload)
        if res is None:
            raise ParseException(payload)
        return cls(**res)
