import customtkinter as ctk
from datetime import datetime
import calendar
import uuid


class CreateUpcomingTaskModal(ctk.CTkToplevel):
    def __init__(self, parent, task_data=None):
        super().__init__(parent)
        
        self.result = None
        self.task_data = task_data
        self.is_edit_mode = task_data is not None
        
        # Configure modal
        self.title("Edit Upcoming Task" if self.is_edit_mode else "Create Upcoming Task")
        self.geometry("500x750")
        self.resizable(False, False)
        
        # Make it transient first
        self.transient(parent)
        
        # Center the modal
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (750 // 2)
        self.geometry(f"500x750+{x}+{y}")
        
        # Make it modal after window is ready
        self.after(10, self._set_modal)
        
        # Configure colors
        self.configure(fg_color="#FFFFFF")
        
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
    
    def create_content(self):
        # Main container with padding
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Header
        header = ctk.CTkLabel(
            container,
            text="Edit Upcoming Task" if self.is_edit_mode else "Create Upcoming Task",
            font=("Poppins SemiBold", 24),
            text_color="#111827"
        )
        header.pack(pady=(0, 20))
        
        # Title field
        title_label = ctk.CTkLabel(
            container,
            text="Title",
            font=("Poppins Medium", 14),
            text_color="#374151",
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 5))
        
        self.title_entry = ctk.CTkEntry(
            container,
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
            container,
            text="Description",
            font=("Poppins Medium", 14),
            text_color="#374151",
            anchor="w"
        )
        desc_label.pack(fill="x", pady=(0, 5))
        
        self.description_textbox = ctk.CTkTextbox(
            container,
            height=120,
            font=("Poppins", 13),
            fg_color="#F9FAFB",
            border_color="#E5E7EB",
            border_width=1
        )
        self.description_textbox.pack(fill="x", pady=(0, 15))
        
        # Date picker section
        date_label = ctk.CTkLabel(
            container,
            text="Due Date",
            font=("Poppins Medium", 14),
            text_color="#374151",
            anchor="w"
        )
        date_label.pack(fill="x", pady=(0, 5))
        
        # Date picker frame
        date_frame = ctk.CTkFrame(container, fg_color="transparent")
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
            command=self._update_days
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
            command=self._update_days
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
            font=("Poppins", 13)
        )
        self.day_spinbox.set(str(datetime.now().day))
        self.day_spinbox.pack(pady=(5, 0))
        
        # Time picker section
        time_label = ctk.CTkLabel(
            container,
            text="Due Time",
            font=("Poppins Medium", 14),
            text_color="#374151",
            anchor="w"
        )
        time_label.pack(fill="x", pady=(0, 5))
        
        # Time picker frame
        time_frame = ctk.CTkFrame(container, fg_color="transparent")
        time_frame.pack(fill="x", pady=(0, 20))
        
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
            font=("Poppins", 13)
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
            font=("Poppins", 13)
        )
        self.minute_spinbox.set(f"{(datetime.now().minute // 5) * 5:02d}")
        self.minute_spinbox.pack(pady=(5, 0))
        
        # Initialize days based on current month/year
        self._update_days()
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 0))
        
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
    
    def populate_fields(self):
        """Populate fields with existing task data"""
        if self.task_data:
            # Set title
            self.title_entry.insert(0, self.task_data.get('title', ''))
            
            # Set description
            if self.task_data.get('description'):
                self.description_textbox.insert("1.0", self.task_data.get('description'))
            
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
        
        print("\033[93m [*] Inputs cleared")
    
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
            # Show error - title is required
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
                    **self.task_data,  # Keep existing fields
                    "title": title,
                    "description": description,
                    "due_date": due_datetime.strftime("%Y-%m-%d"),
                    "due_time": due_datetime.strftime("%H:%M"),
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                print(f"\033[92m [+] Upcoming task updated: {self.result}")
            else:
                # Create new task
                self.result = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "description": description,
                    "due_date": due_datetime.strftime("%Y-%m-%d"),
                    "due_time": due_datetime.strftime("%H:%M"),
                    "completed": False,
                    "deleted": False,
                    "is_upcoming": True,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                print(f"\033[92m [+] Upcoming task created: {self.result}")
            
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