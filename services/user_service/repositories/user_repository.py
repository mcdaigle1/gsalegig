from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        user_data_dict = user_data.model_dump()

        # this is a temporary fix until the name field is removed from the user table
        user_data_dict["name"] = f"{user_data.first_name} {user_data.last_name}"
        user = User(**user_data_dict)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user 

    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()
    
    def search_users(db: Session, status: str = None, age: int = None):
        filters = []

        if status:
            filters.append(User.status == status)
        if age:
            filters.append(User.age == age)

        return db.query(User).filter(*filters).all()

