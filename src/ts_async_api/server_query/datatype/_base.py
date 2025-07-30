"""base type"""

from pydantic import BaseModel

from ..msg import ResBase


class InvokerInfo(BaseModel, extra="forbid"):
    """invoker info"""

    id: int
    name: str
    uid: str


class Version(ResBase):
    """版本信息"""

    version: str
    build: int
    platform: str
