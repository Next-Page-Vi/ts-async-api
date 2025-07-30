"""base type"""

from pydantic import BaseModel


class InvokerInfo(BaseModel, extra="forbid"):
    """invoker info"""

    id: int
    name: str
    uid: str
