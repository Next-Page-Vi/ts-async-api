"""client moved event"""

from .base import EventBase
from .manager import EventManager


class ClientMovedEvent(EventBase):
    """玩家频道移动事件"""

    NAME = "notifyclientmoved"
    ctid: int
    """移动到的频道"""
    reasonid: int
    clid: int
    """client id"""


EventManager.EVENT_TYPE_LIST.append(ClientMovedEvent)
