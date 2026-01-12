import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from client.backend.program_logic import ProgramLogic
from client.backend.piechart_logic import PieChart

''' 
Name: ip_prompt 
Parameters: None
Returns: None 
Purpose: Allows User to input IP for database server 
'''
def ip_prompt():
    root = tk.Tk()
    root.withdraw()
    server_ip = simpledialog.askstring(
        "Server IP",
        "Enter the Server IP (leave blank for localhost 127.0.0.1):"
    )
    SERVER_HOST = server_ip.strip() if server_ip and server_ip.strip() else "127.0.0.1"
    SERVER_PORT = 51000
    root.destroy()
    
    ProgramLogic.configure_server(SERVER_HOST, SERVER_PORT)
    
    ProgramLogic.initialize_user_database()


#StudyQuiz Logic
''' 
Name: StudyQuiz 
Purpose: Contains the Tkinter based GUI 
'''
class StudyQuiz(tk.Tk):
    '''
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Constructor to set initial values of the StudyQuiz gui
    '''
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Study Quiz")

        # Fonts
        self.button_font = ("Segoe UI", 14, "bold")
        self.button_font_small = ("Segoe UI", 10, "bold")
        self.title_font = ("Segoe UI", 24, "bold")
        self.big_text_font = ("Segoe UI", 56, "bold")
        self.box_font_title = ("Segoe UI", 10, "bold")
        self.box_font = ("Segoe UI", 10)

        self.current_frame = None
        self.logic = ProgramLogic()


        self.data_set = {}
        self.qualifications = []
        self.exam_boards = []

        self.current_selection = {
            "qualification": "",
            "subject": "",
            "exam_board": "",
            "topic": ""
        }

        self.main_menu()

#Clear Frame stuff
    '''
    Name: clear_current_frame
    Parameters: None
    Returns: None
    Purpose: Utility to clear frame of current content
    '''
    def clear_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

#Main Menu
    '''
    Name: main_menu
    Parameters: None
    Returns: None
    Purpose: main menu of program allows user to select what they want to do
    '''
    def main_menu(self):
        self.clear_current_frame()
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        tk.Label(frame, text="Study Quiz", font=self.big_text_font, bg="white") \
            .place(relx=0.5, rely=0.2, anchor="center")

        tk.Button(frame, text="Create New Questions", font=self.button_font,
                  width=20, height=2, command=lambda: self.go_to_selection(1)) \
            .place(relx=0.5, rely=0.45, anchor="center")

        tk.Button(frame, text="Existing Question Sets", font=self.button_font,
                  width=20, height=2, command=lambda: self.go_to_selection(2)) \
            .place(relx=0.5, rely=0.65, anchor="center")

        tk.Button(frame, text="Practice Weak Areas", font=self.button_font,
                  width=20, height=2, command=lambda: self.go_to_selection(3)) \
            .place(relx=0.5, rely=0.85, anchor="center")
    '''
    Name: go_to_selection
    Parameters: choice: integer
    Returns: None
    Purpose: Based on user input redirects to specific menu
    '''
    def go_to_selection(self, choice):
        self.clear_current_frame()
        if choice == 3:
            self.weak_area_selection()
        else:
            self.selection_screen(choice)

