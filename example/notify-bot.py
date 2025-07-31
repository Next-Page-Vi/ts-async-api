"""ts server query client logic"""

import logging
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, CliApp

from ts_async_api.server_query.client import Client
from ts_async_api.server_query.event import EventBase
from ts_async_api.server_query.event.notifycliententerview import ClientEnterEvent
from ts_async_api.server_query.event.notifyclientleftview import ClientLeftEventBase
from ts_async_api.server_query.event.notifyclientmoved import ClientMovedEventBase
from ts_async_api.server_query.utils import init_logger

LOGGER = logging.getLogger(__name__)


class AsyncSettings(BaseSettings, cli_enforce_required=True):
    """args"""

    username: str = Field(description="用户名")
    """用户名"""
    password: str = Field(description="密码")
    client_nickname: Optional[str] = Field(default=None, description="bot 在 ts 中显示的名称, 默认为用户名")
    server_id: int = Field(default=1, description="virtual server id")
    log_level: Literal["CRITICAL", "FATAL", "ERROR", "WARN", "INFO", "DEBUG"] = Field(
        default="INFO", description="日志等级"
    )

    async def cli_cmd(self) -> None:
        """Ts server query client main"""
        init_logger(log_level=self.log_level)

        # 会等所有 task 结束后再销毁 client
        async with await Client.new("ts.plusls.com", 10011) as client:
            version = await client.server_version()
            LOGGER.info(
                "Teamspeaker server version: %s.%d, platform: %s", version.version, version.build, version.platform
            )
            await client.login(self.username, self.password)
            await client.use(1, virtual=True, client_nickname=self.client_nickname)
            await client.listen_all_event()

            client.event_manager.register(ClientEnterEvent, client_enter_server_callback)
            client.event_manager.register(ClientLeftEventBase, client_left_server_callback)
            client.event_manager.register(ClientMovedEventBase, client_moved_callback)
            # 需要调用 wait, 不然里头的 task 出异常了不会向外抛出
            await client.wait()


async def client_enter_server_callback(client: Client, event: EventBase) -> bool:
    """Enter server callback"""
    assert isinstance(event, ClientEnterEvent)
    # 可以直接从 server_status 获取对应的信息, 只要执行过程中没有 await
    # await 后不保证还能获取到对应的信息 (因为可能客户端会退出)

    client_info = client.server_status.client_list[event.clid]
    LOGGER.info(
        "用户 %s 加入了服务器, ip: %s, 频道: %s, 客户端版本: %s",
        client_info.client_nickname,
        client_info.connection_client_ip,
        client.server_status.channel_list[client_info.cid].channel_name,
        client_info.client_version,
    )
    return False


async def client_left_server_callback(client: Client, event: EventBase) -> bool:
    """Left server callback"""
    assert isinstance(event, ClientLeftEventBase)
    client_info = client.server_status.client_list[event.clid]
    LOGGER.info(
        "用户 %s 离开了服务器",
        client_info.client_nickname,
    )
    return False


async def client_moved_callback(client: Client, event: EventBase) -> bool:
    """Move channel callback"""
    assert isinstance(event, ClientMovedEventBase)
    client_info = client.server_status.client_list[event.clid]
    LOGGER.info(
        "用户 %s 从频道 %s 切换到频道 %s",
        client_info.client_nickname,
        client.server_status.channel_list[event.cfid].channel_name,
        client.server_status.channel_list[event.ctid].channel_name,
    )
    return False


if __name__ == "__main__":
    CliApp.run(AsyncSettings)
