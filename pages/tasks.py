from PIL import Image  
import customtkinter as ctk  # type: ignore
from datetime import datetime
import json
import os

from modals.create_task_modal import CreateTaskModal


class TasksPage(ctk.CTkFrame):
    def __init__(self, parent, controller=None, navigate_callback=None):
        super().__init__(parent, fg_color="#F9FAFB")
        
        # Support both controller and navigate_callback for compatibility
        self.controller = controller
        self.navigate_callback = navigate_callback or (controller.show_frame if controller else None)
        
        # Store all tasks (including completed and deleted)
        self.all_tasks = []
        # Store only active tasks for display
        self.tasks = []
        
        # Create app bar
        self.create_app_bar()
        
        # Main content area with scrollable frame (hidden scrollbar)
        self.content_container = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            scrollbar_button_color="#F9FAFB",  # Same as background - invisible
            scrollbar_button_hover_color="#E5E7EB"  # Light gray on hover
        )
        self.content_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Tasks content
        self.tasks_list_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.tasks_list_frame.pack(fill="both", expand=True)
        
        # Load and display tasks
        self.load_tasks()
        self.display_tasks()
        
        # Floating create button
        self.create_floating_button()
    
    def tkraise(self, aboveThis=None):
        """Override tkraise to refresh tasks when page is shown"""
        super().tkraise(aboveThis)
        self.refresh_tasks()
    
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
            text="Tasks",
            font=("Poppins SemiBold", 20),
            text_color="#111827"
        )
        title.pack(side="left", padx=15)
    
    def load_tasks(self):
        """Load tasks from JSON file for current user"""
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
                
                # Find user's tasks
                for user in data.get('users', []):
                    if user.get('username') == username:
                        # Load ALL tasks
                        self.all_tasks = user.get('tasks', [])
                        # Filter only active tasks for display (not deleted, not completed)
                        self.tasks = [
                            t for t in self.all_tasks 
                            if not t.get('deleted', False) and not t.get('completed', False)
                        ]
                        print(f"\033[92m [✓] Loaded {len(self.tasks)} active tasks for user: {username}")
                        return
            
            print("\033[93m [!] No current user found")
            
        except Exception as e:
            print(f"\033[91m [!] Error loading tasks: {str(e)}")
    
    def save_tasks(self):
        """Save tasks to JSON file for current user"""
        try:
            file_path = "data/preferences.json"
            
            # Load existing data
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Get current user
            if hasattr(self.controller, 'current_user'):
                username = self.controller.current_user.get('username')
                
                # Update user's tasks
                for user in data.get('users', []):
                    if user.get('username') == username:
                        user['tasks'] = self.all_tasks
                        break
                
                # Save back to file
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                
                print(f"\033[92m [✓] Tasks saved for user: {username}")
            
        except Exception as e:
            print(f"\033[91m [!] Error saving tasks: {str(e)}")
    
    def display_tasks(self):
        """Display all active tasks"""
        # Clear existing widgets
        for widget in self.tasks_list_frame.winfo_children():
            widget.destroy()
        
        if not self.tasks:
            # Show placeholder
            placeholder = ctk.CTkLabel(
                self.tasks_list_frame,
                text="No tasks yet\nClick the + button to create a task",
                font=("Poppins", 14),
                text_color="#9CA3AF",
                justify="center"
            )
            placeholder.pack(expand=True, pady=50)
        else:
            # Display each task
            for task in self.tasks:
                self.create_task_card(task)
    
    def create_task_card(self, task):
        """Create a task card widget"""
        # Main card frame
        card = ctk.CTkFrame(
            self.tasks_list_frame,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.pack(fill="x", pady=8, padx=5)
        
        # Inner container
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="both", padx=15, pady=12)
        
        # Task info
        info_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        info_frame.pack(fill="x")
        
        # Title
        title_label = ctk.CTkLabel(
            info_frame,
            text=task['title'],
            font=("Poppins SemiBold", 15),
            text_color="#111827",
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
        
        # Time
        if task.get('time'):
            time_label = ctk.CTkLabel(
                info_frame,
                text=f"⏰ Due: {task['time']}",
                font=("Poppins", 11),
                text_color="#3B82F6",
                anchor="w"
            )
            time_label.pack(fill="x", pady=(5, 0))
        
        # Buttons container at the bottom
        buttons_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(12, 0))
        
        # Edit button
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Edit",
            height=38,
            corner_radius=8,
            fg_color="#F59E0B",
            hover_color="#D97706",
            font=("Poppins Medium", 13),
            command=lambda: self.edit_task(task['id'])
        )
        edit_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        # Complete button
        complete_btn = ctk.CTkButton(
            buttons_frame,
            text="✓ Mark Complete",
            height=38,
            corner_radius=8,
            fg_color="#10B981",
            hover_color="#059669",
            font=("Poppins Medium", 13),
            command=lambda: self.mark_complete(task['id'])
        )
        complete_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        # Delete button
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️",
            height=38,
            corner_radius=8,
            fg_color="#EF4444",
            hover_color="#DC2626",
            font=("Poppins Medium", 13),
            command=lambda: self.move_to_bin(task['id'])
        )
        delete_btn.pack(side="left", fill="x", expand=True)
    
    def edit_task(self, task_id):
        """Open edit modal for a task"""
        # Find the task
        task_to_edit = None
        for task in self.all_tasks:
            if task['id'] == task_id:
                task_to_edit = task
                break
        
        if not task_to_edit:
            print(f"\033[91m [!] Task not found: {task_id}")
            return
        
        print(f"\033[92m [+] Editing task: {task_to_edit['title']}")
        
        # Open edit modal with task data
        modal = CreateTaskModal(self, task_data=task_to_edit)
        self.wait_window(modal)
        
        # Check if task was updated
        if modal.result:
            # Find and update the task in all_tasks
            for i, task in enumerate(self.all_tasks):
                if task['id'] == task_id:
                    self.all_tasks[i] = modal.result
                    break
            
            # Update in active tasks if it exists there
            for i, task in enumerate(self.tasks):
                if task['id'] == task_id:
                    self.tasks[i] = modal.result
                    break
            
            print(f"\033[92m [✓] Task updated in list: {modal.result}")
            
            # Save to JSON
            self.save_tasks()
            
            # Refresh display
            self.display_tasks()
    
    def mark_complete(self, task_id):
        """Mark task as completed"""
        # Find and update task in all_tasks
        task_found = False
        for task in self.all_tasks:
            if task['id'] == task_id:
                task['completed'] = True
                task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\033[92m [✓] Task marked as complete: {task['title']}")
                task_found = True
                break
        
        # If task not found in all_tasks, it means it's a new task only in self.tasks
        if not task_found:
            for task in self.tasks:
                if task['id'] == task_id:
                    task['completed'] = True
                    task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"\033[92m [✓] Task marked as complete: {task['title']}")
                    # Add it to all_tasks before removing from active tasks
                    self.all_tasks.append(task)
                    break
        
        # Remove from active tasks display
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        
        # Save all tasks and refresh
        self.save_tasks()
        self.display_tasks()
        
        print(f"\033[93m [DEBUG] Total tasks in all_tasks: {len(self.all_tasks)}")
        print(f"\033[93m [DEBUG] Active tasks: {len(self.tasks)}")
    
    def move_to_bin(self, task_id):
        """Move task to bin"""
        # Find and update task in all_tasks
        task_found = False
        for task in self.all_tasks:
            if task['id'] == task_id:
                task['deleted'] = True
                task['deleted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\033[93m [!] Task moved to bin: {task['title']}")
                task_found = True
                break
        
        # If task not found in all_tasks, it means it's a new task only in self.tasks
        if not task_found:
            for task in self.tasks:
                if task['id'] == task_id:
                    task['deleted'] = True
                    task['deleted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"\033[93m [!] Task moved to bin: {task['title']}")
                    # Add it to all_tasks before removing from active tasks
                    self.all_tasks.append(task)
                    break
        
        # Remove from active tasks display
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        
        # Save all tasks and refresh
        self.save_tasks()
        self.display_tasks()
        
        print(f"\033[93m [DEBUG] Total tasks in all_tasks: {len(self.all_tasks)}")
        print(f"\033[93m [DEBUG] Active tasks: {len(self.tasks)}")
    
    def create_floating_button(self):
        fab_container = ctk.CTkFrame(self, fg_color="transparent")
        fab_container.place(relx=1.0, rely=1.0, x=-30, y=-30, anchor="se")
        
        try:
            plus_icon = ctk.CTkImage(
                light_image=Image.open("assets/images/plus.png"),
                dark_image=Image.open("assets/images/plus.png"),
                size=(24, 24)
            )
            fab = ctk.CTkButton(
                fab_container,
                image=plus_icon,
                text="",
                width=60,
                height=60,
                corner_radius=30,
                fg_color="#3B82F6",
                hover_color="#2563EB",
                command=self.create_task
            )
        except Exception as e:
            print(f"\033[92m [-] Could not load plus icon: {e}")
            fab = ctk.CTkButton(
                fab_container,
                text="+",
                width=60,
                height=60,
                corner_radius=30,
                font=("Arial", 28),
                fg_color="#3B82F6",
                hover_color="#2563EB",
                text_color="white",     
                command=self.create_task
            )
        
        fab.pack()

    def refresh_tasks(self):
        """Refresh tasks from JSON - called when page is shown"""
        self.load_tasks()
        self.display_tasks()
        print(f"\033[92m [✓] Tasks refreshed - {len(self.tasks)} tasks loaded")
    
    def go_back(self):
        if self.navigate_callback:
            self.navigate_callback("DashboardPage")
    
    def create_task(self):
        print("\033[92m [+] Create task clicked")
        
        # Open modal                                        
        modal = CreateTaskModal(self)
        self.wait_window(modal)
        
        # Check if task was created
        if modal.result:
            # Add to active tasks
            self.tasks.append(modal.result)
            # Also add to all_tasks
            self.all_tasks.append(modal.result)
            print(f"\033[92m [+] Task added to list: {modal.result}")
            print(f"\033[93m [DEBUG] Total tasks: {len(self.all_tasks)}, Active: {len(self.tasks)}")
            
            # Save to JSON
            self.save_tasks()
            
            # Refresh display
            self.display_tasks()
