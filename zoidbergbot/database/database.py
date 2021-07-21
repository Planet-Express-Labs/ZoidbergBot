import sqlalchemy.orm

from sessions import make_sessions
from confess_server import ConfessServer
from server import Server


def close_session(session: sqlalchemy.orm.Session, data_object):
    session.add(data_object)
    session.commit()
    session.close()


def get_server():
    session = make_sessions()
    server = session.query(Server)
    session.close()
    return server.all()


def initialize_server(guild, enabled_modules, admin_role, mod_role, auto_delete, premium):
    session = make_sessions()
    server = Server(guild, enabled_modules, admin_role, mod_role, None, auto_delete, premium, False)
    close_session(session, server)


def get_confess_server():
    session = make_sessions()
    confess_server = session.query(ConfessServer)
    session.close()
    return confess_server.all()

def initialize_confess_server(guild, confess_channel, logging_channel):
