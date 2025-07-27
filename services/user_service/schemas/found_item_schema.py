from pydantic import BaseModel
from typing import Optional
from schemas.user_schema import UserRead

from schemas.timestamp_schema import TimestampSchema

class FoundItemCreate(BaseModel): 
    title: str
    description: str | None = None
    desired_price: str | None = None
    owner_id: int

class FoundItemRead(BaseModel):  
    title: str
    description: str | None = None
    desired_price: int | None = None
    owner: UserRead

    model_config = {
        "from_attributes": True  # enables loading from ORM objects
    }

class FoundItemUpdate(BaseModel):  
    title: str | Optional[str] = None
    description: str | Optional[str] = None
    desired_price: int | Optional[int] = None
    
class FoundItemDB(TimestampSchema):
    id: int
    title: str | None = None
    description: str | None = None
    desired_price: int | None = None

    model_config = {
        "from_attributes": True  # enables loading from ORM objects
    }