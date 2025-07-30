"""servernotifyregister cmd"""

from enum import Enum, unique
from typing import Optional

from .base import ArgsBase, CmdBase


@unique
class Event(Enum):
    """event enum"""

    SERVER = "server"
    CHANNEL = "channel"
    TEXT_SERVER = "textserver"
    TEXT_CHANNEL = "textchannel"
    TEXT_PRIVATE = "textprivate"


class ServerNotifyRegisterArgs(ArgsBase):
    """servernotifyregister args"""

    event: Event
    id: Optional[int] = None
    """channelID"""


class ServerNotifyRegisterCmd(CmdBase[ServerNotifyRegisterArgs, None]):
    """servernotifyregister cmd"""

    name = "servernotifyregister"
