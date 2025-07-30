"""login cmd"""

from .base import ArgsBase, CmdBase


class LoginArgs(ArgsBase):
    """登录参数"""

    client_login_name: str
    client_login_password: str


class LoginCmd(CmdBase[LoginArgs, None]):
    """login cmd"""

    name = "login"
