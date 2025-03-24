from Generator import QuestionGenerator
from InputHandler import UserInputHandler

class QuizManager:  # Manages the flow of data between all files
    def __init__(self):
        self.UserInputHandler = UserInputHandler()
        self.QuestionGenerator = QuestionGenerator()

    def run(self):
        self.UserInputHandler.TakeUserInputs()
        userInputs = self.UserInputHandler.ReturnInputs()

        questions = self.QuestionGenerator.Generate(userInputs)

        print("generated questions:\n", questions)


if __name__ == "__main__":
    QM = QuizManager()
    QM.run()
