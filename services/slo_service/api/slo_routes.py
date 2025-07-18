from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.base import SessionLocal
from typing import Annotated
from services.slo_service import get_all_slos, get_slo as get_one_slo
from schemas.slo import SloRead

router = APIRouter(prefix="/slos")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{slo_id}")
def get_slo(slo_id: int, db: Annotated[Session, Depends(get_db)]):
    slo = get_one_slo(db, slo_id)
    return SloRead.model_validate(slo)

@router.get("/")
def get_slos(db: Annotated[Session, Depends(get_db)]):
    slos = get_all_slos(db)  
    return [SloRead.model_validate(slo) for slo in slos]  