#Weak Area Selection
    '''
    Name: weak_area_selection
    Parameters: None
    Returns: None
    Purpose: Menu for selecting Questions within specific parameters that user has previously failed on
    '''
    def weak_area_selection(self):
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        tk.Label(frame, text="Practice Weak Areas", font=self.title_font, bg="white") \
            .place(relx=0.5, rely=0.2, anchor="center")


        self.data_set = self.logic.load_weak_area_sets()

        if not self.data_set:
            tk.Label(frame, text="No weak areas found!\nComplete some quizzes first.",
                     font=self.button_font, bg="white", justify="center") \
                .place(relx=0.5, rely=0.5, anchor="center")

            tk.Button(frame, text="Back to Menu", font=self.button_font,
                      command=self.main_menu) \
                .place(relx=0.5, rely=0.7, anchor="center")
            return

        # Create dropdown menus
        qualification_variable = tk.StringVar(value="Qualification")
        subject_variable = tk.StringVar(value="Subject")
        examboard_variable = tk.StringVar(value="Exam Board")
        topic_variable = tk.StringVar(value="Topic")

        qualification_combobox = ttk.Combobox(frame, textvariable=qualification_variable, state="readonly")
        subject_combobox = ttk.Combobox(frame, textvariable=subject_variable, state="disabled")
        examboard_combobox = ttk.Combobox(frame, textvariable=examboard_variable, state="disabled")
        topic_combobox = ttk.Combobox(frame, textvariable=topic_variable, state="disabled")

        qualification_combobox.place(relx=0.2, rely=0.5, anchor="center")
        subject_combobox.place(relx=0.5, rely=0.5, anchor="center")
        examboard_combobox.place(relx=0.8, rely=0.5, anchor="center")
        topic_combobox.place(relx=0.5, rely=0.6, anchor="center")

        confirm_button = tk.Button(frame, text="Confirm", font=self.button_font, state="disabled")
        confirm_button.place(relx=0.5, rely=0.75, anchor="center")

        qualification_combobox["values"] = list(self.data_set.keys())

        '''
        Name: update_confirm_state
        Parameters: None
        Returns: None
        Purpose: Checks dropdown menu content and updates to normal if they are completed
        '''
        def update_confirm_state(event=None):
            if all(v.get() not in ["Qualification", "Subject", "Exam Board", "Topic"]
                   for v in [qualification_variable, subject_variable, examboard_variable, topic_variable]):
                confirm_button.config(state="normal")
            else:
                confirm_button.config(state="disabled")
        '''
        Name: qualification_selected
        Parameters: None
        Returns: None
        Purpose: Enables Subject Dropdown menu
        '''
        def qualification_selected(event):
            subjects = list(self.data_set.get(qualification_variable.get(), {}).keys())
            subject_combobox["values"] = subjects
            subject_combobox.state(["!disabled"])
            subject_variable.set("Subject")
        '''
        Name: subject_selected
        Parameters: None
        Returns: None
        Purpose: Enables ExamBoard Dropdown menu
        '''
        def subject_selected(event):
            examboards = list(
                self.data_set.get(qualification_variable.get(), {})
                .get(subject_variable.get(), {}).keys()
            )
            examboard_combobox["values"] = examboards
            examboard_combobox.state(["!disabled"])
            examboard_variable.set("Exam Board")
        '''
        Name: examboard_selected
        Parameters: None
        Returns: None
        Purpose: Enables Topic Dropdown menu
        '''
        def examboard_selected(event):
            topics = (
                self.data_set.get(qualification_variable.get(), {})
                .get(subject_variable.get(), {})
                .get(examboard_variable.get(), [])
            )
            topic_combobox["values"] = topics
            topic_combobox.state(["!disabled"])
            topic_variable.set("Topic")

        qualification_combobox.bind("<<ComboboxSelected>>", qualification_selected)
        subject_combobox.bind("<<ComboboxSelected>>", subject_selected)
        examboard_combobox.bind("<<ComboboxSelected>>", examboard_selected)
        topic_combobox.bind("<<ComboboxSelected>>", update_confirm_state)

        '''
        Name: confirm_selection
        Parameters: None
        Returns: None
        Purpose: confirms user selection and continues to question_select_screen
        '''
        def confirm_selection():
            q = qualification_variable.get()
            s = subject_variable.get()
            e = examboard_variable.get()
            t = topic_variable.get()

            # Store metadata
            self.current_selection = {
                "qualification": q,
                "subject": s,
                "exam_board": e,
                "topic": t
            }

            questions = self.logic.fetch_weak_area_questions(q, s, e, t)
            if questions:
                self.question_select_screen(questions, is_weak_area=True)
            else:
                messagebox.showinfo("Info", "No weak area questions found for this topic.")

        confirm_button.config(command=confirm_selection)

        # Back button
        tk.Button(frame, text="Back to Menu", font=self.button_font_small,
                  command=self.main_menu) \
            .place(relx=0.5, rely=0.9, anchor="center")

