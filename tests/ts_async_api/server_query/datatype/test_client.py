from ts_async_api.server_query.datatype import ClientBaseInfo, ClientFullInfo


def test_base_info() -> None:
    assert ClientBaseInfo.from_payload(
        b"clid=736 cid=1 client_database_id=3 client_nickname=plusls11 client_type=1"
    ) == ClientBaseInfo(clid=736, cid=1, client_database_id=3, client_nickname="plusls11", client_type=1)


def test_full_info() -> None:
    assert ClientFullInfo.from_payload(
        b"clid=676 cid=68 client_idle_time=69379 client_unique_identifier=Ns35KOd6IRCcTL2b+hpetjLE9oM= "
        rb"client_nickname=plusls client_version=6.0.0-beta2\s[Build:\s1737468425] client_platform=Windows "
        b"client_input_muted=0 client_output_muted=0 client_outputonly_muted=0 client_input_hardware=0 "
        b"client_output_hardware=0 client_default_channel "
        b'client_meta_data={"myts_token":"aaa","tag":"plusls@myteamspeak.com","updated":1753857106806} '
        b"client_is_recording=0 client_version_sign=aaa client_security_hash client_login_name "
        b"client_database_id=3 client_channel_group_id=8 client_servergroups=6,7 client_created=1610883320 "
        b"client_lastconnected=1753857107 client_totalconnections=494 client_away=0 client_away_message "
        b"client_type=0 client_flag_avatar=6b6a40a7403e28a1853ac93124ab2c6e client_talk_power=75 "
        b"client_talk_request=0 client_talk_request_msg client_description client_is_talker=0 "
        b"client_month_bytes_uploaded=0 client_month_bytes_downloaded=13654 client_total_bytes_uploaded=210436 "
        b"client_total_bytes_downloaded=1709233 client_is_priority_speaker=0 client_nickname_phonetic "
        b"client_needed_serverquery_view_power=75 client_default_token client_icon_id=0 "
        b"client_is_channel_commander=0 client_country=CN client_channel_group_inherited_channel_id=68 "
        b"client_badges client_myteamspeak_id=aaa client_integrations "
        b"client_myteamspeak_avatar client_signed_badges client_base64HashClientUID=bbb "
        b"connection_filetransfer_bandwidth_sent=0 connection_filetransfer_bandwidth_received=0 "
        b"connection_packets_sent_total=125633 connection_bytes_sent_total=20228930 "
        b"connection_packets_received_total=39243 connection_bytes_received_total=1679387 "
        b"connection_bandwidth_sent_last_second_total=81 connection_bandwidth_sent_last_minute_total=67 "
        b"connection_bandwidth_received_last_second_total=83 connection_bandwidth_received_last_minute_total=60 "
        b"connection_connected_time=29254821 connection_client_ip=1.1.1.1"
    ) == ClientFullInfo(
        clid=676,
        cid=68,
        client_idle_time=69379,
        client_unique_identifier="Ns35KOd6IRCcTL2b+hpetjLE9oM=",
        client_nickname="plusls",
        client_version="6.0.0-beta2 [Build: 1737468425]",
        client_platform="Windows",
        client_input_muted=False,
        client_output_muted=False,
        client_outputonly_muted=False,
        client_input_hardware=0,
        client_output_hardware=0,
        client_default_channel=None,
        client_meta_data='{"myts_token":"aaa","tag":"plusls@myteamspeak.com","updated":1753857106806}',
        client_is_recording=False,
        client_version_sign="aaa",
        client_security_hash=None,
        client_login_name=None,
        client_database_id=3,
        client_channel_group_id=8,
        client_servergroups=[6, 7],
        client_created=1610883320,
        client_lastconnected=1753857107,
        client_totalconnections=494,
        client_away=False,
        client_away_message=None,
        client_type=0,
        client_flag_avatar="6b6a40a7403e28a1853ac93124ab2c6e",
        client_talk_power=75,
        client_talk_request=0,
        client_talk_request_msg=None,
        client_description=None,
        client_is_talker=False,
        client_month_bytes_uploaded=0,
        client_month_bytes_downloaded=13654,
        client_total_bytes_uploaded=210436,
        client_total_bytes_downloaded=1709233,
        client_is_priority_speaker=False,
        client_nickname_phonetic=None,
        client_needed_serverquery_view_power=75,
        client_default_token=None,
        client_icon_id=0,
        client_is_channel_commander=False,
        client_country="CN",
        client_channel_group_inherited_channel_id=68,
        client_badges=None,
        client_myteamspeak_id="aaa",
        client_integrations=None,
        client_myteamspeak_avatar=None,
        client_signed_badges=None,
        client_base64HashClientUID="bbb",
        connection_filetransfer_bandwidth_sent=0,
        connection_filetransfer_bandwidth_received=0,
        connection_packets_sent_total=125633,
        connection_bytes_sent_total=20228930,
        connection_packets_received_total=39243,
        connection_bytes_received_total=1679387,
        connection_bandwidth_sent_last_second_total=81,
        connection_bandwidth_sent_last_minute_total=67,
        connection_bandwidth_received_last_second_total=83,
        connection_bandwidth_received_last_minute_total=60,
        connection_connected_time=29254821,
        connection_client_ip="1.1.1.1",
    )

    assert ClientFullInfo.from_payload(
        b"clid=736 cid=1 client_idle_time=168135 client_unique_identifier=aaa client_nickname=plusls11 "
        b"client_version=ServerQuery client_platform=ServerQuery client_input_muted=0 client_output_muted=0 "
        b"client_outputonly_muted=0 client_input_hardware=0 client_output_hardware=0 client_default_channel "
        b"client_meta_data client_is_recording=0 client_version_sign client_security_hash client_login_name "
        b"client_database_id=3 client_channel_group_id=8 client_servergroups=6,7 client_created=1610883320 "
        b"client_lastconnected=1753885605 client_totalconnections=502 client_away=0 client_away_message client_type=1 "
        b"client_flag_avatar=6b6a40a7403e28a1853ac93124ab2c6e client_talk_power=75 client_talk_request=0 "
        b"client_talk_request_msg client_description client_is_talker=0 client_month_bytes_uploaded=0 "
        b"client_month_bytes_downloaded=13654 client_total_bytes_uploaded=210436 client_total_bytes_downloaded=1709233 "
        b"client_is_priority_speaker=0 client_unread_messages=0 client_nickname_phonetic "
        b"client_needed_serverquery_view_power=75 client_default_token client_icon_id=0 client_is_channel_commander=0 "
        b"client_country=CN client_channel_group_inherited_channel_id=1 client_badges client_myteamspeak_id "
        b"client_integrations client_myteamspeak_avatar client_signed_badges client_base64HashClientUID=bbb "
        b"connection_filetransfer_bandwidth_sent=0 connection_filetransfer_bandwidth_received=0 "
        b"connection_packets_sent_total=0 connection_bytes_sent_total=0 connection_packets_received_total=0 "
        b"connection_bytes_received_total=0 connection_bandwidth_sent_last_second_total=0 "
        b"connection_bandwidth_sent_last_minute_total=0 connection_bandwidth_received_last_second_total=0 "
        b"connection_bandwidth_received_last_minute_total=0 connection_connected_time=0 "
        b"connection_client_ip=1.1.1.1"
    ) == ClientFullInfo(
        clid=736,
        cid=1,
        client_database_id=3,
        client_nickname="plusls11",
        client_type=1,
        client_idle_time=168135,
        client_unique_identifier="aaa",
        client_version="ServerQuery",
        client_platform="ServerQuery",
        client_input_muted=False,
        client_output_muted=False,
        client_outputonly_muted=False,
        client_input_hardware=0,
        client_output_hardware=0,
        client_default_channel=None,
        client_meta_data=None,
        client_is_recording=False,
        client_version_sign=None,
        client_security_hash=None,
        client_login_name=None,
        client_channel_group_id=8,
        client_servergroups=[6, 7],
        client_created=1610883320,
        client_lastconnected=1753885605,
        client_totalconnections=502,
        client_away=False,
        client_away_message=None,
        client_flag_avatar="6b6a40a7403e28a1853ac93124ab2c6e",
        client_talk_power=75,
        client_talk_request=0,
        client_talk_request_msg=None,
        client_description=None,
        client_is_talker=False,
        client_month_bytes_uploaded=0,
        client_month_bytes_downloaded=13654,
        client_total_bytes_uploaded=210436,
        client_total_bytes_downloaded=1709233,
        client_is_priority_speaker=False,
        client_unread_messages=0,
        client_nickname_phonetic=None,
        client_needed_serverquery_view_power=75,
        client_default_token=None,
        client_icon_id=0,
        client_is_channel_commander=False,
        client_country="CN",
        client_channel_group_inherited_channel_id=1,
        client_badges=None,
        client_myteamspeak_id=None,
        client_integrations=None,
        client_myteamspeak_avatar=None,
        client_signed_badges=None,
        client_base64HashClientUID="bbb",
        connection_filetransfer_bandwidth_sent=0,
        connection_filetransfer_bandwidth_received=0,
        connection_packets_sent_total=0,
        connection_bytes_sent_total=0,
        connection_packets_received_total=0,
        connection_bytes_received_total=0,
        connection_bandwidth_sent_last_second_total=0,
        connection_bandwidth_sent_last_minute_total=0,
        connection_bandwidth_received_last_second_total=0,
        connection_bandwidth_received_last_minute_total=0,
        connection_connected_time=0,
        connection_client_ip="1.1.1.1",
    )
