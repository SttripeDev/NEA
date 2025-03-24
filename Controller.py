from question_logic import Generator as Gen
from question_logic import InputHandler as IH


class QuizManager:
    # Manages the flow of data between all files
    def __init__(self):
        self.UserInputHandler = IH.UserInputHandler()
        self.QuestionGenerator = Gen.QuestionGenerator()

    def run(self):
        self.UserInputHandler.TakeUserInputs()

        userInputs = self.UserInputHandler.ReturnInputs()
        questions = self.QuestionGenerator.Generate(userInputs)
        print(userInputs)
        print(questions)




# class DatabaseManager:



if __name__ == "__main__":
    QM = QuizManager()
    QM.run()
