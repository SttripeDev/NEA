import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog , messagebox
import socket
import json
import random
from marking_system import MarkingSystem

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 51000


root = tk.Tk()
root.withdraw()
server_ip = simpledialog.askstring(
    "Server IP",
    "Enter the Server IP (leave blank for localhost 127.0.0.1):"
)
SERVER_HOST = server_ip.strip() if server_ip and server_ip.strip() else "127.0.0.1"
SERVER_PORT = 51000
root.destroy()

def request_server_data(payload):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))
    s.send(json.dumps(payload).encode())
    response = s.recv(16384).decode()  # bigger buffer for large responses
    s.close()
    try:
        return json.loads(response)
    except Exception:
        return {"status": "error", "message": "Invalid JSON from server"}


def load_data_map():

    data_map = {}
    qualifications = request_server_data({"type": "qualifications"})
    exam_boards = request_server_data({"type": "exam_boards"})

    # if server returned an error, return empty structures
    if not isinstance(qualifications, list) or not isinstance(exam_boards, list):
        return {}, qualifications if isinstance(qualifications, list) else [], exam_boards if isinstance(exam_boards, list) else []

    for q in qualifications:
        q_name = q["name"]
        q_id = q["id"]
        data_map[q_name] = {}

        subjects = request_server_data({"type": "subjects", "qualification_id": q_id})
        if not isinstance(subjects, list):
            continue
        for s in subjects:
            s_name = s["name"]
            e_id = s["exam_board_id"]
            e_name = next((e["name"] for e in exam_boards if e["id"] == e_id), "Unknown")

            topics = request_server_data({
                "type": "topics",
                "qualification_id": q_id,
                "subject_name": s_name,
                "exam_board_id": e_id
            })
            topic_list = [t["name"] for t in topics] if isinstance(topics, list) else []
            # store as nested mapping exam_board_name -> topic_list
            data_map[q_name][s_name] = {e_name: topic_list}

    return data_map, qualifications, exam_boards


def load_existing_sets():

    raw_data = request_server_data({"type": "existing_sets"})
    data_map = {}

    if isinstance(raw_data, list):
        for item in raw_data:
            q_name = item["qualification"]
            s_name = item["subject"]
            e_name = item["exam_board"]
            t_name = item["topic"]

            if q_name not in data_map:
                data_map[q_name] = {}
            if s_name not in data_map[q_name]:
                data_map[q_name][s_name] = {}
            if e_name not in data_map[q_name][s_name]:
                data_map[q_name][s_name][e_name] = []

            if t_name not in data_map[q_name][s_name][e_name]:
                data_map[q_name][s_name][e_name].append(t_name)
    else:
        print("Error: server returned invalid existing_sets data:", raw_data)

    return data_map


