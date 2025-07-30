from ts_async_api.server_query.event import (
    ClientEnterEvent,
    EventManager,
)


def test_enter() -> None:
    assert EventManager.parse_event(
        b"notifycliententerview cfid=0 ctid=1 reasonid=0 clid=729 client_unique_identifier=aaa client_nickname=plusls1 "
        b"client_input_muted=0 client_output_muted=0 client_outputonly_muted=0 client_input_hardware=1 "
        b"client_output_hardware=1 client_meta_data client_is_recording=0 client_database_id=3 "
        b"client_channel_group_id=8 client_servergroups=6 client_away=0 client_away_message client_type=0 "
        b"client_flag_avatar=aa client_talk_power=75 client_talk_request=0 client_talk_request_msg client_description "
        b"client_is_talker=0 client_is_priority_speaker=0 client_unread_messages=0 client_nickname_phonetic "
        b"client_needed_serverquery_view_power=75 client_icon_id=0 client_is_channel_commander=0 client_country=US "
        b"client_channel_group_inherited_channel_id=1 client_badges client_myteamspeak_id=aaa "
        b"client_integrations client_myteamspeak_avatar client_signed_badges"
    ) == ClientEnterEvent(cfid=0, ctid=1, reasonid=0, clid=729)
