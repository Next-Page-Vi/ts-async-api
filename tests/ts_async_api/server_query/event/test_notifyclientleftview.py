from ts_async_api.server_query.datatype import InvokerInfo
from ts_async_api.server_query.event import (
    ClientLeftBanEvent,
    ClientLeftConnectLostEvent,
    ClientLeftKickEvent,
    ClientLeftQuitEmptyEvent,
    ClientLeftQuitEvent,
    EventManager,
)


def test_quit_empty() -> None:
    assert EventManager.parse_event(b"notifyclientleftview cfid=114 ctid=0 clid=514") == ClientLeftQuitEmptyEvent(
        cfid=114, ctid=0, clid=514
    )


def test_quit() -> None:
    assert EventManager.parse_event(
        b"notifyclientleftview cfid=114 ctid=0 reasonid=8 reasonmsg=leaving123 clid=514"
    ) == ClientLeftQuitEvent(cfid=114, ctid=0, clid=514, reasonid=8, reasonmsg="leaving123")


def test_connect_lost() -> None:
    assert EventManager.parse_event(
        b"notifyclientleftview cfid=114 ctid=0 reasonid=3 reasonmsg=connection\\slost clid=514"
    ) == ClientLeftConnectLostEvent(cfid=114, ctid=0, clid=514, reasonid=3, reasonmsg="connection lost")


def test_kick() -> None:
    assert EventManager.parse_event(
        b"notifyclientleftview cfid=114 ctid=0 reasonid=5 "
        b"invokerid=1919 invokername=aaa invokeruid=bbb reasonmsg=wtf clid=514"
    ) == ClientLeftKickEvent(
        cfid=114, ctid=0, clid=514, reasonid=5, invoker=InvokerInfo(id=1919, name="aaa", uid="bbb"), reasonmsg="wtf"
    )


def test_kick_empty_msg() -> None:
    assert EventManager.parse_event(
        b"notifyclientleftview cfid=114 ctid=0 reasonid=5 "
        b"invokerid=1919 invokername=aaa invokeruid=bbb reasonmsg clid=514"
    ) == ClientLeftKickEvent(
        cfid=114, ctid=0, clid=514, reasonid=5, invoker=InvokerInfo(id=1919, name="aaa", uid="bbb"), reasonmsg=None
    )


def test_ban() -> None:
    assert EventManager.parse_event(
        b"notifyclientleftview cfid=114 ctid=0 reasonid=6 "
        b"invokerid=1919 invokername=aaa invokeruid=bbb reasonmsg=wtf bantime=60 clid=514"
    ) == ClientLeftBanEvent(
        cfid=114,
        ctid=0,
        clid=514,
        reasonid=6,
        invoker=InvokerInfo(id=1919, name="aaa", uid="bbb"),
        reasonmsg="wtf",
        bantime=60,
    )
