"""event base"""

from abc import ABC
from typing import ClassVar

from ..datatype import ResBase


class EventBase(ResBase, ABC):
    """事件基类"""

    NAME: ClassVar[str]


def get_event_cls_parent_type_list(cls: type[EventBase]) -> list[type[EventBase]]:
    """获取 event class 的继承树"""
    ret: list[type[EventBase]] = []
    ret.append(cls)
    for c in cls.__bases__:
        if c is EventBase:
            if c not in ret:
                ret.append(c)
            else:
                continue

        if issubclass(c, EventBase) and c not in ret:
            ret.extend(get_event_cls_parent_type_list(c))
    return ret


def get_event_obj_parent_type_list(event: EventBase) -> list[type[EventBase]]:
    """获取 event 的继承树"""
    ret: list[type[EventBase]] = []
    cls = type(event)
    ret.extend(get_event_cls_parent_type_list(cls))
    return ret
