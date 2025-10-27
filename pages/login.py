import customtkinter as ctk  # type: ignore
import json
import os
from pathlib import Path
import hashlib

class LoginPage(ctk.CTkFrame):
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D4E3FF")
        self.controller = controller

        # --- Grid layout ---
        self.grid_rowconfigure((0, 6), weight=1)
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
        )
        self.password_entry.pack(padx=40, pady=(0, 12))

        # --- Error message label ---
        self.error_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(family="Poppins", size=12),
            text_color="#DC2626"
        )
        self.error_label.pack(pady=(0, 10))

        # --- Login Button ---
        self.login_btn = ctk.CTkButton(
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
        self.login_btn.grid(row=4, column=0, sticky="n", pady=(10, 25))
        
        # --- "Create an account" Text ---
        create_account_label = ctk.CTkLabel(
            self,
            text="Create an account",
            text_color="#1E3A8A",
            font=ctk.CTkFont(family="Poppins", size=18, underline=True),
            cursor="hand2"
        )
        create_account_label.grid(row=5, column=0, sticky="n")
        
        def open_register(event):
            self.clear_fields()
            self.controller.show_frame("RegisterPage")
            print("\033[93m [+] Redirecting to Registration Page...")

        create_account_label.bind("<Button-1>", open_register)
        create_account_label.bind("<Enter>", lambda e: create_account_label.configure(text_color="#3B82F6"))
        create_account_label.bind("<Leave>", lambda e: create_account_label.configure(text_color="#1E3A8A"))

        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda e: self.handle_login())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())

    def hash_password(self, password):
        """Hash password using SHA256 to match registration"""
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        """Load users from JSON file"""
        try:
            file_path = "data/preferences.json"
            
            if not os.path.exists(file_path):
                print("\033[91m [!] Error: preferences.json file not found")
                return {"users": []}
            
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except json.JSONDecodeError:
            print("\033[91m [!] Error: Invalid JSON format")
            return {"users": []}
        except Exception as e:
            print(f"\033[91m [!] Error loading users: {str(e)}")
            return {"users": []}

    def validate_fields(self):
        """Validate input fields"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username:
            self.show_error("Please enter your username")
            return False
        
        if not password:
            self.show_error("Please enter your password")
            return False
        
        return True

    def authenticate_user(self, username, password):
        """Authenticate user against stored credentials"""
        data = self.load_users()
        users = data.get("users", [])
        
        # Hash the input password
        hashed_password = self.hash_password(password)
        
        # Search for user in the list
        for user in users:
            if user.get("username") == username:
                # Compare hashed passwords
                if user.get("password") == hashed_password:
                    return True, user
                else:
                    return False, None
        
        return False, None

    def show_error(self, message):
        """Display error message"""
        self.error_label.configure(text=message)
        
        # Reset entry borders to indicate error
        self.username_entry.configure(border_color="#DC2626", border_width=2)
        self.password_entry.configure(border_color="#DC2626", border_width=2)
        
        # Reset borders after 3 seconds
        self.after(3000, self.reset_entry_borders)

    def reset_entry_borders(self):
        """Reset entry field borders"""
        self.username_entry.configure(border_width=0)
        self.password_entry.configure(border_width=0)
        self.error_label.configure(text="")

    def clear_fields(self):
        """Clear all input fields and error messages"""
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.error_label.configure(text="")
        self.reset_entry_borders()

    def handle_login(self):
        """Handle login button click"""
        # Validate fields first
        if not self.validate_fields():
            return
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        print(f"\033[93m [+] Attempting login for user: {username}")
        
        # Disable login button during authentication
        self.login_btn.configure(state="disabled", text="Logging in...")
        
        # Authenticate user
        is_authenticated, user_data = self.authenticate_user(username, password)
        
        if is_authenticated:
            print(f"\033[92m [✓] Login successful for user: {username}")
            self.error_label.configure(text="Login successful!", text_color="#16A34A")
            
            # Wait a moment before redirecting
            self.after(500, lambda: self.redirect_to_dashboard(user_data))
        else:
            print(f"\033[91m [✗] Login failed for user: {username}")
            self.show_error("Invalid username or password")
            self.login_btn.configure(state="normal", text="Login")

    def redirect_to_dashboard(self, user_data):
        """Redirect to dashboard after successful login"""
        print(f"\033[93m [+] Redirecting to Dashboard Page...")
        
        # Store logged-in user info in controller
        self.controller.current_user = user_data
        
        # Get the dashboard frame and update user info
        dashboard_frame = self.controller.frames.get("DashboardPage")
        if dashboard_frame:
            dashboard_frame.update_user_info(user_data.get("username", "User"))
        
        self.clear_fields()
        self.login_btn.configure(state="normal", text="Login")
        self.controller.show_frame("DashboardPage")