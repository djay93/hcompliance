import tkinter as tk
from tkinter import filedialog, messagebox
import os
from hmda.services.vcode_service import VCodeService
from hmda.utils.logger import get_logger
from hmda.core.event_tracker import event_tracker

logger = get_logger(__name__)

class VCodeReplacerScreen:
    def __init__(self, root: tk.Toplevel):
        self.root = root
        
        self.excel_path = tk.StringVar()
        self.vcode_path = os.path.join("hmda", "config", "vcode.json")

        logger.info("Initializing VCodeReplacerScreen")
        self.create_widgets()

    def create_widgets(self):
        # Use a more efficient layout manager
        self.root.columnconfigure(1, weight=1)
        
        # Excel file selection
        self.label_excel = tk.Label(self.root, text="Excel File:")
        self.label_excel.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_excel = tk.Entry(self.root, textvariable=self.excel_path, width=50)
        self.entry_excel.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.button_excel = tk.Button(self.root, text="Browse", command=self.browse_excel)
        self.button_excel.grid(row=0, column=2, padx=5, pady=5)

        # V-Code file display
        self.label_vcode = tk.Label(self.root, text="V-Code File:")
        self.label_vcode.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_vcode = tk.Entry(self.root, textvariable=tk.StringVar(value=self.vcode_path), state='readonly', width=50)
        self.entry_vcode.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Replace button
        self.button_replace = tk.Button(self.root, text="Replace Files", command=self.replace_vcode)
        self.button_replace.grid(row=2, column=1, padx=5, pady=20)

        logger.debug("Widgets created successfully")

    def browse_excel(self):
        logger.debug("Browse Excel button clicked")
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx *.xls")],
                title="Select Excel File"
            )
            if filename:
                self.excel_path.set(filename)
                logger.info(f"Excel file selected: {filename}")
            else:
                logger.warning("No file selected in browse_excel")
        except Exception as e:
            logger.exception("Error in browse_excel")
            messagebox.showerror("Error", f"An error occurred while browsing for Excel file: {str(e)}")

    def replace_vcode(self):
        logger.debug("Replace V-Code button clicked")
        excel_path = self.excel_path.get()
        
        if not excel_path:
            logger.warning("No Excel file selected")
            messagebox.showerror("Error", "Please select a valid Excel file.")
            return

        if not os.path.exists(self.vcode_path):
            logger.error(f"V-Code file not found at {self.vcode_path}")
            messagebox.showerror("Error", f"V-Code file not found at {self.vcode_path}")
            return

        try:
            logger.info(f"Loading V-Code data from {self.vcode_path}")
            vcode_data = VCodeService.load_vcode(self.vcode_path)
            
            event_tracker.add_event("HMDA_FILE_LOADED", f"Loaded HMDA file: {excel_path}")
            
            logger.info(f"Replacing V-Code in {excel_path}")
            VCodeService.replace_vcode(excel_path, vcode_data)
            
            event_tracker.add_event("HMDA_FILE_PROCESSED", f"Processed HMDA file: {excel_path}")
            
            logger.info("V-Code replacement completed successfully")
            messagebox.showinfo("Success", "V-Code replaced successfully!")
        except Exception as e:
            logger.exception("An error occurred during file replacement")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            event_tracker.add_event("ERROR", f"Error processing HMDA file: {str(e)}")
