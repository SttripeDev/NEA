import customtkinter as Tk
import customtkinterthemes
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

        self.button_colour = "#6800D0"
        self.button_hover_colour = "#BA75FF"

        self.main_menu()



        # Previous sets
        # New sets
        # Existing sets
        # settings
        # Credits ig

    def main_menu(self):
        pil_image = Image.open(self.script_dir+'\icons\SettingsIcon.png')
        self.settings_icon = Tk.CTkImage(light_image=pil_image,size=(15,15))

        self.new_set_button = Tk.CTkButton(self, text="Create New Questions", command=None, font=self.button_font,text_color="#ffffff",fg_color=self.button_colour,hover_color=self.button_hover_colour)
        self.previous_set_button = Tk.CTkButton(self, text="Your Question Sets", command=None, font=self.button_font,text_color="#ffffff",fg_color=self.button_colour,hover_color=self.button_hover_colour)
        self.existing_set_button = Tk.CTkButton(self, text="Existing Question Sets", command=None, font=self.button_font,text_color="#ffffff",fg_color=self.button_colour,hover_color=self.button_hover_colour)
        self.settings_button = Tk.CTkButton(self, image=self.settings_icon,anchor="center",text="", command=None,width =32,height=32,fg_color=self.button_colour,hover_color=self.button_hover_colour)

        self.new_set_button.place(relx=0.5,rely=0.5,anchor="center")
        self.previous_set_button.place(relx=0.5,rely=0.6,anchor="center")
        self.existing_set_button.place(relx=0.5,rely=0.7,anchor="center")
        self.settings_button.place(anchor="e",relx=0.97,rely=0.07)



Study_Quiz = StudyQuiz()

Study_Quiz.mainloop()
