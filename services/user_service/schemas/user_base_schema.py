from pydantic import BaseModel

class UserBase(BaseModel):  
    id: int
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    email: str

    model_config = {
        "from_attributes": True  # enables loading from ORM objects
    }
