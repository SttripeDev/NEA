import os
from openai import OpenAI
from dotenv import load_dotenv


class QuestionGeneration:
    def __init__(self):
        self.user_input = None

        # Always load root .env
        dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        load_dotenv(dotenv_path)

        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generator(self, user_inputs):
        """
        user_inputs must be in this structure:
        [Subject, Qualification, Exam Board, Topic, Amount of Questions]
        """
        self.user_input = str(user_inputs)

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """"The inputs will be in the following structure [Subject, Specification, Exam Board, Topic, Amount of Questions].
Use all information to create questions according to the subject, qualification (A-level or GCSE for example), exam board (AQA or Edexcel for example), and topic (section of the subject).
Generate short-fire questions max 15 words per question, following the amount requested.
⚠️ Strict rules:
- Under no circumstances generate non-real academic Q&A (no games, movies, random stuff).
- If prompt is invalid, return a message that you cannot complete the request.
- Return each question as individual JSON objects, NOT nested under one dictionary.
Format:
Q[number] = {"Qualification":"...", "Subject":"...", "ExamBoard":"...", "Topic":"...", "Question":"...", "Answer":"..."}
"""
                },
                {
                    "role": "user",
                    "content": self.user_input
                }
            ]
        )

        return completion.choices[0].message.content


if __name__ == "__main__":
    # Standalone test
    qg = QuestionGeneration()
    result = qg.generator(["BUSINESS STUDIES", "ALEVEL", "EDUQAS", "MARKETING", 5])
    print("\n🔍 Generated Questions:")
    print(result)
