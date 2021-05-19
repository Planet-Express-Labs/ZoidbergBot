from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Server(Base):
    __tablename__ = 'server_data'
    guild = Column(Integer, primary_key=True)
    prefix = Column(String)
    enabled_modules = Column(String)


engine = create_engine('sqlite:///data/servers.db')

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
