import sqlite3
import os
from bot import bot


if not os.path.isfile('data/servers.db'):
    os.mknod("data/severs.db")
    connection = sqlite3.connect('data/servers.db')
    cursor = connection.cursor()
    # The way I'm storing the enabled modules isn't great, but it's not too bad to convert later. I hope.
    cursor.execute("CREATE TABLE server_data (server_ID INTEGER, prefix INTEGER, logging_channel INTEGER, admin_roles INTEGER, enabled_modules TEXT)")
else:
    connection = sqlite3.connect('data/servers.db')


class Server:
    def __init__(self):
        pass

    def setup(self):
        pass
