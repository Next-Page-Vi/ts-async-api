"""ts3 msg"""

import re
from typing import Optional

__MSG_PATTERN: re.Pattern[bytes] = re.compile(
    rb"^([a-zA-Z_][a-zA-Z0-9_]+)(?:=(\S+))?( ([a-zA-Z_][a-zA-Z0-9_]+)(?:=(\S+))?)*$"
)
__MSG_KV_PATTERN: re.Pattern[bytes] = re.compile(rb"([a-zA-Z_][a-zA-Z0-9_]+)(?:=(\S+))?")


def parse_msg(msg_data: bytes) -> Optional[dict[str, Optional[bytes]]]:
    """解析消息"""
    matches = __MSG_PATTERN.fullmatch(msg_data)
    if not matches:
        return None
    ret: dict[str, Optional[bytes]] = {}
    for m in __MSG_KV_PATTERN.finditer(msg_data):
        k, v = m.groups()
        assert k not in ret
        if v is not None:
            ret[k.decode()] = v
        else:
            ret[k.decode()] = None
    return ret
