from typing import Optional
from uuid import UUID

from ..datatype import ResBase


class ChannelBaseInfo(ResBase):
    """channel 的基本信息

    channellist 中返回
    """

    cid: int
    pid: int
    channel_order: int
    channel_name: str
    total_clients: int
    channel_needed_subscribe_power: int


class ChannelFullInfo(ChannelBaseInfo):
    """channel 的完整信息"""

    channel_topic: str
    channel_description: str
    channel_password: Optional[str]
    channel_codec: int
    channel_codec_quality: int
    channel_maxclients: int
    channel_maxfamilyclients: int
    channel_order: int
    channel_flag_permanent: int
    channel_flag_semi_permanent: int
    channel_flag_default: int
    channel_flag_password: int
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
    channel_forced_silence: int
    channel_name_phonetic: Optional[str]
    channel_icon_id: int
    channel_banner_gfx_url: Optional[str]
    channel_banner_mode: int
    seconds_empty: int
