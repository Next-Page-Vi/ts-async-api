"""cmd base"""

from abc import ABC
from asyncio import Queue
from enum import Enum
from logging import getLogger
from types import NoneType, get_original_bases
from typing import ClassVar, Optional, cast, get_args, get_origin

from pydantic import BaseModel

from ..exception import CmdException
from ..msg import ResBase
from ..utils import escape

LOGGER = getLogger(__name__)


class CmdRes(ResBase):
    """命令的执行结果"""

    id: int
    msg: str

    def __bool__(self) -> bool:
        """获取命令是否执行成功"""
        return self.id == 0


class ArgsBase(BaseModel, ABC, extra="forbid"):
    """命令参数"""

    def generate_payload(self) -> bytes:
        """生成命令参数"""
        payload_list: list[bytes] = []
        self_dump = self.model_dump(exclude_unset=True, exclude_defaults=True)
        for k, v in self_dump.items():
            if isinstance(v, Enum):
                v = v.value  # noqa: PLW2901 预期行为, 故意覆盖的
            if isinstance(v, bytes):
                final_v = v
            elif isinstance(v, bool):
                payload_list.append(b"-" + k.encode())
                break
            elif isinstance(v, int):
                final_v = str(v).encode()
            elif isinstance(v, str):
                final_v = v.encode()
            else:
                msg = f"Unsupported value type: {type(v)}, value: {v}, key: {k}"
                raise TypeError(msg)

            payload_list.append(k.encode() + b"=" + escape(final_v))
        return b" ".join(payload_list)


class CmdBase[ArgsType: Optional[ArgsBase], ResType: Optional[ResBase]](ABC):
    """命令"""

    name: ClassVar[str]
    args: ArgsType

    def __init__(self, args: ArgsType) -> None:
        self.args = args

    def generate_payload(self) -> bytes:
        """生成 payload"""
        payload_list: list[bytes] = [self.name.encode()]
        if self.args is not None:
            payload_list.append(self.args.generate_payload())
        payload_list.append(b"\n")
        return b" ".join(payload_list)

    def parse_res(self, msg_data_list: list[bytes]) -> ResType:
        """解析命令结果"""
        orig_cls = get_original_bases(type(self))[0]
        assert get_origin(orig_cls) is CmdBase

        res_type: type[ResType] = get_args(orig_cls)[1]
        if res_type is NoneType:
            return cast("ResType", None)  # ResType 可以是 Optional
        # 不知道为什么没法识别, 强制转换
        return cast("ResType", cast("ResBase", res_type).from_payload(msg_data_list[0].strip()))

    async def parse(self, msg_queue: Queue[bytes]) -> ResType:
        """解析命令"""
        msg_data_list: list[bytes] = []
        cmd_res: Optional[CmdRes] = None
        assert msg_queue.empty()
        while True:
            msg_payload = await msg_queue.get()
            if msg_payload.startswith(b"error id="):
                cmd_res = CmdRes.from_payload(msg_payload[len(b"error ") :].strip())
                LOGGER.debug("cmd %s execute cmd res: %s", self.name, cmd_res)
                if not cmd_res:
                    raise CmdException(self.name, cmd_res)
                break
            msg_data_list.append(msg_payload)
        assert msg_queue.empty()
        res = self.parse_res(msg_data_list)
        LOGGER.debug("cmd %s execute res: %s", self.name, res)
        return res
