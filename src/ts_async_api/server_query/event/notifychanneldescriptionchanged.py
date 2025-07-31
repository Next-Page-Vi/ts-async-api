"""channel description changed event"""

from typing import cast

from pydantic import TypeAdapter

from .base import EventBase
from .manager import EventManager


# TODO(plusls): 完善该事件
class ChannelDescriptionChangedEvent(EventBase, extra="ignore"):
    """频道描述修改事件"""

    NAME = "notifychanneldescriptionchanged"


ChannelDescriptionChangedEventTA = TypeAdapter[ChannelDescriptionChangedEvent](ChannelDescriptionChangedEvent)


EventManager.EVENT_TYPE_LIST[ChannelDescriptionChangedEvent.NAME] = cast(
    "TypeAdapter[EventBase]", ChannelDescriptionChangedEventTA
)
