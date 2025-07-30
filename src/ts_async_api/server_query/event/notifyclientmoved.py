"""client moved event"""

from typing import Annotated, Literal, Optional, cast

from pydantic import Field, TypeAdapter

from ..datatype import InvokerInfo
from ..datatype.pydantic import BytesInt, FlattenInfo
from .base import EventBase
from .manager import EventManager


class ClientMovedEventBase(EventBase):
    """玩家频道移动事件"""

    NAME = "notifyclientmoved"
    ctid: int
    """移动到的频道"""
    clid: int
    """client id"""


class ClientMovedBySelfEvent(ClientMovedEventBase):
    """玩家自己移动"""

    reasonid: Annotated[Literal[0], BytesInt]


class ClientMovedByOtherEvent(ClientMovedEventBase):
    """玩家被移动"""

    reasonid: Annotated[Literal[1], BytesInt]
    invoker: Annotated[InvokerInfo, FlattenInfo(prefix="invoker")]


class ClientMovedByKickEvent(ClientMovedEventBase):
    """玩家被踢出频道"""

    reasonid: Annotated[Literal[4], BytesInt]
    reasonmsg: Optional[str]
    invoker: Annotated[InvokerInfo, FlattenInfo(prefix="invoker")]


type ClientMovedEvent = Annotated[
    ClientMovedBySelfEvent | ClientMovedByOtherEvent | ClientMovedByKickEvent,
    Field(union_mode="smart"),
]

ClientMovedEventTA = TypeAdapter[ClientMovedEvent](ClientMovedEvent)


EventManager.EVENT_TYPE_LIST[ClientMovedEventBase.NAME] = cast("TypeAdapter[EventBase]", ClientMovedEventTA)
