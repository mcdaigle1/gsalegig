from sqlalchemy.orm import Session, joinedload
from models.requested_item import RequestedItem
from schemas.requested_item_schema import RequestedItemCreate

class RequestedItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_requested_item(self, requested_item_data: RequestedItemCreate) -> RequestedItem:
        requested_item = RequestedItem(**requested_item_data.model_dump())

        self.db.add(requested_item)
        self.db.commit()
        self.db.refresh(requested_item)
        return requested_item 

    def get_requested_item(self, requested_item_id: int) -> RequestedItem | None:
        return self.db.query(RequestedItem).options(joinedload(RequestedItem.owner)).get(requested_item_id)

    def get_all_requested_items(self) -> list[RequestedItem]:
        return self.db.query(RequestedItem).all()

    def get_requested_item_by_owner_id(self, owner_id: int) -> list[RequestedItem]:
        return self.db.query(RequestedItem).filter(RequestedItem.owner_id == owner_id) 

