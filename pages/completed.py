import customtkinter as ctk  # type: ignore
from PIL import Image
import json
import os


class CompletedPage(ctk.CTkFrame):
    
    def __init__(self, parent, controller=None, navigate_callback=None):
        super().__init__(parent, fg_color="#F9FAFB")
        
        # Support both controller and navigate_callback for compatibility
        self.controller = controller
        self.navigate_callback = navigate_callback or (controller.show_frame if controller else None)
        
        # Store completed tasks
        self.completed_tasks = []
        
        # Create app bar
        self.create_app_bar()
        
        # Main content area with scrollable frame
        self.content_container = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            scrollbar_button_color="#F9FAFB",  # Hidden scrollbar
            scrollbar_button_hover_color="#E5E7EB"
        )
        self.content_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Completed tasks list frame
        self.tasks_list_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.tasks_list_frame.pack(fill="both", expand=True)
        
        # Load and display completed tasks
        self.load_completed_tasks()
        self.display_completed_tasks()
    
    def tkraise(self, aboveThis=None):
        """Override tkraise to refresh completed tasks when page is shown"""
        super().tkraise(aboveThis)
        self.refresh_completed_tasks()
    
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
    
    def load_completed_tasks(self):
        """Load completed tasks from JSON file for current user"""
        try:
            file_path = "data/preferences.json"
            
            if not os.path.exists(file_path):
                print("\033[91m [!] Error: preferences.json file not found")
                return
            
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Get current user
            if hasattr(self.controller, 'current_user'):
                username = self.controller.current_user.get('username')
                
                # Find user's completed tasks
                for user in data.get('users', []):
                    if user.get('username') == username:
                        all_tasks = user.get('tasks', [])
                        # Filter only completed and not deleted tasks
                        self.completed_tasks = [
                            t for t in all_tasks 
                            if t.get('completed', False) and not t.get('deleted', False)
                        ]
                        # Sort by completion date (most recent first)
                        self.completed_tasks.sort(
                            key=lambda x: x.get('completed_at', ''), 
                            reverse=True
                        )
                        print(f"\033[92m [✓] Loaded {len(self.completed_tasks)} completed tasks for user: {username}")
                        return
            
            print("\033[93m [!] No current user found")
            
        except Exception as e:
            print(f"\033[91m [!] Error loading completed tasks: {str(e)}")
    
    def display_completed_tasks(self):
        """Display all completed tasks"""
        # Clear existing widgets
        for widget in self.tasks_list_frame.winfo_children():
            widget.destroy()
        
        if not self.completed_tasks:
            # Show placeholder
            placeholder = ctk.CTkLabel(
                self.tasks_list_frame,
                text="No completed tasks yet\nComplete tasks will appear here",
                font=("Poppins", 14),
                text_color="#9CA3AF",
                justify="center"
            )
            placeholder.pack(expand=True, pady=50)
        else:
            # Display each completed task
            for task in self.completed_tasks:
                self.create_completed_task_card(task)
    
    def create_completed_task_card(self, task):
        """Create a completed task card widget (no buttons)"""
        # Main card frame with green accent to show it's completed
        card = ctk.CTkFrame(
            self.tasks_list_frame,
            fg_color="#F0FDF4",  # Light green background
            corner_radius=12,
            border_width=2,
            border_color="#10B981"  # Green border
        )
        card.pack(fill="x", pady=8, padx=5)
        
        # Inner container
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="both", padx=15, pady=12)
        
        # Completed checkmark icon at the top
        check_label = ctk.CTkLabel(
            card_content,
            text="✓",
            font=("Arial", 24, "bold"),
            text_color="#10B981",
            width=30,
            height=30
        )
        check_label.pack(anchor="w", pady=(0, 5))
        
        # Task info
        info_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        info_frame.pack(fill="x")
        
        # Title (with strikethrough effect using a line)
        title_label = ctk.CTkLabel(
            info_frame,
            text=task['title'],
            font=("Poppins SemiBold", 15),
            text_color="#059669",
            anchor="w"
        )
        title_label.pack(fill="x")
        
        # Description
        if task.get('description'):
            desc_label = ctk.CTkLabel(
                info_frame,
                text=task['description'],
                font=("Poppins", 12),
                text_color="#6B7280",
                anchor="w",
                wraplength=600,
                justify="left"
            )
            desc_label.pack(fill="x", pady=(3, 0))
        
        # Time (if exists)
        if task.get('time'):
            time_label = ctk.CTkLabel(
                info_frame,
                text=f"⏰ Was due: {task['time']}",
                font=("Poppins", 11),
                text_color="#6B7280",
                anchor="w"
            )
            time_label.pack(fill="x", pady=(5, 0))
        
        # Completed timestamp
        if task.get('completed_at'):
            completed_label = ctk.CTkLabel(
                info_frame,
                text=f"✓ Completed on: {task['completed_at']}",
                font=("Poppins", 11),
                text_color="#10B981",
                anchor="w"
            )
            completed_label.pack(fill="x", pady=(5, 0))
    
    def refresh_completed_tasks(self):
        """Refresh completed tasks from JSON - called when page is shown"""
        self.load_completed_tasks()
        self.display_completed_tasks()
        print(f"\033[92m [✓] Completed tasks refreshed - {len(self.completed_tasks)} tasks loaded")

    def go_back(self):
        if self.navigate_callback:
            self.navigate_callback("DashboardPage")