from ts_async_api.server_query.datatype import ChannelBaseInfo


def test_base_info() -> None:
    assert ChannelBaseInfo.from_payload(
        "cid=42 pid=0 channel_order=0 channel_name=食べる total_clients=0 channel_needed_subscribe_power=0".encode(),
    ) == ChannelBaseInfo(
        cid=42, pid=0, channel_order=0, channel_name="食べる", total_clients=0, channel_needed_subscribe_power=0
    )


# def test_full_info() -> None:
#     assert (
#         ChannelFullInfo.from_payload(
#             b"pid=0 channel_name=AFK channel_topic=AFK channel_description=AFK channel_password channel_codec=4 "
#             b"channel_codec_quality=5 channel_maxclients=-1 channel_maxfamilyclients=-1 channel_order=42 "
#             b"channel_flag_permanent=1 channel_flag_semi_permanent=0 channel_flag_default=1 channel_flag_password=0 "
#             b"channel_codec_latency_factor=1 channel_codec_is_unencrypted=1 channel_security_salt "
#             b"channel_delete_delay=0 channel_unique_identifier=576f641a-e8a9-4b55-a583-514541c17a10 "
#             b"channel_flag_maxclients_unlimited=1 channel_flag_maxfamilyclients_unlimited=1 "
#             b"channel_flag_maxfamilyclients_inherited=0 channel_filepath=files\\/virtualserver_1\\/channel_1 "
#             b"channel_needed_talk_power=4 channel_forced_silence=0 channel_name_phonetic channel_icon_id=0 "
#             b"channel_banner_gfx_url channel_banner_mode=0 seconds_empty=-1"
#         )
#         == ChannelFullInfo()
#     )
