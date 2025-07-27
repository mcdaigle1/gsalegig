from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from models.id_and_timestamp_mixin import IdAndTimestampMixin
from models.base import Base
from models.enums import UserStatus

class User(IdAndTimestampMixin, Base):
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=True, unique=False)
    last_name = Column(String(50), nullable=True, unique=False)
    name = Column(String(50), nullable=False, unique=False)
    email = Column(String(254), nullable=False, unique=True)
    phone_number = Column(String(20))
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.NEW)

    requested_items = relationship("RequestedItem", back_populates="owner", cascade="all, delete-orphan")
    found_items = relationship("FoundItem", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, phone_number={self.phone_number}, \
            email={self.email}, created_at={self.created_at}, updated_at={self.updated_at})>"