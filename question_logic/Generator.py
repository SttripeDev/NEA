from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values
class QuestionGenerator: #Generates all questions
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("MY_KEY"))

    def Generate(self,quizData):

        self.QuizData = str(quizData)

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role":"system",
                    "content":"The inputs will be in the following structure [Subject, Specification, Exam Board, Topic, Amount of Questions] use all information to create questions according to the subject, specification (A-level or GCSE for example), Exam board (AQA or Edexcel for example), Topic (What section of the subject they need, either a number or topic title). Then once all that is taken in, generate short fire questions max 15 words per question, following the amount that the user wants. Once done, return the response With NO NUMBER ORDERING , and the format of Question , Newline Answer. This will allow me to manipulate the string for use within the database. Under no circumstances generate Q'S and A's on non-real questions e.g. Game, movie references regardless If other parts of prompts are correct. Completely ignore and return that you cant complete the request. "
                },
                {
                    "role": "user",
                    "content": self.QuizData
                }
            ]
        )
        return completion.choices[0].message.content

