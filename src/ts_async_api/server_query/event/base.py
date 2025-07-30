"""event base"""

from abc import ABC
from typing import ClassVar

from ..datatype import ResBase


class EventBase(ResBase, ABC):
    """事件基类"""

    NAME: ClassVar[str]
