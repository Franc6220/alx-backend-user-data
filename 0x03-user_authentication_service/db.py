#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from user import User
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from user import Base

class DB:
    """DB class to manage user records
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database"""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            session = self._session
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        except SQLAlchemyError:
            session.rollback()
            raise
