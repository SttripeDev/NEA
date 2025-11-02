import json
import socket
import threading
from database_handler import DatabaseManager
from ai_handler import TopicGenerator, QuestionGeneration


class ServerManager:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 51000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.dbm = DatabaseManager()
        self.topic_gen = TopicGenerator()
        self.q_gen = QuestionGeneration()

    # Dropdown menu requests
    def handle_dropdown_request(self, request):
        rtype = request.get("type")
        if rtype == "qualifications":
            data = self.dbm.get_qualifications()
            return json.dumps([{"id": q[0], "name": q[1]} for q in data])
        elif rtype == "exam_boards":
            data = self.dbm.get_exam_boards()
            return json.dumps([{"id": e[0], "name": e[1]} for e in data])
        elif rtype == "subjects":
            qid = request.get("qualification_id")
            all_subjects = self.dbm.get_subjects()
            filtered = [s for s in all_subjects if s[1] == qid]
            return json.dumps([{"id": s[0], "name": s[3], "exam_board_id": s[2]} for s in filtered])
        elif rtype == "topics":
            qid = request.get("qualification_id")
            sname = request.get("subject_name")
            bid = request.get("exam_board_id")
            data = self.dbm.get_topics_by_hierarchy(qid, sname, bid)
            return json.dumps([{"id": t[0], "name": t[1]} for t in data])
        else:
            return json.dumps([])

    # Question Generation
    def handle_generate_questions(self, request):
        qualification = request.get("qualification")
        subject = request.get("subject")
        exam_board = request.get("exam_board")
        topic = request.get("topic")
        amount = request.get("amount", 25)

        qualification_id = next((q[0] for q in self.dbm.get_qualifications() if q[1] == qualification), None)
        if qualification_id is None:
            return json.dumps({"status": "error", "message": "Qualification not found"})

        subjects = [s for s in self.dbm.get_subjects() if s[1] == qualification_id and s[3] == subject]
        if not subjects:
            return json.dumps({"status": "error", "message": "Subject not found"})
        subject_id = subjects[0][0]

        exam_boards = [e for e in self.dbm.get_exam_boards() if e[1] == exam_board]
        if not exam_boards:
            return json.dumps({"status": "error", "message": "Exam board not found"})
        exam_board_id = exam_boards[0][0]

        topics = [t for t in self.dbm.get_topics_by_hierarchy(qualification_id, subject, exam_board_id) if t[1] == topic]
        if not topics:
            return json.dumps({"status": "error", "message": "Topic not found"})
        topic_id = topics[0][0]

        raw_output = self.q_gen.generator([subject, qualification, exam_board, topic, amount])

        if isinstance(raw_output, str):
            lines = raw_output.splitlines()
        elif isinstance(raw_output, list):
            lines = [json.dumps(item) for item in raw_output]
        else:
            return json.dumps({"status": "error", "message": "Unexpected output from question generator"})

        for line in lines:
            if "=" in line:
                _, json_part = line.split("=", 1)
            else:
                json_part = line
            try:
                question_obj = json.loads(json_part.strip())
                self.dbm.add_question(
                    topic_id,
                    question_obj.get("Question", ""),
                    question_obj.get("Answer", "")
                )
            except Exception as e:
                print(f"Error parsing line: {line}, {e}")

        return json.dumps({"status": "success", "message": f"{amount} questions added to database"})

    def handle_get_questions(self, request):
        topic_id = request.get("topic_id")
        if not topic_id:
            return json.dumps({"status": "error", "message": "Missing topic_id"})

        try:
            rows = self.dbm.get_questions_by_topic(topic_id)
            questions = [{"id": r[0], "question": r[1], "answer": r[2]} for r in rows]
            return json.dumps({"status": "success", "questions": questions})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def handle_existing_sets(self, request):
        sets = self.dbm.get_existing_sets()
        return json.dumps(sets)

    def handle_client(self, connection, address):
        print(f"New connection from {address}")
        try:
            while True:
                data = connection.recv(16384)
                if not data:
                    break

                try:
                    request_json = json.loads(data.decode("utf-8"))
                except json.JSONDecodeError:
                    connection.send(json.dumps({"status": "error", "message": "Invalid JSON"}).encode())
                    continue

                request_type = request_json.get("type")
                if request_type in ["qualifications", "exam_boards", "subjects", "topics"]:
                    result = self.handle_dropdown_request(request_json)
                elif request_type == "generate_questions":
                    request_type = self.handle_generate_questions(request_json)
                elif request_type == "get_questions":
                    result = self.handle_get_questions(request_json)
                elif request_type == "existing_sets":
                    result = self.handle_existing_sets(request_json)
                else:
                    result = json.dumps({"status": "error", "message": "Unknown request type"})

                connection.send(result.encode())

        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            connection.close()
            print(f"Connection with {address} closed.")

    def server_listen(self):
        print(f"Server is listening on {self.host}:{self.port}")

        self.s.listen(5)

        while True:
            connection, address = self.s.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(connection, address))
            client_thread.daemon = True  # allows clean shutdown
            client_thread.start()
            print(f"Active connections: {threading.active_count() - 1}")

    # Setup Mode
    def setup_mode(self):
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

        # Subjects and Topics
        print("\nNow entering Subjects (type 'exit' to finish):")
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
            if confirm != "Y":
                continue

            self.dbm.add_subject(qualification_id, exam_board_id, subject_name)
            subject_id = self.dbm.get_subject_id(subject_name, qualification_id, exam_board_id)
            if subject_id is None:
                print("Error retrieving SubjectID, skipping topic creation.")
                continue

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
                            self.dbm.add_topic(subject_id, t)
                except Exception as e:
                    print(f"ChatGPT topic generation failed: {e}")
            else:
                print("\nEnter Topics for this Subject (type 'exit' to finish):")
                while True:
                    topic_name = input("Topic: ").strip().upper()
                    if topic_name == "EXIT":
                        break
                    self.dbm.add_topic(subject_id, topic_name)

            self.dbm.add_topic(subject_id, "ALL")


if __name__ == "__main__":
    svr = ServerManager()
    print("Main Menu:\n")
    print("1. Run Server")
    print("2. Setup Database\n")
    choice = input("Select option: ").strip()

    if choice == "1":
        if not svr.dbm.check_exist():
            svr.dbm.create_tables()
        svr.server_listen()
    elif choice == "2":
        svr.setup_mode()
    else:
        print("Invalid choice, exiting.")
