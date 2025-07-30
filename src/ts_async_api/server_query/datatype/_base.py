"""base type"""

from abc import ABC
from typing import Self

from pydantic import BaseModel

from ..exception import ParseException
from ..msg import parse_msg
from .pydantic import FlattenMixin, UnescapeMixin


class ResBase(BaseModel, UnescapeMixin, FlattenMixin, ABC, extra="forbid"):
    """命令的执行结果"""

    @classmethod
    def from_payload(cls, payload: bytes) -> Self:
        """从 payload 中反序列化出 Res"""
        res = parse_msg(payload)
        if res is None:
            raise ParseException(payload)
        return cls(**res)


class InvokerInfo(BaseModel, extra="forbid"):
    """invoker info"""

    id: int
    name: str
    uid: str


class Version(ResBase):
    """版本信息"""

    version: str
    build: int
    platform: str
