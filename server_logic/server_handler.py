import sqlite3
import json
import socket

from database_handler import DatabaseManager
class ServerManager:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 51000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.dbm = DatabaseManager()


    def server_listen(self):
        print("Server is listening on port", self.port)
        self.s.listen(1)
        while True:
            connection, address = self.s.accept()
            print("New Connection from", address)
            data = connection.recv(1024)
            data = data.decode('utf-8')
            print("Data recieved from user")
            self.dbm.prepare_data_to_add(data)


if __name__ == "__main__":
    db = DatabaseManager()
    svr = ServerManager()
    if not db.check_exist():
        db.create_table()
    svr.server_listen()
