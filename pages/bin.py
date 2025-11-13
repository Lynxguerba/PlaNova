from PIL import Image   # type: ignore
import customtkinter as ctk  # type: ignore
import json
import os


class BinPage(ctk.CTkFrame):
    
    def __init__(self, parent, controller=None, navigate_callback=None):
        super().__init__(parent, fg_color="#F9FAFB")
        
        # Support both controller and navigate_callback for compatibility
        self.controller = controller
        self.navigate_callback = navigate_callback or (controller.show_frame if controller else None)
        
        # Store deleted tasks
        self.deleted_tasks = []
        
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
        
        # Deleted tasks list frame
        self.tasks_list_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.tasks_list_frame.pack(fill="both", expand=True)
        
        # Load and display deleted tasks
        self.load_deleted_tasks()
        self.display_deleted_tasks()
        
        # Floating empty bin button
        self.delete_floating_button()
        
        # --- Hidden spacer at bottom for padding ---
        bottom_spacer = ctk.CTkFrame(
            self.content_container, 
            fg_color="transparent", 
            height=50
        )
        bottom_spacer.pack(pady=(0, 30))
    
    
    # Override tkraise to refresh deleted tasks when page is shown
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.refresh_deleted_tasks()
    
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
            text="Recycle Bin",
            font=("Poppins SemiBold", 20),
            text_color="#111827"
        )
        title.pack(side="left", padx=15)
    
    # Load deleted tasks from JSON file for current user
    def load_deleted_tasks(self):
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
                
                # Find user's deleted tasks
                for user in data.get('users', []):
                    if user.get('username') == username:
                        all_tasks = user.get('tasks', [])
                        # Filter only deleted tasks
                        self.deleted_tasks = [
                            t for t in all_tasks 
                            if t.get('deleted', False)
                        ]
                        # Sort by deletion date (most recent first)
                        self.deleted_tasks.sort(
                            key=lambda x: x.get('deleted_at', ''), 
                            reverse=True
                        )
                        print(f"\033[92m [✓] Loaded {len(self.deleted_tasks)} deleted tasks for user: {username}")
                        return
            
            print("\033[93m [!] No current user found")
            
        except Exception as e:
            print(f"\033[91m [!] Error loading deleted tasks: {str(e)}")
    
    # Update dashboard counts
    def update_dashboard_counts(self):
        """Update the dashboard counts after any change"""
        try:
            if hasattr(self.controller, 'frames'):
                dashboard = self.controller.frames.get('DashboardPage')
                if dashboard:
                    dashboard.update_task_counts()
                    print(f"\033[92m [✓] Dashboard counts updated")
        except Exception as e:
            print(f"\033[91m [!] Error updating dashboard: {str(e)}")
    
    # Display all deleted tasks
    def display_deleted_tasks(self):
        # Clear existing widgets
        for widget in self.tasks_list_frame.winfo_children():
            widget.destroy()
        
        if not self.deleted_tasks:
            # Show placeholder
            placeholder = ctk.CTkLabel(
                self.tasks_list_frame,
                text="Recycle bin is empty\nDeleted tasks will appear here",
                font=("Poppins", 14),
                text_color="#9CA3AF",
                justify="center"
            )
            placeholder.pack(expand=True, pady=50)
        else:
            # Display each deleted task
            for task in self.deleted_tasks:
                self.create_deleted_task_card(task)
    
    # Create a deleted task card widget with red styling
    def create_deleted_task_card(self, task):
        # Main card frame with red accent
        card = ctk.CTkFrame(
            self.tasks_list_frame,
            fg_color="#FEF2F2",  # Light red background
            corner_radius=12,
            border_width=2,
            border_color="#EF4444"  # Red border
        )
        card.pack(fill="x", pady=8, padx=5)
        
        # Inner container
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="both", padx=15, pady=12)
        
        # Deleted trash icon at the top
        trash_label = ctk.CTkLabel(
            card_content,
            text="🗑",
            font=("Arial", 24),
            text_color="#EF4444",
            width=30,
            height=30
        )
        trash_label.pack(anchor="w", pady=(0, 5))
        
        # Task info
        info_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        info_frame.pack(fill="x")
        
        # Title
        title_label = ctk.CTkLabel(
            info_frame,
            text=task['title'],
            font=("Poppins SemiBold", 15),
            text_color="#DC2626",
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
        
        # Deleted timestamp
        if task.get('deleted_at'):
            deleted_label = ctk.CTkLabel(
                info_frame,
                text=f"🗑 Deleted on: {task['deleted_at']}",
                font=("Poppins", 11),
                text_color="#EF4444",
                anchor="w"
            )
            deleted_label.pack(fill="x", pady=(5, 0))
        
        # Buttons container at the bottom
        buttons_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(12, 0))
        
        # Restore button
        restore_btn = ctk.CTkButton(
            buttons_frame,
            text="↻ Restore",
            height=38,
            corner_radius=8,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            font=("Poppins Medium", 13),
            command=lambda: self.restore_task(task['id'])
        )
        restore_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        # Permanent delete button
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="✕ Delete Forever",
            height=38,
            corner_radius=8,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=("Poppins Medium", 13),
            command=lambda: self.delete_permanently(task['id'])
        )
        delete_btn.pack(side="left", fill="x", expand=True)
    
    # Restore task back to active tasks
    def restore_task(self, task_id):
        try:
            file_path = "data/preferences.json"
            
            # Load existing data
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            if hasattr(self.controller, 'current_user'):
                username = self.controller.current_user.get('username')
                
                # Find and update the task
                for user in data.get('users', []):
                    if user.get('username') == username:
                        all_tasks = user.get('tasks', [])
                        
                        for task in all_tasks:
                            if task.get('id') == task_id:
                                # Remove deleted flags
                                task['deleted'] = False
                                if 'deleted_at' in task:
                                    del task['deleted_at']
                                print(f"\033[92m [✓] Task restored: {task['title']}")
                                break
                        
                        user['tasks'] = all_tasks
                        
                        # IMPORTANT: Update controller's current_user
                        self.controller.current_user['tasks'] = all_tasks
                        break
                
                # Save back to file
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                
                print(f"\033[92m [✓] Task restoration saved to JSON")
                
                # Update dashboard counts
                self.update_dashboard_counts()
        
        except Exception as e:
            print(f"\033[91m [!] Error restoring task: {str(e)}")
        
        # Remove from local deleted tasks list
        self.deleted_tasks = [t for t in self.deleted_tasks if t['id'] != task_id]
        
        # Refresh display
        self.display_deleted_tasks()
    
    # Permanently delete a task
    def delete_permanently(self, task_id):
        task_title = ""
        for task in self.deleted_tasks:
            if task['id'] == task_id:
                task_title = task['title']
                break
        
        # Remove from deleted tasks
        self.deleted_tasks = [t for t in self.deleted_tasks if t['id'] != task_id]
        
        # Also remove from JSON permanently
        try:
            file_path = "data/preferences.json"
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            if hasattr(self.controller, 'current_user'):
                username = self.controller.current_user.get('username')
                
                for user in data.get('users', []):
                    if user.get('username') == username:
                        # Remove task permanently
                        updated_tasks = [t for t in user.get('tasks', []) if t.get('id') != task_id]
                        user['tasks'] = updated_tasks
                        
                        # IMPORTANT: Update controller's current_user
                        self.controller.current_user['tasks'] = updated_tasks
                        break
                
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                
                print(f"\033[91m [✕] Task permanently deleted: {task_title}")
                
                # Update dashboard counts
                self.update_dashboard_counts()
        
        except Exception as e:
            print(f"\033[91m [!] Error permanently deleting task: {str(e)}")
        
        # Refresh display
        self.display_deleted_tasks()
    
    # Empty the entire bin (delete all tasks permanently)
    def empty_bin(self):
        if not self.deleted_tasks:
            print("\033[93m [!] Bin is already empty")
            return
        
        print("\033[91m [!] Emptying bin...")
        
        try:
            file_path = "data/preferences.json"
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            if hasattr(self.controller, 'current_user'):
                username = self.controller.current_user.get('username')
                
                for user in data.get('users', []):
                    if user.get('username') == username:
                        # Remove all deleted tasks
                        updated_tasks = [
                            t for t in user.get('tasks', []) 
                            if not t.get('deleted', False)
                        ]
                        user['tasks'] = updated_tasks
                        
                        # IMPORTANT: Update controller's current_user
                        self.controller.current_user['tasks'] = updated_tasks
                        break
                
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                
                print(f"\033[91m [✕] Bin emptied - {len(self.deleted_tasks)} tasks permanently deleted")
                
                # Update dashboard counts
                self.update_dashboard_counts()
        
        except Exception as e:
            print(f"\033[91m [!] Error emptying bin: {str(e)}")
        
        # Clear deleted tasks and refresh
        self.deleted_tasks = []
        self.display_deleted_tasks()
    
    def delete_floating_button(self):
        fab_container = ctk.CTkFrame(self, fg_color="transparent")
        fab_container.place(relx=1.0, rely=1.0, x=-30, y=-30, anchor="se")
        
        try:
            delete_icon = ctk.CTkImage(
                light_image=Image.open("assets/images/delete.png"),
                dark_image=Image.open("assets/images/delete.png"),
                size=(24, 24)
            )
            fab = ctk.CTkButton(
                fab_container,
                image=delete_icon,
                text="",
                width=60,
                height=60,
                corner_radius=30,
                fg_color="#EF4444",
                hover_color="#DC2626",
                command=self.empty_bin
            )
        except Exception as e:
            print(f"\033[91m [-] Could not load delete icon: {e}")
            fab = ctk.CTkButton(
                fab_container,
                text="🗑",
                width=60,
                height=60,
                corner_radius=30,
                font=("Arial", 24),
                fg_color="#EF4444",
                hover_color="#DC2626",
                text_color="white",
                command=self.empty_bin
            )
        
        fab.pack()
    
    # Refresh deleted tasks from JSON 
    def refresh_deleted_tasks(self):
        self.load_deleted_tasks()
        self.display_deleted_tasks()
        print(f"\033[92m [✓] Deleted tasks refreshed - {len(self.deleted_tasks)} tasks loaded")
    
    def go_back(self):
        if self.navigate_callback:
            self.navigate_callback("DashboardPage")
