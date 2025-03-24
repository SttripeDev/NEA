class UserInputHandler: #Handles all user inputs
    def __init__(self):

        self.AiInputs = { #Set Default State for AiInputs
            "Qualification":"",
            "Subject":"",
            "ExamBoard":"",
            "Topic":"",
            "Amount": '10',
        }

    def TakeUserInputs(self):
        #Appends them to user specification
        self.AiInputs["Qualification"] = input("WHat is the Qualification? : ")
        self.AiInputs["Subject"] = input("What is the subject? : ")
        self.AiInputs["ExamBoard"] = input("What is the Exam Board? : ")
        self.AiInputs["Topic"] = input("What is the Topic? : ")
        self.AiInputs["Amount"] = input("How many questions?")

        if self.AiInputs["Amount"] == "":
            self.AiInputs["Amount"] = "10"

    def ReturnInputs(self):
        return self.AiInputs
