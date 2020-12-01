from sqlalchemy import Column, TIMESTAMP, VARCHAR

from dao.BaseModel import BaseModel


class Task(BaseModel):
    __tablename__ = "parse_task"

    url = Column(VARCHAR, nullable=False)
    created = Column(TIMESTAMP, nullable=False)
