from typing import Optional
from uuid import UUID

from ..datatype import ResBase


class ChannelBaseInfo(ResBase, extra="ignore"):
    """channel 的基本信息

    channellist 中返回
    """

    cid: int
    pid: int
    channel_order: int
    channel_name: str

    # 只有 channellist 中会返回, 不知道有没有别的获取方式
    # channel_needed_subscribe_power: int
    # total_clients: int


class ChannelFullInfo(ChannelBaseInfo, extra="forbid"):
    """channel 的完整信息"""

    channel_topic: Optional[str]
    channel_description: Optional[str]
    channel_password: Optional[str]
    channel_codec: int
    channel_codec_quality: int
    channel_maxclients: int
    channel_maxfamilyclients: int
    channel_order: int
    channel_flag_permanent: bool
    channel_flag_semi_permanent: bool
    channel_flag_default: bool
    channel_flag_password: bool
    channel_codec_latency_factor: int
    channel_codec_is_unencrypted: bool
    channel_security_salt: Optional[str]
    channel_delete_delay: int
    channel_unique_identifier: UUID
    channel_flag_maxclients_unlimited: bool
    channel_flag_maxfamilyclients_unlimited: bool
    channel_flag_maxfamilyclients_inherited: bool
    channel_filepath: str
    channel_needed_talk_power: int
    channel_forced_silence: bool
    channel_name_phonetic: Optional[str]
    channel_icon_id: int
    channel_banner_gfx_url: Optional[str]
    channel_banner_mode: int
    seconds_empty: int
