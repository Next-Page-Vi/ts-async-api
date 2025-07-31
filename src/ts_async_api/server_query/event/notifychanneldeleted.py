"""channel deleted event"""

from typing import cast

from pydantic import TypeAdapter

from .base import EventBase
from .manager import EventManager


# TODO(plusls): 完善该事件
class ChannelDeletedEvent(EventBase, extra="ignore"):
    """频道删除事件"""

    NAME = "notifychanneldeleted"


ChannelDeletedEventTA = TypeAdapter[ChannelDeletedEvent](ChannelDeletedEvent)


EventManager.EVENT_TYPE_LIST[ChannelDeletedEvent.NAME] = cast("TypeAdapter[EventBase]", ChannelDeletedEventTA)
