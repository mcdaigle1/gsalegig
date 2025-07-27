from pydantic import BaseModel
from typing import Optional
from schemas.user_base_schema import UserBase

from schemas.timestamp_schema import TimestampSchema

class RequestedItemCreate(BaseModel): 
    title: str
    description: str | None = None
    desired_price: str | None = None
    owner_id: int

class RequestedItemRead(BaseModel):  
    title: str
    description: str | None = None
    desired_price: int | None = None
    owner: UserBase

    model_config = {
        "from_attributes": True  # enables loading from ORM objects
    }

class RequestedItemUpdate(BaseModel):  
    title: str | Optional[str] = None
    description: str | Optional[str] = None
    desired_price: int | Optional[int] = None
    
class RequestedItemDB(TimestampSchema):
    id: int
    title: str | None = None
    description: str | None = None
    desired_price: int | None = None

    model_config = {
        "from_attributes": True  # enables loading from ORM objects
    }