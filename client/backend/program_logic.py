import socket
import json
import random
from client.backend.marking_system import MarkingSystem
from client.backend.user_database_handler import UserDatabaseManager

''' 
Name: ProgramLogic
Purpose: Contains all logic components of the main_program (backend of GUI)
'''
class ProgramLogic:
    '''
    Name: __init__
    Purpose: Constructor for quiz state and marking system.
    '''
    def __init__(self):
        self.marker = MarkingSystem()
        self.user_db = UserDatabaseManager()
        self.score = 0
        self.current_index = 0
        self.questions = []
        self.incorrect_questions = []
        self.user_answers = {}

        # Store metadata for current quiz
        self.current_quiz_metadata = {
            "qualification": "",
            "subject": "",
            "exam_board": "",
            "topic": ""
        }

        # Track if this is a weak area practice session
        self.is_weak_area_mode = False

    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 51000
    ''' 
    Name: configure_server
    Parameters: host: string , port: integer
    Returns: None
    Purpose: configures the ip and host address of the server user wishes to connect too
    '''
    @classmethod
    def configure_server(cls, host, port):
        cls.SERVER_HOST = host
        cls.SERVER_PORT = port

    ''' 
    Name: request_server_data
    Parameters: payload: dictionary
    Returns: response: json string
    Purpose: Connects to database server sending a payload containing a type of request and request details
    '''
    @classmethod
    def request_server_data(cls, payload):
        """Send request to server and return JSON response."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((cls.SERVER_HOST, cls.SERVER_PORT))
            s.send(json.dumps(payload).encode())
            response = s.recv(16384).decode()
            s.close()

            return json.loads(response)
        except Exception as e:
            print(f"Server communication error: {e}")
            return {"status": "error", "message": f"Connection error: {str(e)}"}

#Load Data logic
    ''' 
    Name: load_parameter_sets
    Parameters: None
    Returns: data_map, qualifications , exam_boards
    Purpose: Requests all available data on database server for later question generation.
    '''
    @classmethod
    def load_parameter_sets(cls):

        data_map = {}

        qualifications = cls.request_server_data({"type": "qualifications"})
        exam_boards = cls.request_server_data({"type": "exam_boards"})

        if not isinstance(qualifications, list) or not isinstance(exam_boards, list):
            return {}, [], []

        for q in qualifications:
            q_name = q["name"]
            q_id = q["id"]
            data_map[q_name] = {}

            subjects = cls.request_server_data({
                "type": "subjects",
                "qualification_id": q_id
            })

            if not isinstance(subjects, list):
                continue

            for s in subjects:
                subject_name = s["name"]
                e_id = s["exam_board_id"]
                e_name = next((e["name"] for e in exam_boards if e["id"] == e_id), "Unknown")

                topics = cls.request_server_data({
                    "type": "topics",
                    "qualification_id": q_id,
                    "subject_name": subject_name,
                    "exam_board_id": e_id
                })

                topic_list = [t["name"] for t in topics] if isinstance(topics, list) else []

                # Initialize exam board dict if not exists
                if subject_name not in data_map[q_name]:
                    data_map[q_name][subject_name] = {}

                data_map[q_name][subject_name][e_name] = topic_list

        return data_map, qualifications, exam_boards

    ''' 
    Name: load_existing_sets
    Parameters: None
    Returns: data_map
    Purpose: Requests server for data based upon if there is questions generated in the StudyQuiz table of the database
    '''
    @classmethod
    def load_existing_sets(cls):

        raw_data = cls.request_server_data({"type": "existing_sets"})
        data_map = {}

        if not isinstance(raw_data, list):
            return data_map

        for item in raw_data:
            q = item["qualification"]
            s = item["subject"]
            e = item["exam_board"]
            t = item["topic"]

            data_map.setdefault(q, {}).setdefault(s, {}).setdefault(e, [])

            if t not in data_map[q][s][e]:
                data_map[q][s][e].append(t)

        return data_map


    ''' 
    Name: fetch_existing_questions
    Parameters: qualification_name: string, subject_name: string , exam_board_name: string, topic_name: string , qualifications: list, exam_boards: list
    Returns: questions: dictionary
    Purpose: Fetch existing questions for a specific topic.
    '''
    @classmethod
    def fetch_existing_questions(cls, qualification_name, subject_name, exam_board_name, topic_name, qualifications, exam_boards):
        qualification_id = next(
            (q["id"] for q in qualifications if q["name"] == qualification_name),
            None
        )
        exam_board_id = next(
            (e["id"] for e in exam_boards if e["name"] == exam_board_name),
            None
        )

        if qualification_id is None or exam_board_id is None:
            return []

        topics = cls.request_server_data({
            "type": "topics",
            "qualification_id": qualification_id,
            "subject_name": subject_name,
            "exam_board_id": exam_board_id
        })

        topic_obj = next((t for t in topics if t["name"] == topic_name), None)
        if not topic_obj:
            return []

        resp = cls.request_server_data({
            "type": "get_questions",
            "topic_id": topic_obj["id"]
        })

        return resp.get("questions", [])
    ''' 
    Name: generate_and_fetch_questions
    Parameters: qualification_name: string, subject_name: string , exam_board_name: string, topic_name: string , qualifications: list, exam_boards: list , amount: integer
    Returns: questions: dictionary
    Purpose: Request server to generate new questions, then fetch them.
    '''
    @classmethod
    def generate_and_fetch_questions(cls, qualification_name, subject_name, exam_board_name, topic_name, qualifications,exam_boards, amount=25):
        payload = {
            "type": "generate_questions",
            "qualification": qualification_name,
            "subject": subject_name,
            "exam_board": exam_board_name,
            "topic": topic_name,
            "amount": amount
        }

        generation = cls.request_server_data(payload)

        if generation.get("status") != "success":
            print(f"Generation failed: {generation.get('message', 'Unknown error')}")
            return []

        # Now fetch the newly generated questions
        qualification_id = next(
            (q["id"] for q in qualifications if q["name"] == qualification_name),
            None
        )
        exam_board_id = next(
            (e["id"] for e in exam_boards if e["name"] == exam_board_name),
            None
        )

        if qualification_id is None or exam_board_id is None:
            return []

        topics = cls.request_server_data({
            "type": "topics",
            "qualification_id": qualification_id,
            "subject_name": subject_name,
            "exam_board_id": exam_board_id
        })

        topic_obj = next((t for t in topics if t["name"] == topic_name), None)
        if not topic_obj:
            return []

        resp = cls.request_server_data({
            "type": "get_questions",
            "topic_id": topic_obj["id"]
        })

        return resp.get("questions", [])

#User Database
    ''' 
    Name: initialize_user_database
    Parameters: None
    Returns: None
    Purpose: initialises the database manager 
    '''
    @classmethod
    def initialize_user_database(cls):
        user_db = UserDatabaseManager()
        user_db.create_tables()
    ''' 
    Name: load_weak_area_sets
    Parameters: None
    Returns: data_map: array
    Purpose: Load weak area sets from user database. 
    '''
    @classmethod
    def load_weak_area_sets(cls):
        user_db = UserDatabaseManager()
        raw_data = user_db.get_weak_area_sets()
        data_map = {}

        for item in raw_data:
            q = item["qualification"]
            s = item["subject"]
            e = item["exam_board"]
            t = item["topic"]

            data_map.setdefault(q, {}).setdefault(s, {}).setdefault(e, [])

            if t not in data_map[q][s][e]:
                data_map[q][s][e].append(t)

        return data_map
    ''' 
    Name: fetch_weak_area_questions
    Parameters: qualification_name:string, subject_name:string, exam_board_name:string, topic_name:string
    Returns: questions: dictionary
    Purpose: Load weak area sets from user database. 
    '''
    @classmethod
    def fetch_weak_area_questions(cls, qualification_name, subject_name, exam_board_name, topic_name):
        """
        Fetch weak area questions from user database.
        Returns: list of question dicts with id, question, answer, tally
        """
        user_db = UserDatabaseManager()

        # Get IDs from user database
        qualification_id = user_db.get_qualification_id(qualification_name)
        exam_board_id = user_db.get_exam_board_id(exam_board_name)

        if not qualification_id or not exam_board_id:
            return []

        # Get topic ID
        topics = user_db.get_topics_by_hierarchy(qualification_id, subject_name, exam_board_id)
        topic_obj = next((t for t in topics if t[1] == topic_name), None)

        if not topic_obj:
            return []

        topic_id = topic_obj[0]

        # Fetch questions
        rows = user_db.get_incorrect_questions_by_topic(topic_id)

        return [{
            "id": r[0],
            "question": r[1],
            "answer": r[2],
            "tally": r[3]
        } for r in rows]

#Quiz Logic
    ''' 
    Name: fetch_weak_area_questions
    Parameters: questions:array, qualification:string, subject:string, exam_board:string, topic:string
    Returns: None
    Purpose: Initialize a new quiz session with given questions and metadata.
    '''
    def start_quiz(self, questions, qualification="", subject="", exam_board="", topic="", is_weak_area=False):
        """"""
        self.questions = questions
        self.score = 0
        self.current_index = 0
        self.incorrect_questions = []
        self.user_answers = {}
        self.is_weak_area_mode = is_weak_area

        # Store metadata
        self.current_quiz_metadata = {
            "qualification": qualification,
            "subject": subject,
            "exam_board": exam_board,
            "topic": topic
        }

#Multiple Choice Logic
    ''' 
    Name: current_question
    Parameters: None
    Returns: None , questions:string
    Purpose: Get the current question or None if quiz is complete.
    '''
    def current_question(self):
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None
    ''' 
    Name: has_next
    Parameters: None
    Returns: True or False:Boolean
    Purpose: Check if there are more questions.
    '''
    def has_next(self):
        return self.current_index < len(self.questions)
    ''' 
    Name: next_question
    Parameters: None
    Returns: None
    Purpose: Move to the next question.
    '''
    def next_question(self):
        self.current_index += 1
    ''' 
    Name: generate_mc_options
    Parameters: None
    Returns: options:array
    Purpose: Generate multiple choice options for current question.
    '''
    def generate_mc_options(self):
        current = self.current_question()
        if not current:
            return []

        correct = current["answer"]

        # Get wrong answers from other questions
        others = [q["answer"] for q in self.questions if q != current]

        # Sample up to 3 wrong answers
        num_wrong = min(3, len(others))
        wrong = random.sample(others, num_wrong) if num_wrong > 0 else []

        # Combine and shuffle
        options = wrong + [correct]
        random.shuffle(options)

        return options
    ''' 
    Name: submit_mc_answer
    Parameters: selected_answer
    Returns: None
    Purpose: Check multiple choice answer, update score, and advance.
    '''
    def submit_mc_answer(self, selected_answer):
        current = self.current_question()
        if not current:
            return

        if selected_answer == current["answer"]:
            self.score += 1
        else:
            self.incorrect_questions.append(current)

        self.next_question()

#Typed Answer Logic
    ''' 
    Name: save_typed_answer
    Parameters: question_id: int , text:string
    Returns: None
    Purpose: Store user's typed answer for later marking.
    '''
    def save_typed_answer(self, question_id, text):
        self.user_answers[question_id] = text
    ''' 
    Name: mark_typed_answer
    Parameters: None
    Returns: None
    Purpose: Mark all typed answers using the marking system.Updates score and incorrect_questions.
    '''
    def mark_typed_answers(self):
        self.score = 0
        self.incorrect_questions = []

        for q in self.questions:
            user_text = self.user_answers.get(q["id"], "")
            correct_answer = q["answer"]

            # Use marking system to check similarity
            is_correct = self.marker.marker(user_text, correct_answer)

            if is_correct:
                self.score += 1
            else:
                self.incorrect_questions.append(q)

#Results and database updates
    ''' 
    Name: get_results
    Parameters: None
    Returns: dictionary of score total and incorrect_questions.
    Purpose: Calculate and return quiz results. Also updates user database with incorrect questions
    '''
    def get_results(self):

        if self.user_answers:
            self.mark_typed_answers()

        if self.score < len(self.questions):
            self._update_user_database()

        return {
            "score": self.score,
            "total": len(self.questions),
            "incorrect_questions": self.incorrect_questions
        }
    ''' 
    Name: update_user_database
    Parameters: None
    Returns: None
    Purpose: Update user database with incorrect questions. (Normal Mode) , removes correct questions and updates tally for incorrect (Weak Area Mode)
    '''
    def _update_user_database(self):

        if self.is_weak_area_mode:
            correct_question_ids = [q["id"] for q in self.questions if q not in self.incorrect_questions]
            for qid in correct_question_ids:
                self.user_db.remove_correct_question(qid)

            topic_id = self._ensure_user_db_hierarchy()
            if topic_id:
                for q in self.incorrect_questions:
                    self.user_db.add_incorrect_question(
                        q["id"],
                        topic_id,
                        q["question"],
                        q["answer"]
                    )
        else:
            topic_id = self._ensure_user_db_hierarchy()
            if topic_id:
                for q in self.incorrect_questions:
                    self.user_db.add_incorrect_question(
                        q["id"],
                        topic_id,
                        q["question"],
                        q["answer"]
                    )
    ''' 
    Name: _ensure_user_db_hierarchy
    Parameters: None
    Returns: None
    Purpose: Ensure database heirarchy matches that of servers database.
    '''
    def _ensure_user_db_hierarchy(self):
        return self.user_db.ensure_hierarchy_exists(
            self.current_quiz_metadata["qualification"],
            self.current_quiz_metadata["subject"],
            self.current_quiz_metadata["exam_board"],
            self.current_quiz_metadata["topic"]
        )

