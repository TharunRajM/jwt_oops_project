from uuid import uuid4
from datetime import datetime

from .Task import Task


class TaskService:

    def __init__(self, task_archive):
        self.task_archive = task_archive


    def get_user_tasks(self, user_id):

        return self.task_archive.get(user_id, [])


    def create_task(self, title, description, user_id):

        new_task = Task(
            id=f"TASK_ID_{str(uuid4())}",
            title=title,
            description=description,
            user_id=user_id,
            created_at=datetime.now().isoformat()
        )

        if user_id not in self.task_archive:
            self.task_archive[user_id] = []

        self.task_archive[user_id].append(new_task)

        return new_task


    def find_task_by_id(self, user_id, task_id):

        task_list = self.task_archive.get(user_id, [])

        for task in task_list:

            if task.id == task_id:
                return task

        return None


    def update_task(
        self,
        user_id,
        task_id,
        title=None,
        description=None
    ):

        task = self.find_task_by_id(
            user_id,
            task_id
        )

        if not task:
            return None

        if title:
            task.title = title

        if description:
            task.description = description

        return task


    def delete_task(self, user_id, task_id):

        task = self.find_task_by_id(
            user_id,
            task_id
        )

        if not task:
            return False

        self.task_archive[user_id].remove(task)

        return True