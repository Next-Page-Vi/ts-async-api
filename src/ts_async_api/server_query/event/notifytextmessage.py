"""text message event"""

from typing import cast

from pydantic import TypeAdapter

from .base import EventBase
from .manager import EventManager


# TODO(plusls): 完善该事件
class TextMessageEvent(EventBase, extra="ignore"):
    """文本事件"""

    NAME = "notifytextmessage"


TextMessageEventTA = TypeAdapter[TextMessageEvent](TextMessageEvent)


EventManager.EVENT_TYPE_LIST[TextMessageEvent.NAME] = cast("TypeAdapter[EventBase]", TextMessageEventTA)
