class UserInputHandler:  # Handles all user inputs
    def __init__(self):
        self.ai_input_format = {  # Set Default State for AiInputs
            "Qualification": "",
            "Subject": "",
            "ExamBoard": "",
            "Topic": "",
            "Amount": '10',
        }

    def take_user_input(self):
        # Appends them to user specification
        self.ai_input_format["Qualification"] = input("WHat is the Qualification? : ")
        self.ai_input_format["Subject"] = input("What is the subject? : ")
        self.ai_input_format["ExamBoard"] = input("What is the Exam Board? : ")
        self.ai_input_format["Topic"] = input("What is the Topic? : ")
        self.ai_input_format["Amount"] = input("How many questions?")

        if self.ai_input_format["Amount"] == "":
            self.ai_input_format["Amount"] = "10"

    def return_input(self):  # Returns the value to controller script
        return self.ai_input_format
