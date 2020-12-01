from typing import List

from .base import DB
from .DataModel import ParseData


class DataDAO:
    def __init__(self, db: DB):
        self.__db = db

    def save_data(self, data: ParseData):
        self.__db.get_session().add(data)

    def get_data_by_task_id(self, _id: int, limit: int) -> List[ParseData]:
        result = self.__db.get_session().query(ParseData)\
            .filter(ParseData.task_id == _id).limit(limit).all()
        return result

