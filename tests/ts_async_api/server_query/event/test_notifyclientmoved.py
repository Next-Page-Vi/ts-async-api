from ts_async_api.server_query.event import ClientMovedEvent, Invoker


def test_move() -> None:
    assert ClientMovedEvent.from_payload(b"ctid=114 reasonid=0 clid=514") == ClientMovedEvent(
        ctid=114, reasonid=0, clid=514
    )


def test_move_with_invoker() -> None:
    assert ClientMovedEvent.from_payload(
        b"ctid=114 reasonid=1 invokerid=1919 invokername=aaa invokeruid=bbb clid=514"
    ) == ClientMovedEvent(ctid=114, reasonid=1, clid=514, invoker=Invoker(id=1919, name="aaa", uid="bbb"))


def test_kick() -> None:
    assert ClientMovedEvent.from_payload(
        b"ctid=114 reasonid=4 invokerid=1919 invokername=aaa invokeruid=bbb reasonmsg=wtf clid=514"
    ) == ClientMovedEvent(
        ctid=114, reasonid=4, clid=514, reasonmsg="wtf", invoker=Invoker(id=1919, name="aaa", uid="bbb")
    )
