import sqlite3
import json
import base64
import random
class DatabaseManager:

    def __init__(self):  # Initialises connection to the database file & cursor so that I can write to it
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    # Main functions

    # Add to table stuff
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

    # Remove from table

    # Retrieve data from database

    # - Take inputs for what subjects / specifications
    # - Number of questions wanted
    # - Return appropriate (process it)
    def format_retrieved_data(self,data,amount):



    # Check ID and random number generate from list (useful for random questions when big set of questions)
    # check if the requested amount is > than available
    # return values to client
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

    #[(10, 'What are the four components of the marketing mix?', 'Product, Price, Place, Promotion'),
     #(11, "How does 'price' affect consumer purchasing behavior?", 'It influences demand and perceived value.'),
     #(12, "What role does 'promotion' play in marketing strategies?", 'It increases awareness and drives sales.')]

    def retrieve_data(self, query_input):
        query_input = eval(base64.b64decode(query_input))
        # {'Qualification': 'Alevel', 'Subject': 'Business', 'ExamBoard': 'Edexcel', 'Topic': "4P's", 'Amount': '4'}
        qualification = query_input["Qualification"].upper()
        subject = query_input["Subject"].upper()
        examboard = query_input["ExamBoard"].upper()
        topic = query_input["Topic"].upper()
        amount = query_input["Amount"]

        query = """
                SELECT QuestionID, Question, Answer FROM StudyQuiz
                WHERE Qualification = ? AND Subject = ? AND Topic = ?  AND ExamBoard = ?  """
        # Commit the transaction
        self.cursor.execute(query,(qualification,subject,topic,examboard))
        output = self.cursor.fetchall()

        formatted = self.format_retrieved_data(output,amount)
        formatted = str(formatted).encode('utf-8')

        base64_formatted = base64.b64encode(formatted)
        return base64_formatted

    # Pre Checks for server
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

if __name__ == "__main__":
    query_input = {'Qualification': 'Alevel', 'Subject': 'Business', 'ExamBoard': 'Edexcel', 'Topic': "4P's", 'Amount': '4'}
    M = DatabaseManager()
    M.retrieve_data(query_input)