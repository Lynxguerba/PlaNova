import customtkinter as ctk # type: ignore # tpye: ignore
from components.button import CustomButton 


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F3F4F6")
        self.controller = controller

        # --- Grid setup ---
        self.grid_rowconfigure(0, weight=1)  # top spacer
        self.grid_rowconfigure(1, weight=3)  # title + form
        self.grid_rowconfigure(2, weight=2)  # button
        self.grid_rowconfigure(3, weight=1)  # bottom spacer
        self.grid_columnconfigure(0, weight=1)

        # --- Title ---
        title = ctk.CTkLabel(
            self,
            text="Login",
            font=ctk.CTkFont(family="Poppins", size=36, weight="bold"),
            text_color="#1E3A8A"
        )
        title.grid(row=1, column=0, sticky="n", pady=(10, 10))

        # --- Login Form Container ---
        form_frame = ctk.CTkFrame(self, fg_color="#F3F4F6")
        form_frame.grid(row=1, column=0, sticky="s", pady=(0, 20))

        # Username label + entry
        username_label = ctk.CTkLabel(
            form_frame,
            text="Username",
            font=ctk.CTkFont(family="Poppins", size=12),
            text_color="#374151"
        )
        username_label.pack(anchor="w", padx=40, pady=(0, 5))

        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your username",
            width=250,
            height=36,
            corner_radius=8
        )
        self.username_entry.pack(padx=40, pady=(0, 15))

        # Password label + entry
        password_label = ctk.CTkLabel(
            form_frame,
            text="Password",
            font=ctk.CTkFont(family="Poppins", size=12),
            text_color="#374151"
        )
        password_label.pack(anchor="w", padx=40, pady=(0, 5))

        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your password",
            width=250,
            height=36,
            corner_radius=8,
            show="•"
        )
        self.password_entry.pack(padx=40, pady=(0, 10))

        # --- Login Button ---
        login_btn = ctk.CTkButton(
            self,
            text="Login",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="white",
            corner_radius=12,
            width=160,
            height=40,
            command=self.handle_login
        )
        login_btn.grid(row=2, column=0, sticky="n", pady=(10, 0))

        # --- Bottom Spacer ---
        bottom_spacer = ctk.CTkFrame(self, fg_color="#F3F4F6")
        bottom_spacer.grid(row=3, column=0, sticky="we")

    def handle_login(self):
        """Handle login logic"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        print(f"Username: {username}, Password: {password}")
        # Example: Navigate to next page
        # self.controller.show_frame("DashboardPage")
