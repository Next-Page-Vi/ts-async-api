"""version cmd"""

from ..msg import ResBase
from .base import CmdBase


class VersionRsp(ResBase):
    """版本信息"""

    version: str
    build: int
    platform: str


class VersionCmd(CmdBase[None, VersionRsp]):
    """version cmd"""

    name = "version"
