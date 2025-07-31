"""channelinfo cmd"""

from typing import override

from ..datatype import ChannelFullInfo
from .base import ArgsBase, CmdBase


class ChannelInfoArgs(ArgsBase):
    """channelinfo 参数"""

    cid: int


class ChannelInfoCmd(CmdBase[ChannelInfoArgs, ChannelFullInfo]):
    """channelinfo cmd"""

    name = "channelinfo"

    @override
    def parse_res(self, msg_data_list: list[bytes]) -> ChannelFullInfo:
        """解析命令结果"""
        # 返回的结果不包含 cid, 需要补上
        return ChannelFullInfo.from_payload(f"cid={self.args.cid} ".encode() + msg_data_list[0].strip())
