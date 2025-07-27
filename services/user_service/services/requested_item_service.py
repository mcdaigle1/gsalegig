from sqlalchemy.orm import Session
from fastapi import HTTPException

from schemas.requested_item_schema import RequestedItemCreate
from repositories.requested_item_repository import RequestedItemRepository
from models.requested_item import RequestedItem

class RequestedItemService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = RequestedItemRepository(db)

    def create_requested_item(self, requested_item: RequestedItemCreate):
        new_requested_item = self.repo.create_requested_item(requested_item)
        return new_requested_item

    def get_requested_item(self, requested_item_id: int) -> RequestedItem | None:
        return self.repo.get_requested_item(requested_item_id)

    def get_all_requested_items(self) -> list[RequestedItem]:
        return self.repo.get_all_requested_items()

    def get_requested_item_by_owner(self, owner_id: int) -> list[RequestedItem]:
        return self.repo.get_requested_item_by_owner_id(owner_id)