from question_logic import Generator as Gen
from question_logic import InputHandler as IH
from database_logic import DatabaseHandler as DBH

class QuizManager:
    # Manages the flow of data between all files
    def __init__(self):
        self.UserInputHandler = IH.UserInputHandler()
        self.QuestionGenerator = Gen.QuestionGenerator()
        self.DatabaseManager = DBH.DataBaseManager()


    def run(self):
        self.UserInputHandler.TakeUserInputs()

        userInputs = self.UserInputHandler.ReturnInputs()
        questions = self.QuestionGenerator.Generate(userInputs)
        print(questions ,"\n")

        self.DatabaseManager.PrepareData(userInputs,questions)











if __name__ == "__main__":
    QM = QuizManager()
    QM.run()