#Selection Screen
    '''
    Name: selection_screen
    Parameters: choice: integer
    Returns: None
    Purpose: Selection screen for Question Generation and Existing Question sets , allows users to pick what to quiz / generate
    '''
    def selection_screen(self, choice):
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        title_text = "Question Generation" if choice == 1 else "Existing Question Sets"
        tk.Label(frame, text=title_text, font=self.title_font, bg="white") \
            .place(relx=0.5, rely=0.2, anchor="center")

        qualification_variable = tk.StringVar(value="Qualification")
        subject_variable = tk.StringVar(value="Subject")
        examboard_variable = tk.StringVar(value="Exam Board")
        topic_variable = tk.StringVar(value="Topic")

        qualification_combobox = ttk.Combobox(frame, textvariable=qualification_variable, state="readonly")
        subject_combobox = ttk.Combobox(frame, textvariable=subject_variable, state="disabled")
        examboard_combobox = ttk.Combobox(frame, textvariable=examboard_variable, state="disabled")
        topic_combobox = ttk.Combobox(frame, textvariable=topic_variable, state="disabled")

        qualification_combobox.place(relx=0.2, rely=0.5, anchor="center")
        subject_combobox.place(relx=0.5, rely=0.5, anchor="center")
        examboard_combobox.place(relx=0.8, rely=0.5, anchor="center")
        topic_combobox.place(relx=0.5, rely=0.6, anchor="center")

        confirm_button = tk.Button(frame, text="Confirm", font=self.button_font, state="disabled")
        confirm_button.place(relx=0.5, rely=0.75, anchor="center")

        # Load datasets from logic layer
        if choice == 1:
            self.data_set, self.qualifications, self.exam_boards = self.logic.load_parameter_sets()
        else:
            self.data_set = self.logic.load_existing_sets()
            self.qualifications = self.logic.request_server_data({"type": "qualifications"})
            self.exam_boards = self.logic.request_server_data({"type": "exam_boards"})

        qualification_combobox["values"] = list(self.data_set.keys())

        '''
        Name: update_confirm_state
        Parameters: None
        Returns: None
        Purpose: Checks dropdown menu content and updates to normal if they are completed
        '''
        def update_confirm_state(event=None):
            if all(v.get() not in ["Qualification", "Subject", "Exam Board", "Topic"]
                   for v in [qualification_variable, subject_variable, examboard_variable, topic_variable]):
                confirm_button.config(state="normal")
            else:
                confirm_button.config(state="disabled")
        '''
        Name: qualification_selected
        Parameters: None
        Returns: None
        Purpose: Enables Subject Dropdown menu
        '''
        def qualification_selected(event):
            subjects = list(self.data_set.get(qualification_variable.get(), {}).keys())
            subject_combobox["values"] = subjects
            subject_combobox.state(["!disabled"])
            subject_variable.set("Subject")
        '''
        Name: subject_selected
        Parameters: None
        Returns: None
        Purpose: Enables ExamBoard Dropdown menu
        '''
        def subject_selected(event):
            examboards = list(
                self.data_set.get(qualification_variable.get(), {})
                .get(subject_variable.get(), {}).keys()
            )
            examboard_combobox["values"] = examboards
            examboard_combobox.state(["!disabled"])
            examboard_variable.set("Exam Board")
        '''
        Name: examboard_selected
        Parameters: None
        Returns: None
        Purpose: Enables Topic Dropdown menu
        '''
        def examboard_selected(event):
            topics = (
                self.data_set.get(qualification_variable.get(), {})
                .get(subject_variable.get(), {})
                .get(examboard_variable.get(), [])
            )
            topic_combobox["values"] = topics
            topic_combobox.state(["!disabled"])
            topic_variable.set("Topic")

        qualification_combobox.bind("<<ComboboxSelected>>", qualification_selected)
        subject_combobox.bind("<<ComboboxSelected>>", subject_selected)
        examboard_combobox.bind("<<ComboboxSelected>>", examboard_selected)
        topic_combobox.bind("<<ComboboxSelected>>", update_confirm_state)

        '''
        Name: confirm_selection
        Parameters: None
        Returns: None
        Purpose: confirms user selection and continues to question_select_screen or question_gen_screen based upon choice value
        '''
        def confirm_selection():
            q = qualification_variable.get()
            s = subject_variable.get()
            e = examboard_variable.get()
            t = topic_variable.get()

            self.current_selection = {
                "qualification": q,
                "subject": s,
                "exam_board": e,
                "topic": t
            }

            if choice == 1:
                self.question_gen_screen(q, s, e, t)
            else:
                questions = self.logic.fetch_existing_questions(
                    q, s, e, t, self.qualifications, self.exam_boards
                )
                if questions:
                    self.question_select_screen(questions)
                else:
                    messagebox.showinfo("Info", "No questions found.")

        confirm_button.config(command=confirm_selection)

