"""channel edited event"""

from typing import cast

from pydantic import TypeAdapter

from .base import EventBase
from .manager import EventManager


# TODO(plusls): 完善该事件
class ChannelEditedEvent(EventBase, extra="ignore"):
    """频道属性修改事件"""

    NAME = "notifychanneledited"


ChannelEditedEventTA = TypeAdapter[ChannelEditedEvent](ChannelEditedEvent)


EventManager.EVENT_TYPE_LIST[ChannelEditedEvent.NAME] = cast("TypeAdapter[EventBase]", ChannelEditedEventTA)
