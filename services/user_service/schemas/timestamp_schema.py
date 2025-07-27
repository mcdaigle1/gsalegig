from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# Shared schema
class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # Enables ORM mode in Pydantic v2+