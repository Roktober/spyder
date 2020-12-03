from typing import List

from .Base import DB
from spyder.dao.model.TaskModel import Task


class TaskDAO:
    def __init__(self, db: DB):
        self._db = db

    def save_data(self, data: Task) -> int:
        """Return inserted key"""
        return self._db.get_session().add_get_key(data)

    def get_by_url(self, url: str) -> List[Task]:
        return self._db.get_session().query(Task)\
            .filter(Task.url == url).all()
