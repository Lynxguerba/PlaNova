from PIL import Image   # type: ignore
import customtkinter as ctk  # type: ignore
from datetime import datetime
import uuid
import json
import os

class CreateTaskModal(ctk.CTkToplevel):
    def __init__(self, parent, task_data=None):
        super().__init__(parent)
        
        self.result = None
        self.task_data = task_data  # Store task data for editing
        self.is_edit_mode = task_data is not None
        self.parent = parent
        
        # Track selected users
        self.selected_users = []
        self.user_checkboxes = {}
        
        # Configure modal
        self.title("Edit Task" if self.is_edit_mode else "Create New Task")
        self.geometry("500x800")
        self.resizable(False, False)
        
        # Make it transient first
        self.transient(parent)
        
        # Center the modal
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (800 // 2)
        self.geometry(f"500x800+{x}+{y}")
        
        # Make it modal after window is ready
        self.after(10, self._set_modal)
        
        # Configure colors
        self.configure(fg_color="#FFFFFF")
        
        # Load available users
        self.available_users = self.load_available_users()
        
        # Create content
        self.create_content()
        
        # If editing, populate fields
        if self.is_edit_mode:
            self.populate_fields()
    
    def _set_modal(self):
        """Set modal behavior after window is viewable"""
        try:
            self.grab_set()
            self.focus_set()
        except Exception as e:
            print(f"\033[91m [-] Could not set modal: {e}")
    
    def load_available_users(self):
        """Load all users except current user from JSON"""
        try:
            file_path = "data/preferences.json"
            
            if not os.path.exists(file_path):
                return []
            
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            users = data.get("users", [])
            
            # Get current user from parent's controller
            current_username = None
            if hasattr(self.parent, 'controller') and hasattr(self.parent.controller, 'current_user'):
                current_username = self.parent.controller.current_user.get('username')
            
            # Return all usernames except current user
            available = [u['username'] for u in users if u['username'] != current_username]
            print(f"\033[92m [+] Available users for invitation: {available}")
            return available
            
        except Exception as e:
            print(f"\033[91m [!] Error loading users: {e}")
            return []
    
    def create_content(self):
        # Main scrollable container
        main_container = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            scrollbar_button_color="#E5E7EB",
            scrollbar_button_hover_color="#D1D5DB"
        )
        main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Header
        header = ctk.CTkLabel(
            main_container,
            text="Edit Task" if self.is_edit_mode else "Create New Task",
            font=("Poppins SemiBold", 24),
            text_color="#111827"
        )
        header.pack(pady=(0, 20))
        
        # Title field
        title_label = ctk.CTkLabel(
            main_container,
            text="Title",
            font=("Poppins Medium", 14),
            text_color="#374151",
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 5))
        
        self.title_entry = ctk.CTkEntry(
            main_container,
            height=45,
            font=("Poppins", 13),
            placeholder_text="Enter task title",
            fg_color="#F9FAFB",
            border_color="#E5E7EB",
            border_width=1
        )
        self.title_entry.pack(fill="x", pady=(0, 15))
        
        # Description field
        desc_label = ctk.CTkLabel(
            main_container,
            text="Description",
            font=("Poppins Medium", 14),
            text_color="#374151",
            anchor="w"
        )
        desc_label.pack(fill="x", pady=(0, 5))
        
        self.description_textbox = ctk.CTkTextbox(
            main_container,
            height=100,
            font=("Poppins", 13),
            fg_color="#F9FAFB",
            border_color="#E5E7EB",
            border_width=1
        )
        self.description_textbox.pack(fill="x", pady=(0, 15))
        
        # Time picker section
        time_label = ctk.CTkLabel(
            main_container,
            text="Due Time (Optional)",
            font=("Poppins Medium", 14),
            text_color="#374151",
            anchor="w"
        )
        time_label.pack(fill="x", pady=(0, 5))
        
        # Time picker frame
        time_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        time_frame.pack(fill="x", pady=(0, 15))
        
        # Hour picker
        hour_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        hour_frame.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            hour_frame,
            text="Hour",
            font=("Poppins", 11),
            text_color="#6B7280"
        ).pack()
        
        self.hour_spinbox = ctk.CTkOptionMenu(
            hour_frame,
            values=[f"{i:02d}" for i in range(24)],
            width=80,
            height=40,
            fg_color="#F9FAFB",
            button_color="#3B82F6",
            button_hover_color="#2563EB",
            dropdown_fg_color="#FFFFFF",
            font=("Poppins", 13),
            text_color="#111827"
        )
        self.hour_spinbox.set(f"{datetime.now().hour:02d}")
        self.hour_spinbox.pack(pady=(5, 0))
        
        # Minute picker
        minute_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        minute_frame.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            minute_frame,
            text="Minute",
            font=("Poppins", 11),
            text_color="#6B7280"
        ).pack()
        
        self.minute_spinbox = ctk.CTkOptionMenu(
            minute_frame,
            values=[f"{i:02d}" for i in range(0, 60, 5)],
            width=80,
            height=40,
            fg_color="#F9FAFB",
            button_color="#3B82F6",
            button_hover_color="#2563EB",
            dropdown_fg_color="#FFFFFF",
            font=("Poppins", 13),
            text_color="#111827"
        )
        self.minute_spinbox.set(f"{(datetime.now().minute // 5) * 5:02d}")
        self.minute_spinbox.pack(pady=(5, 0))
        
        # Invite Users section - only hide for shared tasks (tasks created by others)
        show_invite = True
        if self.is_edit_mode and self.task_data.get('is_shared'):
            show_invite = False  # Can't modify shared tasks (tasks you received)
        
        if show_invite:
            invite_label = ctk.CTkLabel(
                main_container,
                text="Invite Users (Optional)",
                font=("Poppins Medium", 14),
                text_color="#374151",
                anchor="w"
            )
            invite_label.pack(fill="x", pady=(0, 5))
            
            # User selection with checkboxes
            if self.available_users:
                # Container for user checkboxes with border
                users_container = ctk.CTkFrame(
                    main_container,
                    fg_color="#F9FAFB",
                    border_color="#E5E7EB",
                    border_width=1,
                    corner_radius=8
                )
                users_container.pack(fill="x", pady=(0, 10))
                
                # Scrollable frame for many users
                users_scroll = ctk.CTkScrollableFrame(
                    users_container,
                    fg_color="transparent",
                    height=150,
                    scrollbar_button_color="#D1D5DB",
                    scrollbar_button_hover_color="#9CA3AF"
                )
                users_scroll.pack(fill="both", expand=True, padx=10, pady=10)
                
                # Create checkbox for each user
                for username in self.available_users:
                    user_frame = ctk.CTkFrame(users_scroll, fg_color="transparent")
                    user_frame.pack(fill="x", pady=5)
                    
                    var = ctk.BooleanVar()
                    checkbox = ctk.CTkCheckBox(
                        user_frame,
                        text=f"@{username}",
                        variable=var,
                        font=("Poppins", 13),
                        text_color="#374151",
                        fg_color="#3B82F6",
                        hover_color="#2563EB",
                        border_color="#D1D5DB",
                        command=lambda u=username, v=var: self.toggle_user_selection(u, v)
                    )
                    checkbox.pack(anchor="w")
                    self.user_checkboxes[username] = var
                
                # Selected users display
                self.selected_label = ctk.CTkLabel(
                    main_container,
                    text="Selected: None",
                    font=("Poppins", 11),
                    text_color="#6B7280",
                    anchor="w"
                )
                self.selected_label.pack(fill="x", pady=(0, 20))
            else:
                no_users_label = ctk.CTkLabel(
                    main_container,
                    text="No other users available to invite",
                    font=("Poppins", 11),
                    text_color="#9CA3AF",
                    anchor="w"
                )
                no_users_label.pack(fill="x", pady=(0, 20))
        else:
            if self.is_edit_mode and self.task_data.get('is_shared'):
                info_label = ctk.CTkLabel(
                    main_container,
                    text="⚠️ Cannot modify invitations for shared tasks",
                    font=("Poppins", 11),
                    text_color="#F59E0B",
                    anchor="w"
                )
                info_label.pack(fill="x", pady=(0, 20))
        
        # Buttons frame (fixed at bottom)
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", side="bottom", padx=30, pady=20)
        
        # Clear button
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="Clear",
            height=45,
            font=("Poppins Medium", 14),
            fg_color="transparent",
            border_width=2,
            border_color="#E5E7EB",
            text_color="#6B7280",
            hover_color="#F3F4F6",
            command=self.clear_inputs
        )
        clear_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Create/Update button
        action_btn = ctk.CTkButton(
            buttons_frame,
            text="Update Task" if self.is_edit_mode else "Create Task",
            height=45,
            font=("Poppins SemiBold", 14),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white",
            command=self.create_task
        )
        action_btn.pack(side="left", fill="x", expand=True)
    
    def toggle_user_selection(self, username, var):
        """Handle user checkbox toggle"""
        if var.get():
            if username not in self.selected_users:
                self.selected_users.append(username)
        else:
            if username in self.selected_users:
                self.selected_users.remove(username)
        
        # Update selected label
        if self.selected_users:
            selected_text = ", ".join([f"@{u}" for u in self.selected_users])
            self.selected_label.configure(text=f"Selected: {selected_text}")
        else:
            self.selected_label.configure(text="Selected: None")
        
        print(f"\033[92m [+] Selected users: {self.selected_users}")
    
    def populate_fields(self):
        """Populate fields with existing task data"""
        if self.task_data:
            # Set title
            self.title_entry.insert(0, self.task_data.get('title', ''))
            
            # Set description
            if self.task_data.get('description'):
                self.description_textbox.insert("1.0", self.task_data.get('description'))
            
            # Set time if available
            if self.task_data.get('time'):
                time_parts = self.task_data['time'].split(':')
                if len(time_parts) == 2:
                    self.hour_spinbox.set(time_parts[0])
                    self.minute_spinbox.set(time_parts[1])
            
            # Set invited users if available
            if self.user_checkboxes and self.task_data.get('invited_users'):
                invited_users = self.task_data.get('invited_users', [])
                for username in invited_users:
                    if username in self.user_checkboxes:
                        self.user_checkboxes[username].set(True)
                        self.selected_users.append(username)
                
                # Update selected label
                if self.selected_users:
                    selected_text = ", ".join([f"@{u}" for u in self.selected_users])
                    self.selected_label.configure(text=f"Selected: {selected_text}")
            # Backward compatibility: check for old single invited_user field
            elif self.user_checkboxes and self.task_data.get('invited_user'):
                old_invited = self.task_data.get('invited_user')
                if old_invited in self.user_checkboxes:
                    self.user_checkboxes[old_invited].set(True)
                    self.selected_users.append(old_invited)
                    self.selected_label.configure(text=f"Selected: @{old_invited}")
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.title_entry.delete(0, "end")
        self.description_textbox.delete("1.0", "end")
        self.hour_spinbox.set(f"{datetime.now().hour:02d}")
        self.minute_spinbox.set(f"{(datetime.now().minute // 5) * 5:02d}")
        
        # Clear all checkboxes
        for var in self.user_checkboxes.values():
            var.set(False)
        self.selected_users.clear()
        if hasattr(self, 'selected_label'):
            self.selected_label.configure(text="Selected: None")
        
        print("\033[93m [*] Inputs cleared")
    
    def create_task(self):
        """Validate and create/update task"""
        title = self.title_entry.get().strip()
        description = self.description_textbox.get("1.0", "end").strip()
        hour = self.hour_spinbox.get()
        minute = self.minute_spinbox.get()
        
        if not title:
            # Show error - title is required
            self.show_error("Title is required!")
            return
        
        # Store result
        if self.is_edit_mode:
            # Update existing task
            self.result = {
                **self.task_data,  # Keep existing fields
                "title": title,
                "description": description,
                "time": f"{hour}:{minute}" if hour and minute else None,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Handle invitation logic for edit mode
            if self.user_checkboxes and not self.task_data.get('is_shared'):
                # Only allow inviting for tasks you own (not shared tasks)
                old_invited_users = self.task_data.get('invited_users', [])
                # Backward compatibility
                if not old_invited_users and self.task_data.get('invited_user'):
                    old_invited_users = [self.task_data.get('invited_user')]
                
                new_invited_users = self.selected_users.copy()
                
                # Update invited_users field
                self.result["invited_users"] = new_invited_users
                
                # Find newly invited users
                newly_invited = [u for u in new_invited_users if u not in old_invited_users]
                
                # Create shared tasks for newly invited users
                if newly_invited:
                    current_username = self.get_current_username()
                    for username in newly_invited:
                        success = self.create_shared_task(
                            username, 
                            self.task_data['id'],
                            title, 
                            description, 
                            f"{hour}:{minute}" if hour and minute else None,
                            current_username
                        )
                        if success:
                            print(f"\033[92m [✓] New invitation sent to {username}")
                        else:
                            print(f"\033[91m [✗] Failed to send invitation to {username}")
            
            print(f"\033[92m [+] Task updated: {self.result}")
        else:
            # Create new task
            task_id = str(uuid.uuid4())
            current_username = self.get_current_username()
            
            self.result = {
                "id": task_id,
                "title": title,
                "description": description,
                "time": f"{hour}:{minute}" if hour and minute else None,
                "invited_users": self.selected_users.copy(),
                "invited_by": current_username,
                "is_shared": False,  # This is the original task, not a shared copy
                "completed": False,
                "deleted": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_upcoming": False  # Ensure it's marked as NOT upcoming
            }
            print(f"\033[92m [+] Task created: {self.result}")
            
            # Create shared copies for all invited users
            if self.selected_users:
                for username in self.selected_users:
                    success = self.create_shared_task(
                        username, 
                        task_id, 
                        title, 
                        description, 
                        f"{hour}:{minute}" if hour and minute else None, 
                        current_username
                    )
                    if success:
                        print(f"\033[92m [✓] Shared task successfully created for {username}")
                    else:
                        print(f"\033[91m [✗] Failed to create shared task for {username}")
        
        self.destroy()
    
    def get_current_username(self):
        """Get current logged-in username"""
        if hasattr(self.parent, 'controller') and hasattr(self.parent.controller, 'current_user'):
            return self.parent.controller.current_user.get('username')
        return None
    
    def create_shared_task(self, invited_username, original_task_id, title, description, time, invited_by):
        """Create a shared copy of the task for the invited user"""
        try:
            file_path = "data/preferences.json"
            
            # Read the current data
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Find the invited user
            user_found = False
            for user in data.get('users', []):
                if user.get('username') == invited_username:
                    user_found = True
                    
                    # Create shared task
                    shared_task = {
                        "id": str(uuid.uuid4()),  # New unique ID for shared copy
                        "original_task_id": original_task_id,  # Reference to original
                        "title": title,
                        "description": description,
                        "time": time,
                        "invited_by": invited_by,
                        "is_shared": True,  # Mark as shared copy
                        "completed": False,
                        "deleted": False,
                        "is_upcoming": False,  # Regular task, not upcoming
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Initialize tasks array if it doesn't exist
                    if "tasks" not in user:
                        user["tasks"] = []
                    
                    # Add to invited user's tasks
                    user["tasks"].append(shared_task)
                    
                    print(f"\033[92m [+] Shared task added to {invited_username}'s task list")
                    break
            
            if not user_found:
                print(f"\033[91m [!] User {invited_username} not found in database")
                return False
            
            # Save back to file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"\033[92m [✓] Shared task saved to JSON for user: {invited_username}")
            return True
                    
        except Exception as e:
            print(f"\033[91m [!] Error creating shared task: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def show_error(self, message):
        """Show error message"""
        error_label = ctk.CTkLabel(
            self,
            text=message,
            font=("Poppins", 12),
            text_color="#EF4444"
        )
        error_label.place(relx=0.5, rely=0.95, anchor="center")
        
        # Remove error after 3 seconds
        self.after(3000, error_label.destroy)
