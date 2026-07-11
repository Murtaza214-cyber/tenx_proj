# app/features/users/user_service.py
from .user_repository import UserRepository
from app.features.users.user_schemas import UserCreate

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, user_data: UserCreate):
        existing_user_email = self.repository.get_by_email(user_data.email)
        
        if existing_user_email:
           raise ValueError("Email already registered")
        
        if self.repository.get_by_username(user_data.username):
            raise ValueError("Username already registered")
        return self.repository.create(user_data)
    
    def get_user_by_email(self, email: str):
        return self.repository.get_by_email(email)
    
    def get_user_by_username(self, username: str):
        return self.repository.get_by_username(username)