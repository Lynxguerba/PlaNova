import customtkinter as ctk  # type: ignore
import json
import os
import hashlib

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D4E3FF")
        self.controller = controller

        # --- Grid layout ---
        self.grid_rowconfigure((0, 5), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Title ---
        title = ctk.CTkLabel(
            self,
            text="Sign Up!",
            font=ctk.CTkFont(family="Poppins", size=36, weight="bold"),
            text_color="#1E3A8A"
        )
        title.grid(row=1, column=0, sticky="n", pady=(40, 0))

        subtitle = ctk.CTkLabel(
            self,
            text="Create your Account!",
            font=ctk.CTkFont(family="Poppins", size=18),
            text_color="#4B5563"
        )
        subtitle.grid(row=2, column=0, sticky="n", pady=(5, 15))

        # --- Form container ---
        form_frame = ctk.CTkFrame(self, fg_color="#D4E3FF")
        form_frame.grid(row=3, column=0, sticky="n")

        entry_width = 400
        entry_height = 55

        # Email
        email_label = ctk.CTkLabel(
            form_frame,
            text="Email",
            font=ctk.CTkFont(family="Poppins", size=14),
            text_color="#1E3A8A"
        )
        email_label.pack(anchor="w", padx=40, pady=(5, 3))

        self.email_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your email",
            width=entry_width,
            height=entry_height,
            corner_radius=12,
            border_width=0,
            font=ctk.CTkFont(family="Poppins", size=14),
        )
        self.email_entry.pack(padx=40, pady=(0, 12))
        
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

        # --- Error/Success message label ---
        self.message_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(family="Poppins", size=12),
            text_color="#DC2626"
        )
        self.message_label.pack(pady=(0, 10))

        # --- Create Button ---
        self.create_btn = ctk.CTkButton(
            self,
            text="Create",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="white",
            font=ctk.CTkFont(family="Poppins", size=20, weight="bold"),
            corner_radius=12,
            height=65,
            width=400,
            command=self.handle_register
        )
        self.create_btn.grid(row=4, column=0, sticky="n", pady=(10, 25))
        
        # --- "Sign In Account" Text ---
        sign_in_label = ctk.CTkLabel(
            self,
            text="Sign In Account",
            text_color="#1E3A8A",
            font=ctk.CTkFont(family="Poppins", size=18, underline=True),
            cursor="hand2"
        )
        sign_in_label.grid(row=5, column=0, sticky="n")
        
        def open_login(event):
            self.clear_fields()
            self.controller.show_frame("LoginPage")
            print("\033[93m [+] Redirecting to Login Page...")

        sign_in_label.bind("<Button-1>", open_login)
        sign_in_label.bind("<Enter>", lambda e: sign_in_label.configure(text_color="#3B82F6"))
        sign_in_label.bind("<Leave>", lambda e: sign_in_label.configure(text_color="#1E3A8A"))

        # Bind Enter key to register
        self.email_entry.bind("<Return>", lambda e: self.handle_register())
        self.username_entry.bind("<Return>", lambda e: self.handle_register())
        self.password_entry.bind("<Return>", lambda e: self.handle_register())

    def show_error(self, message):
        """Display error message"""
        self.message_label.configure(text=message, text_color="#DC2626")
        
        # Reset entry borders to indicate error
        self.email_entry.configure(border_color="#DC2626", border_width=2)
        self.username_entry.configure(border_color="#DC2626", border_width=2)
        self.password_entry.configure(border_color="#DC2626", border_width=2)
        
        # Reset borders after 3 seconds
        self.after(3000, self.reset_entry_borders)

    def show_success(self, message):
        """Display success message"""
        self.message_label.configure(text=message, text_color="#16A34A")

    def reset_entry_borders(self):
        """Reset entry field borders"""
        self.email_entry.configure(border_width=0)
        self.username_entry.configure(border_width=0)
        self.password_entry.configure(border_width=0)
        self.message_label.configure(text="")

    def clear_fields(self):
        """Clear all input fields and messages"""
        self.email_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.message_label.configure(text="")
        self.reset_entry_borders()

    def validate_inputs(self, email, username, password):
        """Validate that all fields are filled"""
        if not email.strip():
            self.show_error("Email is required!")
            return False
        if not username.strip():
            self.show_error("Username is required!")
            return False
        if not password.strip():
            self.show_error("Password is required!")
            return False
        
        # Basic email validation
        if "@" not in email or "." not in email:
            self.show_error("Please enter a valid email address!")
            return False
        
        return True

    def hash_password(self, password):
        """Hash password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        """Load existing users from JSON file"""
        file_path = "data/preferences.json"
        
        # Create directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Create file if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump({"users": []}, f, indent=4)
            return {"users": []}
        
        # Load existing data
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"users": []}

    def save_user(self, email, username, password):
        """Save user data to JSON file"""
        data = self.load_users()
        
        # Check if username or email already exists
        for user in data["users"]:
            if user["username"] == username:
                self.show_error("Username already exists!")
                return False
            if user["email"] == email:
                self.show_error("Email already registered!")
                return False
        
        # Add new user
        new_user = {
            "email": email,
            "username": username,
            "password": self.hash_password(password)
        }
        data["users"].append(new_user)
        
        # Save to file
        file_path = "data/preferences.json"
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        return True

    def handle_register(self):
        """Handle registration process"""
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validate inputs
        if not self.validate_inputs(email, username, password):
            return
        
        # Disable create button during registration
        self.create_btn.configure(state="disabled", text="Creating...")
        
        # Save user data
        print(f"\033[93m [+] Email: {email}, Username: {username}")
        
        if self.save_user(email, username, password):
            print("\033[92m [+] User registered successfully!")
            self.show_success("Account created successfully!")
            
            # Wait a moment before redirecting
            self.after(1000, lambda: self.redirect_to_login())
        else:
            print("\033[91m [!] Registration failed!")
            self.create_btn.configure(state="normal", text="Create")

    def redirect_to_login(self):
        """Redirect to login page after successful registration"""
        self.clear_fields()
        self.create_btn.configure(state="normal", text="Create")
        self.controller.show_frame("LoginPage")
        print("\033[93m [+] Redirecting to Login Page...")