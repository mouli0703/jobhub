from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class JobUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    status: Literal["queued", "running", "done", "failed"] | None = None


class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    owner_id: int
    created_at: datetime