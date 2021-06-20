from sessions import make_sessions
from confess_server import ConfessServer
from server import Server


def get_server():
    session = make_sessions()
    server = session.query(Server)
    session.close()
    return server.all()


def get_confess_server():
    session = make_sessions()
    confess_server = session.query(ConfessServer)
    session.close()
    return confess_server.all()
