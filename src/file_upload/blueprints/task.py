from flask import Blueprint, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from .auth import user_database
from ..Classes.TaskService import TaskService
from ..Classes.UserService import UserService


task_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/tasks"
)


# Temporary in-memory task storage
task_archive = {}


# Create service objects
task_service = TaskService(task_archive)
user_service = UserService(user_database)




@task_bp.get("/")
@jwt_required()
def handle_task():

    user_id = get_jwt_identity()

    # Verify user exists
    user = user_service.find_user_by_id(user_id)

    if not user:
        return {
            "message": "User not found"
        }, 404

    # Get tasks from TaskService
    tasks = task_service.get_user_tasks(user_id)

    # Convert Task objects to dictionaries
    task_list = []

    for task in tasks:
        task_list.append(task.get_dictionary())

    return task_list, 200



@task_bp.post("/")
@jwt_required()
def add_task():

    body_args = request.get_json(silent=True) or {}

    user_id = get_jwt_identity()

    title = body_args.get("title")
    description = body_args.get("description")


    # Validate title
    if not title:
        return {
            "message": "Task title is required"
        }, 400


    # Verify user exists
    user = user_service.find_user_by_id(user_id)

    if not user:
        return {
            "message": "User not found"
        }, 404


    # Create task using TaskService
    task = task_service.create_task(
        title=title,
        description=description,
        user_id=user_id
    )


    return {
        "message": "Task created successfully",
        "task": task.get_dictionary()
    }, 201




@task_bp.put("/<task_id>")
@jwt_required()
def handle_update_task(task_id):

    body_params = request.get_json(silent=True) or {}

    user_id = get_jwt_identity()

    title = body_params.get("title")
    description = body_params.get("description")


    # Update task using TaskService
    updated_task = task_service.update_task(
        user_id=user_id,
        task_id=task_id,
        title=title,
        description=description
    )


    if not updated_task:
        return {
            "message": "Task not found"
        }, 404


    return {
        "message": "Task updated successfully",
        "task": updated_task.get_dictionary()
    }, 200




@task_bp.delete("/<task_id>")
@jwt_required()
def handle_delete_task(task_id):

    user_id = get_jwt_identity()


    # Delete task using TaskService
    deleted = task_service.delete_task(
        user_id=user_id,
        task_id=task_id
    )


    if not deleted:
        return {
            "message": "Task not found"
        }, 404


    return {
        "message": "Task deleted successfully"
    }, 200