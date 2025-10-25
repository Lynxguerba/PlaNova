from core.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()





# import tkinter as tk
# from tkinter import messagebox

# class ModernEntry(tk.Frame):
#     def __init__(self, parent, placeholder="", show="", **kwargs):
#         super().__init__(parent, bg="#ffffff")
#         self.show = show
#         self.placeholder = placeholder
#         self.placeholder_active = True
        
#         self.entry = tk.Entry(
#             self, 
#             font=("Segoe UI", 11),
#             bg="#ffffff",
#             fg="#2c3e50",
#             relief="flat",
#             bd=0,
#             show=show if show else "",
#             **kwargs
#         )
#         self.entry.pack(fill="both", expand=True, padx=12, pady=10)
        
#         # Add placeholder if provided
#         if placeholder:
#             self.entry.insert(0, placeholder)
#             self.entry.config(fg="#95a5a6", show="")
#             self.entry.bind("<FocusIn>", self.on_focus_in)
#             self.entry.bind("<FocusOut>", self.on_focus_out)
    
#     def on_focus_in(self, event):
#         if self.placeholder_active:
#             self.entry.delete(0, tk.END)
#             self.entry.config(fg="#2c3e50", show=self.show if self.show else "")
#             self.placeholder_active = False
    
#     def on_focus_out(self, event):
#         if not self.entry.get():
#             self.entry.insert(0, self.placeholder)
#             self.entry.config(fg="#95a5a6", show="")
#             self.placeholder_active = True
    
#     def get(self):
#         if self.placeholder_active:
#             return ""
#         return self.entry.get()
    
#     def focus(self):
#         self.entry.focus()

# class ModernButton(tk.Canvas):
#     def __init__(self, parent, text, command, **kwargs):
#         super().__init__(parent, height=45, bd=0, highlightthickness=0, relief="flat")
#         self.command = command
#         self.text = text
#         self.bg_color = kwargs.get('bg', '#3498db')
#         self.hover_color = kwargs.get('hover_bg', '#2980b9')
#         self.text_color = kwargs.get('fg', '#ffffff')
        
#         self.config(bg=self.bg_color)
#         self.bind("<Enter>", self.on_enter)
#         self.bind("<Leave>", self.on_leave)
#         self.bind("<Button-1>", self.on_click)
        
#         self.draw_button()
    
#     def draw_button(self):
#         self.delete("all")
#         width = self.winfo_width() if self.winfo_width() > 1 else 300
#         self.create_text(
#             width/2, 22.5,
#             text=self.text,
#             font=("Segoe UI", 11, "bold"),
#             fill=self.text_color
#         )
    
#     def on_enter(self, e):
#         self.config(bg=self.hover_color)
    
#     def on_leave(self, e):
#         self.config(bg=self.bg_color)
    
#     def on_click(self, e):
#         self.command()

# def login():
#     username = entry_username.get()
#     password = entry_password.get()
    
#     if not username or not password:
#         messagebox.showwarning("Input Required", "Please enter both username and password")
#         return
    
#     # Example: Hardcoded username and password
#     if username == "admin" and password == "1234":
#         messagebox.showinfo("Login Successful", f"Welcome, {username}!")
#     else:
#         messagebox.showerror("Login Failed", "Invalid username or password")

# # --- Main Window ---
# root = tk.Tk()
# root.title("Login")
# root.geometry("600x500")
# root.config(bg="#ecf0f1")
# root.resizable(False, False)

# # Center window on screen
# root.update_idletasks()
# width = root.winfo_width()
# height = root.winfo_height()
# x = (root.winfo_screenwidth() // 2) - (width // 2)
# y = (root.winfo_screenheight() // 2) - (height // 2)
# root.geometry(f'{width}x{height}+{x}+{y}')

# # --- Main Container ---
# container = tk.Frame(root, bg="#ffffff")
# container.place(relx=0.5, rely=0.5, anchor="center", width=340, height=420)

# # Add subtle shadow effect with a border
# shadow = tk.Frame(root, bg="#bdc3c7")
# shadow.place(relx=0.5, rely=0.5, anchor="center", width=344, height=424)
# container.lift()

# # --- Header Section ---
# header_frame = tk.Frame(container, bg="#3498db", height=100)
# header_frame.pack(fill="x")
# header_frame.pack_propagate(False)

# label_title = tk.Label(
#     header_frame, 
#     text="Welcome Back", 
#     font=("Segoe UI", 22, "bold"), 
#     bg="#3498db",
#     fg="#ffffff"
# )
# label_title.pack(pady=15)

# label_subtitle = tk.Label(
#     header_frame,
#     text="Sign in to continues",
#     font=("Segoe UI", 10),
#     bg="#3498db",
#     fg="#ecf0f1"
# )
# label_subtitle.pack()

# # --- Form Section ---
# form_frame = tk.Frame(container, bg="#ffffff")
# form_frame.pack(fill="both", expand=True, padx=30, pady=30)

# # Username
# label_username = tk.Label(
#     form_frame, 
#     text="Username", 
#     font=("Segoe UI", 10, "bold"), 
#     bg="#ffffff",
#     fg="#2c3e50",
#     anchor="w"
# )
# label_username.pack(fill="x", pady=(0, 5))

# username_frame = tk.Frame(form_frame, bg="#ecf0f1", height=45)
# username_frame.pack(fill="x", pady=(0, 15))
# username_frame.pack_propagate(False)

# entry_username = ModernEntry(username_frame, placeholder="Enter your username")
# entry_username.pack(fill="both", expand=True, padx=1, pady=1)

# # Password
# label_password = tk.Label(
#     form_frame, 
#     text="Password", 
#     font=("Segoe UI", 10, "bold"), 
#     bg="#ffffff",
#     fg="#2c3e50",
#     anchor="w"
# )
# label_password.pack(fill="x", pady=(0, 5))

# password_frame = tk.Frame(form_frame, bg="#ecf0f1", height=45)
# password_frame.pack(fill="x", pady=(0, 25))
# password_frame.pack_propagate(False)

# entry_password = ModernEntry(password_frame, placeholder="Enter your password", show="*")
# entry_password.pack(fill="both", expand=True, padx=1, pady=1)

# # Login Button
# btn_login = ModernButton(
#     form_frame, 
#     text="LOGIN", 
#     command=login,
#     bg="#3498db",
#     hover_bg="#2980b9",
#     fg="#ffffff"
# )
# btn_login.pack(fill="x", pady=(0, 10))
# btn_login.bind("<Configure>", lambda e: btn_login.draw_button())

# # Forgot Password Link
# forgot_label = tk.Label(
#     form_frame,
#     text="Forgot password?",
#     font=("Segoe UI", 9, "underline"),
#     bg="#ffffff",
#     fg="#3498db",
#     cursor="hand2"
# )
# forgot_label.pack()
# forgot_label.bind("<Button-1>", lambda e: messagebox.showinfo("Info", "Password recovery not implemented"))

# # Bind Enter key to login
# root.bind('<Return>', lambda e: login())

# # Focus on username entry
# entry_username.focus()

# root.mainloop()