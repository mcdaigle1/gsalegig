from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING

from schemas.timestamp_schema import TimestampSchema
from schemas.user_base_schema import UserBase

if TYPE_CHECKING:
    from schemas.requested_item_schema import RequestedItemRead

class UserCreate(BaseModel): 
    first_name: str
    last_name: str
    phone_number: str | None = None
    email: str

class UserRead(UserBase):  
    id: int

    requested_items: Optional[List["RequestedItemRead"]] = None

    model_config = {
        "from_attributes": True  # enables loading from ORM objects
    }

class UserSearchParams(BaseModel):
    email: Optional[str] = None
    status: Optional[str] = None

    def is_empty(self) -> bool:
        return self.email is None and self.status is None and self.age is None

class UserDependencyParams(BaseModel):
    get_requested_items: Optional[bool] = None
    get_found_items: Optional[bool] = None

    def is_empty(self) -> bool:
        return self.get_requested_items is None and self.get_requested_items is None

class UserUpdate(BaseModel):  
    phone_number: str | Optional[str] = None
    email: str | Optional[str] = None
    
class UserDB(TimestampSchema):
    id: int
    phone_number: str | None = None
    email: str

    model_config = {
        "from_attributes": True  # enables loading from ORM objects
    }

from schemas.requested_item_schema import RequestedItemRead
UserRead.model_rebuild()