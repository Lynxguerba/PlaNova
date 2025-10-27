from PIL import Image  
import customtkinter as ctk  # type: ignore
from datetime import datetime, timedelta
import calendar


class CreateUpcomingTaskModal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.result = None
        
        # Configure modal
        self.title("Create Upcoming Task")
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
            text="Create Upcoming Task",
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
        
        # Create button
        create_btn = ctk.CTkButton(
            buttons_frame,
            text="Create Task",
            height=45,
            font=("Poppins SemiBold", 14),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white",
            command=self.create_task
        )
        create_btn.pack(side="left", fill="x", expand=True)
    
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
        """Validate and create task"""
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
            
            # Check if date is in the past
            if due_datetime < datetime.now():
                self.show_error("Due date cannot be in the past!")
                return
            
            # Store result
            self.result = {
                "title": title,
                "description": description,
                "due_date": due_datetime.strftime("%Y-%m-%d"),
                "due_time": due_datetime.strftime("%H:%M"),
                "due_datetime": due_datetime
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


class UpcomingPage(ctk.CTkFrame):
    def __init__(self, parent, controller=None, navigate_callback=None):
        super().__init__(parent, fg_color="#F9FAFB")
        
        # Support both controller and navigate_callback for compatibility
        self.controller = controller
        self.navigate_callback = navigate_callback or (controller.show_frame if controller else None)
        
        # Store tasks
        self.tasks = []
        
        # Create app bar
        self.create_app_bar()
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Tasks content (placeholder)
        self.create_tasks_content()
        
        # Floating create button
        self.create_floating_button()
    
    def create_app_bar(self):
        """Create the top app bar with back button"""
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
            text="Upcoming Tasks",
            font=("Poppins SemiBold", 20),
            text_color="#111827"
        )
        title.pack(side="left", padx=15)
    
    def create_tasks_content(self):
        """Create the main tasks content area"""
        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="No upcoming tasks yet\nClick the + button to create a task",
            font=("Poppins", 14),
            text_color="#9CA3AF",
            justify="center"
        )
        placeholder.pack(expand=True)
    
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
            print(f"\033[91m [-] Could not load plus icon: {e}")
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
    
    def go_back(self):
        if self.navigate_callback:
            self.navigate_callback("DashboardPage")
    
    def create_task(self):
        print("\033[92m [+] Create upcoming task clicked")
        
        # Open modal
        modal = CreateUpcomingTaskModal(self)
        self.wait_window(modal)
        
        # Check if task was created
        if modal.result:
            self.tasks.append(modal.result)
            print(f"\033[92m [+] Upcoming task added to list: {modal.result}")
            # Here you can update the UI to show the new task