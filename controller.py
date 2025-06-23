
from question_logic import question_generator as question_gen
from question_logic import input_handler as input_handler

import socket
import json


class ServerClient:
    """
    Name: ServerClient
    Purpose: Connect to Database server and handle processes such as insertion and retrieval
    """

    def __init__(self):
        """
        Name: __init__
        Parameters: host: string, port:integer , s:socket
        Returns: None
        Purpose: Constructor to set the initial values of the connection details
        """

        self.host = '127.0.0.1'
        self.port = 51000
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    def database_insertion(self,raw_data):

        """
        Name: database_insertion
        Parameters: raw_data: array, s:socket
        Returns: None
        Purpose: sends raw_data to the database server
        """

        self.s.connect((self.host, self.port))

        self.s.send(raw_data.encode())

    def database_retrieval(self,query):
        """
        Name: database_retrieval
        Parameters: query: array, s:socket , encode_query:json array
        Returns: formatted_data:array
        Purpose: sends request data from server with query and returns that back to user as formatted_data
        """
        self.s.connect((self.host, self.port))

        encode_query = json.dumps(query)
        self.s.send(encode_query.encode())

        formatted_data = self.s.recv(1024)
        formatted_data = formatted_data.decode()
        formatted_data = json.loads(formatted_data)
        print(formatted_data)




class QuizManager:
    """
        Name: QuizManager
        Purpose: Manages user inputs and the movement of data
    """
    def __init__(self):
        """
            Name: __init__
            Parameters: user_input_handler:function, question_generation:function , raw_data:string , user_inputs:string
            Returns: None
            Purpose: Constructor that sets the initial value of required variables
        """
        self.user_input_handler = input_handler.UserInputHandler()
        self.question_generation = question_gen.QuestionGeneration()

        self.raw_data = None
        self.user_inputs = None

    def question_controller(self):
        """
            Name: question_controller
            Parameters: self.user_input_handler:function, self.user_inputs:array, self.raw_data: array , svr_manager: function
            Returns: self.raw_data
            Purpose: takes user input , sends to have questions created , sends that to database server
        """
        self.user_input_handler.take_user_input()

        self.user_inputs = self.user_input_handler.return_input()
        self.raw_data = self.question_generation.generator(self.user_inputs)
        print(self.raw_data)
        svr_manager = ServerClient()
        svr_manager.database_insertion(self.raw_data)

    def retrieval_controller(self):
        """
            Name: retrieval_controller
            Parameters:self.user_input_handler:function, self.user_inputs:array, svr_manager:function
            Returns: self.user_inputs
            Purpose: takes user input , sends the data to database to be processed to recieve specified data.
        """

        self.user_input_handler.take_user_input()
        self.user_inputs = self.user_input_handler.return_input()


        print(self.user_inputs)

        svr_manager = ServerClient()
        svr_manager.database_retrieval(self.user_inputs)
if __name__ == "__main__":
    def menu():
        print("[1] Question Generation")
        print("[2] Retrieval of Questions")
        print("  ")
        check = int(input("Enter: "))
        if check == 1:
            quiz_manager = QuizManager()
            quiz_manager.question_controller()
        elif check == 2:
            quiz_manager = QuizManager()
            quiz_manager.retrieval_controller()
        else:
            menu()

    menu()