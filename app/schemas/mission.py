from pydantic import BaseModel


class MissionCreate(BaseModel):
    name: str
    object_name: str
    status: str
    planned_date: str
    notes: str | None = None


class MissionStatusUpdate(BaseModel):
    status: str