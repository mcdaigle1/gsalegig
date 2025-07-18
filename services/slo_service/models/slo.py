from sqlalchemy import Column, String
from models.id_and_timestamp_mixin import IdAndTimestampMixin
from models.base import Base

class Slo(IdAndTimestampMixin, Base):
    __tablename__ = 'slos'

    name = Column(String(50), unique=True, nullable=False)
    query = Column(String(1000), nullable=True)
    type = Column(String(10), nullable=False)

    def __repr__(self):
        return f"<Slo(id={self.id}, name={self.name}, promql={self.promql}, created_at={self.created_at}, updated_at={self.updated_at})>"