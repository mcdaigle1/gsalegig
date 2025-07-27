from sqlalchemy.orm import Session
from fastapi import HTTPException

from schemas.user_schema import UserCreate
from repositories.user_repository import UserRepository
from models.user import User

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def create_user(self, user: UserCreate):
        db_user = self.get_user_by_email(user.email)
        if db_user:
            raise HTTPException(status_code=400, detail=f"Email {user.email} already registered")

        # user.name = user.first_name + " " + user.last_name
        new_user = self.repo.create_user(user)
        return new_user

    def get_user(self, user_id: int) -> User | None:
        return self.repo.get_user(user_id)

    def get_all_users(self) -> list[User]:
        return self.repo.get_all_users()