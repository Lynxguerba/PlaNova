# appbar.py
import customtkinter as ctk # type: ignore
from PIL import Image # type: ignore

class AppBar(ctk.CTkFrame):
    def __init__(self, parent, controller=None, profile_letter="D", username="Dinno Guerba", settings_icon_path="setting.png", **kwargs):
        super().__init__(parent, fg_color="transparent", height=70, **kwargs)
        self.controller = controller

        # --- Left Side: Profile Circle + Name ---
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.pack(side="left", padx=20, pady=10)

        # Circle (Profile)
        profile_circle = ctk.CTkCanvas(left_frame, width=40, height=40, bg="#D4E3FF", highlightthickness=0)
        profile_circle.create_oval(2, 2, 38, 38, fill="#1E3A8A", outline="")
        profile_circle.create_text(20, 20, text=profile_letter.upper(), fill="white", font=("Poppins", 16, "bold"))
        profile_circle.pack(side="left")

        # Name label
        name_label = ctk.CTkLabel(
            left_frame,
            text=username,
            font=ctk.CTkFont(family="Poppins", size=15, weight="bold"),
            text_color="#1E3A8A",
        )
        name_label.pack(side="left", padx=(10, 0))

        # --- Right Side: Settings Icon ---
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=10)

        # Load PNG settings icon
        settings_img = ctk.CTkImage(
            dark_image=Image.open(settings_icon_path),
            light_image=Image.open(settings_icon_path),
            size=(26, 26)
        )
        settings_button = ctk.CTkButton(
            right_frame,
            image=settings_img,
            text="",
            fg_color="transparent",
            hover_color="#D4E3FF",
            width=40,
            command=self.open_settings
        )
        settings_button.pack(side="right")

    def open_settings(self):
        print("Settings button clicked")
        if self.controller:
            self.controller.show_frame("SettingsPage")
        
