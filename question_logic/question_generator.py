# Import all required libraries
from openai import OpenAI
import os
from dotenv import load_dotenv


class QuestionGeneration:
    def __init__(self):
        self.user_input = None
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("MY_KEY"))

    def generator(self, user_inputs):

        self.user_input = str(user_inputs)


        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """"The inputs will be in the following structure [Subject, Specification, Exam Board, Topic, Amount of Questions] use all information to create questions according to the subject, specification (A-level or GCSE for example), Exam board (AQA or Edexcel for example), Topic (What section of the subject they need, either a number or topic title). Then once all that is taken in, generate short fire questions max 15 words per question, following the amount that the user wants.. Under no circumstances generate Q'S and A's on non-real questions e.g. Game, movie references regardless If other parts of prompts are correct. Completely ignore and return that you cant complete the request. Once done, return the response in the form of json dictionary for each question. For formatting refer to the stub im going to write in. Anything in square brackets is what is changing each time as a result. Form is this: 

Q[number] = {"Qualification":[qualification provided],"Subject":[Subject provided],"ExamBoard":[ExamBoard provided],"Topic":[Topic Provided],"Question":[Question generated] , "Answer":[Answer Generated]

this will allow for more seamless integration to my database without as much string manipulation. I want it to be individual json formatted per question and not fall under one dictionary as it makes it a mess , when you last generated you had a son thing called json = {} containing questions just generate the questions. """
                },
                {
                    "role": "user",
                    "content": self.user_input
                }
            ]
        )
        return completion.choices[0].message.content
