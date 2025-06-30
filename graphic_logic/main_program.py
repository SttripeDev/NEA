import customtkinter as Tk
import os
from PIL import Image
class StudyQuiz(Tk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry('800x600')
        self.title("Study Quiz")
        self.script_dir = os.path.dirname(os.path.abspath(__file__))


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
            self,
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
            self,
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
        self.lightmode_toggle.place_forget()
        self.darkmode_toggle.place_forget()
        self.default_toggle.place_forget()
        self.home_button.place_forget()
        self.bg_frame.place_forget()
        self.main_menu()
    def main_menu(self):
        self.program_title = Tk.CTkLabel(
            self,
            text="Study Quiz",
            font=self.big_text_font,
            text_color=self.title_colour)

        self.new_set_button = Tk.CTkButton(
            self,
            text="Create New Questions",
            command=lambda: self.goto_selection(1),
            font=self.button_font,
            text_color=self.text_colour,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour,
            width=90,
            height=50)

        self.existing_set_button = Tk.CTkButton(
            self,
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
            self,
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
            self,
            text="Light Mode",
            command=on_mode_change,
            font=self.button_font,
            text_color=self.text_colour,
            bg_color=self.button_colour,
            variable=self.theme_var,
            value=1
        )

        self.darkmode_toggle = Tk.CTkRadioButton(
            self,
            text="Dark Mode",
            font=self.button_font,
            text_color=self.text_colour,
            bg_color=self.button_colour,
            command=on_mode_change,
            variable=self.theme_var,
            value=2
        )

        self.default_toggle = Tk.CTkRadioButton(
            self,
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
        self.program_title.place_forget()
        self.new_set_button.place_forget()
        self.existing_set_button.place_forget()
        self.settings_button.place_forget()
        if choice == 1:
            self.selection_screen()


    def selection_screen(self):

        qualification_types = [
            "A-LEVEL", "GCSE"
        ]

        subjects_by_qualification = {
            "A-Level": ["Computer Science", "Maths", "Business", "Chemistry"],
            "GCSE": ["English", "Science", "Geography"]
        }

        exam_boards_by_qualification_and_subject = {
            "A-Level": {
                "Computer Science": ["AQA", "OCR", "Edexcel"],
                "Maths": ["Edexcel", "AQA", "OCR"],
                "Business": ["Eduqas", "AQA", "OCR"],
                "Chemistry": ["AQA", "OCR"]
            },
            "GCSE": {
                "English": ["AQA", "Edexcel", "WJEC"],
                "Science": ["OCR", "AQA", "Edexcel"],
                "Geography": ["Edexcel", "OCR", "AQA"]
            }
        }

        def qualification_select(choice):
            print("combobox dropdown clicked:", choice)

        combobox_var = Tk.StringVar(value="Qualification")
        qualification_combobox = Tk.CTkComboBox(self, values=qualification_types,
                                              variable=combobox_var, state="readonly")
        combobox_var.set("GCSE")
        qualification_combobox.place(relx=0.2,rely=0.5,anchor="center")

        def subject_select(choice):
            print("combobox dropdown clicked:", choice)

        combobox_var = Tk.StringVar(value="Subject")
        subject_combobox = Tk.CTkComboBox(self, values=subjects_by_qualification[qualification_combobox.get()],
                                              variable=combobox_var, state="readonly")
        combobox_var.set("Science")
        subject_combobox.place(relx=0.5,rely=0.5,anchor="center")

        def examboard_select(choice):
            print("combobox dropdown clicked:", choice)

        combobox_var = Tk.StringVar(value="Subject")
        examboard_combobox = Tk.CTkComboBox(self, values=exam_boards_by_qualification_and_subject[subject_combobox[qualification_combobox.get()].get()],
                                          variable=combobox_var, state="readonly")
        combobox_var.set("Subject")
        examboard_combobox.place(relx=0.8, rely=0.5, anchor="center")
# Check
# Check whether coming from "Create New Questions"
# Box for qualification
# Box for Subject
# Box for ExamBoard
# Box for Topic

# class QuestionCreationScreen(Tk.CTk):
#
#     def __init__(self):
#         super().__init__()
#
#
#
#     def selection_screen(self,choice):
#         # Check whether coming from "Create New Questions"
#         # Box for qualification
#         # Box for Subject
#         # Box for ExamBoard
#         # Box for Topic
#
#
#         def qualification_callback(choice):
#             print("combobox dropdown clicked:", choice)
#
#         combobox_var = Tk.StringVar(value="option 2")
#         combobox = Tk.CTkComboBox(StudyQuiz, values=["A-Level", "GCSE"],
#                                              command=qualification_callback, variable=combobox_var)
#         combobox_var.set("option 2")
#         combobox.place(relx=0.5,rely=0.5,anchor="center")
#     def send_2_creator(self):
#         None
#         # Take the inputs from selection screen
#         # Send them to controller.py to be processed and sent to database
#
#     def retrieval_request(self):
#         # Take the inputs from selection screen
#         # Send them to controller to be sent to database for a request of data
#         None


study_quiz = StudyQuiz()
# question_creation_screen = QuestionCreationScreen()

study_quiz.mainloop()

##Switch to SBERT !!!