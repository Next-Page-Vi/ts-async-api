"""event"""

from collections import defaultdict
from collections.abc import Awaitable, Callable
from logging import getLogger
from typing import TYPE_CHECKING, ClassVar, Optional

from pydantic import TypeAdapter
from sortedcontainers import SortedDict

from ..exception import ParseException
from ..msg import parse_msg
from .base import EventBase, get_event_obj_parent_type_list

if TYPE_CHECKING:
    from ..client import Client
else:
    from typing import Any

    Client = Any

EVENT_LIST: list[type[EventBase]] = []

LOGGER = getLogger(__name__)


class EventManager:
    """事件管理器"""

    EVENT_TYPE_LIST: ClassVar[dict[str, TypeAdapter[EventBase]]] = {}
    event_listener: dict[type[EventBase], SortedDict[int, list[Callable[["Client", EventBase], Awaitable[bool]]]]]

    def __init__(self) -> None:
        self.event_listener = defaultdict(lambda: SortedDict())

    def register(
        self, event: type[EventBase], callback: Callable[["Client", EventBase], Awaitable[bool]], priority: int = 0
    ) -> None:
        """注册事件"""
        priority_event_list = self.event_listener[event]
        priority_event_list.setdefault(priority, []).append(callback)

    @classmethod
    def parse_event(cls, payload: bytes) -> Optional[EventBase]:
        """解析事件"""
        for event_name, event_ta in cls.EVENT_TYPE_LIST.items():
            event_payload_prefix = f"{event_name} ".encode()
            if payload.startswith(event_payload_prefix):
                payload_suffix = payload[len(event_payload_prefix) :]
                res = parse_msg(payload_suffix)
                if res is None:
                    raise ParseException(payload)
                return event_ta.validate_python(res)
        return None

    async def dispatch(self, client: "Client", event: EventBase) -> None:
        """按优先级顺序分发事件。callback 返回 True 表示跳过后续 callback"""
        event_type_list = get_event_obj_parent_type_list(event)

        # (-优先级, class 继承 idx, 插入 idx, callback)
        all_callback_list: list[tuple[int, int, int, Callable[[Client, EventBase], Awaitable[bool]]]] = []

        for event_type_idx, event_type in enumerate(event_type_list):
            priority_event_list = self.event_listener[event_type]
            for pri, callback_list in reversed(list(priority_event_list.items())):
                all_callback_list.extend(
                    (-pri, event_type_idx, i, callback) for i, callback in enumerate(callback_list)
                )
        all_callback_list.sort()
        for _, _, _, callback in all_callback_list:
            try:
                if await callback(client, event):
                    break
            except:
                LOGGER.exception("exception when call event callback, event: %s, callback: %s", event, callback)
                raise

    def remove(self, event_type: type[EventBase], callback: Callable[["Client", EventBase], Awaitable[bool]]) -> None:
        """手动移除指定的 callback"""
        priority_event_list = self.event_listener[event_type]
        for callback_list in reversed(list(priority_event_list.values())):
            # 偷懒了, 实现的比较暴力
            if callback in callback_list:
                callback_list.remove(callback)
                break
        else:
            # 找不到 callback 则报错
            msg = f"Can not found callback {callback} when remove."
            raise ValueError(msg)
