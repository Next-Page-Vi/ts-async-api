"""login cmd"""

from typing import Optional

from .base import ArgsBase, CmdBase


class UseArgs(ArgsBase):
    """use args"""

    sid: int
    port: Optional[int] = None
    client_nickname: Optional[str] = None
    virtual: bool = False


class UseCmd(CmdBase[UseArgs, None]):
    """use cmd"""

    name = "use"
