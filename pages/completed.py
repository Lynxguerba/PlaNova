import customtkinter as ctk  # type: ignore
from PIL import Image

class CompletedPage(ctk.CTkFrame):
    
    def __init__(self, parent, controller=None, navigate_callback=None):
        super().__init__(parent, fg_color="#F9FAFB")
        
        # Support both controller and navigate_callback for compatibility
        self.controller = controller
        self.navigate_callback = navigate_callback or (controller.show_frame if controller else None)
        
        # Create app bar
        self.create_app_bar()
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
     
    
    def create_app_bar(self):
        app_bar = ctk.CTkFrame(self, fg_color="#F9FAFB", height=100, corner_radius=0)
        app_bar.pack(fill="x", side="top")
        app_bar.pack_propagate(False)
        
        app_bar_content = ctk.CTkFrame(app_bar, fg_color="transparent")
        app_bar_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Back button
        try:
            back_icon = ctk.CTkImage(
                light_image=Image.open("assets/images/back.png"),
                dark_image=Image.open("assets/images/back.png"),
                size=(50, 50)
            )
            back_button = ctk.CTkButton(
                app_bar_content,
                image=back_icon,
                text="",
                width=40,
                height=40,
                fg_color="transparent",
                hover_color="#F3F4F6",
                corner_radius=8,
                command=lambda: (print("\033[92m [+] Back Button Clicked"), self.go_back())
            )
        except Exception as e:
            print(f"\033[91m [-] Could not load back icon: {e}")
            back_button = ctk.CTkButton(
                app_bar_content,
                text="←",
                width=30,
                height=30,
                font=("Arial", 20),
                fg_color="transparent",
                hover_color="#F3F4F6",
                text_color="#374151",
                corner_radius=8,
                command=self.go_back
            )
        
        back_button.pack(side="left")
        
        title = ctk.CTkLabel(
            app_bar_content,
            text="Completed Tasks",
            font=("Poppins SemiBold", 20),
            text_color="#111827"
        )
        title.pack(side="left", padx=15)
    
    def create_tasks_content(self):
        
        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="No tasks yet completed tasks",
            font=("Poppins", 14),
            text_color="#9CA3AF",
            justify="center"
        )
        placeholder.pack(expand=True)

    def go_back(self):
        if self.navigate_callback:
            self.navigate_callback("DashboardPage")

