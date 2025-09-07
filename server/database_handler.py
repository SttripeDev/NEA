import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def check_exist(self):
        return os.path.exists(self.db_name)

    def create_tables(self):
        conn = self.connect()
        c = conn.cursor()

        # ExamBoards table
        c.execute("""
            CREATE TABLE IF NOT EXISTS ExamBoards (
                ExamBoardID INTEGER PRIMARY KEY AUTOINCREMENT,
                ExamBoardName TEXT UNIQUE NOT NULL
            )
        """)

        # Qualifications table
        c.execute("""
            CREATE TABLE IF NOT EXISTS Qualifications (
                QualificationID INTEGER PRIMARY KEY AUTOINCREMENT,
                QualificationName TEXT UNIQUE NOT NULL
            )
        """)

        # Subjects table
        c.execute("""
            CREATE TABLE IF NOT EXISTS Subjects (
                SubjectID INTEGER PRIMARY KEY AUTOINCREMENT,
                QualificationID INTEGER NOT NULL,
                ExamBoardID INTEGER NOT NULL,
                SubjectName TEXT NOT NULL,
                FOREIGN KEY(QualificationID) REFERENCES Qualifications(QualificationID),
                FOREIGN KEY(ExamBoardID) REFERENCES ExamBoards(ExamBoardID),
                UNIQUE(QualificationID, ExamBoardID, SubjectName)
            )
        """)

        # Topics table
        c.execute("""
            CREATE TABLE IF NOT EXISTS Topics (
                TopicID INTEGER PRIMARY KEY AUTOINCREMENT,
                SubjectID INTEGER NOT NULL,
                TopicName TEXT NOT NULL,
                FOREIGN KEY(SubjectID) REFERENCES Subjects(SubjectID),
                UNIQUE(SubjectID, TopicName)
            )
        """)

        # StudyQuiz table
        c.execute("""
            CREATE TABLE IF NOT EXISTS StudyQuiz (
                QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
                TopicID INTEGER NOT NULL,
                Question TEXT NOT NULL,
                Answer TEXT NOT NULL,
                FOREIGN KEY(TopicID) REFERENCES Topics(TopicID)
            )
        """)

        conn.commit()
        conn.close()

    # Add Data
    def add_exam_board(self, exam_board_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO ExamBoards (ExamBoardName) VALUES (?)", (exam_board_name,))
        conn.commit()
        conn.close()

    def add_qualification(self, qualification_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO Qualifications (QualificationName) VALUES (?)", (qualification_name,))
        conn.commit()
        conn.close()

    def add_subject(self, qualification_id, exam_board_id, subject_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""
            INSERT OR IGNORE INTO Subjects (QualificationID, ExamBoardID, SubjectName)
            VALUES (?, ?, ?)
        """, (qualification_id, exam_board_id, subject_name))
        conn.commit()
        conn.close()

    def add_topic(self, subject_id, topic_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO Topics (SubjectID, TopicName) VALUES (?, ?)", (subject_id, topic_name))
        conn.commit()
        conn.close()

    def add_question(self, topic_id, question, answer):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO StudyQuiz (TopicID, Question, Answer)
            VALUES (?, ?, ?)
        """, (topic_id, question.strip(), answer.strip()))
        conn.commit()
        conn.close()
        print(f"✅ Question inserted into TopicID {topic_id}")

    # Retrieval Methods
    def get_exam_boards(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM ExamBoards")
        rows = c.fetchall()
        conn.close()
        return rows

    def get_qualifications(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM Qualifications")
        rows = c.fetchall()
        conn.close()
        return rows

    def get_subjects(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM Subjects")
        rows = c.fetchall()
        conn.close()
        return rows

    def get_subject_id(self, subject_name, qualification_id, exam_board_id):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""
            SELECT SubjectID FROM Subjects
            WHERE SubjectName = ? AND QualificationID = ? AND ExamBoardID = ?
        """, (subject_name, qualification_id, exam_board_id))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    def get_topics_by_hierarchy(self, qualification_id, subject_name, exam_board_id):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""
            SELECT t.TopicID, t.TopicName
            FROM Topics t
            JOIN Subjects s ON t.SubjectID = s.SubjectID
            WHERE s.QualificationID = ? AND s.SubjectName = ? AND s.ExamBoardID = ?
        """, (qualification_id, subject_name, exam_board_id))
        rows = c.fetchall()
        conn.close()
        return rows

    def get_existing_sets(self):

        conn = self.connect()
        c = conn.cursor()
        c.execute("""
            SELECT DISTINCT q.QualificationName, s.SubjectName, e.BoardName, t.TopicName
            FROM StudyQuiz sq
            JOIN Topics t ON sq.TopicID = t.TopicID
            JOIN Subjects s ON t.SubjectID = s.SubjectID
            JOIN Qualifications q ON s.QualificationID = q.QualificationID
            JOIN ExamBoards e ON s.ExamBoardID = e.BoardID
            ORDER BY q.QualificationName, s.SubjectName, e.BoardName, t.TopicName
        """)
        rows = c.fetchall()
        conn.close()

        result = []
        for row in rows:
            result.append({
                "qualification": row[0],
                "subject": row[1],
                "exam_board": row[2],
                "topic": row[3]
            })
        return result

    # Retrieve ID methods
    def get_qualification_id(self, qualification_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT QualificationID FROM Qualifications WHERE QualificationName = ?", (qualification_name,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    def get_exam_board_id(self, exam_board_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT ExamBoardID FROM ExamBoards WHERE ExamBoardName = ?", (exam_board_name,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    def get_topic_id(self, subject_id, topic_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT TopicID FROM Topics WHERE SubjectID = ? AND TopicName = ?", (subject_id, topic_name))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    def get_questions_by_topic(self, topic_id):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""
            SELECT QuestionID, Question, Answer
            FROM StudyQuiz
            WHERE TopicID = ?
        """, (topic_id,))
        rows = c.fetchall()
        conn.close()
        return rows

