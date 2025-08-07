from ts_async_api.server_query.utils import unescape


def test_unescape() -> None:
    assert unescape(rb"\s\s") == b"  "
