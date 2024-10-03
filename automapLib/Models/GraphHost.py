from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class GraphHost(BaseModel):
    name: str
    hostid: str
    label: Optional[str]
    iconid_off: Optional[str]
