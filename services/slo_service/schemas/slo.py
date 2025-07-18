from pydantic import BaseModel
from typing import Literal

from schemas.id_and_timestamp_schema import IdAndTimestampSchema

class SloCreate(BaseModel):  # For requests
    name: str
    query: str
    type: Literal["promql"]

class SloRead(IdAndTimestampSchema):    # For responses
    id: int
    query: str

    model_config = {
        "from_attributes": True  # enables loading from ORM objects
    }