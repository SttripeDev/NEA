import customtkinter as Tk

class RetrievalAndCreator:

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



    def send_2_creator(self):
        None

    def retrieval_request(self):
        None
