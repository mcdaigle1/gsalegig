from sqlalchemy.orm import Session
from models.user import User
from models.base import SessionLocal

def seed():
    db: Session = SessionLocal()
    if not db.query(User).filter_by(email="admin@example.com").first():
        db.add(User(email="admin@example.com", phone_number="1234567890"))
        db.commit()
    db.close()

if __name__ == "__main__":
    seed()