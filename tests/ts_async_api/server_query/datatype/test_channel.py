from uuid import UUID

from ts_async_api.server_query.datatype import ChannelBaseInfo
from ts_async_api.server_query.datatype._channel import ChannelFullInfo


def test_base_info() -> None:
    assert ChannelBaseInfo.from_payload(
        "cid=42 pid=0 channel_order=0 channel_name=食べる total_clients=0 channel_needed_subscribe_power=0".encode(),
    ) == ChannelBaseInfo(
        cid=42,
        pid=0,
        channel_order=0,
        channel_name="食べる",
    )


def test_full_info() -> None:
    assert ChannelFullInfo.from_payload(
        b"cid=1 pid=0 channel_name=AFK channel_topic=AFK channel_description=AFK channel_password channel_codec=4 "
        b"channel_codec_quality=5 channel_maxclients=-1 channel_maxfamilyclients=-1 channel_order=42 "
        b"channel_flag_permanent=1 channel_flag_semi_permanent=0 channel_flag_default=1 channel_flag_password=0 "
        b"channel_codec_latency_factor=1 channel_codec_is_unencrypted=1 channel_security_salt "
        b"channel_delete_delay=0 channel_unique_identifier=576f641a-e8a9-4b55-a583-514541c17a10 "
        b"channel_flag_maxclients_unlimited=1 channel_flag_maxfamilyclients_unlimited=1 "
        b"channel_flag_maxfamilyclients_inherited=0 channel_filepath=files\\/virtualserver_1\\/channel_1 "
        b"channel_needed_talk_power=4 channel_forced_silence=0 channel_name_phonetic channel_icon_id=0 "
        b"channel_banner_gfx_url channel_banner_mode=0 seconds_empty=-1"
    ) == ChannelFullInfo(
        cid=1,
        pid=0,
        channel_name="AFK",
        channel_topic="AFK",
        channel_description="AFK",
        channel_password=None,
        channel_codec=4,
        channel_codec_quality=5,
        channel_maxclients=-1,
        channel_maxfamilyclients=-1,
        channel_order=42,
        channel_flag_permanent=True,
        channel_flag_semi_permanent=False,
        channel_flag_default=True,
        channel_flag_password=False,
        channel_codec_latency_factor=1,
        channel_codec_is_unencrypted=True,
        channel_security_salt=None,
        channel_delete_delay=0,
        channel_unique_identifier=UUID("576f641a-e8a9-4b55-a583-514541c17a10"),
        channel_flag_maxclients_unlimited=True,
        channel_flag_maxfamilyclients_unlimited=True,
        channel_flag_maxfamilyclients_inherited=False,
        channel_filepath="files/virtualserver_1/channel_1",
        channel_needed_talk_power=4,
        channel_forced_silence=False,
        channel_name_phonetic=None,
        channel_icon_id=0,
        channel_banner_gfx_url=None,
        channel_banner_mode=0,
        seconds_empty=-1,
    )

    assert ChannelFullInfo.from_payload(
        b"cid=1 pid=0 channel_name=AFK channel_topic channel_description channel_password channel_codec=4 "
        b"channel_codec_quality=5 channel_maxclients=-1 channel_maxfamilyclients=-1 channel_order=42 "
        b"channel_flag_permanent=1 channel_flag_semi_permanent=0 channel_flag_default=1 channel_flag_password=0 "
        b"channel_codec_latency_factor=1 channel_codec_is_unencrypted=1 channel_security_salt "
        b"channel_delete_delay=0 channel_unique_identifier=576f641a-e8a9-4b55-a583-514541c17a10 "
        b"channel_flag_maxclients_unlimited=1 channel_flag_maxfamilyclients_unlimited=1 "
        b"channel_flag_maxfamilyclients_inherited=0 channel_filepath=files\\/virtualserver_1\\/channel_1 "
        b"channel_needed_talk_power=4 channel_forced_silence=0 channel_name_phonetic channel_icon_id=0 "
        b"channel_banner_gfx_url channel_banner_mode=0 seconds_empty=-1"
    ) == ChannelFullInfo(
        cid=1,
        pid=0,
        channel_name="AFK",
        channel_topic=None,
        channel_description=None,
        channel_password=None,
        channel_codec=4,
        channel_codec_quality=5,
        channel_maxclients=-1,
        channel_maxfamilyclients=-1,
        channel_order=42,
        channel_flag_permanent=True,
        channel_flag_semi_permanent=False,
        channel_flag_default=True,
        channel_flag_password=False,
        channel_codec_latency_factor=1,
        channel_codec_is_unencrypted=True,
        channel_security_salt=None,
        channel_delete_delay=0,
        channel_unique_identifier=UUID("576f641a-e8a9-4b55-a583-514541c17a10"),
        channel_flag_maxclients_unlimited=True,
        channel_flag_maxfamilyclients_unlimited=True,
        channel_flag_maxfamilyclients_inherited=False,
        channel_filepath="files/virtualserver_1/channel_1",
        channel_needed_talk_power=4,
        channel_forced_silence=False,
        channel_name_phonetic=None,
        channel_icon_id=0,
        channel_banner_gfx_url=None,
        channel_banner_mode=0,
        seconds_empty=-1,
    )
