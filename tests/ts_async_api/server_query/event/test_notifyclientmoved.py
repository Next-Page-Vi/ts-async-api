from ts_async_api.server_query.event import (
    ClientMovedByKickEvent,
    ClientMovedByOtherEvent,
    ClientMovedBySelfEvent,
    EventManager,
    Invoker,
)


def test_move() -> None:
    assert EventManager.parse_event(b"notifyclientmoved ctid=114 reasonid=0 clid=514") == ClientMovedBySelfEvent(
        ctid=114, reasonid=0, clid=514
    )


def test_move_with_invoker() -> None:
    assert EventManager.parse_event(
        b"notifyclientmoved ctid=114 reasonid=1 invokerid=1919 invokername=aaa invokeruid=bbb clid=514"
    ) == ClientMovedByOtherEvent(ctid=114, reasonid=1, clid=514, invoker=Invoker(id=1919, name="aaa", uid="bbb"))


def test_kick() -> None:
    assert EventManager.parse_event(
        b"notifyclientmoved ctid=114 reasonid=4 invokerid=1919 invokername=aaa invokeruid=bbb reasonmsg=wtf clid=514"
    ) == ClientMovedByKickEvent(
        ctid=114, reasonid=4, clid=514, reasonmsg="wtf", invoker=Invoker(id=1919, name="aaa", uid="bbb")
    )


def test_kick_no_msg() -> None:
    assert EventManager.parse_event(
        b"notifyclientmoved ctid=114 reasonid=4 invokerid=1919 invokername=aaa invokeruid=bbb reasonmsg clid=514"
    ) == ClientMovedByKickEvent(
        ctid=114, reasonid=4, clid=514, reasonmsg=None, invoker=Invoker(id=1919, name="aaa", uid="bbb")
    )
