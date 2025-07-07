import customtkinter as Tk
import os
from PIL import Image
class StudyQuiz(Tk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry('800x600')
        self.title("Study Quiz")
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.page = None

        self.button_font = Tk.CTkFont("Segoe UI", size=14, weight="bold")
        self.title_font = Tk.CTkFont("Segoe UI",size=24,weight="bold")
        self.big_text_font = Tk.CTkFont("Segoe UI",size=56,weight="bold")
        self.text_colour = "#FFFFFF"
        self.title_colour = ""
        mode = Tk.get_appearance_mode()
        if mode == "Light":
            self.title_colour = "#000000"
        elif mode == "Dark":
            self.title_colour = "#FFFFFF"
        else:
            self.title_colour = "#000000"


        self.button_colour = "#6800D0"
        self.button_hover_colour = "#BA75FF"

        pil_image_home = Image.open(self.script_dir + '\icons\HomeIcon.png')
        self.home_icon = Tk.CTkImage(light_image=pil_image_home, size=(15, 15))
        self.home_button = Tk.CTkButton(
            self.page,
            image=self.home_icon,
            anchor="center",
            text="",
            command=self.clear_settings,
            width=32,
            height=32,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour)

        pil_image = Image.open(self.script_dir + '\icons\SettingsIcon.png')
        self.settings_icon = Tk.CTkImage(light_image=pil_image, size=(15, 15))
        self.settings_button = Tk.CTkButton(
            self.page,
            image=self.settings_icon,
            anchor="center",
            text="",
            command=self.settings_menu,
            width=32,
            height=32,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour)

        self.main_menu()

        # Previous sets
        # New sets
        # Existing sets
        # settings
        # Credits ig
    def clear_settings(self):
        self.bg_frame.place_forget()
        self.main_menu()
    def main_menu(self):

        self.main_menu_frame = Tk.CTkFrame(self,bg_color=self.title_colour)
        page = self.main_menu_frame
        self.main_menu_frame.place(relwidth=1,relheight=1)

        self.program_title = Tk.CTkLabel(
            self.main_menu_frame,
            text="Study Quiz",
            font=self.big_text_font,
            text_color=self.title_colour)

        self.new_set_button = Tk.CTkButton(
            self.main_menu_frame,
            text="Create New Questions",
            command=lambda: self.goto_selection(1),
            font=self.button_font,
            text_color=self.text_colour,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour,
            width=90,
            height=50)

        self.existing_set_button = Tk.CTkButton(
            self.main_menu_frame,
            text="Existing Question Sets",
            command=lambda: self.goto_selection(2),
            font=self.button_font,
            text_color=self.text_colour,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour,
            width = 90,
            height = 50)


        self.program_title.place(relx=0.5,rely=0.3,anchor="center")
        self.new_set_button.place(relx=0.5,rely=0.5,anchor="center")

        self.existing_set_button.place(relx=0.5,rely=0.7,anchor="center")
        self.settings_button.place(anchor="e",relx=0.97,rely=0.07)
    def settings_menu(self):
        # Hide main menu buttons
        self.program_title.place_forget()
        self.new_set_button.place_forget()
        self.existing_set_button.place_forget()
        self.settings_button.place_forget()

        # Show the home button
        self.home_button.place(anchor="e", relx=0.97, rely=0.07)

        self.bg_frame = Tk.CTkFrame(
            self,
            fg_color=self.button_colour,  # Set your desired color here (e.g., blue)
            corner_radius=12  # Optional: rounded corners
        )
        self.bg_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3, relheight=0.5)

        self.settings_title = Tk.CTkLabel(
            self.bg_frame,
            text = "Settings",
            text_color = self.text_colour,
            font= self.title_font,
            bg_color=self.button_colour

        )
        self.settings_title.place(relx=0.5, rely =0.3,anchor="center")
        self.theme_var = Tk.IntVar(value=0)  # 0: System, 1: Light, 2: Dark

        def on_mode_change():
            v = self.theme_var.get()
            if v == 1:
                Tk.set_appearance_mode("light")
                self.title_colour = "#000000"
            elif v == 2:
                Tk.set_appearance_mode("dark")
                self.title_colour = "#FFFFFF"
            else:
                Tk.set_appearance_mode("system")
                mode = Tk.get_appearance_mode()
                if mode == "Light":
                    self.title_colour = "#000000"
                else:
                    self.title_colour = "#FFFFFF"

        self.lightmode_toggle = Tk.CTkRadioButton(
            self.bg_frame,
            text="Light Mode",
            command=on_mode_change,
            font=self.button_font,
            text_color=self.text_colour,
            bg_color=self.button_colour,
            variable=self.theme_var,
            value=1
        )

        self.darkmode_toggle = Tk.CTkRadioButton(
            self.bg_frame,
            text="Dark Mode",
            font=self.button_font,
            text_color=self.text_colour,
            bg_color=self.button_colour,
            command=on_mode_change,
            variable=self.theme_var,
            value=2
        )

        self.default_toggle = Tk.CTkRadioButton(
            self.bg_frame,
            text="System Default",
            font=self.button_font,
            text_color=self.text_colour,
            bg_color=self.button_colour,
            command=on_mode_change,
            variable=self.theme_var,
            value=0
        )


        self.lightmode_toggle.place(relx=0.5, rely=0.4, anchor="center")
        self.darkmode_toggle.place(relx=0.5, rely=0.5, anchor="center")
        self.default_toggle.place(relx=0.5, rely=0.6, anchor="center")

    def goto_selection(self,choice):
        self.main_menu_frame.forget()
        if choice == 1:
            self.selection_screen()


    def selection_screen(self):

        all_settings = { #Temporary until database intergration (I just want to get the GUI to work first)
            "A-Level":{"Computer Science":["OCR","AQA","Edexcel"],
                        "Business Studies":["Eduqas","Edexcel","AQA"],
                       "Mathematics":["Edexcel","AQA","OCR"]},
            "GCSE":{"Business Studies":["Edexcel","AQA"],
                    "Computer Science":["Edexcel","AQA","OCR"],
                    "Geography":["Edexcel","AQA","OCR"]}
        }

        selection_screen_frame = Tk.CTkFrame(self,bg_color=self.title_colour)
        selection_screen_frame.place(relwidth=1,relheight=1)

        def qualification_listen(choice):
            subjects = list(all_settings[choice].keys())
            subject_combobox.configure(values=subjects, state="readonly")
            subject_var.set("Subject")
            # Reset exam board
            examboard_combobox.configure(values=["Exam Board"], state="disabled")
            examboard_var.set("Exam Board")
            confirm_button_state()
        def subject_listen(choice):

            qualification = qualification_var.get()
            if qualification in all_settings and choice in all_settings[qualification]:
                boards = all_settings[qualification][choice]
                examboard_combobox.configure(values=boards, state="readonly")
                examboard_var.set("Exam Board")
            else:
                examboard_combobox.configure(values=["Exam Board"], state="disabled")
                examboard_var.set("Exam Board")
            confirm_button_state()

        def confirm_button_state(_=None):
            board = examboard_var.get()
            qualification = qualification_var.get()
            subject = subject_var.get()
            if board != "Exam Board" and qualification != "Qualification" and subject != "Subject":
                confirm_button.configure(state="normal")
            else:
                confirm_button.configure(state="disabled")

        def goto_topic_select():
            qualification = qualification_var.get()
            subject = subject_var.get()
            examboard = examboard_var.get()


        selection_screen_title = Tk.CTkLabel(selection_screen_frame,text="Question Generation",text_color=self.title_colour,font=self.title_font)
        selection_screen_title.place(relx=0.5, rely=0.3,anchor="center")

        qualification_var = Tk.StringVar(value="Qualification")
        qualification_combobox = Tk.CTkComboBox(
            selection_screen_frame,
            values=list(all_settings.keys()),
            variable=qualification_var,
            state="readonly",
            command=qualification_listen
        )
        qualification_combobox.place(relx=0.2, rely=0.5, anchor="center")

        subject_var = Tk.StringVar(value="Subject")
        subject_combobox = Tk.CTkComboBox(
            selection_screen_frame,
            values=["Subject"],
            variable=subject_var,
            state="disabled",
            command=subject_listen
        )
        subject_combobox.place(relx=0.5, rely=0.5, anchor="center")

        examboard_var = Tk.StringVar(value="Exam Board")
        examboard_combobox = Tk.CTkComboBox(
            selection_screen_frame,
            values=["Exam Board"],
            variable=examboard_var,
            state="disabled",
            command=confirm_button_state
        )
        examboard_combobox.place(relx=0.8, rely=0.5, anchor="center")

        confirm_button = Tk.CTkButton(
            selection_screen_frame,
            text="Confirm",
            font=self.button_font,
            text_color=self.text_colour,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour,
            state="disabled",
            command=goto_topic_select)

        confirm_button.place(relx=0.5,rely=0.7, anchor="center")




    def topic_select_screen(self):
        None

# Check
# Check whether coming from "Create New Questions"
# Box for qualification
# Box for Subject
# Box for ExamBoard
# Box for Topic




study_quiz = StudyQuiz()
# question_creation_screen = QuestionCreationScreen()

study_quiz.mainloop()

##Switch to SBERT !!!