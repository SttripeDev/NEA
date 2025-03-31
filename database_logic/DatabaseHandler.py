import sqlite3

TestData = { #Set Default State for AiInputs
            "Qualification":"Alevel",
            "Subject":"Business",
            "ExamBoard":"Eduqas",
            "Topic":"Motivational Theories",
            "Amount": '3',
        }
TestQuestions = """ 
What are Maslow's hierarchy of needs?  
Maslow's hierarchy includes five levels: physiological, safety, love/belonging, esteem, and self-actualization.

Explain Herzberg's two-factor theory.  
Herzberg's theory divides factors into hygiene (dissatisfaction) and motivators (satisfaction).

What is the significance of McGregor's Theory X and Theory Y?  
Theory X assumes employees are lazy, while Theory Y believes they are self-motivated. """


class DataBaseManager:

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def Add2Table(self,qualification, subject, examboard, topic, question, answer):
        self.cursor.execute("""
        INSERT INTO StudyQuiz (Qualification, Subject, ExamBoard, Topic, Question, Answer)
        VALUES (?, ?, ?, ?, ?, ?)""", [qualification, subject, examboard, topic, question, answer])
        self.conn.commit()  # Commit the transaction


    def PrepareData(self,Data, questions):
        # Split The dictionary into Each part
        Qualification = Data['Qualification']  # Sets values for 99% of database
        Subject = Data['Subject']
        ExamBoard = Data['ExamBoard']
        Topic = Data['Topic']
        Amount = int(Data['Amount'])

        lines = questions.split('\n')  # Sorts questions to be inputted
        cleaned = [line for line in lines if line.strip()]
        print(cleaned)

        cleaned3DList = []

        for x in range(Amount*2):
            



    def CreateTable(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS StudyQuiz (
            Qualification TEXT,
            Subject TEXT,
            ExamBoard TEXT,
            Topic TEXT,
            Question TEXT,
            Answer TEXT,
            PRIMARY KEY (Qualification, Subject, ExamBoard, Topic, Question)
        )""")


    def CheckExist(self):
        table_name = 'StudyQuiz'
        self.cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=?;
        """, (table_name,))
        result = self.cursor.fetchone()
        return result is not None


if __name__ == "__main__":
    db = DataBaseManager()

    if not db.CheckExist():
        db.CreateTable()
    db.PrepareData(TestData,TestQuestions)

