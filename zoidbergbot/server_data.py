from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Server(Base):
    __tablename__ = 'server_data'
    guild = Column(Integer, primary_key=True)
    prefix = Column(String)
    enabled_modules = Column(String)  # Reserved for future use
    # I'll probably change this to something that will allow more then just two levels of permission, but that's later.
    # If admin_role == 0, then it's just going to go off of each role's permissions.
    admin_role = Column(bool)
    mod_role = Column(bool)
    cooldown = Column(Integer)  # Reserved for future use
    auto_delete = Column(Integer)  # Reserved for future use
    premium = Column(bool)  # Reserved for future use


engine = create_engine('sqlite:///data/servers.db')

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
