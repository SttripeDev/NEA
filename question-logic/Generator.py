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
                    "content":"The inputs will be in the following structure [Subject, Specification, Exam Board, Topic, Amount of Questions] use all information to create questions according to the subject, specification (A-level or GCSE for example), Exam board (AQA or Edexcel for example), Topic (What section of the subject they need, either a number or topic title). Then once all that is taken in, generate shortfire questions max 15 words per question, following the amount that the user wants. Once done, return them to me without any extra text but Q followed by Answer."
                },
                {
                    "role": "user",
                    "content": self.QuizData
                }
            ]
        )
        return completion.choices[0].message.content

