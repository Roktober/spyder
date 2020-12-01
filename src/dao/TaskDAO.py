from typing import List

from .base import DB
from .TaskModel import Task
from .DataModel import ParseData


class TaskDAO:
    def __init__(self, db: DB):
        self.__db = db

    def save_data(self, data: Task) -> int:
        """Return inserted key"""
        return self.__db.get_session().add_get_key(data)

    def get_by_url(self, url: str) -> List[Task]:
        return self.__db.get_session().query(Task).filter(Task.url == url).all()
