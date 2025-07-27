import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.base import SessionLocal
from services.user_service import UserService
from schemas.user_schema import UserRead, UserCreate, UserSearchParams, UserDependencyParams

router = APIRouter(prefix="/users")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger = logging.getLogger("user_routes")
    logger.debug("in create_user with name: %s %s and email: %s", user.first_name, user.last_name, user.email)

    try:
        return UserService(db).create_user(user)
    except Exception as e:
        error_str = "error creating user with name: %s and email: %s" % (user.first_name, user.last_name, user.email)
        logger.exception(error_str)
        raise RuntimeError(error_str) from e

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    search_params: UserSearchParams = Depends(),
    dependency_params: UserDependencyParams = Depends()
):
    logger = logging.getLogger("user_routes")
    logger.debug(
        "in get_user for user ID: %s with search_params: %s and dependency_params: %s", 
        user_id, 
        search_params.model_dump(exclude_none=True),
        dependency_params.model_dump(exclude_none=True))

    try:
        user = UserService(db).get_user(user_id, search_params, dependency_params)
        return UserRead.model_validate(user)
    except Exception as e:
        error_string = "error getting user with id: %d" % user_id
        logger.exception(error_string)
        raise RuntimeError(error_string) from e

@router.get("/", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    logger = logging.getLogger("user_routes") 
    logger.debug("in get_users")

    try:
        users = UserService(db).get_all_users()  
        return [UserRead.model_validate(user) for user in users]
    except Exception as e:
        error_str = "error getting all users"
        logger.exception(error_str)
        raise RuntimeError(error_str) from e   



