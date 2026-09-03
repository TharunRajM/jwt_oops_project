from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth import user_database
from datetime import datetime
from ..Classes.Task import Task
from uuid import uuid4


task_bp = Blueprint("tasks",__name__, url_prefix="/tasks")

task_archive = {}

@task_bp.get("/")
@jwt_required()
def handle_task():
    email = get_jwt_identity()
    found_list = list(filter(lambda x: x.email == email, user_database))
    if not found_list:
        return "Resource not found", 404
    user = found_list[0]
    tasks = task_archive.get(user.id, [])
    list_task = list(map(lambda x:x.get_dictionary(), tasks))
    return list_task
    

@task_bp.post("/")
@jwt_required()
def add_task(): 
    body_args=  request.json
    email = get_jwt_identity()
    found_list = list(filter(lambda x: x.email == email, user_database))
    if not found_list:
        return "Resource not found", 404
    user = found_list[0]
    task = Task(
            id= f"TASK_ID_{str(uuid4())}",
            title= body_args.get("title"),
            description=body_args.get("description"),
            user_id=user.id,
            created_at=str(datetime.now())
        )
    
    if user.id in task_archive:
        task_archive[user.id].append(task)
    else:
        task_archive[user.id] = [task]


    return {"message":"Task created"}, 201


@task_bp.put("/<task_id>")
@jwt_required()
def handle_update_task(task_id):
    email = get_jwt_identity()
    found_list = list(filter(lambda x: x.email == email, user_database))
    if not found_list:
        return "Resource not found", 404
    user = found_list[0]

    body_params = request.json
    new_title = body_params.get("title")
    new_description = body_params.get("description")

    task_list = task_archive.get(user.id)

    for index, task in enumerate(task_list):
        if task.id == task_id:
            task_list[index]['title'] = new_title
            task_list[index]['description'] = new_description
            break