#Question Screens
    '''
    Name: question_gen_screen
    Parameters: qualification:string , subject:string, exam_board:string, topic:string
    Returns: None
    Purpose: Takes paramaters and sends to server to be used in question generation within ai_handler.py
    '''
    def question_gen_screen(self, qualification, subject, exam_board, topic):
        self.clear_current_frame()
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        tk.Label(frame, text="Generating Questions", font=self.title_font, bg="white") \
            .place(relx=0.5, rely=0.45, anchor="center")

        status_label = tk.Label(frame, text="Please wait...", font=self.button_font, bg="white")
        status_label.place(relx=0.5, rely=0.55, anchor="center")

        self.update_idletasks()

        # Call logic layer to generate questions
        questions = self.logic.generate_and_fetch_questions(
            qualification, subject, exam_board, topic,
            self.qualifications, self.exam_boards
        )

        if questions:
            status_label.config(text="Questions generated successfully!")
            tk.Button(frame, text="Continue", font=self.button_font,
                      command=lambda: self.question_select_screen(questions)) \
                .place(relx=0.5, rely=0.8, anchor="center")
        else:
            status_label.config(text="Failed to generate questions")
            tk.Button(frame, text="Back to Menu", font=self.button_font,
                      command=self.main_menu) \
                .place(relx=0.5, rely=0.8, anchor="center")


    '''
    Name: question_select_screen
    Parameters: questions: array
    Returns: None
    Purpose: User selection on what questions they would like to be asked , with addition of how many attempts if user is coming from weak_area_selection
    '''
    def question_select_screen(self, questions, is_weak_area=False):
        self.clear_current_frame()
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        # Scrollable Question List
        canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
        scroll_frame = tk.Frame(canvas, bg="white")
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=50, pady=(20, 80))
        scrollbar.pack(side="right", fill="y")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        '''
        Name: on_frame_configure
        Parameters: event
        Returns: None
        Purpose: Scrollable box
        '''

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", on_frame_configure)

        question_vars = {}

        for q in questions:
            qid = q["id"]
            qtext = q["question"]
            atext = q["answer"]
            tally = q.get("tally", None)

            var = tk.BooleanVar(value=True)
            question_vars[qid] = var

            # Add tally info to title if in weak area mode
            title_text = f"Question {qid}"
            if is_weak_area and tally:
                title_text += f" (Failed {tally} time{'s' if tally > 1 else ''})"

            box = tk.LabelFrame(scroll_frame, text=title_text, bg="white",
                                padx=10, pady=5, font=self.box_font_title)
            box.pack(fill="x", pady=5)

            tk.Label(box, text=f"Q: {qtext}", anchor="w", justify="left", bg="white",
                     wraplength=600, font=self.box_font).pack(fill="x")
            tk.Label(box, text=f"A: {atext}", anchor="w", justify="left", bg="white",
                     fg="gray", wraplength=600, font=self.box_font).pack(fill="x")
            tk.Checkbutton(box, text="Include", variable=var, bg="white").pack(anchor="w")

        # Buttons
        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(side="bottom", fill="x", pady=20)

        '''
        Name: toggle_all
        Parameters: select (bool)
        Returns: None
        Purpose: toggle select all questions
        '''

        def toggle_all(select=True):
            for var in question_vars.values():
                var.set(select)

        tk.Button(button_frame, text="Select All", font=self.button_font,
                  command=lambda: toggle_all(True)).pack(side="left", padx=40)
        tk.Button(button_frame, text="Deselect All", font=self.button_font,
                  command=lambda: toggle_all(False)).pack(side="left", padx=40)

        '''
        Name: confirm_selection
        Parameters: None
        Returns: None
        Purpose: confirm selection of which questions and passes on to question_type_selection
        '''

        def confirm_selection():
            selected_ids = [qid for qid, var in question_vars.items() if var.get()]
            chosen_questions = [q for q in questions if q["id"] in selected_ids]
            if chosen_questions:
                self.question_type_selection(chosen_questions, is_weak_area)
            else:
                messagebox.showwarning("No Selection", "Please select at least one question.")

        tk.Button(button_frame, text="Confirm", font=self.button_font,
                  command=confirm_selection).pack(side="right", padx=40)


    '''
    Name: question_type_selection
    Parameters: chosen_questions : array
    Returns: None
    Purpose: User selection of either typed input or multiple choice questions
    '''
    def question_type_selection(self, chosen_questions, is_weak_area=False):
        self.chosen_questions = chosen_questions
        self.is_weak_area_mode = is_weak_area

        # Start quiz with metadata
        self.logic.start_quiz(
            chosen_questions,
            self.current_selection["qualification"],
            self.current_selection["subject"],
            self.current_selection["exam_board"],
            self.current_selection["topic"],
            is_weak_area
        )

        self.clear_current_frame()
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        tk.Label(frame, text="Question Type", font=self.big_text_font, bg="white") \
            .place(relx=0.5, rely=0.3, anchor="center")

        tk.Button(frame, text="Multiple Choice", font=self.button_font,
                  command=self.multiple_choice) \
            .place(relx=0.3, rely=0.7, anchor="center")

        tk.Button(frame, text="Typed Answer", font=self.button_font,
                  command=self.typed_answer) \
            .place(relx=0.7, rely=0.7, anchor="center")

