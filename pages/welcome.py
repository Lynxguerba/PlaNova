import customtkinter as ctk  # type: ignore
from components.button import CustomButton
import os
from PIL import Image # type: ignore

class WelcomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D4E3FF")  # background color
        self.controller = controller
        

        # --- Load image ---
        image_path = os.path.join("assets", "images", "logo.png")
        self.top_image = ctk.CTkImage(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path),
            size=(280, 280) 
        )

        # --- Layout grid ---
        self.grid_rowconfigure(0, weight=0)  # spacer
        self.grid_rowconfigure(1, weight=1)  # image
        self.grid_rowconfigure(2, weight=1)  # title
        self.grid_rowconfigure(3, weight=1)  # subtitle
        # self.grid_rowconfigure(4, weight=1)  # button
        self.grid_columnconfigure(0, weight=1)

        # --- Top Image ---
        image_label = ctk.CTkLabel(self, text="", image=self.top_image)
        image_label.grid(row=0, column=0, pady=(180, 80))
  
        # --- Title ---
        title = ctk.CTkLabel(
            self,
            text="PlaNova",
            font=ctk.CTkFont(family="Poppins", size=40, weight="bold"),
            text_color="#1E3A8A"
        )
        title.grid(row=1, column=0, sticky="n")

        # --- Subtitle ---
        subtitle = ctk.CTkLabel(
            self,
            text="“Ignite your productivity. Start each day with focus, balance, and a clear sense of direction.”",
            font=ctk.CTkFont(family="Poppins", size=20, slant="italic"),
            text_color="#4B5563",
            wraplength=320,   # wrap text after 320px
            justify="center"  # center align the text
        )
        subtitle.grid(row=2, column=0, sticky="n")

        # --- Get Started Button (bottom aligned) ---
        get_started_btn = ctk.CTkButton(
            self,
            text="Get Started",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="white",
            font=ctk.CTkFont(family="Poppins", size=20, weight="bold"),
            corner_radius=12,
            height=70,
            width=400,
            command=lambda: (print("\033[93m [+] Redirecting to the Login Page..."),controller.show_frame("LoginPage"))
        )
        # Place near bottom with padding
        get_started_btn.grid(row=3, column=0, sticky="s", padx=40, pady=(10, 30))
