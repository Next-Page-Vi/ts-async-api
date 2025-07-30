"""clientinfo cmd"""

from typing import override

from ..datatype import ClientFullInfo
from .base import ArgsBase, CmdBase


class ClientInfoArgs(ArgsBase):
    """clientinfo 参数"""

    # clientinfo 本身支持一次查询多个 client
    # 这里并未封装成 list 是因为假设查询 clid=114|clid=1|clid=514
    # 尽管 clid=1 的数据没查出来, 但是命令既不会报错, 也返回了 2个结果
    # 难以得知查询结果是否一致
    clid: int


class ClientInfoCmd(CmdBase[ClientInfoArgs, ClientFullInfo]):
    """clientinfo cmd"""

    name = "clientinfo"

    @override
    def parse_res(self, msg_data_list: list[bytes]) -> ClientFullInfo:
        """解析命令结果"""
        # 返回的结果不包含 clid, 需要补上
        return ClientFullInfo.from_payload(f"clid={self.args.clid} ".encode() + msg_data_list[0].strip())
