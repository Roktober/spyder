from sqlalchemy import Column, TIMESTAMP, VARCHAR

from spyder.dao.model.BaseModel import BaseModel


class Task(BaseModel):
    __tablename__ = "parse_task"

    url = Column(VARCHAR, nullable=False)
    created = Column(TIMESTAMP, nullable=False)
