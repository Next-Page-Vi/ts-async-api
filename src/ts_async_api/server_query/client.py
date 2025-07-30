"""server query client"""

import asyncio
from asyncio import CancelledError, Event as AsyncioEvent, Lock, Queue, Semaphore, StreamReader, StreamWriter, Task
from logging import getLogger
from types import TracebackType
from typing import Optional, Self, cast

from pydantic import BaseModel

from .cmd.base import ArgsBase, CmdBase
from .cmd.login import LoginArgs, LoginCmd
from .cmd.servernotifyregister import Event, ServerNotifyRegisterArgs, ServerNotifyRegisterCmd
from .cmd.use import UseArgs, UseCmd
from .cmd.version import VersionCmd, VersionRsp
from .event import EventManager
from .msg import ResBase

LOGGER = getLogger(__name__)


class SshConfig(BaseModel, extra="forbid"):
    """ssh 设置"""

    # TODO(@plusls): 后面支持 ssh 通道


class Client:
    """ts client"""

    __CMD_COUNT: int = 10
    __CMD_COUNT_TIMEOUT: int = 3
    """每 3 s 可以执行 10 条指令"""

    host: str
    port: int
    ssh_config: Optional[SshConfig]
    keep_alive_interval: float
    event_manager: EventManager

    __execute_lock: Lock
    __execute_sem: Semaphore
    """执行限速器"""

    __task_queue_handler_task: Task[None]
    __task_queue: Queue[Task[None]]
    """任务队列

    event task 和 execute sem 填充会放入其中
    """
    __task_queue_shutdown_event: AsyncioEvent

    # IO
    __reader: StreamReader
    __writer: StreamWriter
    __msg_queue: Queue[bytes]
    __msg_recv_task: Task[None]

    __keepalive_task: Task[None]

    @classmethod
    async def new(
        cls, host: str, port: int, keep_alive_interval: float = 10, ssh_config: Optional[SshConfig] = None
    ) -> Self:
        """创建 ts client"""
        ret = cls()
        ret.host = host
        ret.port = port
        ret.ssh_config = ssh_config
        ret.keep_alive_interval = keep_alive_interval
        ret.event_manager = EventManager()

        ret.__execute_lock = Lock()
        ret.__execute_sem = Semaphore(cls.__CMD_COUNT)

        ret.__task_queue_handler_task = asyncio.create_task(ret.__event_task_loop())
        ret.__task_queue = Queue()
        ret.__task_queue_shutdown_event = AsyncioEvent()

        (ret.__reader, ret.__writer) = await cls.__connect(host, port, ssh_config=ssh_config)
        await ret.__reader.readuntil(b"specific command.\n\r")
        LOGGER.debug("Connect to ts server %s:%d success.", host, port)
        ret.__msg_queue = Queue()
        ret.__msg_recv_task = asyncio.create_task(ret.__msg_recv_loop())

        ret.__keepalive_task = asyncio.create_task(ret.__keepalive_loop())

        return ret

    async def listen_all_event(self) -> None:
        """监听所有事件"""
        for event in Event:
            if event not in (Event.CHANNEL,):
                await self.execute_cmd(ServerNotifyRegisterCmd(args=ServerNotifyRegisterArgs(event=event)))
        # 监听 0 可以收到所有频道的消息
        await self.execute_cmd(ServerNotifyRegisterCmd(args=ServerNotifyRegisterArgs(event=Event.CHANNEL, id=0)))

    # async def __update_execute_sem_loop(self) -> None:
    #     """定时补充 sem"""
    #     while True:
    #         try:
    #             await asyncio.sleep(self.__CMD_COUNT_TIMEOUT)
    #             if __execute_finish_sem.
    #             self.__execute_sem._value
    #         except CancelledError:
    #             break

    async def __event_task_loop(self) -> None:
        """Event task loop

        为了避免 event handler 卡住 __msg_recv_loop, 需要 create 新的 task 来处理
        """
        task_queue_shutdown_event_handler = asyncio.create_task(self.__task_queue_shutdown_event.wait())
        while True:
            done, _ = await asyncio.wait(
                (asyncio.create_task(self.__task_queue.get()), task_queue_shutdown_event_handler),
                return_when=asyncio.FIRST_COMPLETED,
            )
            if task_queue_shutdown_event_handler in done:
                break
            task = cast("Task[None]", next(iter(done)))
            await task

    async def __msg_recv_loop(self) -> None:
        """从服务器接受消息"""
        while True:
            try:
                msg_payload = await self.__recv_line()
            except CancelledError:
                break
            LOGGER.debug("Recv msg: %s", msg_payload)
            # 如果是事件消息, 则分发事件
            event = self.event_manager.parse_event(msg_payload)
            if event is not None:
                LOGGER.debug("Recv event: %s", event)
                self.__task_queue.put_nowait(asyncio.create_task(self.event_manager.dispatch(event)))
                continue
            # 否则加入 __msg_queue
            self.__msg_queue.put_nowait(msg_payload)

    async def __keepalive_loop(self) -> None:
        """防止超时"""
        while True:
            try:
                await asyncio.sleep(self.keep_alive_interval)
                await self.server_version()
            except CancelledError:
                break

    async def __recv_line(self) -> bytes:
        return (await self.__reader.readuntil(b"\n\r"))[:-2]

    @staticmethod
    async def __connect(host: str, port: int, ssh_config: Optional[SshConfig]) -> tuple[StreamReader, StreamWriter]:  # noqa: ARG004
        return await asyncio.open_connection(host, port)

    async def __aenter__(self) -> Self:
        """__aenter__"""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        """__aexit__"""
        self.__task_queue_shutdown_event.set()
        await self.__task_queue_handler_task

        self.__keepalive_task.cancel()
        await self.__keepalive_task

        self.__msg_recv_task.cancel()
        await self.__msg_recv_task

        self.__writer.close()
        await self.__writer.wait_closed()

    async def __fill_execute_sem(self) -> None:
        await asyncio.sleep(self.__CMD_COUNT_TIMEOUT)
        self.__execute_sem.release()

    async def execute_cmd[
        ArgsType: Optional[ArgsBase],
        ResType: Optional[ResBase],
    ](self, cmd: CmdBase[ArgsType, ResType]) -> ResType:
        """执行命令"""
        payload = cmd.generate_payload()
        async with self.__execute_lock:
            await self.__execute_sem.acquire()
            LOGGER.debug("Write cmd payload %s", payload)
            self.__writer.write(payload)
            await self.__writer.drain()
            self.__task_queue.put_nowait(asyncio.create_task(self.__fill_execute_sem()))
            return await cmd.parse(self.__msg_queue)

    async def server_version(self) -> VersionRsp:
        """获取 ts server 的版本"""
        return await self.execute_cmd(VersionCmd(args=None))

    async def login(self, username: str, password: str) -> None:
        """登录 ts server"""
        return await self.execute_cmd(
            LoginCmd(args=LoginArgs(client_login_name=username, client_login_password=password))
        )

    async def use(
        self,
        server_id: int,
        *,
        virtual: bool = False,
        client_nickname: Optional[str] = None,
        port: Optional[int] = None,
    ) -> None:
        """切换当前操作的 virtual server"""
        return await self.execute_cmd(
            UseCmd(args=UseArgs(sid=server_id, virtual=virtual, client_nickname=client_nickname, port=port))
        )

    async def wait(self) -> None:
        """等待接收事件"""
        await asyncio.gather(self.__keepalive_task, self.__msg_recv_task)
