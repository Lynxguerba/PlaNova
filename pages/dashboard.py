import customtkinter as ctk # type: ignore
from components.appbar import AppBar
from PIL import Image, ImageSequence # type: ignore
import random
import json 
import os
from datetime import datetime, timedelta

class DashboardPage(ctk.CTkFrame):
    
    # UI
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D4E3FF")
        self.controller = controller
        
        # Track session start time
        self.session_start_time = datetime.now()

        # --- App Bar (top section) ---
        self.appbar = AppBar(
            self,
            controller=self.controller,
            profile_letter="U",  # Default, will be updated when user logs in
            username="User",     # Default, will be updated when user logs in
            settings_icon_path="assets/images/setting.png"
        )
        self.appbar.pack(fill="x", pady=(10, 0))
        
        # Main content area with scrollable frame
        self.content_container = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            scrollbar_button_color="#D4E3FF",  # Visible scrollbar
            scrollbar_button_hover_color="#95AAC8"  # Darker on hover
        )
        self.content_container.pack(fill="both", expand=True, padx=20, pady=(10, 0))

        # --- Image Display Section ---
        self.image_label = ctk.CTkLabel(self.content_container, text="")
        self.image_label.pack(pady=(40, 20))

        # --- Quote Display Section ---
        self.quote_label = ctk.CTkLabel(
            self.content_container,
            text="",
            font=ctk.CTkFont(family="Poppins", size=14, slant="italic"),
            text_color="#1E3A8A",
            wraplength=400,
            justify="center"
        )
        self.quote_label.pack(pady=(0, 10))

        # --- Load Images ---
        self.image_paths = [
            "assets/images/dash1.png",
            "assets/images/dash2.png",
            "assets/images/dash3.png",
            "assets/images/dash4.png"
        ]
        
        self.images = [
            ctk.CTkImage(light_image=Image.open(path), size=(380, 250))
            for path in self.image_paths
        ]

         # --- Quotes ---
        self.quotes = [
            "“Great things are done by a series of small things brought together.” – Vincent van Gogh",
            "“Don’t watch the clock; do what it does. Keep going.” – Sam Levenson",
            "“You don’t have to be great to start, but you have to start to be great.” – Zig Ziglar",
            "“It does not matter how slowly you go as long as you do not stop.” – Confucius",
        ]

        # Start the random rotation
        self.update_content()
        
        # --- Dashboard Grid Section ---
        grid_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        grid_frame.pack(pady=(10, 20))

        # Configure grid layout (2x2)
        for row in range(2):
            grid_frame.grid_rowconfigure(row, weight=1, minsize=200)
        for col in range(2):
            grid_frame.grid_columnconfigure(col, weight=1, uniform="col", minsize=220)

        # --- Card Data ---
        cards = [
            {"name": "Tasks", "image": "assets/icons/tasks.gif", "page": "TasksPage", "count_key": "active"},
            {"name": "Upcoming", "image": "assets/icons/upcomming.gif", "page": "UpcomingPage", "count_key": "upcoming"},
            {"name": "Completed", "image": "assets/icons/completed.gif", "page": "CompletedPage", "count_key": "completed"},
            {"name": "Bin", "image": "assets/icons/bin.gif", "page": "BinPage", "count_key":"deleted"},
        ]

        # Store label references for updating counts
        self.card_labels = {}

        # --- Create 2x2 Boxes ---
        for i, card in enumerate(cards):
            row, col = divmod(i, 2)

            card_frame = ctk.CTkFrame(
                grid_frame,
                fg_color="white",
                corner_radius=20,
                border_color="white",
                width=300,
                height=180
            )
            card_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

            # --- Animated GIF (custom loader) ---
            gif_label = ctk.CTkLabel(card_frame, text="")
            gif_label.pack(pady=(20, 10))
            self.animate_gif(card["image"], gif_label, size=(80, 80))

            # --- Label with count ---
            label = ctk.CTkLabel(
                card_frame,
                text=f"{card['name']} (0)",
                font=ctk.CTkFont(family="Poppins", size=16, weight="bold"),
                text_color="#1E3A8A"
            )
            label.pack()
            
            # Store reference to label for updating
            self.card_labels[card['count_key']] = label
            
            # Click Event - must be defined after all child widgets are created
            def open_page(event=None, page=card["page"], name=card["name"]):
                print(f"\033[94m [+] Card Frame clicked: {name}")
                if hasattr(self.controller, "show_frame"):
                    self.controller.show_frame(page)
            
            # Bind click to card frame and all its children
            card_frame.bind("<Button-1>", open_page)
            gif_label.bind("<Button-1>", open_page)
            label.bind("<Button-1>", open_page)
        
        # --- Wellbeing / Time Tracking Section ---
        wellbeing_section = ctk.CTkFrame(
            self.content_container,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )
        wellbeing_section.pack(fill="x", pady=(30, 0), padx=10)
        
        # Section title
        wellbeing_title = ctk.CTkLabel(
            wellbeing_section,
            text="📊 App Usage & Wellbeing",
            font=ctk.CTkFont(family="Poppins", size=18, weight="bold"),
            text_color="#1E3A8A"
        )
        wellbeing_title.pack(pady=(20, 15))
        
        # Current date display
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        date_label = ctk.CTkLabel(
            wellbeing_section,
            text=f"📅 {current_date}",
            font=ctk.CTkFont(family="Poppins", size=14),
            text_color="#6B7280"
        )
        date_label.pack(pady=(0, 20))
        
        # Stats container (Today and Week Average)
        stats_container = ctk.CTkFrame(wellbeing_section, fg_color="transparent")
        stats_container.pack(fill="x", padx=30, pady=(0, 20))
        
        # Today's time
        today_frame = ctk.CTkFrame(
            stats_container,
            fg_color="#EFF6FF",
            corner_radius=15,
            border_width=2,
            border_color="#3B82F6"
        )
        today_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        today_label = ctk.CTkLabel(
            today_frame,
            text="Today",
            font=ctk.CTkFont(family="Poppins", size=13, weight="bold"),
            text_color="#1E3A8A"
        )
        today_label.pack(pady=(15, 5))
        
        self.today_time_label = ctk.CTkLabel(
            today_frame,
            text="0m",
            font=ctk.CTkFont(family="Poppins", size=24, weight="bold"),
            text_color="#3B82F6"
        )
        self.today_time_label.pack(pady=(0, 15))
        
        # Week average
        week_frame = ctk.CTkFrame(
            stats_container,
            fg_color="#F0FDF4",
            corner_radius=15,
            border_width=2,
            border_color="#10B981"
        )
        week_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        week_label = ctk.CTkLabel(
            week_frame,
            text="Week Average",
            font=ctk.CTkFont(family="Poppins", size=13, weight="bold"),
            text_color="#1E3A8A"
        )
        week_label.pack(pady=(15, 5))
        
        self.week_avg_label = ctk.CTkLabel(
            week_frame,
            text="0m",
            font=ctk.CTkFont(family="Poppins", size=24, weight="bold"),
            text_color="#10B981"
        )
        self.week_avg_label.pack(pady=(0, 15))
        
        # Weekly chart title
        chart_title = ctk.CTkLabel(
            wellbeing_section,
            text="Weekly Usage Pattern",
            font=ctk.CTkFont(family="Poppins", size=14, weight="bold"),
            text_color="#374151"
        )
        chart_title.pack(pady=(10, 10))
        
        # Weekly bars container
        bars_container = ctk.CTkFrame(wellbeing_section, fg_color="transparent", height=180)
        bars_container.pack(fill="x", padx=30, pady=(0, 20))
        bars_container.pack_propagate(False)
        
        # Days of the week
        days = ["S", "M", "T", "W", "T", "F", "S"]
        self.day_bars = []
        self.day_time_labels = []
        
        # Create a frame for each day
        for i, day in enumerate(days):
            day_container = ctk.CTkFrame(bars_container, fg_color="transparent")
            day_container.pack(side="left", fill="both", expand=True, padx=5)
            
            # Time label above bar
            time_label = ctk.CTkLabel(
                day_container,
                text="0m",
                font=ctk.CTkFont(family="Poppins", size=10),
                text_color="#6B7280"
            )
            time_label.pack(pady=(0, 5))
            self.day_time_labels.append(time_label)
            
            # Bar container (for vertical bar)
            bar_outer = ctk.CTkFrame(
                day_container,
                fg_color="#E5E7EB",
                corner_radius=8,
                width=40,
                height=100
            )
            bar_outer.pack()
            bar_outer.pack_propagate(False)
            
            # Actual colored bar (starts from bottom)
            bar_inner = ctk.CTkFrame(
                bar_outer,
                fg_color="#3B82F6",
                corner_radius=6,
                width=36,
                height=0  # Will be updated based on usage
            )
            bar_inner.place(relx=0.5, rely=1.0, anchor="s")
            self.day_bars.append(bar_inner)
            
            # Day label
            day_label = ctk.CTkLabel(
                day_container,
                text=day,
                font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
                text_color="#374151"
            )
            day_label.pack(pady=(8, 0))
        
        # --- Hidden spacer at bottom for padding ---
        bottom_spacer = ctk.CTkFrame(
            self.content_container, 
            fg_color="transparent", 
            height=50
        )
        bottom_spacer.pack(pady=(0, 30))
        
        # Load and update usage data
        self.load_usage_data()
        self.update_usage_display()
        
        # Start live tracking
        self.start_time_tracking()
        
        # Update counts if user is already logged in
        if hasattr(controller, 'current_user') and controller.current_user:
            self.update_task_counts()

    def load_usage_data(self):
        """Load usage data from JSON file"""
        try:
            file_path = "data/preferences.json"
            
            if not os.path.exists(file_path):
                self.usage_data = {}
                return
            
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            if hasattr(self.controller, 'current_user'):
                username = self.controller.current_user.get('username')
                
                for user in data.get('users', []):
                    if user.get('username') == username:
                        self.usage_data = user.get('usage_data', {})
                        print(f"\033[92m [✓] Loaded usage data for user: {username}")
                        return
            
            self.usage_data = {}
            
        except Exception as e:
            print(f"\033[91m [!] Error loading usage data: {str(e)}")
            self.usage_data = {}
    
    def save_usage_data(self):
        """Save usage data to JSON file"""
        try:
            file_path = "data/preferences.json"
            
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            if hasattr(self.controller, 'current_user'):
                username = self.controller.current_user.get('username')
                
                for user in data.get('users', []):
                    if user.get('username') == username:
                        user['usage_data'] = self.usage_data
                        break
                
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                
                print(f"\033[92m [✓] Usage data saved for user: {username}")
        
        except Exception as e:
            print(f"\033[91m [!] Error saving usage data: {str(e)}")
    
    def start_time_tracking(self):
        """Start tracking time spent in app"""
        self.session_start_time = datetime.now()
        # Update every minute
        self.after(60000, self.update_time_tracking)
    
    def update_time_tracking(self):
        """Update time tracking data"""
        try:
            # Calculate session duration
            session_duration = (datetime.now() - self.session_start_time).total_seconds() / 60  # in minutes
            
            # Get today's date
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Update today's usage
            if today not in self.usage_data:
                self.usage_data[today] = 0
            
            self.usage_data[today] += 1  # Add 1 minute
            
            # Save data
            self.save_usage_data()
            
            # Update display
            self.update_usage_display()
            
            # Schedule next update
            self.after(60000, self.update_time_tracking)
            
        except Exception as e:
            print(f"\033[91m [!] Error updating time tracking: {str(e)}")
    
    def update_usage_display(self):
        """Update the usage display with current data"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Get today's usage
            today_minutes = self.usage_data.get(today, 0)
            
            # Format today's time
            if today_minutes < 60:
                today_text = f"{int(today_minutes)}m"
            else:
                hours = int(today_minutes / 60)
                minutes = int(today_minutes % 60)
                today_text = f"{hours}h {minutes}m"
            
            self.today_time_label.configure(text=today_text)
            
            # Calculate week average
            week_dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
            week_total = sum(self.usage_data.get(date, 0) for date in week_dates)
            week_avg = week_total / 7
            
            # Format week average
            if week_avg < 60:
                week_text = f"{int(week_avg)}m"
            else:
                hours = int(week_avg / 60)
                minutes = int(week_avg % 60)
                week_text = f"{hours}h {minutes}m"
            
            self.week_avg_label.configure(text=week_text)
            
            # Update weekly bars
            max_usage = max([self.usage_data.get(date, 0) for date in week_dates] + [1])
            
            for i in range(7):
                date = week_dates[6 - i]  # Reverse to show Sunday to Saturday
                usage = self.usage_data.get(date, 0)
                
                # Calculate bar height (max 90 pixels)
                bar_height = int((usage / max_usage) * 90) if max_usage > 0 else 0
                
                # Update bar
                self.day_bars[i].configure(height=bar_height)
                
                # Update time label
                if usage < 60:
                    time_text = f"{int(usage)}m"
                else:
                    hours = int(usage / 60)
                    time_text = f"{hours}h"
                
                self.day_time_labels[i].configure(text=time_text if usage > 0 else "0m")
            
        except Exception as e:
            print(f"\033[91m [!] Error updating usage display: {str(e)}")

    def update_user_info(self, username):
        """Update the AppBar with logged-in user's information"""
        if username:
            # Get the first letter of username (uppercase)
            profile_letter = username[0].upper() if username else "U"
            
            # Update AppBar
            self.appbar.update_user(profile_letter, username)
            
            print(f"\033[92m [✓] Dashboard updated for user: {username}")
            
            # Load usage data for this user
            self.load_usage_data()
            self.update_usage_display()
            
            # Update task counts
            self.update_task_counts()

    def update_task_counts(self):
        """Update the task counts displayed on each card"""
        try:
            # Get current user data from controller
            if not hasattr(self.controller, 'current_user') or not self.controller.current_user:
                return
            
            user_data = self.controller.current_user
            
            # Get tasks from user data
            if "tasks" not in user_data:
                return
            
            tasks = user_data["tasks"]
            
            # Count different task types
            active_count = len([t for t in tasks if not t.get("deleted", False) and not t.get("completed", False) and not t.get("is_upcoming", False)])
            upcoming_count = len([t for t in tasks if t.get("is_upcoming", False) and not t.get("deleted", False) and not t.get("completed", False)])
            completed_count = len([t for t in tasks if t.get("completed", False) and not t.get("deleted", False)])
            deleted_count = len([t for t in tasks if t.get("deleted", False)])
            
            # Update labels
            self.card_labels['active'].configure(text=f"Tasks ({active_count})")
            self.card_labels['upcoming'].configure(text=f"Upcoming ({upcoming_count})")
            self.card_labels['completed'].configure(text=f"Completed ({completed_count})")
            self.card_labels['deleted'].configure(text=f"Bin ({deleted_count})")
            
            print(f"\033[92m [+] Task counts updated: Active={active_count}, Upcoming={upcoming_count}, Completed={completed_count}, Deleted={deleted_count}")
            
        except Exception as e:
            print(f"\033[91m [x] Error updating task counts: {e}")

    def update_content(self):
        """Randomly change the image and quote every 5 seconds"""
        img = random.choice(self.images)
        quote = random.choice(self.quotes)
        self.image_label.configure(image=img)
        self.quote_label.configure(text=quote)

        # Keep references (important for Tkinter image display)
        self.image_label.image = img

        # Schedule next update (5000 ms = 5 sec)
        self.after(5000, self.update_content)
        
    # --- GIF Animation Handler ---
    def animate_gif(self, gif_path, label, size=(80, 80)):
        """Animate GIF frames"""
        gif = Image.open(gif_path)
        frames = [frame.copy().resize(size) for frame in ImageSequence.Iterator(gif)]
        photo_frames = [ctk.CTkImage(light_image=frame, size=size) for frame in frames]

        def play(index=0):
            label.configure(image=photo_frames[index])
            label.image = photo_frames[index]
            next_index = (index + 1) % len(photo_frames)
            self.after(50, play, next_index) 

        play()  # Start animation
            
    def tkraise(self, *args, **kwargs):
        """Override tkraise to update counts when page is shown"""
        super().tkraise(*args, **kwargs)
        self.update_task_counts()
        self.update_usage_display()
