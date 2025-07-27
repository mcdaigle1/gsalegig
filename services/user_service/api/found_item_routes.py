import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.base import SessionLocal
from services.found_item_service import FoundItemService
from schemas.found_item_schema import FoundItemRead, FoundItemCreate

router = APIRouter(prefix="/found_items")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FoundItemRead, status_code=201)
def create_found_item(found_item: FoundItemCreate, db: Session = Depends(get_db)):
    logger = logging.getLogger("found_item_routes")
    logger.debug("in create_found_item with title: %s for user: %s", found_item.title, found_item.owner_id)

    try:
        return FoundItemService(db).create_found_item(found_item)
    except Exception as e:
        error_str = "error creating found_item with title: %s for user: %s" % (found_item.title, found_item.owner_id)
        logger.exception(error_str)
        raise RuntimeError(error_str) from e

@router.get("/{found_item_id}", response_model=FoundItemRead)
def get_found_item(
    found_item_id: int, 
    db: Session = Depends(get_db),
):
    logger = logging.getLogger("found_item_routes")
    logger.debug("in get_found_item for found_item ID: %s", found_item_id)

    try:
        found_item = FoundItemService(db).get_found_item(found_item_id)
        return FoundItemRead.model_validate(found_item)
    except Exception as e:
        error_string = "error getting found_item with id: %d" % found_item_id
        logger.exception(error_string)
        raise RuntimeError(error_string) from e

@router.get("/", response_model=list[FoundItemRead])
def get_found_items(db: Session = Depends(get_db)):
    logger = logging.getLogger("found_item_routes") 
    logger.debug("in get_found_items")

    try:
        found_items = FoundItemService(db).get_all_found_items()  
        return [FoundItemRead.model_validate(found_item) for found_item in found_items]
    except Exception as e:
        error_str = "error getting all found_items"
        logger.exception(error_str)
        raise RuntimeError(error_str) from e   



