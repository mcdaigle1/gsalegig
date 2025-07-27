from sqlalchemy.orm import Session, joinedload
from models.found_item import FoundItem
from schemas.found_item_schema import FoundItemCreate

class FoundItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_found_item(self, found_item_data: FoundItemCreate) -> FoundItem:
        found_item = FoundItem(**found_item_data.model_dump())

        self.db.add(found_item)
        self.db.commit()
        self.db.refresh(found_item)
        return found_item 

    def get_found_item(self, found_item_id: int) -> FoundItem | None:
        return self.db.query(FoundItem).options(joinedload(FoundItem.owner)).get(found_item_id)

    def get_all_found_items(self) -> list[FoundItem]:
        return self.db.query(FoundItem).all()

    def get_found_item_by_owner_id(self, owner_id: int) -> list[FoundItem]:
        return self.db.query(FoundItem).filter(FoundItem.owner_id == owner_id) 

