"""client left event"""

from typing import Annotated, Literal, Optional, cast

from pydantic import Field, TypeAdapter

from ..datatype import InvokerInfo
from ..datatype.pydantic import BytesInt, FlattenInfo
from .base import EventBase
from .manager import EventManager


class ClientLeftEventBase(EventBase):
    """玩家退出服务器"""

    NAME = "notifyclientleftview"
    cfid: int
    ctid: int
    clid: int
    """被踢出或者 ban 时会有 reasonid"""


class ClientLeftQuitEmptyEvent(ClientLeftEventBase):
    """玩家自己退出服务器 (ts5 或者 ts3 不设置 Disconnect Message)"""


class ClientLeftQuitEvent(ClientLeftEventBase):
    """玩家自己退出服务器"""

    reasonid: Annotated[Literal[8], BytesInt]
    reasonmsg: str


class ClientLeftConnectLostEvent(ClientLeftEventBase):
    """玩家因连接断开离开服务器"""

    reasonid: Annotated[Literal[3], BytesInt]
    reasonmsg: str


class ClientLeftKickEvent(ClientLeftEventBase):
    """玩家被踢出服务器"""

    reasonid: Annotated[Literal[5], BytesInt]
    reasonmsg: Optional[str]
    invoker: Annotated[InvokerInfo, FlattenInfo(prefix="invoker")]


class ClientLeftBanEvent(ClientLeftEventBase):
    """玩家在服务器中被 ban"""

    reasonid: Annotated[Literal[6], BytesInt]
    reasonmsg: Optional[str]
    invoker: Annotated[InvokerInfo, FlattenInfo(prefix="invoker")]
    bantime: int
    """为 0 时表示永久 ban"""


type ClientLeftEvent = Annotated[
    ClientLeftKickEvent
    | ClientLeftQuitEvent
    | ClientLeftConnectLostEvent
    | ClientLeftBanEvent
    | ClientLeftQuitEmptyEvent,
    Field(union_mode="smart"),
]

ClientLeftEventTA = TypeAdapter[ClientLeftEvent](ClientLeftEvent)

EventManager.EVENT_TYPE_LIST[ClientLeftEventBase.NAME] = cast("TypeAdapter[EventBase]", ClientLeftEventTA)
