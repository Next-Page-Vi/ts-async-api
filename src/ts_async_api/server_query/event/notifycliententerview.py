"""client enter event"""

from typing import cast

from pydantic import TypeAdapter

from .base import EventBase
from .manager import EventManager


class ClientEnterEvent(EventBase, extra="ignore"):
    """用户登录事件"""

    NAME = "notifycliententerview"
    cfid: int
    ctid: int
    """移动到的频道"""
    reasonid: int
    clid: int
    """client id"""

    # 还有很多额外的字段, 但是考虑到 clientinfo 命令可以获取到这些信息, 因此在这不保存这些信息


ClientEnterEventTA = TypeAdapter[ClientEnterEvent](ClientEnterEvent)


EventManager.EVENT_TYPE_LIST[ClientEnterEvent.NAME] = cast("TypeAdapter[EventBase]", ClientEnterEventTA)
