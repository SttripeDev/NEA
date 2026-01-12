# user_database_handler.py
import sqlite3
import os

''' 
Name: UserDatabaseManager
Purpose: Manages local user database that mirrors server database structure , storing a tally of incorrect questions
'''
class UserDatabaseManager:
    '''
    Name: __init__
    Purpose: Constructor for database path location
    '''
    def __init__(self, db_name="user_database.db"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(current_dir, db_name)
    ''' 
    Name: connect
    Parameters: None
    Returns: None
    Purpose: connect to local database file found at self.db_name
    '''
    def connect(self):
        return sqlite3.connect(self.db_name)
    ''' 
    Name: check_exist
    Parameters: None
    Returns: None
    Purpose: Check if there is a database to be found at the path
    '''
    def check_exist(self):
        return os.path.exists(self.db_name)
    ''' 
    Name: create_tables
    Parameters: None
    Returns: None
    Purpose: Create all necessary tables mirroring server structure.
    '''
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
                  CREATE TABLE IF NOT EXISTS Qualifications(
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
                      UNIQUE(QualificationID, ExamBoardID,SubjectName)
                      )
                  """)

        # Topics table
        c.execute("""
                  CREATE TABLE IF NOT EXISTS Topics(
                      TopicID INTEGER PRIMARY KEY AUTOINCREMENT,
                      SubjectID INTEGER NOT NULL,
                      TopicName TEXT NOT NULL,
                      FOREIGN KEY(SubjectID) REFERENCES Subjects(SubjectID),
                      UNIQUE(SubjectID,TopicName)
                      )
                  """)

        # StudyQuiz table with Tally column
        c.execute("""
                  CREATE TABLE IF NOT EXISTS StudyQuiz(
                      QuestionID INTEGER PRIMARY KEY,
                      TopicID INTEGER NOT NULL,
                      Question TEXT NOT NULL,
                      Answer TEXT NOT NULL,
                      Tally INTEGER DEFAULT 1,
                      FOREIGN KEY(TopicID) REFERENCES Topics(TopicID)
                      )
                  """)

        conn.commit()
        conn.close()


#Add Data
    ''' 
    Name: add_exam_board
    Parameters: exam_board_name: string
    Returns: None
    Purpose: Add exam board , ignores if it already exist
    '''
    def add_exam_board(self, exam_board_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO ExamBoards (ExamBoardName) VALUES (?)", (exam_board_name,))
        conn.commit()
        conn.close()
    ''' 
    Name: add_qualification
    Parameters: qualification_name: string
    Returns: None
    Purpose: Add qualification, ignores if it already exist
    '''
    def add_qualification(self, qualification_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO Qualifications (QualificationName) VALUES (?)", (qualification_name,))
        conn.commit()
        conn.close()
    ''' 
    Name: add_subject
    Parameters: qualification_id:integer , exam_board_id:integer , subject_name:string
    Returns: None
    Purpose: Add subject, ignores if it already exist
    '''
    def add_subject(self, qualification_id, exam_board_id, subject_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""
                  INSERT
                  OR IGNORE INTO Subjects (QualificationID, ExamBoardID, SubjectName)
            VALUES (?, ?, ?)
                  """, (qualification_id, exam_board_id, subject_name))
        conn.commit()
        conn.close()
    ''' 
    Name: add_topic
    Parameters: subject_id:integer , topic_name: string
    Returns: None
    Purpose: Add topic, ignores if it already exist
    '''
    def add_topic(self, subject_id, topic_name):
        """Add topic, ignore if exists."""
        conn = self.connect()
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO Topics (SubjectID, TopicName) VALUES (?, ?)", (subject_id, topic_name))
        conn.commit()
        conn.close()
    ''' 
    Name: add_incorrect_question
    Parameters: question_id:integer , topic_id: integer , question: string , answer:string
    Returns: None
    Purpose: Add an incorrect question to the database. If question already exists, increment the tally instead.
    '''
    def add_incorrect_question(self, question_id, topic_id, question, answer):
        conn = self.connect()
        c = conn.cursor()

        # Check if question already exists
        c.execute("SELECT Tally FROM StudyQuiz WHERE QuestionID = ?", (question_id,))
        existing = c.fetchone()

        if existing:
            # Increment tally
            new_tally = existing[0] + 1
            c.execute("UPDATE StudyQuiz SET Tally = ? WHERE QuestionID = ?", (new_tally, question_id))
        else:
            # Insert new question with tally = 1
            c.execute("""
                      INSERT INTO StudyQuiz (QuestionID, TopicID, Question, Answer, Tally)
                      VALUES (?, ?, ?, ?, 1)
                      """, (question_id, topic_id, question.strip(), answer.strip()))

        conn.commit()
        conn.close()
    ''' 
    Name: remove_correct_question
    Parameters: question_id:integer 
    Returns: None
    Purpose: Remove a question that was answered correctly.
    '''
    def remove_correct_question(self, question_id):
        conn = self.connect()
        c = conn.cursor()
        c.execute("DELETE FROM StudyQuiz WHERE QuestionID = ?", (question_id,))
        conn.commit()
        conn.close()

