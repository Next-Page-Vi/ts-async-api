"""version cmd"""

from ..datatype import Version
from .base import CmdBase


class VersionCmd(CmdBase[None, Version]):
    """version cmd"""

    name = "version"
