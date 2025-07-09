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

        self.current_frame = None

        # NAVBAR (always present)
        self.navbar_frame = Tk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.navbar_frame.place(relx=1.0, rely=0.0, anchor="ne", relwidth=0.25, relheight=0.12)

        # Load icons
        pil_home = Image.open(os.path.join(self.script_dir, "icons", "HomeIcon.png"))
        pil_settings = Image.open(os.path.join(self.script_dir, "icons", "SettingsIcon.png"))
        self.home_icon = Tk.CTkImage(light_image=pil_home, size=(20, 20))
        self.settings_icon = Tk.CTkImage(light_image=pil_settings, size=(20, 20))

        # SETTINGS button (always visible)
        self.settings_button = Tk.CTkButton(
            self.navbar_frame,
            image=self.settings_icon,
            text="",
            width=36,
            height=36,
            command=self.settings_menu,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour
        )
        # Place settings button at top-right in navbar frame
        self.settings_button.place(relx=0.82, rely=0.5, anchor="center")

        # HOME button (only visible on non-home screens)
        self.home_button = Tk.CTkButton(
            self.navbar_frame,
            image=self.home_icon,
            text="",
            width=36,
            height=36,
            command=self.main_menu,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour
        )
        # Do not place it yet; only place on non-home screens

        self.main_menu()

    def clear_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def main_menu(self):
        self.clear_current_frame()
        self.home_button.place_forget()  # Hide home button on home screen

        frame = Tk.CTkFrame(self, bg_color=self.title_colour)
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        program_title = Tk.CTkLabel(
            frame,
            text="Study Quiz",
            font=self.big_text_font,
            text_color=self.title_colour)

        new_set_button = Tk.CTkButton(
            frame,
            text="Create New Questions",
            command=lambda: self.goto_selection(1),
            font=self.button_font,
            text_color=self.text_colour,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour,
            width=90,
            height=50)

        existing_set_button = Tk.CTkButton(
            frame,
            text="Existing Question Sets",
            command=lambda: self.goto_selection(2),
            font=self.button_font,
            text_color=self.text_colour,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour,
            width=90,
            height=50)

        program_title.place(relx=0.5, rely=0.3, anchor="center")
        new_set_button.place(relx=0.5, rely=0.5, anchor="center")
        existing_set_button.place(relx=0.5, rely=0.7, anchor="center")
        # Do NOT place settings button again here!

    def settings_menu(self):
        self.clear_current_frame()
        self.home_button.place(relx=0.64, rely=0.5, anchor="center")  # Show home button (left of settings)

        frame = Tk.CTkFrame(self)
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        bg_frame = Tk.CTkFrame(
            frame,
            fg_color=self.button_colour,
            corner_radius=12
        )
        bg_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3, relheight=0.5)

        settings_title = Tk.CTkLabel(
            bg_frame,
            text="Settings",
            text_color=self.text_colour,
            font=self.title_font,
            bg_color=self.button_colour
        )
        settings_title.place(relx=0.5, rely=0.3, anchor="center")
        theme_var = Tk.IntVar(value=0)

        def on_mode_change():
            v = theme_var.get()
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

        lightmode_toggle = Tk.CTkRadioButton(
            bg_frame,
            text="Light Mode",
            command=on_mode_change,
            font=self.button_font,
            text_color=self.text_colour,
            bg_color=self.button_colour,
            variable=theme_var,
            value=1
        )

        darkmode_toggle = Tk.CTkRadioButton(
            bg_frame,
            text="Dark Mode",
            font=self.button_font,
            text_color=self.text_colour,
            bg_color=self.button_colour,
            command=on_mode_change,
            variable=theme_var,
            value=2
        )

        default_toggle = Tk.CTkRadioButton(
            bg_frame,
            text="System Default",
            font=self.button_font,
            text_color=self.text_colour,
            bg_color=self.button_colour,
            command=on_mode_change,
            variable=theme_var,
            value=0
        )

        lightmode_toggle.place(relx=0.5, rely=0.4, anchor="center")
        darkmode_toggle.place(relx=0.5, rely=0.5, anchor="center")
        default_toggle.place(relx=0.5, rely=0.6, anchor="center")

    def goto_selection(self, choice):
        self.clear_current_frame()
        self.home_button.place(relx=0.64, rely=0.5, anchor="center")  # Show home button on navbar
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

        frame = Tk.CTkFrame(self, bg_color=self.title_colour)
        frame.place(relwidth=1, relheight=1)
        self.current_frame = frame

        selection_screen_title = Tk.CTkLabel(frame, text="Question Generation", text_color=self.title_colour, font=self.title_font)
        selection_screen_title.place(relx=0.5, rely=0.3, anchor="center")

        qualification_var = Tk.StringVar(value="Qualification")
        subject_var = Tk.StringVar(value="Subject")
        examboard_var = Tk.StringVar(value="Exam Board")

        def qualification_listen(choice):
            subjects = list(all_settings[choice].keys())
            subject_combobox.configure(values=subjects, state="readonly")
            subject_var.set("Subject")
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
            # TODO: add next screen logic

        qualification_combobox = Tk.CTkComboBox(
            frame,
            values=list(all_settings.keys()),
            variable=qualification_var,
            state="readonly",
            command=qualification_listen
        )
        qualification_combobox.place(relx=0.2, rely=0.5, anchor="center")

        subject_combobox = Tk.CTkComboBox(
            frame,
            values=["Subject"],
            variable=subject_var,
            state="disabled",
            command=subject_listen
        )
        subject_combobox.place(relx=0.5, rely=0.5, anchor="center")

        examboard_combobox = Tk.CTkComboBox(
            frame,
            values=["Exam Board"],
            variable=examboard_var,
            state="disabled",
            command=confirm_button_state
        )
        examboard_combobox.place(relx=0.8, rely=0.5, anchor="center")

        confirm_button = Tk.CTkButton(
            frame,
            text="Confirm",
            font=self.button_font,
            text_color=self.text_colour,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour,
            state="disabled",
            command=goto_topic_select
        )
        confirm_button.place(relx=0.5, rely=0.7, anchor="center")

    def topic_select_screen(self):
        pass

if __name__ == "__main__":
    study_quiz = StudyQuiz()
    study_quiz.mainloop()