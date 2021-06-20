from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://dbuser:dbpassword@localhost:5432/sqlalchemy-orm-tutorial')

_MakeSession = sessionmaker(bind=engine)

Base = declarative_base()


def make_sessions():
    Base.metadata.create_all(engine)
    return _MakeSession()
