
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class GraphLink(BaseModel):
    host1: str
    host2: str
    label: Optional[str]
    color: Optional[str]
    link_type: Optional[int]
    draw_type: Optional[int]

