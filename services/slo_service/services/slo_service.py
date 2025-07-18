from sqlalchemy.orm import Session
from models.slo import Slo

def get_slo(db: Session, slo_id: int) -> Slo | None:
    return db.query(Slo).filter(Slo.id == slo_id).first()

def get_all_slos(db: Session) -> list[Slo]:
    return db.query(Slo).all()

def get_slo_by_name(db: Session, slo_name: str) -> Slo | None:
    return db.query(Slo).filter(Slo.name == slo_name).first() 

