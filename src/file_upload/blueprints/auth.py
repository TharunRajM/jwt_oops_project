from flask import Blueprint, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from ..Classes.AuthService import AuthService
from ..Classes.UserService import UserService


auth_blueprint = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# Temporary in-memory database
user_database = []


# Create service objects
auth_service = AuthService(user_database)
user_service = UserService(user_database)


# =========================================================
# REGISTER USER
# =========================================================

@auth_blueprint.post("/register")
def handle_register():

    user_data = request.get_json(silent=True) or {}

    username = user_data.get("username")
    email = user_data.get("email")
    password = user_data.get("password")
    role = user_data.get("role", "user")


    # Validate required fields
    if not username or not email or not password:

        return {
            "message": "Username, email and password are required"
        }, 400


    # Call AuthService
    new_user, error = auth_service.register_user(
        username,
        email,
        password,
        role
    )


    if error:

        return {
            "message": error
        }, 400


    return {

        "message": "User creation successful",

        "user": new_user.get_dictionary()

    }, 201


# =========================================================
# LOGIN USER
# =========================================================

@auth_blueprint.post("/login")
def handle_login():

    user_data = request.get_json(silent=True) or {}

    email = user_data.get("email")
    password = user_data.get("password")


    # Validate input
    if not email or not password:

        return {
            "message": "Email and password are required"
        }, 400


    # Call AuthService
    result, error = auth_service.login_user(
        email,
        password
    )


    if error:

        return {
            "message": error
        }, 401


    return {

        "message": "Login successful",

        "access_token": result["access_token"],

        "user": result["user"].get_dictionary()

    }, 200


# =========================================================
# GET CURRENT USER
# =========================================================

@auth_blueprint.get("/me")
@jwt_required()
def handle_me():

    user_id = get_jwt_identity()


    # Call UserService
    user = user_service.find_user_by_id(
        user_id
    )


    if not user:

        return {
            "message": "User not found"
        }, 404


    return user.get_dictionary(), 200