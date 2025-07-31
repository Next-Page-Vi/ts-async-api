"""channellist cmd"""

from ..datatype import ChannelBaseInfo
from .base import ArgsBase, CmdBase


class ChannelListArgs(ArgsBase):
    """channellist 参数"""

    topic: bool = False
    """include `channel_topic`"""
    flags: bool = False
    """include `channel_flag_default`, `channel_flag_password`,
    `channel_flag_permanent` and `channel_flag_semi_permanent`"""
    voice: bool = False
    """include `channel_codec`, `channel_codec_quality` and `channel_needed_talk_power`"""
    limits: bool = False
    """include `total_clients_family`"""
    icon: bool = False
    """include `channel_icon_id`"""
    secondsempty: bool = False
    """include `seconds_empty`"""
    banners: bool = False
    """include `channel_banner_gfx_url` and `channel_banner_mode`"""


class ChannelListCmd(CmdBase[ChannelListArgs, list[ChannelBaseInfo]]):
    """channellist cmd"""

    name = "channellist"