#Retrieval methods
    ''' 
    Name: get_exam_boards
    Parameters: None
    Returns: rows : tuple
    Purpose: Get all exam boards.
    '''
    def get_exam_boards(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM ExamBoards")
        rows = c.fetchall()
        conn.close()
        return rows
    ''' 
    Name: get_qualifcations
    Parameters: None
    Returns: rows : tuple
    Purpose: Get all Qualifications.
    '''
    def get_qualifications(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM Qualifications")
        rows = c.fetchall()
        conn.close()
        return rows
    ''' 
    Name: get_subjects
    Parameters: None
    Returns: rows : tuple
    Purpose: Get all subjects.
    '''
    def get_subjects(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM Subjects")
        rows = c.fetchall()
        conn.close()
        return rows
    ''' 
    Name: get_subject_id
    Parameters: subject_name:string, qualification_id:integer, exam_board_id:integer
    Returns: row[0] : integer
    Purpose: Get subject ID by name and parent IDs.
    '''
    def get_subject_id(self, subject_name, qualification_id, exam_board_id):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""
                  SELECT SubjectID
                  FROM Subjects
                  WHERE SubjectName = ?
                    AND QualificationID = ?
                    AND ExamBoardID = ?
                  """, (subject_name, qualification_id, exam_board_id))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    ''' 
    Name: get_topics_by_hierarchy
    Parameters: subject_name:string, qualification_id:integer, exam_board_id:integer
    Returns: rows:tuple
    Purpose: Get topics for a specific qualification/subject/exam board combination.
    '''
    def get_topics_by_hierarchy(self, qualification_id, subject_name, exam_board_id):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""
                  SELECT t.TopicID, t.TopicName
                  FROM Topics t
                           JOIN Subjects s ON t.SubjectID = s.SubjectID
                  WHERE s.QualificationID = ?
                    AND s.SubjectName = ?
                    AND s.ExamBoardID = ?
                  """, (qualification_id, subject_name, exam_board_id))
        rows = c.fetchall()
        conn.close()
        return rows
    ''' 
    Name: get_qualification_id
    Parameters: qualification_name
    Returns: row[0] : integer
    Purpose: Get qualification ID by name.
    '''
    def get_qualification_id(self, qualification_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT QualificationID FROM Qualifications WHERE QualificationName = ?", (qualification_name,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    ''' 
    Name: get_exam_board_id
    Parameters: exam_board_name
    Returns: row[0] : integer
    Purpose: Get exam board ID by name.
    '''
    def get_exam_board_id(self, exam_board_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT ExamBoardID FROM ExamBoards WHERE ExamBoardName = ?", (exam_board_name,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    ''' 
    Name: get_topic_id
    Parameters: subject_id:integer, topic_name:string
    Returns: row[0] : integer
    Purpose: Get topic ID by subject ID and topic name.
    '''
    def get_topic_id(self, subject_id, topic_name):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT TopicID FROM Topics WHERE SubjectID = ? AND TopicName = ?", (subject_id, topic_name))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    ''' 
    Name: get_incorrect_questions_by_topic
    Parameters: topic_id:integer 
    Returns: rows:tuple
    Purpose: Get all incorrect questions for a specific topic.
    '''
    def get_incorrect_questions_by_topic(self, topic_id):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""
                  SELECT QuestionID, Question, Answer, Tally
                  FROM StudyQuiz
                  WHERE TopicID = ?
                  ORDER BY Tally DESC
                  """, (topic_id,))
        rows = c.fetchall()
        conn.close()
        return rows
    ''' 
    Name: get_weak_area_sets
    Parameters: None
    Returns: result:array
    Purpose:Get all qualification/subject/exam_board/topic combinations that have incorrect questions. Returns structured data for dropdown menus.
    '''
    def get_weak_area_sets(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""
                  SELECT DISTINCT q.QualificationName, s.SubjectName, e.ExamBoardName, t.TopicName
                  FROM StudyQuiz sq
                           JOIN Topics t ON sq.TopicID = t.TopicID
                           JOIN Subjects s ON t.SubjectID = s.SubjectID
                           JOIN Qualifications q ON s.QualificationID = q.QualificationID
                           JOIN ExamBoards e ON s.ExamBoardID = e.ExamBoardID
                  ORDER BY q.QualificationName, s.SubjectName, e.ExamBoardName, t.TopicName
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
    ''' 
    Name: ensure_hierarchy_exists
    Parameters: qualification_name:string, subject_name:string, exam_board_name:string, topic_name:string
    Returns: topic_id:integer
    Purpose:Ensure all hierarchy components exist in database before adding questions. Returns topic_id or None if creation fails.
    '''
    def ensure_hierarchy_exists(self, qualification_name, subject_name, exam_board_name, topic_name):
        self.add_qualification(qualification_name)
        qualification_id = self.get_qualification_id(qualification_name)
        if not qualification_id:
            return None

        self.add_exam_board(exam_board_name)
        exam_board_id = self.get_exam_board_id(exam_board_name)
        if not exam_board_id:
            return None

        self.add_subject(qualification_id, exam_board_id, subject_name)
        subject_id = self.get_subject_id(subject_name, qualification_id, exam_board_id)
        if not subject_id:
            return None

        self.add_topic(subject_id, topic_name)
        topic_id = self.get_topic_id(subject_id, topic_name)

        return topic_id
    ''' 
    Name: has_weak_areas
    Parameters: None
    Returns: count:integer
    Purpose:Check if user has any weak areas stored.
    '''
    def has_weak_areas(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM StudyQuiz")
        count = c.fetchone()[0]
        conn.close()
        return count > 0