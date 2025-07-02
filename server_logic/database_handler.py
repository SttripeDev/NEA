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
        Name: __init__
        Parameters: self.conn: sqlite3.connect, self.cursor:cursor ,
        Returns: None
        Purpose: Constructor to set the initial values of the connection location and cursor
        """
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()




    def add_2_table(self, formatted_dictionary):
        """
        Name: add_2_table
        Parameters: formatted_dictionary:dictionary, qualification:string, subject:string, exam_board:string, topic:string,question:string,answer:string
        Returns: None
        Purpose: seperates the dictionary into individual strings then commits them to database.
        """
        qualification = formatted_dictionary["Qualification"].upper()
        subject = formatted_dictionary["Subject"].upper()
        exam_board = formatted_dictionary["ExamBoard"].upper()
        topic = formatted_dictionary["Topic"].upper()
        question = formatted_dictionary["Question"]
        answer = formatted_dictionary["Answer"]

        self.cursor.execute("""
        INSERT INTO StudyQuiz (Qualification, Subject, ExamBoard, Topic, Question, Answer)
        VALUES (?, ?, ?, ?, ?, ?)""", [qualification, subject, exam_board, topic, question, answer])

        self.conn.commit()
    def prepare_data_to_add(self, raw_data):
        """
        Name: preparte_data_to_add
        Parameters: raw_data:array , filtered_raw_list:array
        Returns: None
        Purpose: filters the list of unrequired characters , then loops through list to make it a dictionary to send to add_2_table
        """
        raw_list = raw_data.split("\n")

        filtered_raw_list = [item for item in raw_list if item not in ("```", "", "json", "```json")]

        for x in range(len(filtered_raw_list)):
            data = filtered_raw_list[x]
            raw_dictionary = data.split(' = ')[1]

            formatted_dictionary = json.loads(raw_dictionary)

            self.add_2_table(formatted_dictionary)

    def format_retrieved_data(self,data,amount):
        """
        Name: format_retrieved_data
        Parameters: data:array, amount:integer
        Returns: None
        Purpose: format the data from retrieval to return to client .
        """

        id_list = []
        for x in range(len(data)):
            id_list.insert(x,data[x][0])
        question_list = []
        q_and_a = []
        for x in range(len(data)):
            random_question_id = random.choice(id_list)
            id_list.remove(random_question_id)
            for y in range(len(data)):
                if random_question_id == data[y][0]:
                    question = data[y][1]
                    answer = data[y][2]
                    q_and_a = [question,answer]
                    question_list.insert(x, q_and_a)
                else:
                    continue

        return question_list

    def retrieve_data(self, query_input):
        """
        Name: retrieved_data
        Parameters: query_input: array
        Returns: formatted
        Purpose: decodes the data and seperated it into seperate variables to send a database request.
        """
        query_input = json.loads(query_input)
        qualification = query_input["Qualification"].upper()
        subject = query_input["Subject"].upper()
        examboard = query_input["ExamBoard"].upper()
        topic = query_input["Topic"].upper()
        amount = query_input["Amount"]

        query = """
                SELECT QuestionID, Question, Answer FROM StudyQuiz
                WHERE Qualification = ? AND Subject = ? AND Topic = ?  AND ExamBoard = ?  """

        self.cursor.execute(query,(qualification,subject,topic,examboard))
        output = self.cursor.fetchall()

        formatted = self.format_retrieved_data(output,amount)
        formatted = json.dumps(formatted)

        return formatted


    def create_table(self):
        """
        Name: create_table
        Parameters: self.cursor:sqlite3.cursor
        Returns: None
        Purpose: Creates the StudyQuiz Table
        """
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

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ExamBoard (
            BoardID INTEGER PRIMARY KEY AUTOINCREMENT ,
            BoardName TEXT)""")



    def add_prerequisites(self):
        examBoard = ["AQA","EDEXCEL","EDUQAS","OCR"]
        for x in range(len(examBoard)):

            self.cursor.execute("""
                INSERT INTO ExamBoard (BoardName)
                VALUES (?)""",[examBoard[x]])

            self.conn.commit()
    def check_exist(self):
        """
        Name: check_exist
        Parameters: table_name:string
        Returns: results
        Purpose: Checks it 'StudyQuiz' exists
        """
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
    db = DatabaseManager()
    if not db.check_exist():
        db.create_table()
        db.add_prerequisites()