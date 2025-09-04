import tkinter as tk
from tkinter import ttk

class StudyQuiz(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.title("Study Quiz")


        self.button_font = ("Segoe UI", 14, "bold")
        self.title_font = ("Segoe UI", 24, "bold")
        self.big_text_font = ("Segoe UI", 56, "bold")

        self.current_frame = None

        self.main_menu()

    def clear_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def main_menu(self):
        self.clear_current_frame()

        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        program_title = tk.Label(
            frame,
            text="Study Quiz",
            font=self.big_text_font,
            fg="black",
            bg="white"
        )
        program_title.place(relx=0.5, rely=0.3, anchor="center")

        new_set_button = tk.Button(
            frame,
            text="Create New Questions",
            command=lambda: self.goto_selection(1),
            font=self.button_font,
            width=20,
            height=2
        )
        new_set_button.place(relx=0.5, rely=0.5, anchor="center")

        existing_set_button = tk.Button(
            frame,
            text="Existing Question Sets",
            command=lambda: self.goto_selection(2),
            font=self.button_font,
            width=20,
            height=2
        )
        existing_set_button.place(relx=0.5, rely=0.7, anchor="center")

    def goto_selection(self, choice):
        self.clear_current_frame()
        if choice == 1:
            self.selection_screen()
        # elif choice == 2:
        #     self.existing_sets_screen()

    def selection_screen(self):
        all_settings = {
            "A-Level": {
                "Computer Science": ["OCR", "AQA", "Edexcel"],
                "Business Studies": ["Eduqas", "Edexcel", "AQA"],
                "Mathematics": ["Edexcel", "AQA", "OCR"]
            },
            "GCSE": {
                "Business Studies": ["Edexcel", "AQA"],
                "Computer Science": ["Edexcel", "AQA", "OCR"],
                "Geography": ["Edexcel", "AQA", "OCR"]
            }
        }

        frame = tk.Frame(self, bg="white")
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        selection_screen_title = tk.Label(
            frame,
            text="Question Generation",
            font=self.title_font,
            fg="black",
            bg="white"
        )
        selection_screen_title.place(relx=0.5, rely=0.2, anchor="center")

        qualification_var = tk.StringVar(value="Qualification")
        subject_var = tk.StringVar(value="Subject")
        examboard_var = tk.StringVar(value="Exam Board")

        def qualification_listen(event):
            choice = qualification_var.get()
            subjects = list(all_settings[choice].keys())
            subject_combobox["values"] = subjects
            subject_combobox.state(["!disabled"])
            subject_var.set("Subject")

            examboard_combobox["values"] = ["Exam Board"]
            examboard_combobox.state(["disabled"])
            examboard_var.set("Exam Board")
            confirm_button_state()

        def subject_listen(event):
            qualification = qualification_var.get()
            choice = subject_var.get()
            if qualification in all_settings and choice in all_settings[qualification]:
                boards = all_settings[qualification][choice]
                examboard_combobox["values"] = boards
                examboard_combobox.state(["!disabled"])
                examboard_var.set("Exam Board")
            else:
                examboard_combobox["values"] = ["Exam Board"]
                examboard_combobox.state(["disabled"])
                examboard_var.set("Exam Board")
            confirm_button_state()

        def confirm_button_state(event=None):
            board = examboard_var.get()
            qualification = qualification_var.get()
            subject = subject_var.get()
            if board != "Exam Board" and qualification != "Qualification" and subject != "Subject":
                confirm_button.config(state="normal")
            else:
                confirm_button.config(state="disabled")

        def goto_topic_select():
            qualification = qualification_var.get()
            subject = subject_var.get()
            examboard = examboard_var.get()
            print(f"Chosen: {qualification}, {subject}, {examboard}")  # TODO: next screen

        qualification_combobox = ttk.Combobox(
            frame,
            textvariable=qualification_var,
            values=list(all_settings.keys()),
            state="readonly"
        )
        qualification_combobox.bind("<<ComboboxSelected>>", qualification_listen)
        qualification_combobox.place(relx=0.2, rely=0.5, anchor="center")

        subject_combobox = ttk.Combobox(
            frame,
            textvariable=subject_var,
            values=["Subject"],
            state="disabled"
        )
        subject_combobox.bind("<<ComboboxSelected>>", subject_listen)
        subject_combobox.place(relx=0.5, rely=0.5, anchor="center")

        examboard_combobox = ttk.Combobox(
            frame,
            textvariable=examboard_var,
            values=["Exam Board"],
            state="disabled"
        )
        examboard_combobox.bind("<<ComboboxSelected>>", confirm_button_state)
        examboard_combobox.place(relx=0.8, rely=0.5, anchor="center")

        confirm_button = tk.Button(
            frame,
            text="Confirm",
            font=self.button_font,
            state="disabled",
            command=goto_topic_select
        )
        confirm_button.place(relx=0.5, rely=0.7, anchor="center")


if __name__ == "__main__":
    study_quiz = StudyQuiz()
    study_quiz.mainloop()
