import sqlite3
import json
import socket
from database_handler import DatabaseManager
from topic_handler import TopicGenerator


class ServerManager:
    '''
    Name: ServerManager
    Purpose: Controls server behaviour including listening for client connections,
    forwarding requests to the database, and handling setup for Exam Boards,
    Qualifications, Subjects, and Topics.
    '''

    def __init__(self):
        '''
        Name: __init__
        Parameters: None
        Returns: None
        Purpose: Constructor that initialises host, port, socket, and database manager.
        '''
        self.host = "127.0.0.1"
        self.port = 51000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.dbm = DatabaseManager()
        self.topic_gen = TopicGenerator()

    def database_insert(self, data):
        '''
        Name: database_insert
        Parameters: data: string
        Returns: None
        Purpose: Sends formatted JSON data to the database for insertion.
        '''
        self.dbm.prepare_data_to_add(data)

    def database_retrieve(self, data):
        '''
        Name: database_retrieve
        Parameters: data: string
        Returns: string
        Purpose: Sends request to the database and retrieves formatted data.
        '''
        return self.dbm.retrieve_data(data)

    def available_topics(self, data):
        '''
        Name: available_topics
        Parameters: data: string
        Returns: None
        Purpose: Placeholder for future feature to list available topics.
        '''
        None

    def server_listen(self):
        '''
        Name: server_listen
        Parameters: None
        Returns: None
        Purpose: Starts listening for client connections and handles requests.
        '''
        print("Server is listening on port", self.port)
        self.s.listen(1)
        while True:
            connection, address = self.s.accept()
            print("New connection from", address)
            data = connection.recv(1024).decode("utf-8")
            print("Data received from user")
            if data.startswith("```json"):
                self.database_insert(data)
            else:
                result = self.database_retrieve(data)
                connection.send(result.encode())
            connection.close()

    def setup_mode(self):
        '''
        Name: setup_mode
        Parameters: None
        Returns: None
        Purpose: Guides the user through setting up Exam Boards, Qualifications,
        Subjects and Topics in the database. Optionally integrates with ChatGPT
        to generate topics.
        '''
        print("\nSetup Mode Selected")
        self.dbm.create_tables()

        # Exam Boards
        print("\nEnter Exam Boards (type 'exit' to finish):")
        while True:
            exam_board = input("Exam Board: ").strip().upper()
            if exam_board == "EXIT":
                break
            self.dbm.add_exam_board(exam_board)

        # Qualifications
        print("\nEnter Qualifications (type 'exit' to finish):")
        while True:
            qualification = input("Qualification: ").strip().upper()
            if qualification == "EXIT":
                break
            self.dbm.add_qualification(qualification)

        # Subjects
        print("\nNow entering Subjects (type 'exit' as subject name to finish):")
        while True:
            print("\nAvailable Qualifications:")
            for q in self.dbm.get_qualifications():
                print(f"{q[0]}. {q[1]}")

            qualification_id = input("Select Qualification ID: ").strip()
            if qualification_id.upper() == "EXIT":
                break

            print("\nAvailable Exam Boards:")
            for e in self.dbm.get_exam_boards():
                print(f"{e[0]}. {e[1]}")

            exam_board_id = input("Select Exam Board ID: ").strip()
            if exam_board_id.upper() == "EXIT":
                break

            subject_name = input("Enter Subject Name: ").strip().upper()
            if subject_name == "EXIT":
                break

            confirm = input(f"Confirm Subject '{subject_name}'? (Y/N): ").strip().upper()
            if confirm == "Y":
                self.dbm.add_subject(qualification_id, exam_board_id, subject_name)

                # Topics
                choice = input("\nDo you want to auto-generate topics with ChatGPT? (Y/N): ").strip().upper()
                if choice == "Y":
                    try:
                        topics = self.topic_gen.generate_topics(
                            qualification=qualification_id,
                            subject=subject_name,
                            exam_board=exam_board_id
                        )
                        print("\nTopics suggested by ChatGPT:")
                        for i, t in enumerate(topics, start=1):
                            print(f"{i}. {t}")

                        approve = input("Accept these topics? (Y/N): ").strip().upper()
                        if approve == "Y":
                            for t in topics:
                                self.dbm.add_topic(subject_name, t)
                    except Exception as e:
                        print(f"ChatGPT topic generation failed: {e}")
                else:
                    print("\nEnter Topics for this Subject (type 'exit' to finish):")
                    while True:
                        topic_name = input("Topic: ").strip().upper()
                        if topic_name == "EXIT":
                            break
                        self.dbm.add_topic(subject_name, topic_name)

                # Always add "ALL" topic
                self.dbm.add_topic(subject_name, "ALL")

        print("\nSetup complete!")


if __name__ == "__main__":
    svr = ServerManager()
    print("=== Main Menu ===")
    print("1. Run Server")
    print("2. Setup Database")
    choice = input("Select option: ").strip()

    if choice == "1":
        if not svr.dbm.check_exist():
            svr.dbm.create_tables()
        svr.server_listen()
    elif choice == "2":
        svr.setup_mode()
    else:
        print("Invalid choice, exiting.")
