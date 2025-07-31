"""channel password changed event"""

from typing import cast

from pydantic import TypeAdapter

from .base import EventBase
from .manager import EventManager


# TODO(plusls): 完善该事件
class ChannelPasswordChangedEvent(EventBase, extra="ignore"):
    """频道密码修改事件"""

    NAME = "notifychannelpasswordchanged"


ChannelPasswordChangedEventTA = TypeAdapter[ChannelPasswordChangedEvent](ChannelPasswordChangedEvent)


EventManager.EVENT_TYPE_LIST[ChannelPasswordChangedEvent.NAME] = cast(
    "TypeAdapter[EventBase]", ChannelPasswordChangedEventTA
)
