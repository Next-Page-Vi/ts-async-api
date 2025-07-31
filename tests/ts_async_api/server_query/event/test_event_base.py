from ts_async_api.server_query.event.base import EventBase, get_event_cls_parent_type_list
from ts_async_api.server_query.event.notifyclientleftview import ClientLeftEventBase, ClientLeftKickEvent


def test_get_event_cls_parent_type_list() -> None:
    assert get_event_cls_parent_type_list(ClientLeftEventBase) == [ClientLeftEventBase, EventBase]
    assert get_event_cls_parent_type_list(ClientLeftKickEvent) == [ClientLeftKickEvent, ClientLeftEventBase, EventBase]
