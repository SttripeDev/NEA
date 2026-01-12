import os
import json
from openai import OpenAI
from dotenv import load_dotenv
''' 
Name: TopicGenerator
Purpose: Contains the ChatGPT api calls for topic list generation
'''
class TopicGeneration:
    '''
    Name: __init__
    Purpose: Constructor for topic generation containing apikey setting
    '''
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        load_dotenv(dotenv_path)

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    ''' 
    Name: generate_topics 
    Parameters: qualification,subject,exam_board
    Returns: topics:array 
    Purpose: API request to generate topic list using chatGPT
    '''
    def generate_topics(self, qualification, subject, exam_board):
        user_input = f"[{subject}, {qualification}, {exam_board}]"

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """The input will always be structured as 
                    [Subject, Qualification, Exam Board].

                    Based on this, generate a comprehensive list of TOPICS
                    that would normally appear in a specification for that course.

                     Important formatting rules:
                    - Return ONLY valid JSON in the form of a Python list of strings.
                      Example: ["Topic 1", "Topic 2", "Topic 3"]
                    - Do not include explanations or extra text.
                    """
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        raw_output = completion.choices[0].message.content.strip()

        try:
            topics = json.loads(raw_output)
            return topics
        except Exception:
            print("⚠ ChatGPT returned unexpected format:")
            print(raw_output)
            return []
''' 
Name: QuestionGeneration
Purpose: Contains the ChatGPT api calls for question generation
'''
class QuestionGeneration:
    '''
    Name: __init__
    Purpose: Constructor for topic generation containing apikey setting
    '''
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        load_dotenv(dotenv_path)

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    ''' 
    Name: generate_questions 
    Parameters: user_inputs
    Returns: questions:JSON 
    Purpose: API request to generate questions using chatGPT
    '''
    def generate_questions(self, user_inputs):
        subject, qualification, exam_board, topic, amount = user_inputs

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an academic Q&A generator.
Inputs are always [Subject, Qualification, Exam Board, Topic, Amount].
Generate exactly the requested number of Q&A pairs.

⚠️ STRICT RULES:
- Return ONLY a valid JSON array.
- Each item must be a JSON object with keys: Qualification, Subject, ExamBoard, Topic, Question, Answer.
- No markdown, no explanations, no labels like Q1=.
- Short-fire questions (max 15 words).
"""
                },
                {
                    "role": "user",
                    "content": json.dumps({
                        "Subject": subject,
                        "Qualification": qualification,
                        "ExamBoard": exam_board,
                        "Topic": topic,
                        "Amount": amount
                    })
                }
            ],
            temperature=0.7
        )

        raw_output = completion.choices[0].message.content.strip()

        try:
            questions = json.loads(raw_output)
        except json.JSONDecodeError:
            raise ValueError("GPT did not return valid JSON")

        return questions
