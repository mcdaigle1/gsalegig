from sqlalchemy.orm import Session

from schemas.found_item_schema import FoundItemCreate
from repositories.found_item_repository import FoundItemRepository
from models.found_item import FoundItem

class FoundItemService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = FoundItemRepository(db)

    def create_found_item(self, found_item: FoundItemCreate):
        new_found_item = self.repo.create_found_item(found_item)
        return new_found_item

    def get_found_item(self, found_item_id: int) -> FoundItem | None:
        return self.repo.get_found_item(found_item_id)

    def get_all_found_items(self) -> list[FoundItem]:
        return self.repo.get_all_found_items()

    def get_found_item_by_owner(self, owner_id: int) -> list[FoundItem]:
        return self.repo.get_found_item_by_owner_id(owner_id)