"""server edited event"""

from typing import cast

from pydantic import TypeAdapter

from .base import EventBase
from .manager import EventManager


# TODO(plusls): 完善该事件
class ServerEditedEvent(EventBase, extra="ignore"):
    """服务器信息修改事件"""

    NAME = "notifyserveredited"


ServerEditedEventTA = TypeAdapter[ServerEditedEvent](ServerEditedEvent)


EventManager.EVENT_TYPE_LIST[ServerEditedEvent.NAME] = cast("TypeAdapter[EventBase]", ServerEditedEventTA)
