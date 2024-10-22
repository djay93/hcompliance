import tkinter as tk

class WarningScreen:
    def __init__(self, root: tk.Toplevel):
        self.root = root
        
        label = tk.Label(self.root, text="Warning!", font=("Arial", 16, "bold"))
        label.pack(pady=20)

        message = tk.Label(self.root, text="This is a warning message.")
        message.pack(pady=10)
