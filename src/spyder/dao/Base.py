import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from spyder.dao.model.BaseModel import Base
from spyder.dao.model.TaskModel import Task
from spyder.dao.model.DataModel import ParseData


class DBSession:
    """Helper class for work with session"""
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *entities, **kwargs):
        """Get query builder"""
        return self._session.query(*entities, **kwargs)

    def add(self, data):
        """Insert object"""
        self._session.add(data)
        self.__commit_session()

    def add_get_key(self, data):
        """Insert and return key"""
        self._session.add(data)
        self._session.flush()
        self.__commit_session()
        return data.id

    def __commit_session(self):
        self._session.commit()

    def __close_session(self):
        self._session.close()

    def __accept_session(self):
        self.__commit_session()
        self.__close_session()


class DB:
    """
    Helper class
    Create engine and session factory
    """
    HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
    PORT = os.getenv("POSTGRES_PORT", 5432)
    DB = os.getenv("POSTGRES_DB")
    USER = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")

    def __init__(self):
        self.engine = create_engine(f"postgresql+psycopg2://{DB.USER}:"
                                    f"{DB.PASSWORD}"
                                    f"@{DB.HOST}:"
                                    f"{DB.PORT}/{DB.DB}")

        Base.metadata.create_all(self.engine)
        Task.metadata.create_all(self.engine)
        ParseData.metadata.create_all(self.engine)

        self.session_factory = sessionmaker(bind=self.engine)

    def get_session(self) -> DBSession:
        return DBSession(self.session_factory())
