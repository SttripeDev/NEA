# imports all the classes from the other scripts into one controller file
from question_logic import question_generator as question_gen
from question_logic import input_handler as input_handler
from database_logic import database_handler as database_handler

import socket


class ServerClient:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 51000
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    def database_insertion(self,raw_data):

        self.s.connect((self.host, self.port))
        self.s.send(raw_data.encode())

    def database_retrieval(self):
        print("Need to code this fr")
class QuizManager:

    def __init__(self):
        # Initialises values for raw_data, user_inputs as well as defining user_input_handler , question_generation , database_manager
        self.user_input_handler = input_handler.UserInputHandler()
        self.question_generation = question_gen.QuestionGeneration()
        self.database_manager = database_handler.DatabaseManager()
        self.raw_data = None
        self.user_inputs = None

    def run(self):
        # Controls the movement of data from user input to generation to sending to database
        self.user_input_handler.take_user_input()

        self.user_inputs = self.user_input_handler.return_input()
        self.raw_data = self.question_generation.generator(self.user_inputs)
        print(self.raw_data)
        svr_manager = ServerClient()
        svr_manager.database_insertion(self.raw_data)


if __name__ == "__main__":
    quiz_manager = QuizManager()
    quiz_manager.run()
