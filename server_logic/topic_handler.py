import os
import json
from openai import OpenAI
from dotenv import load_dotenv


class TopicGenerator:
    def __init__(self):
        # Always load the root .env (one level up from server_logic/)
        dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        load_dotenv(dotenv_path)

        # Use OpenAI with API key from env
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_topics(self, qualification, subject, exam_board):
        """
        Uses ChatGPT to suggest topics for a given Subject + Qualification + Exam Board.
        Returns a Python list of topics.
        """

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


if __name__ == "__main__":
    # Standalone test
    tg = TopicGenerator()
    topics = tg.generate_topics("ALEVEL", "BUSINESS STUDIES", "EDUQAS")

    print("\n🔍 Suggested Topics:")
    for i, t in enumerate(topics, start=1):
        print(f"{i}. {t}")
