import customtkinter as ctk # type: ignore

class CustomButton(ctk.CTkButton):
    def __init__(self, parent, text="", command=None, fg_color="#2563EB"):
        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color="#1D4ED8",
            text_color="white",
            corner_radius=12,
            height=10,
            width=50
        )
