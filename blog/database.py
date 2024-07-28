from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread":False})

'''create_engine creates a new SQLAlchemy engine instance.'''

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()


'''sessionmaker is a factory for creating new SQLAlchemy Session objects.'''

'''Base: This base class keeps track of classes and tables that inherit from it. It serves as a registry.
All your database models (tables) will extend this Base class.'''
