import customtkinter as ctk # type: ignore
from components.appbar import AppBar
from PIL import Image, ImageSequence # type: ignore
import random

class DashboardPage(ctk.CTkFrame):
    
    # UI
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D4E3FF")
        self.controller = controller

        # --- App Bar (top section) ---
        self.appbar = AppBar(
            self,
            controller=self.controller,
            profile_letter="U",  # Default, will be updated when user logs in
            username="User",     # Default, will be updated when user logs in
            settings_icon_path="assets/images/setting.png"
        )
        self.appbar.pack(fill="x", pady=(10, 0))

        # --- Image Display Section ---
        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(pady=(40, 20))

        # --- Quote Display Section ---
        self.quote_label = ctk.CTkLabel(
            self,
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
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(pady=(10, 30))

        # Configure grid layout (2x2)
        for row in range(2):
            grid_frame.grid_rowconfigure(row, weight=1, minsize=200)
        for col in range(2):
            grid_frame.grid_columnconfigure(col, weight=1, uniform="col", minsize=220)

        # --- Card Data ---
        cards = [
            {"name": "Tasks", "image": "assets/icons/tasks.gif", "page": "TasksPage"},
            {"name": "Upcoming", "image": "assets/icons/upcomming.gif", "page": "UpcomingPage"},
            {"name": "Completed", "image": "assets/icons/completed.gif", "page": "CompletedPage"},
            {"name": "Bin", "image": "assets/icons/bin.gif", "page": "BinPage"},
        ]

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

            # --- Label ---
            label = ctk.CTkLabel(
                card_frame,
                text=card["name"],
                font=ctk.CTkFont(family="Poppins", size=16, weight="bold"),
                text_color="#1E3A8A"
            )
            label.pack()
            
            # Click Event - must be defined after all child widgets are created
            def open_page(event=None, page=card["page"], name=card["name"]):
                print(f"\033[94m [+] Card Frame clicked: {name}")
                if hasattr(self.controller, "show_frame"):
                    self.controller.show_frame(page)
            
            # Bind click to card frame and all its children
            card_frame.bind("<Button-1>", open_page)
            gif_label.bind("<Button-1>", open_page)
            label.bind("<Button-1>", open_page)

    def update_user_info(self, username):
        """Update the AppBar with logged-in user's information"""
        if username:
            # Get the first letter of username (uppercase)
            profile_letter = username[0].upper() if username else "U"
            
            # Update AppBar
            self.appbar.update_user(profile_letter, username)
            
            print(f"\033[92m [✓] Dashboard updated for user: {username}")

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