class StudyQuiz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Study Quiz")

        self.button_font = ("Segoe UI", 14, "bold")
        self.button_font_small = ("Segoe UI",10 ,"bold")
        self.title_font = ("Segoe UI", 24, "bold")
        self.big_text_font = ("Segoe UI", 56, "bold")
        self.box_font_title = ("Segoe UI", 10, "bold")
        self.box_font = ("Segoe UI", 10)
        self.current_frame = None


        try:
            self.data_map, self.qualifications, self.exam_boards = load_data_map()
        except Exception:
            self.data_map, self.qualifications, self.exam_boards = {}, [], []

        self.main_menu()

    def clear_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    # Main Menu and Selection
    def main_menu(self):
        self.clear_current_frame()
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        tk.Label(frame, text="Study Quiz", font=self.big_text_font, fg="black", bg="white") \
            .place(relx=0.5, rely=0.3, anchor="center")

        tk.Button(frame, text="Create New Questions", font=self.button_font,
                  width=20, height=2, command=lambda: self.goto_selection(1)) \
            .place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(frame , text ="Existing Question Sets",font=self.button_font,width=20,height=2,command=lambda: self.goto_selection(2)) \
            .place(relx=0.5, rely=0.7, anchor="center")

    def goto_selection(self, choice):
        self.clear_current_frame()
        if choice == 1:
            self.selection_screen(1)
        elif choice == 2:
            self.selection_screen(2)

    def selection_screen(self, choice):
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        title_text = "Question Generation" if choice == 1 else "Existing Question Sets"
        tk.Label(frame, text=title_text, font=self.title_font, fg="black", bg="white") \
            .place(relx=0.5, rely=0.2, anchor="center")

        qualification_var = tk.StringVar(value="Qualification")
        subject_var = tk.StringVar(value="Subject")
        examboard_var = tk.StringVar(value="Exam Board")
        topic_var = tk.StringVar(value="Topic")

        qualification_combobox = ttk.Combobox(frame, textvariable=qualification_var, state="readonly")
        subject_combobox = ttk.Combobox(frame, textvariable=subject_var, state="disabled")
        examboard_combobox = ttk.Combobox(frame, textvariable=examboard_var, state="disabled")
        topic_combobox = ttk.Combobox(frame, textvariable=topic_var, state="disabled")

        qualification_combobox.place(relx=0.2, rely=0.5, anchor="center")
        subject_combobox.place(relx=0.5, rely=0.5, anchor="center")
        examboard_combobox.place(relx=0.8, rely=0.5, anchor="center")
        topic_combobox.place(relx=0.5, rely=0.6, anchor="center")

        confirm_button = tk.Button(frame, text="Confirm", font=self.button_font, state="disabled")
        confirm_button.place(relx=0.5, rely=0.75, anchor="center")

        # Load Data based on choice
        if choice == 1:
            self.data_map, _, _ = load_data_map()
        else:
            self.data_map = load_existing_sets()

        qualification_combobox["values"] = list(self.data_map.keys())

        # Helpers
        def update_confirm_state(event=None):
            if all(var.get() not in ["Qualification", "Subject", "Exam Board", "Topic"]
                   for var in [qualification_var, subject_var, examboard_var, topic_var]):
                confirm_button.config(state="normal")
            else:
                confirm_button.config(state="disabled")

        def qualification_selected(event):
            q_name = qualification_var.get()
            subjects = list(self.data_map.get(q_name, {}).keys())
            subject_combobox["values"] = subjects
            subject_combobox.state(["!disabled"])
            subject_var.set("Subject")

            examboard_combobox.set("Exam Board")
            examboard_combobox.state(["disabled"])
            topic_combobox.set("Topic")
            topic_combobox.state(["disabled"])
            update_confirm_state()

        def subject_selected(event):
            q_name = qualification_var.get()
            s_name = subject_var.get()
            examboards = list(self.data_map.get(q_name, {}).get(s_name, {}).keys())
            examboard_combobox["values"] = examboards
            examboard_combobox.state(["!disabled"])
            examboard_var.set("Exam Board")

            topic_combobox.set("Topic")
            topic_combobox.state(["disabled"])
            update_confirm_state()

        def examboard_selected(event):
            q_name = qualification_var.get()
            s_name = subject_var.get()
            e_name = examboard_var.get()
            topics = self.data_map.get(q_name, {}).get(s_name, {}).get(e_name, [])
            topic_combobox["values"] = topics
            topic_combobox.state(["!disabled"])
            topic_var.set("Topic")
            update_confirm_state()

        # Confirm Button stuff
        def confirm_selection():
            q_name = qualification_var.get()
            s_name = subject_var.get()
            e_name = examboard_var.get()
            t_name = topic_var.get()

            if choice == 1:

                payload = {
                    "type": "generate_questions",
                    "qualification": q_name,
                    "subject": s_name,
                    "exam_board": e_name,
                    "topic": t_name,
                    "amount": 25
                }
                self.question_gen_screen(payload)
            else:

                qualification_id = next((q["id"] for q in (self.qualifications or []) if q["name"] == q_name), None)
                exam_board_id = next((e["id"] for e in (self.exam_boards or []) if e["name"] == e_name), None)
                if qualification_id is None or exam_board_id is None:
                    tk.messagebox.showerror("Error", "Could not find IDs for selection")
                    return


                topics_resp = request_server_data({
                    "type": "topics",
                    "qualification_id": qualification_id,
                    "subject_name": s_name,
                    "exam_board_id": exam_board_id
                })
                topic_obj = next((t for t in topics_resp if t["name"] == t_name), None) if isinstance(topics_resp,
                                                                                                      list) else None
                topic_id = topic_obj["id"] if topic_obj else None

                if topic_id is None:
                    tk.messagebox.showerror("Error", "Topic not found")
                    return


                questions_resp = request_server_data({
                    "type": "get_questions",
                    "topic_id": topic_id
                })
                if questions_resp.get("status") == "success":
                    questions = questions_resp.get("questions", [])
                    if questions:
                        self.question_select_screen(questions)
                    else:
                        tk.messagebox.showinfo("Info", "No questions available in this set")
                else:
                    tk.messagebox.showerror("Error", questions_resp.get("message", "Unknown error"))

        # Bindings
        qualification_combobox.bind("<<ComboboxSelected>>", qualification_selected)
        subject_combobox.bind("<<ComboboxSelected>>", subject_selected)
        examboard_combobox.bind("<<ComboboxSelected>>", examboard_selected)
        topic_combobox.bind("<<ComboboxSelected>>", update_confirm_state)

        confirm_button.config(command=confirm_selection)

    # Generating Loading Screen
    def question_gen_screen(self, payload):

        self.clear_current_frame()

        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        tk.Label(frame, text="Generating Questions", font=self.title_font, fg="black", bg="white") \
            .place(relx=0.5, rely=0.45, anchor="center")
        status_label = tk.Label(frame, text="Please wait...", font=self.button_font, fg="black", bg="white")
        status_label.place(relx=0.5, rely=0.55, anchor="center")

        # Forces Tkinter to update before server request (socket causes a pause)
        self.update_idletasks()


        response = request_server_data(payload)

        if response.get("status") == "success":
            status_label.config(text="Question Generation Successful...")

            qualification_name = payload.get("qualification")
            exam_board_name = payload.get("exam_board")
            subject_name = payload.get("subject")
            topic_name = payload.get("topic")

            qualification_id = next((q["id"] for q in (self.qualifications or []) if q["name"] == qualification_name), None)
            exam_board_id = next((e["id"] for e in (self.exam_boards or []) if e["name"] == exam_board_name), None)

            questions = []
            if qualification_id is not None and exam_board_id is not None:

                topics_resp = request_server_data({
                    "type": "topics",
                    "qualification_id": qualification_id,
                    "subject_name": subject_name,
                    "exam_board_id": exam_board_id
                })

                if isinstance(topics_resp, list):
                    topic_obj = next((t for t in topics_resp if t["name"] == topic_name), None)
                    topic_id = topic_obj["id"] if topic_obj else None
                elif isinstance(topics_resp, dict) and topics_resp.get("status") == "success":

                    topics_list = topics_resp.get("topics", [])
                    topic_obj = next((t for t in topics_list if t["name"] == topic_name), None)
                    topic_id = topic_obj["id"] if topic_obj else None
                else:
                    topic_id = None

                if topic_id is not None:
                    q_response = request_server_data({
                        "type": "get_questions",
                        "topic_id": topic_id
                    })
                    if q_response.get("status") == "success" and isinstance(q_response.get("questions"), list):
                        questions = q_response["questions"]
                    else:

                        questions = []
                else:
                    questions = []
            else:
                questions = []

            if questions:

                self.after(10000, lambda: self.question_select_screen(questions))

                continue_button = tk.Button(
                    frame, text="Continue", font=self.button_font, state="normal",
                    command=lambda: self.question_select_screen(questions)
                )
                continue_button.place(relx=0.5, rely=0.8, anchor="center")
            else:
                tk.Label(frame, text="No questions returned from server.", font=self.button_font, fg="red", bg="white") \
                    .place(relx=0.5, rely=0.65, anchor="center")
                tk.Button(frame, text="Back", font=self.button_font, command=self.selection_screen) \
                    .place(relx=0.5, rely=0.8, anchor="center")

        else:
            status_label.config(text="Question Generation Failed...")
            tk.Label(frame, text=response.get("message", "Generation error"), font=self.button_font, fg="red", bg="white") \
                .place(relx=0.5, rely=0.65, anchor="center")
            tk.Button(frame, text="Retry", font=self.button_font, state="normal", command=self.selection_screen) \
                .place(relx=0.5, rely=0.8, anchor="center")

    # Question Selection and Question Type
    def question_select_screen(self, questions):

        self.clear_current_frame()

        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        # Srollable Question List
        canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
        scroll_frame = tk.Frame(canvas, bg="white")

        canvas.pack(side="top", fill="both", expand=True, padx=50, pady=(20, 80))
        canvas.create_window((0, 0), window=scroll_frame, anchor="n")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", on_frame_configure)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Format for boxes
        self.question_vars = {}

        for q in questions:
            qid = q["id"]
            qtext = q["question"]
            atext = q["answer"]

            var = tk.BooleanVar(value=True)
            self.question_vars[qid] = var

            box = tk.LabelFrame(scroll_frame, text=f"Question {qid}", bg="white", padx=10, pady=5,font=self.box_font_title)
            box.pack(fill="x", pady=5)

            tk.Label(box, text=f"Q: {qtext}", anchor="w", justify="left", bg="white", wraplength=600,font=self.box_font) \
                .pack(fill="x")
            tk.Label(box, text=f"A: {atext}", anchor="w", justify="left", bg="white", fg="gray", wraplength=600,font=self.box_font) \
                .pack(fill="x")

            tk.Checkbutton(box, text="Include", variable=var, bg="white").pack(anchor="w")

        # Buttons at the bottom of screen
        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(side="bottom", fill="x", pady=20)

        def toggle_all(select=True):
            for var in self.question_vars.values():
                var.set(select)

        tk.Button(button_frame, text="Select All", font=self.button_font,
                  command=lambda: toggle_all(True)).pack(side="left", padx=40)

        tk.Button(button_frame, text="Deselect All", font=self.button_font,
                  command=lambda: toggle_all(False)).pack(side="left", padx=40)

        def confirm_selection():
            selected = [qid for qid, var in self.question_vars.items() if var.get()]
            chosen_questions = [q for q in questions if q["id"] in selected]
            print("Selected questions for quiz:", chosen_questions)
            self.question_type_selection(chosen_questions)

        tk.Button(button_frame, text="Confirm", font=self.button_font,
                  command=confirm_selection).pack(side="right", padx=40)


    def question_type_selection(self,chosen_questions):
        self.clear_current_frame()

        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        question_type_text = tk.Label(frame, text="Question Type", font=self.big_text_font) \
            .place(relx=0.5, rely=0.3, anchor="center")

        multiple_choice_button = tk.Button(frame, text="Multiple Choice", font=self.button_font,
                                    command=lambda: self.multiple_choice(chosen_questions)) \
            .place(relx=0.3, rely=0.7, anchor="center")

        typed_answer_button = tk.Button(frame, text="Typed Answer", font=self.button_font,
                                 command=lambda: self.typed_answer(chosen_questions)) \
            .place(relx=0.7, rely=0.7, anchor="center")

    # Actual Quiz

    def multiple_choice(self, chosen_questions):

        self.score = 0
        self.incorrect_questions = []
        self.current_question_index = 0
        self.chosen_questions = chosen_questions
        self.show_multiple_choice_question()

    def show_multiple_choice_question(self):

        self.clear_current_frame()
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        current_question = self.chosen_questions[self.current_question_index]
        question_text = current_question["question"]
        correct_answer = current_question["answer"]


        tk.Label(frame,text=f"Question {self.current_question_index+1}/{len(self.chosen_questions)}",font=self.title_font,bg="white") \
            .pack(pady=(20, 10))


        tk.Label(frame,text=question_text,font=self.button_font,wraplength=600,bg="white") \
            .pack(pady=(10, 30))


        other_answers = [question["answer"] for question in self.chosen_questions if question != current_question]
        wrong_answers = random.sample(other_answers, min(3, len(other_answers)))
        all_answers = wrong_answers + [correct_answer]
        random.shuffle(all_answers)

        def handle_answer_selection(selected_answer):
            if selected_answer == correct_answer:
                self.score += 1
            else:
                self.incorrect_questions.append(current_question)

            self.current_question_index += 1
            if self.current_question_index < len(self.chosen_questions):
                self.show_multiple_choice_question()
            else:
                self.results()


        for answer_option in all_answers:
            tk.Button(
                frame,
                text=answer_option,
                font=self.button_font,
                command=lambda selected=answer_option: handle_answer_selection(selected)
            ).pack(pady=10)

    def typed_answer(self, chosen_questions):
        self.user_answers = {}
        self.current_question_index = 0
        self.chosen_questions = chosen_questions
        self.show_typed_question()

    def show_typed_question(self):
        self.clear_current_frame()
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        current_question = self.chosen_questions[self.current_question_index]
        question_text = current_question["question"]

        tk.Label(frame,text=f"Question {self.current_question_index + 1}/{len(self.chosen_questions)}",font=self.title_font,bg="white") \
            .place(relx=0.5, rely=0.2, anchor="center")

        tk.Label(frame,text=question_text,font=self.button_font,wraplength=600,bg="white") \
            .place(relx=0.5, rely=0.3, anchor="center")

        answer_box = tk.Text(frame, width=50, height=10, wrap="word", font=("Segoe UI", 12))
        answer_box.place(relx=0.5, rely=0.5, anchor="center")

        def save_and_next():
            self.user_answers[current_question["id"]] = answer_box.get("1.0", tk.END).strip()
            self.current_question_index += 1

            if self.current_question_index < len(self.chosen_questions):
                self.show_typed_question()
            else:
                self.results_typed()

        tk.Button(frame, text="Confirm", font=self.button_font, command=save_and_next) \
            .place(relx=0.5, rely=0.7, anchor="center")

    def results_typed(self):
        marker = MarkingSystem()

        self.score = 0
        self.incorrect_questions = []

        for question in self.chosen_questions:
            user_answer = self.user_answers.get(question["id"], "")
            correct_answer = question["answer"]

            if marker.marker(user_answer, correct_answer):
                self.score += 1
            else:
                self.incorrect_questions.append(question)

        self.results()

    def results(self):

        self.clear_current_frame()
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame


        tk.Label(frame, text="Results", font=self.big_text_font, bg="white").pack(pady=20)

        tk.Label(
            frame,
            text=f"Score: {self.score}/{len(self.chosen_questions)}",
            font=self.title_font,
            bg="white"
        ).pack(pady=10)

        if self.incorrect_questions:
            tk.Label(frame, text="You got these wrong:", font=self.button_font, bg="white").pack(pady=10)

            scroll_canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
            scroll_frame = tk.Frame(scroll_canvas, bg="white")
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=scroll_canvas.yview)
            scroll_canvas.configure(yscrollcommand=scrollbar.set)

            scroll_canvas.pack(side="left", fill="both", expand=True, padx=50, pady=10)
            scrollbar.pack(side="right", fill="y")
            scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

            def on_frame_configure(event):
                scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

            scroll_frame.bind("<Configure>", on_frame_configure)

            for incorrect in self.incorrect_questions:
                q_text = incorrect["question"]
                a_text = incorrect["answer"]
                tk.Label(scroll_frame,text=f"Q: {q_text}\nA: {a_text}",font=self.box_font,wraplength=600,justify="left",bg="white",anchor="w")\
                    .pack(fill="x", pady=5)

        # Buttons at the bottom
        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(side="bottom", pady=30)

        tk.Button(button_frame, text="Retry Incorrect", font=self.button_font_small,
                  command=lambda: self.question_type_selection(self.incorrect_questions)).pack(side="left", padx=20)

        tk.Button(button_frame, text="Back to Menu", font=self.button_font_small,
                  command=self.main_menu).pack(side="left", padx=20)


if __name__ == "__main__":
    app = StudyQuiz()
    app.mainloop()
