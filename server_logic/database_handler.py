import sqlite3
import json



class DatabaseManager:

    def __init__(self):  # Initialises connection to the database file & cursor so that I can write to it
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def add_2_table(self, formatted_dictionary):
        # Adds data to the table by separating the json dictionary into each part
        qualification = formatted_dictionary["Qualification"].upper()
        subject = formatted_dictionary["Subject"].upper()
        exam_board = formatted_dictionary["ExamBoard"].upper()
        topic = formatted_dictionary["Topic"].upper()
        question = formatted_dictionary["Question"]
        answer = formatted_dictionary["Answer"]

        # Inputted into database by use of SQL
        self.cursor.execute("""
        INSERT INTO StudyQuiz (Qualification, Subject, ExamBoard, Topic, Question, Answer)
        VALUES (?, ?, ?, ?, ?, ?)""", [qualification, subject, exam_board, topic, question, answer])
        # Commit the transaction
        self.conn.commit()

    def prepare_data_to_add(self, raw_data):
        # Splits the string based on new lines to allow for all questions to be in one list
        raw_list = raw_data.split("\n")

        # Remove unwanted details in the list
        filtered_raw_list = [item for item in raw_list if item not in ("```", "", "json", "```json")]

        # Loops the length of the list to filter remaining attributes

        for x in range(len(filtered_raw_list)):
            data = filtered_raw_list[x]
            raw_dictionary = data.split(' = ')[1]

            # Convert the list to a dictionary
            formatted_dictionary = json.loads(raw_dictionary)

            # Add to the table
            self.add_2_table(formatted_dictionary)

    def create_table(self):
        # Creates table in the correct format with questionID as primary key
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS StudyQuiz (
            QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
            Qualification TEXT,
            Subject TEXT,
            ExamBoard TEXT,
            Topic TEXT,
            Question TEXT,
            Answer TEXT
        )""")

    def check_exist(self):
        # A method of ensuring the table does exist.
        table_name = 'StudyQuiz'
        self.cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=?;
        """, (table_name,))
        result = self.cursor.fetchone()
        return result is not None
