"""exception"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cmd import CmdRes
else:
    from typing import Any

    CmdRes = Any


class TsException(Exception):
    """ts exception"""


class ParseException(TsException):
    """parse exception"""

    parse_msg: bytes

    def __init__(self, parse_msg: bytes) -> None:
        self.parse_msg = parse_msg
        super().__init__(f"Can not parse msg {parse_msg!r}")


class CmdException(TsException):
    """cmd exception"""

    cmd: str
    res: CmdRes

    def __init__(self, cmd: str, res: CmdRes) -> None:
        self.cmd = cmd
        self.res = res
        super().__init__(f"Execute cmd {cmd!r} failed, id: {res.id}, msg: {res.msg}")
