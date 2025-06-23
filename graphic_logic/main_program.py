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
        self.text_colour = "#FFFFFF"

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


        self.new_set_button = Tk.CTkButton(
            self,
            text="Create New Questions",
            command=None,
            font=self.button_font,
            text_color=self.text_colour,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour,
            width=90,
            height=50)

        self.previous_set_button = Tk.CTkButton(
            self,
            text="Your Question Sets",
            command=None,
            font=self.button_font,
            text_color=self.text_colour,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour,
            width=90,
            height=50)

        self.existing_set_button = Tk.CTkButton(
            self,
            text="Existing Question Sets",
            command=None,
            font=self.button_font,
            text_color=self.text_colour,
            fg_color=self.button_colour,
            hover_color=self.button_hover_colour,
            width = 90,
            height = 50)



        self.new_set_button.place(relx=0.5,rely=0.5,anchor="center")
        self.previous_set_button.place(relx=0.5,rely=0.6,anchor="center")
        self.existing_set_button.place(relx=0.5,rely=0.7,anchor="center")
        self.settings_button.place(anchor="e",relx=0.97,rely=0.07)

    def settings_menu(self):
        # Hide main menu buttons
        self.new_set_button.place_forget()
        self.previous_set_button.place_forget()
        self.existing_set_button.place_forget()
        self.settings_button.place_forget()

        # Show the home button
        self.home_button.place(anchor="e", relx=0.97, rely=0.07)

        self.bg_frame = Tk.CTkFrame(
            self,
            fg_color=self.button_colour,  # Set your desired color here (e.g., blue)
            corner_radius=12  # Optional: rounded corners
        )
        self.bg_frame.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.3, relheight=0.5)

        self.theme_var = Tk.IntVar(value=0)  # 0: System, 1: Light, 2: Dark

        def on_mode_change():
            v = self.theme_var.get()
            if v == 1:
                Tk.set_appearance_mode("light")
            elif v == 2:
                Tk.set_appearance_mode("dark")
            else:
                Tk.set_appearance_mode("system")

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


        self.lightmode_toggle.place(relx=0.5, rely=0.3, anchor="center")
        self.darkmode_toggle.place(relx=0.5, rely=0.4, anchor="center")
        self.default_toggle.place(relx=0.5, rely=0.5, anchor="center")

class RetrievalAndCreation:

    def __init__(self):
        self.geometry('800x600')
        self.title("Study Quiz")
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.button_font = Tk.CTkFont("Segoe UI", size=14, weight="bold")
        self.title_font = Tk.CTkFont("Segoe UI", size=24, weight="bold")
        self.text_colour = "#FFFFFF"

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

    def selection_screen(self):

        # Box for qualification
        # Box for Subject
        # Box for ExamBoard
        # Box for Topic
        None
    def send_2_creator(self):
        None

    def retrieval_request(self):
        None
Study_Quiz = StudyQuiz()

Study_Quiz.mainloop()
