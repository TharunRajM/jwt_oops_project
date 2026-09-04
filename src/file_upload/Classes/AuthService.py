from uuid import uuid4
from flask_jwt_extended import create_access_token, jwt_required
from .User import User
from .UserService import UserService

class AuthService:
    def __init__(self, user_database):
        self.user_service = UserService(user_database)

    def register_user(self, username, email, password, role="user"):
        existing_user = self.user_service.find_user_by_email(email)
        if existing_user:
            return {
                "message": "Email already exists"
            }, 400

        new_user = User(
            id=str(uuid4()),
            username = username,
            email = email,
            password = password,
            role = role
        )
        self.user_service.add_user(new_user)
        return new_user, None
    def login_user(self,email,password):
        user = self.user_service.find_user_by_email(email)
        if not user:
            return {
                "message": "User not found"
            }, 404

        if not user.check_password(password):
            return {
                "message": "Invalid password"
            }, 401

        access_token = create_access_token(identity=user.id)
        return {
            "access_token": access_token,
            "user":user
        }, None
