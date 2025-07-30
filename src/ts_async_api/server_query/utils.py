"""utils"""

import logging
import os
from typing import Literal

__ESCAPE_MAP: dict[int, bytes] = {
    b"\\"[0]: rb"\\",
    b"/"[0]: rb"\/",
    b" "[0]: rb"\s",
    b"|"[0]: rb"\p",
    b"\a"[0]: rb"\a",
    b"\b"[0]: rb"\b",
    b"\f"[0]: rb"\f",
    b"\n"[0]: rb"\n",
    b"\r"[0]: rb"\r",
    b"\t"[0]: rb"\t",
    b"\v"[0]: rb"\v",
}
__UNESCAPE_MAP: dict[bytes, int] = {v: k for k, v in __ESCAPE_MAP.items()}
__MAX_ESCAPE_LEN = max(len(k) for k in __UNESCAPE_MAP)


def escape(data: bytes) -> bytes:
    """Escapes characters that need escaping according to __ESCAPE_MAP"""
    return b"".join(__ESCAPE_MAP.get(b, bytes([b])) for b in data)


def unescape(data: bytes) -> bytes:
    """Undo escaping of characters according to __ESCAPE_MAP"""
    result = bytearray()
    i = 0
    while i < len(data):
        if data[i : i + 1] == b"\\":
            for match_len in range(2, __MAX_ESCAPE_LEN + 1):  # 尝试匹配 \x 这样的
                part = data[i : i + match_len]
                res = __UNESCAPE_MAP.get(part)
                if res is not None:
                    result.append(res)
                    i += match_len
                    continue
        result.append(data[i])
        i += 1
    return bytes(result)


def init_logger(
    log_level: Literal["CRITICAL", "FATAL", "ERROR", "WARN", "INFO", "DEBUG"] = "DEBUG",
) -> None:
    """初始化日志"""
    logging.root.setLevel(level=log_level)
    if "PYTEST_VERSION" not in os.environ:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        formatter = logging.Formatter(log_format)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logging.root.addHandler(stream_handler)
