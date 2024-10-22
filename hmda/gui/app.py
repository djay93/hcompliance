import tkinter as tk
from typing import Type
from datetime import datetime

from hmda.utils.logger import get_logger
from hmda.gui.vcode_replacer_screen import VCodeReplacerScreen
from hmda.gui.warning_screen import WarningScreen
from hmda.gui.hello_world import HelloScreen
from hmda.gui.event_log_screen import EventLogScreen
from hmda.core.event_tracker import EventTracker

logger = get_logger(__name__)

class GUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.center_window(self.root, 800, 400)  # Increased width to accommodate new layout
        self.root.title("HMDA File Replacer")
        
        logger.info("🖥️ Initializing GUI")
        
        self.label = tk.Label(root, text="HMDA File Replacer Options:")
        self.label.pack(pady=10)

        self.event_tracker = EventTracker()

        self.buttons = [
            ("V-Code Replacer", self.show_vcode_replacer),
            ("Warning Screen", self.show_warning),
            ("Hello World", self.show_hello_world),
            ("Event Log", self.show_event_log)
        ]

        for text, command in self.buttons:
            frame = tk.Frame(root)
            frame.pack(fill=tk.X, padx=10, pady=5)

            label = tk.Label(frame, text=text, width=15, anchor='w')
            label.pack(side=tk.LEFT)

            last_executed = tk.Label(frame, text="Never", width=20)
            last_executed.pack(side=tk.LEFT)

            status = tk.Label(frame, text="Not started", width=15, fg="gray")
            status.pack(side=tk.LEFT)

            button = tk.Button(frame, text="Run", command=lambda cmd=command, lbl=text: self.run_command(cmd, lbl))
            button.pack(side=tk.LEFT)

            setattr(self, f"{text.lower().replace(' ', '_')}_last_executed", last_executed)
            setattr(self, f"{text.lower().replace(' ', '_')}_status", status)

        logger.info("✅ GUI initialization complete")

    def run_command(self, command, label):
        command()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        getattr(self, f"{label.lower().replace(' ', '_')}_last_executed").config(text=current_time)
        getattr(self, f"{label.lower().replace(' ', '_')}_status").config(text="Completed", fg="green")

    @staticmethod
    def center_window(window: tk.Tk | tk.Toplevel, width: int, height: int) -> None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def show_screen(self, screen_class: Type[VCodeReplacerScreen | WarningScreen | HelloScreen | EventLogScreen], title: str) -> None:
        logger.info(f"Opening {title} screen")
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        self.center_window(new_window, 600, 400)
        new_window.title(title)
        screen_class(new_window)
        new_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close(new_window))

    def show_vcode_replacer(self) -> None:
        self.show_screen(VCodeReplacerScreen, "VCode Replacer")

    def show_warning(self) -> None:
        self.show_screen(WarningScreen, "Warning")

    def show_hello_world(self) -> None:
        self.show_screen(HelloScreen, "Hello World")

    def show_event_log(self) -> None:
        self.show_screen(EventLogScreen, "Event Log")

    def on_close(self, window: tk.Toplevel) -> None:
        logger.info("Closing screen and returning to main menu")
        window.destroy()
        self.root.deiconify()
    
    def update_status(self):
        for text, _ in self.buttons:
            status_label = getattr(self, f"{text.lower().replace(' ', '_')}_status")
            current_status = self.event_tracker.get_status(text)
            if current_status == "completed":
                status_label.config(text="✅ Completed", fg="green")
            elif current_status == "in_progress":
                status_label.config(text="⏳ In Progress", fg="orange")
            elif current_status == "not_started":
                status_label.config(text="Not Started", fg="gray")
            else:
                status_label.config(text=current_status, fg="blue")
        
        # Schedule the next update in 1 second
        self.root.after(1000, self.update_status)

    def run(self):
        logger.info("Starting GUI")
        self.update_status()  # Start the status update loop
        self.root.mainloop()
