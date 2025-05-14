# imports all the classes from the other scripts into one controller file
from question_logic import question_generator as question_gen
from question_logic import input_handler as input_handler

import socket
import base64

class ServerClient:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 51000
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    def database_insertion(self,raw_data):

        self.s.connect((self.host, self.port))

        self.s.send(raw_data.encode())

    def database_retrieval(self,query):

        self.s.connect((self.host, self.port))

        encode_query = str(query).encode('utf-8')

        base64_dict = base64.b64encode(encode_query)

        self.s.send(base64_dict)
        formatted_data = self.s.recv(1024)
        formatted_data = formatted_data.decode('utf-8')
        print(formatted_data)




class QuizManager:

    def __init__(self):
        # Initialises values for raw_data, user_inputs as well as defining user_input_handler , question_generation , database_manager
        self.user_input_handler = input_handler.UserInputHandler()
        self.question_generation = question_gen.QuestionGeneration()

        self.raw_data = None
        self.user_inputs = None

    def question_controller(self):
        # Controls the movement of data from user input to generation to sending to database
        self.user_input_handler.take_user_input()

        self.user_inputs = self.user_input_handler.return_input()
        self.raw_data = self.question_generation.generator(self.user_inputs)
        print(self.raw_data)
        svr_manager = ServerClient()
        svr_manager.database_insertion(self.raw_data)

    def retrieval_controller(self):

        #Takes inputs

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