"""client left view event"""

from .base import EventBase
from .manager import EventManager


class ClientLeftViewEvent(EventBase):
    """玩家退出服务器"""

    NAME = "notifyclientleftview"
    cfid: int
    ctid: int
    clid: int


EventManager.EVENT_TYPE_LIST.append(ClientLeftViewEvent)
