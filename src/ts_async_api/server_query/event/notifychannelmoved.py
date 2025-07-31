"""channel moved event"""

from typing import cast

from pydantic import TypeAdapter

from .base import EventBase
from .manager import EventManager


# TODO(plusls): 完善该事件
class ChannelMovedEvent(EventBase, extra="ignore"):
    """频道移动事件"""

    NAME = "notifychannelmoved"


ChannelMovedEventTA = TypeAdapter[ChannelMovedEvent](ChannelMovedEvent)


EventManager.EVENT_TYPE_LIST[ChannelMovedEvent.NAME] = cast("TypeAdapter[EventBase]", ChannelMovedEventTA)