#Multiple Choice
    '''
    Name: multiple_choice
    Parameters: 
    Returns: None
    Purpose: passes on to show_multiple_choice_question
    '''
    def multiple_choice(self):
        self.show_multiple_choice_question()
    '''
    Name: show_multiple_choice_question
    Parameters: 
    Returns: None
    Purpose: Asks the user multiple choice questions , filling other boxes with other questions answers.
    '''
    def show_multiple_choice_question(self):
        self.clear_current_frame()
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        current = self.logic.current_question()
        if not current:
            self.show_results()
            return

        question_text = current["question"]
        options = self.logic.generate_mc_options()
        total = len(self.chosen_questions)
        current_num = self.logic.current_index + 1

        tk.Label(frame, text=f"Question {current_num}/{total}",
                 font=self.title_font, bg="white").pack(pady=(20, 10))
        tk.Label(frame, text=question_text, font=self.button_font, wraplength=600, bg="white") \
            .pack(pady=(10, 30))

        def handle_selection(answer):
            self.logic.submit_mc_answer(answer)
            self.show_multiple_choice_question()

        for opt in options:
            tk.Button(frame, text=opt, font=self.button_font,
                      command=lambda a=opt: handle_selection(a)).pack(pady=10)

#Typed Questions
    '''
    Name: typed_answer
    Parameters: 
    Returns: None
    Purpose: passes on to show_typed_question
    '''
    def typed_answer(self):
        self.show_typed_question()
    '''
    Name: show_typed_answer
    Parameters: 
    Returns: None
    Purpose: Asks the user multiple choice questions , filling other boxes with other questions answers.
    '''
    def show_typed_question(self):
        self.clear_current_frame()
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        current_idx = self.logic.current_index
        if current_idx >= len(self.chosen_questions):
            self.show_results()
            return

        current = self.chosen_questions[current_idx]
        question_text = current["question"]
        total = len(self.chosen_questions)

        tk.Label(frame, text=f"Question {current_idx + 1}/{total}",
                 font=self.title_font, bg="white").place(relx=0.5, rely=0.2, anchor="center")
        tk.Label(frame, text=question_text, font=self.button_font, wraplength=600, bg="white") \
            .place(relx=0.5, rely=0.3, anchor="center")

        answer_box = tk.Text(frame, width=50, height=10, wrap="word", font=("Segoe UI", 12))
        answer_box.place(relx=0.5, rely=0.5, anchor="center")

        def save_next():
            user_answer = answer_box.get("1.0", "end").strip()
            self.logic.save_typed_answer(current["id"], user_answer)
            self.logic.next_question()
            self.show_typed_question()

        tk.Button(frame, text="Confirm", font=self.button_font, command=save_next) \
            .place(relx=0.5, rely=0.7, anchor="center")

