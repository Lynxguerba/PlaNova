import customtkinter as ctk  # type: ignore
from PIL import Image  # type: ignore


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D4E3FF")
        self.controller = controller

        # === GRID CONFIGURATION ===
        self.grid_rowconfigure((1, 10), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # === APP BAR (TOP AREA) ===
        self.appbar = ctk.CTkFrame(self, fg_color="#D4E3FF", height=60)
        self.appbar.grid(row=0, column=0, sticky="new")  # fixed top
        self.appbar.grid_propagate(False)

        # --- Back Button (Image Icon Only) ---
        back_icon = ctk.CTkImage(
            light_image=Image.open("assets/images/back.png"),
            dark_image=Image.open("assets/images/back.png"),
            size=(50, 50)
        )

        back_btn = ctk.CTkButton(
            self.appbar,
            image=back_icon,
            text="",  # no text
            width=50,
            height=50,
            corner_radius=15,
            fg_color="transparent",
            hover_color="#D4E3FF",
            command=lambda: (print("\033[92m [+] Back Button Clicked"), controller.show_frame("DashboardPage"))
        )
        back_btn.pack(side="left", padx=12, pady=10)

        # === MAIN CONTENT ===
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=30, pady=(10, 30))
        content.grid_propagate(True)

        # --- Profile Circle (Centered) ---
        profile_frame = ctk.CTkFrame(content, fg_color="#92BAFF", corner_radius=100, width=100, height=100)
        profile_frame.pack(pady=(30, 10))
        profile_frame.pack_propagate(False)

        profile_label = ctk.CTkLabel(profile_frame, text="D", font=("Poppins Bold", 40), text_color="#1E3A8A")
        profile_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- Info Section ---
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(pady=10, fill="x")

        # Email
        email_label = ctk.CTkLabel(info_frame, text="Email", font=("Poppins SemiBold", 18), text_color="#374151")
        email_label.pack(anchor="w", pady=(5, 2))
        email_value = ctk.CTkLabel(info_frame, text="dinnomguerba@gmail.com", font=("Poppins", 16), text_color="#6B7280")
        email_value.pack(anchor="w")

        # Username
        username_label = ctk.CTkLabel(info_frame, text="Username", font=("Poppins SemiBold", 18), text_color="#374151")
        username_label.pack(anchor="w", pady=(10, 2))
        username_value = ctk.CTkLabel(info_frame, text="dnguerba", font=("Poppins", 16), text_color="#6B7280")
        username_value.pack(anchor="w")

        # Password
        password_label = ctk.CTkLabel(info_frame, text="Password", font=("Poppins SemiBold", 18), text_color="#374151")
        password_label.pack(anchor="w", pady=(10, 2))

        password_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        password_frame.pack(anchor="w")

        self.password_hidden = True
        self.password_value = ctk.CTkLabel(password_frame, text="********", font=("Poppins", 16), text_color="#6B7280")
        self.password_value.pack(side="left", padx=(0, 8))

        toggle_button = ctk.CTkButton(
            password_frame,
            text="👁️",
            width=25,
            height=25,
            fg_color="transparent",
            hover_color="#E5E7EB",
            text_color="#374151",
            corner_radius=8,
            command=self.toggle_password
        )
        toggle_button.pack(side="left")

        # --- Logout Button (Full-width + margin) ---
        logout_button = ctk.CTkButton(
            content,
            text="Logout",
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            font=("Poppins Bold", 15),
            corner_radius=10,
            width=400,
            height=55,
            command=lambda: (print("\033[91m [+] Logout account"),controller.show_frame("LoginPage"))
        )
        logout_button.pack(pady=(40, 10))

    # === PASSWORD TOGGLE FUNCTION ===
    def toggle_password(self):
        if self.password_hidden:
            self.password_value.configure(text="dnguerba1215")  # example visible password
        else:
            self.password_value.configure(text="********")
        self.password_hidden = not self.password_hidden
