class UserInputHandler:
    """
        Name: __init__
        Parameters: self.ai_input_format ,
        Returns: None
        Purpose: Defines the default state for ai_input_format
    """
    def __init__(self):
        self.ai_input_format = {
            "Qualification": "",
            "Subject": "",
            "ExamBoard": "",
            "Topic": "",
            "Amount": '10',
        }

    def take_user_input(self):

        self.ai_input_format["Qualification"] = input("WHat is the Qualification? : ")
        self.ai_input_format["Subject"] = input("What is the subject? : ")
        self.ai_input_format["ExamBoard"] = input("What is the Exam Board? : ")
        self.ai_input_format["Topic"] = input("What is the Topic? : ")
        self.ai_input_format["Amount"] = input("How many questions?")

        if self.ai_input_format["Amount"] == "":
            self.ai_input_format["Amount"] = "10"

    def return_input(self):
        return self.ai_input_format
