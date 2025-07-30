"""client moved event"""

from .base import EventBase
from .manager import EventManager


class ClientMovedEvent(EventBase):
    """玩家频道移动事件"""

    NAME = "notifyclientmoved"
    ctid: int
    reasonid: int
    clid: int


EventManager.EVENT_TYPE_LIST.append(ClientMovedEvent)
