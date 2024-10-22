import tkinter as tk

class HelloScreen:
    def __init__(self, root: tk.Toplevel):
        self.root = root
        
        label = tk.Label(self.root, text="Hello, World!", font=("Arial", 16, "bold"))
        label.pack(pady=20)

        message = tk.Label(self.root, text="Welcome to the Hello World screen.")
        message.pack(pady=10)
