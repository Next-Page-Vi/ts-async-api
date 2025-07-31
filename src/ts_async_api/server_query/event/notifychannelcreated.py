"""channel created event"""

from typing import cast

from pydantic import TypeAdapter

from .base import EventBase
from .manager import EventManager


# TODO(plusls): 完善该事件
class ChannelCreatedEvent(EventBase, extra="ignore"):
    """频道创建事件"""

    NAME = "notifychannelcreated"


ChannelCreatedEventTA = TypeAdapter[ChannelCreatedEvent](ChannelCreatedEvent)


EventManager.EVENT_TYPE_LIST[ChannelCreatedEvent.NAME] = cast("TypeAdapter[EventBase]", ChannelCreatedEventTA)
