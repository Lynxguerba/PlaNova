import customtkinter as ctk  # type: ignore
# from components.button import CustomButton

class BinPage(ctk.CTkFrame):
    
    # UI
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D4E3FF")
        self.controller = controller

        # --- Grid layout ---
        self.grid_rowconfigure((0, 5), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Title ---
        title = ctk.CTkLabel(
            self,
            text="Welcome!",
            font=ctk.CTkFont(family="Poppins", size=36, weight="bold"),
            text_color="#1E3A8A"
        )
        title.grid(row=1, column=0, sticky="n", pady=(40, 0))

        subtitle = ctk.CTkLabel(
            self,
            text="Sign in to your account",
            font=ctk.CTkFont(family="Poppins", size=18),
            text_color="#4B5563"
        )
        subtitle.grid(row=2, column=0, sticky="n", pady=(5, 15))

        # --- Form container ---
        form_frame = ctk.CTkFrame(self, fg_color="#D4E3FF")
        form_frame.grid(row=3, column=0, sticky="n")

        entry_width = 400
        entry_height = 55

        # Username
        username_label = ctk.CTkLabel(
            form_frame,
            text="Username",
            font=ctk.CTkFont(family="Poppins", size=14),
            text_color="#1E3A8A"
        )
        username_label.pack(anchor="w", padx=40, pady=(5, 3))

        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your username",
            width=entry_width,
            height=entry_height,
            corner_radius=12,
            border_width=0,
            font=ctk.CTkFont(family="Poppins", size=14),
            # fg_color="#E6E6E6"
        )
        self.username_entry.pack(padx=40, pady=(0, 12))

        # Password
        password_label = ctk.CTkLabel(
            form_frame,
            text="Password",
            font=ctk.CTkFont(family="Poppins", size=14),
            text_color="#1E3A8A"
        )
        password_label.pack(anchor="w", padx=40, pady=(0, 3))

        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your password",
            width=entry_width,
            height=entry_height,
            corner_radius=12,
            border_width=0,
            font=ctk.CTkFont(family="Poppins", size=14),
            show="•",
            # fg_color="#E6E6E6"
        )
        self.password_entry.pack(padx=40, pady=(0, 25))

        # --- Login Button ---
        login_btn = ctk.CTkButton(
            self,
            text="Login",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="white",
            font=ctk.CTkFont(family="Poppins", size=20, weight="bold"),
            corner_radius=12,
            height=65,
            width=400,
            command=self.handle_login
        )
        login_btn.grid(row=4, column=0, sticky="n", pady=(10, 25))
        
        # --- "Create an account" Text ---
        create_account_label = ctk.CTkLabel(
            self,
            text="Create an account",
            text_color="#1E3A8A",
            font=ctk.CTkFont(family="Poppins", size=18, underline=True)
        )
        create_account_label.grid(row=5, column=0, sticky="n")
        
        def open_register(event):
            self.controller.show_frame("RegisterPage")
            print("Redirecting to registration page...")

        create_account_label.bind("<Button-1>", open_register)
        create_account_label.bind("<Enter>", lambda e: create_account_label.configure(text_color="#3B82F6"))
        create_account_label.bind("<Leave>", lambda e: create_account_label.configure(text_color="#1E3A8A"))



    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Username: {username}, Password: {password}")
        self.controller.show_frame("DashboardPage")
        
        


