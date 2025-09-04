import json
import random
import sqlite3


class DatabaseManager:
    """
    Name: DatabaseManager
    Purpose: Controls the flow in and out of the database
    """

    def __init__(self):
        """
        Constructor to set the initial values of the connection location and cursor
        """
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    # -------------------- INSERTIONS --------------------

    def add_exam_board(self, board_name):
        self.cursor.execute("INSERT INTO ExamBoards (BoardName) VALUES (?)", (board_name,))
        self.conn.commit()

    def add_qualification(self, qual_name):
        self.cursor.execute("INSERT INTO Qualifications (QualificationName) VALUES (?)", (qual_name,))
        self.conn.commit()

    def add_subject(self, qualification_id, exam_board_id, subject_name):
        self.cursor.execute("""
            INSERT INTO Subjects (QualificationID, ExamBoardID, SubjectName)
            VALUES (?, ?, ?)
        """, (qualification_id, exam_board_id, subject_name))
        self.conn.commit()

    def add_topic(self, subject_id, topic_name):
        self.cursor.execute("""
            INSERT INTO Topics (SubjectID, TopicName)
            VALUES (?, ?)
        """, (subject_id, topic_name))
        self.conn.commit()

    def add_question(self, topic_id, question, answer):
        self.cursor.execute("""
            INSERT INTO StudyQuiz (TopicID, Question, Answer)
            VALUES (?, ?, ?)
        """, (topic_id, question, answer))
        self.conn.commit()

    # -------------------- RETRIEVAL --------------------

    def get_exam_boards(self):
        self.cursor.execute("SELECT * FROM ExamBoards")
        return self.cursor.fetchall()

    def get_qualifications(self):
        self.cursor.execute("SELECT * FROM Qualifications")
        return self.cursor.fetchall()

    def get_subjects(self):
        self.cursor.execute("SELECT * FROM Subjects")
        return self.cursor.fetchall()

    def get_topics_by_subject(self, subject_id):
        self.cursor.execute("SELECT * FROM Topics WHERE SubjectID=?", (subject_id,))
        return self.cursor.fetchall()

    def get_questions_by_topic(self, topic_id, amount):
        self.cursor.execute("""
            SELECT QuestionID, Question, Answer FROM StudyQuiz WHERE TopicID = ?
        """, (topic_id,))
        data = self.cursor.fetchall()
        return self.format_retrieved_data(data, amount)

    # -------------------- HELPERS --------------------

    def format_retrieved_data(self, data, amount):
        id_list = [row[0] for row in data]
        question_list = []
        for _ in range(min(amount, len(id_list))):
            random_question_id = random.choice(id_list)
            id_list.remove(random_question_id)
            for row in data:
                if row[0] == random_question_id:
                    question_list.append([row[1], row[2]])
                    break
        return question_list

    def retrieve_data(self, query_input):
        query_input = json.loads(query_input)
        topic_id = query_input["TopicID"]
        amount = query_input["Amount"]

        output = self.get_questions_by_topic(topic_id, amount)
        formatted = json.dumps(output)
        return formatted

    # -------------------- TABLE CREATION --------------------

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ExamBoards (
            BoardID INTEGER PRIMARY KEY AUTOINCREMENT,
            BoardName TEXT
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Qualifications (
            QualificationID INTEGER PRIMARY KEY AUTOINCREMENT,
            QualificationName TEXT
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subjects (
            SubjectID INTEGER PRIMARY KEY AUTOINCREMENT,
            QualificationID INTEGER,
            ExamBoardID INTEGER,
            SubjectName TEXT,
            FOREIGN KEY(QualificationID) REFERENCES Qualifications(QualificationID),
            FOREIGN KEY(ExamBoardID) REFERENCES ExamBoards(BoardID)
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Topics (
            TopicID INTEGER PRIMARY KEY AUTOINCREMENT,
            SubjectID INTEGER,
            TopicName TEXT,
            FOREIGN KEY(SubjectID) REFERENCES Subjects(SubjectID)
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS StudyQuiz (
            QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
            TopicID INTEGER,
            Question TEXT,
            Answer TEXT,
            FOREIGN KEY(TopicID) REFERENCES Topics(TopicID)
        )""")

    def check_exist(self, table_name="StudyQuiz"):
        self.cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name=?;
        """, (table_name,))
        result = self.cursor.fetchone()
        return result is not None
