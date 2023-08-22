# Path: src/backend/langflow/database/models/flow.py

from langflow.services.database.models.base import SQLModelSerializable
from sqlmodel import Field, JSON, Column
from uuid import UUID, uuid4
from typing import Dict, Optional
from pydantic import field_validator

# if TYPE_CHECKING:


class FlowBase(SQLModelSerializable):
    name: str = Field(index=True)
    description: Optional[str] = Field(index=True, default="")
    data: Optional[Dict] = Field(default=None)

    @field_validator("data")
    @classmethod
    def validate_json(cls, v):
        # dict_keys(['description', 'name', 'id', 'data'])
        if not v:
            return v
        if not isinstance(v, dict):
            raise ValueError("Flow must be a valid JSON")

        # data must contain nodes and edges
        if "nodes" not in v.keys():
            raise ValueError("Flow must have nodes")
        if "edges" not in v.keys():
            raise ValueError("Flow must have edges")

        return v


class Flow(FlowBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    data: Optional[Dict] = Field(default=None, sa_column=Column(JSON))


class FlowCreate(FlowBase):
    pass


class FlowRead(FlowBase):
    id: UUID


class FlowUpdate(SQLModelSerializable):
    name: Optional[str] = None
    description: Optional[str] = None
    data: Optional[Dict] = None