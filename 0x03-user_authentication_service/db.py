#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User


# Define the Base for ORM models
Base = declarative_base()

class DB:
    """DB class to manage user records"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
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
            session.commit()               # Commit the new user to the database
            session.refresh(new_user)      # Refresh to load the new ID
            return new_user
        except SQLAlchemyError:
            session.rollback()             # Rollback in case of an error
            raise

    def find_user_by(self, **kwargs) -> User:
        """
        Find user by arbitrary keyword arguments
        and returns the first row found in the users table
        as filtered by the method’s input arguments.
        """
        if not kwargs:
            raise InvalidRequestError("No query parameters provided")

        # Check if all keys in kwargs are valid attributes of User
        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalid query parameter: {key}")

        try:
            user = session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user matching the provided criteria was found.")
            return user
        except InvalidRequestError:
            raise
