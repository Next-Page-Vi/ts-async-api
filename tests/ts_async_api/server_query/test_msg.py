from ts_async_api.server_query.msg import parse_msg


def test_parse_msg() -> None:
    assert parse_msg(b"version=3.13.7 build=1655727713 platform=Linux") == {
        "version": b"3.13.7",
        "build": b"1655727713",
        "platform": b"Linux",
    }
    assert parse_msg(b"id=0 msg=ok\\sok") == {"id": b"0", "msg": b"ok ok"}
    assert parse_msg(b"123") is None
    assert parse_msg(b"id=0 msg=ok\\sok ") is None
