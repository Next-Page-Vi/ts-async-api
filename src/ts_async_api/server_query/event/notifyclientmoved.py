"""client moved event"""

from typing import Annotated, Optional

from ..utils import FlattenInfo
from .base import EventBase, Invoker
from .manager import EventManager


class ClientMovedEvent(EventBase):
    """玩家频道移动事件"""

    NAME = "notifyclientmoved"
    ctid: int
    """移动到的频道"""
    reasonid: int
    """移动理由
    自己移动: 0
    被移动: 1
    kick: 4
    """
    reasonmsg: Optional[str] = None
    """被 kick 时会有 reasonmsg"""
    clid: int
    """client id"""
    invoker: Annotated[Optional[Invoker], FlattenInfo(prefix="invoker")] = None
    """玩家是被移动时会有该字段"""


EventManager.EVENT_TYPE_LIST.append(ClientMovedEvent)
