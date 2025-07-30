from typing import Optional

from ..datatype import ResBase
from ..datatype.pydantic import BytesIntList


class ClientBaseInfo(ResBase):
    """客户端的基本信息

    clientlist 中返回
    """

    clid: int
    cid: int
    """channel id"""
    client_database_id: int
    client_nickname: str
    client_type: int


class ClientFullInfo(ClientBaseInfo):
    """client 的完整信息"""

    client_idle_time: int
    client_unique_identifier: str
    client_version: str
    client_platform: str
    client_input_muted: bool
    client_output_muted: bool
    client_outputonly_muted: bool
    client_input_hardware: int
    client_output_hardware: int
    client_default_channel: Optional[int]
    client_meta_data: Optional[str]
    client_is_recording: bool
    client_version_sign: Optional[str]
    client_security_hash: Optional[str]
    client_login_name: Optional[str]
    client_channel_group_id: int
    client_servergroups: BytesIntList
    client_created: int
    client_lastconnected: int
    client_totalconnections: int
    client_away: bool
    client_away_message: Optional[str]
    client_flag_avatar: str
    client_talk_power: int
    client_talk_request: int
    client_talk_request_msg: Optional[str]
    client_description: Optional[str]
    client_is_talker: bool
    client_month_bytes_uploaded: int
    client_month_bytes_downloaded: int
    client_total_bytes_uploaded: int
    client_total_bytes_downloaded: int
    client_is_priority_speaker: bool
    client_unread_messages: Optional[int] = None
    client_nickname_phonetic: Optional[str]
    client_needed_serverquery_view_power: int
    client_default_token: Optional[str]
    client_icon_id: int
    client_is_channel_commander: bool
    client_country: str
    client_channel_group_inherited_channel_id: int
    client_badges: Optional[str]
    client_myteamspeak_id: Optional[str]
    client_integrations: Optional[str]
    client_myteamspeak_avatar: Optional[str]
    client_signed_badges: Optional[str]
    client_base64HashClientUID: str  # noqa: N815
    connection_filetransfer_bandwidth_sent: int
    connection_filetransfer_bandwidth_received: int
    connection_packets_sent_total: int
    connection_bytes_sent_total: int
    connection_packets_received_total: int
    connection_bytes_received_total: int
    connection_bandwidth_sent_last_second_total: int
    connection_bandwidth_sent_last_minute_total: int
    connection_bandwidth_received_last_second_total: int
    connection_bandwidth_received_last_minute_total: int
    connection_connected_time: int
    connection_client_ip: str
