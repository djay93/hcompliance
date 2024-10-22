import tkinter as tk
from tkinter import ttk
from hmda.core.event_tracker import event_tracker
from hmda.utils.logger import get_logger

logger = get_logger(__name__)

class EventLogScreen:
    def __init__(self, root: tk.Toplevel):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create a treeview to display events
        self.tree = ttk.Treeview(self.root, columns=("Timestamp", "Type", "Description"), show="headings")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Description", text="Description")
        self.tree.column("Timestamp", width=200)
        self.tree.column("Type", width=100)
        self.tree.column("Description", width=300)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Add a refresh button
        refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_events)
        refresh_button.grid(row=1, column=0, pady=10)

        self.refresh_events()

    def refresh_events(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch and display events
        events = event_tracker.get_events()
        for event in events:
            self.tree.insert("", "end", values=(event["timestamp"], event["type"], event["description"]))

        logger.info("Event log refreshed")
