# appbar.py
import customtkinter as ctk # type: ignore
from PIL import Image # type: ignore

class AppBar(ctk.CTkFrame):
    def __init__(self, parent, controller=None, profile_letter="U", username="User", settings_icon_path="setting.png", **kwargs):
        super().__init__(parent, fg_color="transparent", height=70, **kwargs)
        self.controller = controller
        
        # Store references for updating later
        self.profile_letter = profile_letter
        self.username = username
        
        # --- Left Side: Profile Circle + Name ---
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.pack(side="left", padx=20, pady=10)
        
        # Circle (Profile) - Store canvas reference
        self.profile_canvas = ctk.CTkCanvas(left_frame, width=40, height=40, bg="#D4E3FF", highlightthickness=0)
        self.profile_canvas.create_oval(2, 2, 38, 38, fill="#1E3A8A", outline="", tags="circle")
        self.profile_text_id = self.profile_canvas.create_text(
            20, 20, 
            text=profile_letter.upper(), 
            fill="white", 
            font=("Poppins", 16, "bold"),
            tags="letter"
        )
        self.profile_canvas.pack(side="left")
        
        # Name label - Store reference
        self.name_label = ctk.CTkLabel(
            left_frame,
            text=username,
            font=ctk.CTkFont(family="Poppins", size=15, weight="bold"),
            text_color="#1E3A8A",
        )
        self.name_label.pack(side="left", padx=(10, 0))
        
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
    
    def update_user(self, profile_letter, username):
        """Update the profile letter and username"""
        self.profile_letter = profile_letter.upper()
        self.username = username
        
        # Update the canvas text
        self.profile_canvas.itemconfig(self.profile_text_id, text=self.profile_letter)
        
        # Update the username label
        self.name_label.configure(text=username)
        
        print(f"\033[92m [✓] AppBar updated: {self.profile_letter} - {username}")
    
    def open_settings(self):
        print("\033[94m [+] Settings button clicked")
        if self.controller:
            self.controller.show_frame("SettingsPage")