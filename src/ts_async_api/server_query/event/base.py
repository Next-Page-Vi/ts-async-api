"""event base"""

from abc import ABC
from typing import ClassVar

from pydantic import BaseModel

from ..msg import ResBase


class EventBase(ResBase, ABC):
    """事件基类"""

    NAME: ClassVar[str]


class Invoker(BaseModel, extra="forbid"):
    """invoker info"""

    id: int
    name: str
    uid: str
