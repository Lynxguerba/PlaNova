import customtkinter as ctk # type: ignore
from pages.welcome import WelcomePage
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.dashboard import DashboardPage
from pages.settings import SettingsPage
from pages.tasks import TasksPage
from pages.upcoming import UpcomingPage
from pages.completed import CompletedPage
from pages.bin import BinPage 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window setup ---
        self.title("PlaNova")
        self.app_width = 480
        self.app_height = 900

        # --- App theme ---
        ctk.set_appearance_mode("light") 
        ctk.set_default_color_theme("blue") 

        # --- Center window on screen ---
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.app_width // 2)
        y = (screen_height // 2) - (self.app_height // 2)
        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")

        # --- Fixed portrait-style window ---
        self.resizable(False, False)
        self.configure(fg_color="#84CAFF")

        # --- Container for all pages ---
        container = ctk.CTkFrame(self, fg_color="#BBE1FF")
        container.pack(fill="both", expand=True)

        # Ensure all pages resize evenly inside the container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # --- Store and initialize all pages ---
        self.frames = {}
        for Page in (WelcomePage, LoginPage, RegisterPage, DashboardPage, SettingsPage, TasksPage, UpcomingPage, CompletedPage, BinPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # --- Show the first page---
        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        #  Raise the specified page to the front.
        frame = self.frames[page_name]
        frame.tkraise()