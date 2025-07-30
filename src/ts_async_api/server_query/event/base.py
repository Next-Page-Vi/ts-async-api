"""event base"""

from abc import ABC
from typing import ClassVar

from ..msg import ResBase


class EventBase(ResBase, ABC):
    """事件基类"""

    NAME: ClassVar[str]
