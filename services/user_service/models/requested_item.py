from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models.id_and_timestamp_mixin import IdAndTimestampMixin
from models.base import Base
from models.enums import RequestedItemStatus

class RequestedItem(IdAndTimestampMixin, Base):
    __tablename__ = 'requested_items'

    title = Column(String(50), nullable=True, unique=False)
    description = Column(String(256), nullable=True, unique=False)
    desired_price = Column(Numeric(10, 2), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(RequestedItemStatus), nullable=False, default=RequestedItemStatus.NEW)

    owner = relationship("User", back_populates="requested_items")

    def __repr__(self):
        return f"<RequestedItem(id={self.id}, title={self.title}, description={self.description}, \
            price={self.price}, owner_id={self.owner_id})>"
    
    print("Item model loaded")