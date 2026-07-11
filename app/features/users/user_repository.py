# app/features/users/user_repository.py
from sqlalchemy.orm import Session
from app.features.users.users_models import UserDB
from app.features.users.user_schemas import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(UserDB).filter(UserDB.email == email).first()

    def get_by_id(self, user_id: int):
        return self.db.query(UserDB).filter(UserDB.id == user_id).first()

    def get_by_username(self, username: str):
        return self.db.query(UserDB).filter(UserDB.username == username).first()

    def create(self, user_data: UserCreate):
        user = UserDB(username=user_data.username, email=user_data.email, role=user_data.role, hashed_password=user_data.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        user.hashed_password = None  # Clear hashed password before returning
        return user