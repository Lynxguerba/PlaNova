import customtkinter as ctk # type: ignore
from datetime import datetime
import calendar
import uuid
import json
import os
from io import BytesIO
from tkinter import filedialog
from PIL import Image # type: ignore
import base64
import cv2 # type: ignore

class CreateUpcomingTaskModal(ctk.CTkToplevel):
    def __init__(self, parent, task_data=None):
        super().__init__(parent)
        
        self.result = None
        self.task_data = task_data
        self.is_edit_mode = task_data is not None
        self.parent = parent
        
        # Track selected users
        self.selected_users = []
        self.user_checkboxes = {}
        
        # Track image
        self.selected_image_path = None
        self.selected_image_base64 = None
        self.image_preview_label = None
        
        self.camera_window = None
        self.camera_capture = None
        
        # Configure modal
        self.title("Edit Upcoming Task" if self.is_edit_mode else "Create Upcoming Task")
        self.geometry("500x900")
        self.resizable(False, False)
        
        # Make it transient first
        self.transient(parent)
        
        # Center the modal
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (900 // 2)
        self.geometry(f"500x900+{x}+{y}")
        
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
            scrollbar_button_color="#FFFFFF",
            scrollbar_button_hover_color="#D1D5DB"
        )
        main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Header
        header = ctk.CTkLabel(
            main_container,
            text="Edit Upcoming Task" if self.is_edit_mode else "Create Upcoming Task",
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
        
        # Image upload section
        image_label = ctk.CTkLabel(
            main_container,
            text="Image (Optional)",
            font=("Poppins Medium", 14),
            text_color="#374151",
            anchor="w"
        )
        image_label.pack(fill="x", pady=(0, 5))
        
        # Image upload container
        image_container = ctk.CTkFrame(
            main_container,
            fg_color="#F9FAFB",
            border_color="#E5E7EB",
            border_width=1,
            corner_radius=8
        )
        image_container.pack(fill="x", pady=(0, 15))
        
        # Buttons frame for image options
        image_buttons_frame = ctk.CTkFrame(image_container, fg_color="transparent")
        image_buttons_frame.pack(pady=10, padx=10, fill="x")
        
        # Upload button
        upload_btn = ctk.CTkButton(
            image_buttons_frame,
            text="📄 Choose Image",
            height=40,
            font=("Poppins Medium", 13),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.select_image
        )
        upload_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Camera capture button
        camera_btn = ctk.CTkButton(
            image_buttons_frame,
            text="📷 Take Photo",
            height=40,
            font=("Poppins Medium", 13),
            fg_color="#10B981",
            hover_color="#059669",
            command=self.open_camera
        )
        camera_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Image preview label
        self.image_preview_label = ctk.CTkLabel(
            image_container,
            text="No image selected",
            font=("Poppins", 11),
            text_color="#6B7280"
        )
        self.image_preview_label.pack(pady=(0, 10))
        
        # Remove image button (hidden by default)
        self.remove_image_btn = ctk.CTkButton(
            image_container,
            text="❌ Remove Image",
            height=35,
            font=("Poppins", 11),
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.remove_image
        )
      
        
        # Date picker section
        date_label = ctk.CTkLabel(
            main_container,
            text="Due Date",
            font=("Poppins Medium", 14),
            text_color="#374151",
            anchor="w"
        )
        date_label.pack(fill="x", pady=(0, 5))
        
        # Date picker frame
        date_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        date_frame.pack(fill="x", pady=(0, 15))
        
        # Year picker
        year_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        year_frame.pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            year_frame,
            text="Year",
            font=("Poppins", 11),
            text_color="#6B7280"
        ).pack()
        
        current_year = datetime.now().year
        self.year_spinbox = ctk.CTkOptionMenu(
            year_frame,
            values=[str(year) for year in range(current_year, current_year + 5)],
            width=90,
            height=40,
            fg_color="#F9FAFB",
            button_color="#3B82F6",
            button_hover_color="#2563EB",
            dropdown_fg_color="#FFFFFF",
            font=("Poppins", 13),
            command=self._update_days,
            text_color="#111827"
        )
        self.year_spinbox.set(str(current_year))
        self.year_spinbox.pack(pady=(5, 0))
        
        # Month picker
        month_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        month_frame.pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            month_frame,
            text="Month",
            font=("Poppins", 11),
            text_color="#6B7280"
        ).pack()
        
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.month_spinbox = ctk.CTkOptionMenu(
            month_frame,
            values=months,
            width=80,
            height=40,
            fg_color="#F9FAFB",
            button_color="#3B82F6",
            button_hover_color="#2563EB",
            dropdown_fg_color="#FFFFFF",
            font=("Poppins", 13),
            command=self._update_days,
            text_color="#111827"
        )
        self.month_spinbox.set(months[datetime.now().month - 1])
        self.month_spinbox.pack(pady=(5, 0))
        
        # Day picker
        day_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        day_frame.pack(side="left")
        
        ctk.CTkLabel(
            day_frame,
            text="Day",
            font=("Poppins", 11),
            text_color="#6B7280"
        ).pack()
        
        self.day_spinbox = ctk.CTkOptionMenu(
            day_frame,
            values=[str(i) for i in range(1, 32)],
            width=70,
            height=40,
            fg_color="#F9FAFB",
            button_color="#3B82F6",
            button_hover_color="#2563EB",
            dropdown_fg_color="#FFFFFF",
            font=("Poppins", 13),
            text_color="#111827"
        )
        self.day_spinbox.set(str(datetime.now().day))
        self.day_spinbox.pack(pady=(5, 0))
        
        # Time picker section
        time_label = ctk.CTkLabel(
            main_container,
            text="Due Time",
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
        minute_frame.pack(side="left")
        
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
        
        # Initialize days based on current month/year
        self._update_days()
        
        # Invite Users section - only hide for shared tasks
        show_invite = True
        if self.is_edit_mode and self.task_data.get('is_shared'):
            show_invite = False
        
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
    
    def select_image(self):
        """Open file dialog to select an image"""
        try:
            file_path = filedialog.askopenfilename(
                title="Select an Image",
                filetypes=[
                    ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                # Load and validate image
                img = Image.open(file_path)
                
                # Resize if too large (max 800x800)
                max_size = (800, 800)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffered = BytesIO()
                img.save(buffered, format=img.format or "PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                # Store image data
                self.selected_image_path = file_path
                self.selected_image_base64 = img_base64
                
                # Update preview
                filename = os.path.basename(file_path)
                self.image_preview_label.configure(
                    text=f"✓ {filename} ({img.width}x{img.height})",
                    text_color="#10B981"
                )
                
                # Show remove button
                self.remove_image_btn.pack(pady=(0, 10), padx=10)
                
                print(f"\033[92m [+] Image selected: {filename}")
                
        except Exception as e:
            print(f"\033[91m [!] Error selecting image: {e}")
            self.show_error("Failed to load image")
    
    def remove_image(self):
        """Remove selected image"""
        self.selected_image_path = None
        self.selected_image_base64 = None
        self.image_preview_label.configure(
            text="No image selected",
            text_color="#6B7280"
        )
        self.remove_image_btn.pack_forget()
        print("\033[93m [*] Image removed")
    
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
            
            # Set image if available
            if self.task_data.get('image_base64'):
                self.selected_image_base64 = self.task_data.get('image_base64')
                self.image_preview_label.configure(
                    text="✓ Image attached",
                    text_color="#10B981"
                )
                self.remove_image_btn.pack(pady=(0, 10), padx=10)
            
            # Set date if available
            if self.task_data.get('due_date'):
                try:
                    due_date_obj = datetime.strptime(self.task_data['due_date'], "%Y-%m-%d")
                    
                    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                    
                    self.year_spinbox.set(str(due_date_obj.year))
                    self.month_spinbox.set(months[due_date_obj.month - 1])
                    self.day_spinbox.set(str(due_date_obj.day))
                    
                    # Update days after setting month and year
                    self._update_days()
                except Exception as e:
                    print(f"\033[91m [-] Error parsing date: {e}")
            
            # Set time if available
            if self.task_data.get('due_time'):
                time_parts = self.task_data['due_time'].split(':')
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
    
    def _update_days(self, *args):
        """Update the day dropdown based on selected month and year"""
        try:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            
            selected_month = months.index(self.month_spinbox.get()) + 1
            selected_year = int(self.year_spinbox.get())
            
            # Get the number of days in the selected month
            _, num_days = calendar.monthrange(selected_year, selected_month)
            
            # Update day dropdown
            current_day = int(self.day_spinbox.get())
            self.day_spinbox.configure(values=[str(i) for i in range(1, num_days + 1)])
            
            # Adjust current day if it exceeds the new maximum
            if current_day > num_days:
                self.day_spinbox.set(str(num_days))
        except Exception as e:
            print(f"\033[91m [-] Error updating days: {e}")
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.title_entry.delete(0, "end")
        self.description_textbox.delete("1.0", "end")
        
        # Reset to current date and time
        now = datetime.now()
        self.year_spinbox.set(str(now.year))
        self.month_spinbox.set(["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][now.month - 1])
        self.day_spinbox.set(str(now.day))
        self.hour_spinbox.set(f"{now.hour:02d}")
        self.minute_spinbox.set(f"{(now.minute // 5) * 5:02d}")
        
        # Clear image
        self.remove_image()
        
        # Clear all checkboxes
        for var in self.user_checkboxes.values():
            var.set(False)
        self.selected_users.clear()
        if hasattr(self, 'selected_label'):
            self.selected_label.configure(text="Selected: None")
        
        print("\033[93m [*] Inputs cleared")
    
    def get_current_username(self):
        """Get current logged-in username"""
        if hasattr(self.parent, 'controller') and hasattr(self.parent.controller, 'current_user'):
            return self.parent.controller.current_user.get('username')
        return None
    
    def create_shared_task(self, invited_username, original_task_id, title, description, due_date, due_time, invited_by, image_base64=None):
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
                        "id": str(uuid.uuid4()),
                        "original_task_id": original_task_id,
                        "title": title,
                        "description": description,
                        "due_date": due_date,
                        "due_time": due_time,
                        "image_base64": image_base64,
                        "invited_by": invited_by,
                        "is_shared": True,
                        "completed": False,
                        "deleted": False,
                        "is_upcoming": True,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Initialize tasks array if it doesn't exist
                    if "tasks" not in user:
                        user["tasks"] = []
                    
                    # Add to invited user's tasks
                    user["tasks"].append(shared_task)
                    
                    print(f"\033[92m [+] Shared upcoming task added to {invited_username}'s task list")
                    break
            
            if not user_found:
                print(f"\033[91m [!] User {invited_username} not found in database")
                return False
            
            # Save back to file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"\033[92m [✓] Shared upcoming task saved to JSON for user: {invited_username}")
            return True
                    
        except Exception as e:
            print(f"\033[91m [!] Error creating shared task: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def create_task(self):
        """Validate and create/update task"""
        title = self.title_entry.get().strip()
        description = self.description_textbox.get("1.0", "end").strip()
        
        # Get date and time
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        year = int(self.year_spinbox.get())
        month = months.index(self.month_spinbox.get()) + 1
        day = int(self.day_spinbox.get())
        hour = int(self.hour_spinbox.get())
        minute = int(self.minute_spinbox.get())
        
        if not title:
            self.show_error("Title is required!")
            return
        
        try:
            # Create datetime object
            due_datetime = datetime(year, month, day, hour, minute)
            
            # Check if date is in the past (only for new tasks)
            if not self.is_edit_mode and due_datetime < datetime.now():
                self.show_error("Due date cannot be in the past!")
                return
            
            # Store result
            if self.is_edit_mode:
                # Update existing task
                self.result = {
                    **self.task_data,
                    "title": title,
                    "description": description,
                    "due_date": due_datetime.strftime("%Y-%m-%d"),
                    "due_time": due_datetime.strftime("%H:%M"),
                    "image_base64": self.selected_image_base64,
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Handle invitation logic for edit mode
                if self.user_checkboxes and not self.task_data.get('is_shared'):
                    old_invited_users = self.task_data.get('invited_users', [])
                    if not old_invited_users and self.task_data.get('invited_user'):
                        old_invited_users = [self.task_data.get('invited_user')]
                    
                    new_invited_users = self.selected_users.copy()
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
                                due_datetime.strftime("%Y-%m-%d"),
                                due_datetime.strftime("%H:%M"),
                                current_username,
                                self.selected_image_base64
                            )
                            if success:
                                print(f"\033[92m [✓] New invitation sent to {username}")
                            else:
                                print(f"\033[91m [✗] Failed to send invitation to {username}")
                
                print(f"\033[92m [+] Upcoming task updated: {self.result}")
            else:
                # Create new task
                task_id = str(uuid.uuid4())
                current_username = self.get_current_username()
                
                self.result = {
                    "id": task_id,
                    "title": title,
                    "description": description,
                    "due_date": due_datetime.strftime("%Y-%m-%d"),
                    "due_time": due_datetime.strftime("%H:%M"),
                    "image_base64": self.selected_image_base64,
                    "invited_users": self.selected_users.copy(),
                    "invited_by": current_username,
                    "is_shared": False,
                    "completed": False,
                    "deleted": False,
                    "is_upcoming": True,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                print(f"\033[92m [+] Upcoming task created: {self.result}")
                
                # Create shared copies for all invited users
                if self.selected_users:
                    for username in self.selected_users:
                        success = self.create_shared_task(
                            username, 
                            task_id, 
                            title, 
                            description,
                            due_datetime.strftime("%Y-%m-%d"),
                            due_datetime.strftime("%H:%M"),
                            current_username,
                            self.selected_image_base64
                        )
                        if success:
                            print(f"\033[92m [✓] Shared upcoming task successfully created for {username}")
                        else:
                            print(f"\033[91m [✗] Failed to create shared task for {username}")
                        

            self.destroy()
            
        except ValueError as e:
            self.show_error("Invalid date selected!")
            print(f"\033[91m [-] Date error: {e}")
    
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
        
    def open_camera(self):
        """Open camera in a new window for photo capture"""
        try:
            # Create camera window
            self.camera_window = ctk.CTkToplevel(self)
            self.camera_window.title("Camera Capture")
            self.camera_window.geometry("800x650")
            self.camera_window.transient(self)
            
            # Center camera window
            self.camera_window.update_idletasks()
            x = self.winfo_x() + (self.winfo_width() // 2) - (800 // 2)
            y = self.winfo_y() + (self.winfo_height() // 2) - (650 // 2)
            self.camera_window.geometry(f"800x650+{x}+{y}")
            
            # Initialize camera
            self.camera_capture = cv2.VideoCapture(0)
            
            if not self.camera_capture.isOpened():
                self.show_error("Could not access camera")
                self.camera_window.destroy()
                return
            
            # Camera preview label
            self.camera_label = ctk.CTkLabel(
                self.camera_window,
                text="",
                fg_color="#000000"
            )
            self.camera_label.pack(pady=20, padx=20)
            
            # Buttons frame
            camera_buttons = ctk.CTkFrame(self.camera_window, fg_color="transparent")
            camera_buttons.pack(pady=10)
            
            # Capture button
            capture_btn = ctk.CTkButton(
                camera_buttons,
                text="📸 Capture",
                height=45,
                width=150,
                font=("Poppins SemiBold", 14),
                fg_color="#10B981",
                hover_color="#059669",
                command=self.capture_photo
            )
            capture_btn.pack(side="left", padx=10)
            
            # Cancel button
            cancel_btn = ctk.CTkButton(
                camera_buttons,
                text="❌ Cancel",
                height=45,
                width=150,
                font=("Poppins SemiBold", 14),
                fg_color="#EF4444",
                hover_color="#DC2626",
                command=self.close_camera
            )
            cancel_btn.pack(side="left", padx=10)
            
            # Start video feed
            self.update_camera_feed()
            
            # Handle window close
            self.camera_window.protocol("WM_DELETE_WINDOW", self.close_camera)
            
        except Exception as e:
            print(f"\033[91m [!] Error opening camera: {e}")
            self.show_error("Failed to open camera")

    def update_camera_feed(self):
        """Update camera feed in real-time"""
        if self.camera_capture and self.camera_capture.isOpened():
            ret, frame = self.camera_capture.read()
            
            if ret:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Resize frame for display
                display_width = 760
                height, width = frame_rgb.shape[:2]
                ratio = display_width / width
                display_height = int(height * ratio)
                frame_resized = cv2.resize(frame_rgb, (display_width, display_height))
                
                # Convert to PIL Image
                img_pil = Image.fromarray(frame_resized)
                
                # Convert to CTkImage
                ctk_image = ctk.CTkImage(
                    light_image=img_pil,
                    dark_image=img_pil,
                    size=(display_width, display_height)
                )
                
                # Update label
                self.camera_label.configure(image=ctk_image)
                self.camera_label.image = ctk_image  # Keep reference
            
            # Schedule next update
            if self.camera_window and self.camera_window.winfo_exists():
                self.camera_window.after(10, self.update_camera_feed)

    def capture_photo(self):
        """Capture current frame from camera"""
        if self.camera_capture and self.camera_capture.isOpened():
            ret, frame = self.camera_capture.read()
            
            if ret:
                try:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Convert to PIL Image
                    img = Image.fromarray(frame_rgb)
                    
                    # Resize if too large (max 800x800)
                    max_size = (800, 800)
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Convert to base64
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    
                    # Store image data
                    self.selected_image_path = "camera_capture.png"
                    self.selected_image_base64 = img_base64
                    
                    # Update preview
                    self.image_preview_label.configure(
                        text=f"✅ Camera photo captured ({img.width}x{img.height})",
                        text_color="#10B981"
                    )
                    
                    # Show remove button
                    self.remove_image_btn.pack(pady=(0, 10), padx=10)
                    
                    print(f"\033[92m [+] Photo captured from camera")
                    
                    # Close camera
                    self.close_camera()
                    
                except Exception as e:
                    print(f"\033[91m [!] Error capturing photo: {e}")
                    self.show_error("Failed to capture photo")

    def close_camera(self):
        """Close camera and cleanup"""
        if self.camera_capture:
            self.camera_capture.release()
            self.camera_capture = None
        
        if self.camera_window:
            self.camera_window.destroy()
            self.camera_window = None
        
        print("\033[93m [*] Camera closed")
