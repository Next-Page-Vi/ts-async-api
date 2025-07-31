"""clientlist cmd"""


from ..datatype import ClientBaseInfo
from .base import ArgsBase, CmdBase


class ClientListArgs(ArgsBase):
    """clientlist 参数"""

    uid: bool = False
    """Reports the client unique identifier"""
    away: bool = False
    """Adds client away status and message"""
    voice: bool = False
    """Adds information on whether the user is talking, \
    their mute/hardware status and if they are recording/priority speaker"""
    times: bool = False
    """Add idle, created and last connected time."""
    groups: bool = False
    """Includes info on server and channel groups."""
    info: bool = False
    """Adds client version and platform"""
    country: bool = False
    """Reports the client country code"""
    ip: bool = False
    """Adds the client IP, depending on the callers **PERMISSION_b_client_remoteaddress_view** permission"""
    icon: bool = False
    """Adds the client icon id"""
    badges: bool = False
    """Reports on the clients badges"""


class ClientListCmd(CmdBase[ClientListArgs, list[ClientBaseInfo]]):
    """clientlist cmd"""

    name = "clientlist"