#Results

    '''
    Name: show_results
    Parameters: 
    Returns: None
    Purpose: Results screen after completing a test
    '''
    def show_results(self):
        self.clear_current_frame()
        
        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        results = self.logic.get_results()
        score = results["score"]
        total = results["total"]
        incorrect = results["incorrect_questions"]

        correct_count = score
        incorrect_count = total - score

        tk.Label(frame, text="Results", font=self.big_text_font, bg="white").pack(pady=20)

        top_container = tk.Frame(frame, bg="white")
        top_container.pack(fill="both", expand=False, padx=50, pady=10)


        chart_frame = tk.Frame(top_container, bg="white")
        chart_frame.pack(side="left", fill="both", expand=True)

        pie_chart = PieChart(chart_frame, correct=correct_count, incorrect=incorrect_count, bg="white")
        pie_chart.pack(fill="both", expand=True, padx=20, pady=20)

        score_frame = tk.Frame(top_container, bg="white")
        score_frame.pack(side="right", fill="both", expand=True)

        tk.Label(score_frame, text=f"Score: {score}/{total}",
                 font=self.title_font, bg="white").pack(pady=20, anchor="center")

        tk.Label(score_frame, text=f"Correct: {correct_count}",
                 font=self.button_font, bg="white", fg="#00AA00").pack(pady=5, anchor="center")

        tk.Label(score_frame, text=f"Incorrect: {incorrect_count}",
                 font=self.button_font, bg="white", fg="#AA0000").pack(pady=5, anchor="center")

        if total > 0:
            percentage = (score / total) * 100
            tk.Label(score_frame, text=f"{percentage:.1f}%",
                     font=("Segoe UI", 36, "bold"), bg="white").pack(pady=20, anchor="center")

        if incorrect:
            tk.Label(frame, text="You got these wrong:", font=self.button_font, bg="white").pack(pady=10)

            scroll_canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
            scroll_frame = tk.Frame(scroll_canvas, bg="white")
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=scroll_canvas.yview)
            scroll_canvas.configure(yscrollcommand=scrollbar.set)

            scroll_canvas.pack(side="left", fill="both", expand=True, padx=50, pady=10)
            scrollbar.pack(side="right", fill="y")
            scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            '''
            Name: on_frame_configure
            Parameters: 
            Returns: None
            Purpose: scrollable section of screen
            '''
            def on_frame_configure(event):
                scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

            scroll_frame.bind("<Configure>", on_frame_configure)

            for q in incorrect:
                tk.Label(scroll_frame, text=f"Q: {q['question']}\nA: {q['answer']}",
                         font=self.box_font, wraplength=600, justify="left", bg="white", anchor="w").pack(fill="x",
                                                                                                          pady=5)
        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(side="bottom", pady=30)

        if incorrect:
            tk.Button(button_frame, text="Retry Incorrect", font=self.button_font_small,
                      command=lambda: self.question_type_selection(incorrect, self.is_weak_area_mode)).pack(side="left",
                                                                                                            padx=20)

        tk.Button(button_frame, text="Back to Menu", font=self.button_font_small,
                  command=self.main_menu).pack(side="left", padx=20)

if __name__ == "__main__":
    ip_prompt()
    app = StudyQuiz()
    app.mainloop()