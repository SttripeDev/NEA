import sqlite3


connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Set Default State for AiInputs
Data = {
    "Qualification": "Alevel",
    "Subject": "Maths",
    "ExamBoard": "AQA",
    "Topic": "Quadratics",
    "Amount": "1",
}

questions = """
1. 'What do the 4P's of marketing stand for?', 'Product, Price, Place, Promotion'
2. 'What is Maths?' , 'To do stuff'"""


def PrepareData(Data,Questions):
    #Split The dictionary into Each part
    Qualification = Data['Qualification']
    Subject = Data['Subject']
    ExamBoard = Data['ExamBoard']
    Topic = Data['Topic']
    Amount = int(Data['Amount'])

    # for x in range(Amount):
    #     None

def Add2Table(Data):
    cursor.execute("""
    INSERT INTO StudyQuiz (Qualification, Subject, ExamBoard, Topic, Question, Answer)
    VALUES (?, ?, ?, ?, ?, ?)""",
    (Data['Qualification'], Data['Subject'], Data['ExamBoard'], Data['Topic'], Data['Question'], Data['Answer']))
    connection.commit()  # Commit the transaction

def CreateTable():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS StudyQuiz (
        Qualification TEXT,
        Subject TEXT,
        ExamBoard TEXT,
        Topic TEXT,
        Question TEXT,
        Answer TEXT,
        PRIMARY KEY (Qualification, Subject, ExamBoard, Topic, Question)
    )""")

def CheckExist():
    table_name = 'StudyQuiz'
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?;
    """, (table_name,))
    result = cursor.fetchone()
    return result is not None

if __name__ == "__main__":
    if not CheckExist():
        CreateTable()
    Add2Table(Data)
    connection.close()  # Close the connection