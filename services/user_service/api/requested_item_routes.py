import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.base import SessionLocal
from services.requested_item_service import RequestedItemService
from schemas.requested_item_schema import RequestedItemRead, RequestedItemCreate

router = APIRouter(prefix="/requested_items")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RequestedItemRead, status_code=201)
def create_requested_item(requested_item: RequestedItemCreate, db: Session = Depends(get_db)):
    logger = logging.getLogger("requested_item_routes")
    logger.debug("in create_requested_item with title: %s for user: %s", requested_item.title, requested_item.owner_id)

    try:
        return RequestedItemService(db).create_requested_item(requested_item)
    except Exception as e:
        error_str = "error creating requested_item with title: %s for user: %s" % (requested_item.title, requested_item.owner_id)
        logger.exception(error_str)
        raise RuntimeError(error_str) from e

@router.get("/{requested_item_id}", response_model=RequestedItemRead)
def get_requested_item(
    requested_item_id: int, 
    db: Session = Depends(get_db),
):
    logger = logging.getLogger("requested_item_routes")
    logger.debug("in get_requested_item for requested_item ID: %s", requested_item_id)

    try:
        requested_item = RequestedItemService(db).get_requested_item(requested_item_id)
        return RequestedItemRead.model_validate(requested_item)
    except Exception as e:
        error_string = "error getting requested_item with id: %d" % requested_item_id
        logger.exception(error_string)
        raise RuntimeError(error_string) from e

@router.get("/", response_model=list[RequestedItemRead])
def get_requested_items(db: Session = Depends(get_db)):
    logger = logging.getLogger("requested_item_routes") 
    logger.debug("in get_requested_items")

    try:
        requested_items = RequestedItemService(db).get_all_requested_items()  
        return [RequestedItemRead.model_validate(requested_item) for requested_item in requested_items]
    except Exception as e:
        error_str = "error getting all requested_items"
        logger.exception(error_str)
        raise RuntimeError(error_str) from e   



