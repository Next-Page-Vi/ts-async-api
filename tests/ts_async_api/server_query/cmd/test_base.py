from ts_async_api.server_query.cmd import CmdRes


def test_cmd_res() -> None:
    assert CmdRes.from_payload(b"id=0 msg=ok\\sok") == CmdRes(id=0, msg="ok ok")
    assert CmdRes.from_payload(b"id=524 msg=client\\sis\\sflooding extra_msg=please\\swait\\s1\\sseconds") == CmdRes(
        id=524, msg="client is flooding", extra_msg="please wait 1 seconds"
    )
