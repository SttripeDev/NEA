import sqlite3
import json
import socket

from database_handler import DatabaseManager
class ServerManager:
    """
    Name: ServerManager
    Purpose: Controls all server purposes, accepting connections , sending requests to the database and sending and recieving data from the client.
    """
    def __init__(self):
        """
        Name: __init__
        Parameters: None
        Returns: None
        Purpose: Constructor that sets the initial value of required variables
        """
        self.host = "127.0.0.1"
        self.port = 51000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.dbm = DatabaseManager()

    def database_insert(self,data):
        """
        Name: database_insert
        Parameters: data:array
        Returns: None
        Purpose: Send the data to the database for insertion
        """
        self.dbm.prepare_data_to_add(data)

    def database_retrieve(self,data):
        """
        Name: database_retrieve
        Parameters: data:array
        Returns: formatted_data
        Purpose: sends the data for a request of specific database entries
        """
        formatted_data = self.dbm.retrieve_data(data)
        return formatted_data

    def available_topics(self,data):
        None  #to be done once topic select is coded fully :)

    def server_listen(self):
        """
        Name: server_listen
        Parameters: None
        Returns: formatted_data
        Purpose: Waits for a user connection and based on the data provided determines if data needs to be sent for insertion or for retrieval
        """
        print("Server is listening on port", self.port)
        self.s.listen(1)
        while True:
            connection, address = self.s.accept()
            print("New Connection from", address)
            data = connection.recv(1024)
            data = data.decode('utf-8')
            print("Data received from user")
            if data.startswith("```json") == True:
                self.database_insert(data)
            else:
                result = self.database_retrieve(data)
                connection.send(result.encode())
            connection.close()



if __name__ == "__main__":
    db = DatabaseManager()
    svr = ServerManager()
    if not db.check_exist():
        db.create_table()
        db.add_prerequisites()
    svr.server_listen()
