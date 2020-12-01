from sqlalchemy import Column, TIMESTAMP, VARCHAR, TEXT, Integer, ForeignKey

from dao.BaseModel import BaseModel


class ParseData(BaseModel):
    __tablename__ = "parse_data"

    url = Column(VARCHAR, nullable=True)
    title = Column(VARCHAR, nullable=False)
    html = Column(TEXT, nullable=True)
    created = Column(TIMESTAMP, nullable=True)
    task_id = Column(Integer, ForeignKey("parse_task.id", ondelete="CASCADE"),
                     nullable=False, index=True)
