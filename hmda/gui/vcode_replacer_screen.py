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
        
        self.excel_path1 = tk.StringVar()
        self.excel_path2 = tk.StringVar()
        self.excel_path3 = tk.StringVar()
        self.excel_path4 = tk.StringVar()
        self.email_option = tk.StringVar(value="send")
        self.vcode_path = os.path.join("hmda", "config", "vcode.json")

        logger.info("Initializing VCodeReplacerScreen")
        self.create_widgets()

    def create_widgets(self):
        # Using layout manager
        self.root.columnconfigure(1, weight=1)
        
        # Excel file selection 1
        self.label_excel1 = tk.Label(self.root, text="Excel 1:")
        self.label_excel1.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_excel1 = tk.Entry(self.root, textvariable=self.excel_path1, width=50)
        self.entry_excel1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.button_excel1 = tk.Button(self.root, text="Browse", command=lambda: self.browse_excel(self.excel_path1))
        self.button_excel1.grid(row=0, column=2, padx=5, pady=5)

        # Excel file selection 2
        self.label_excel2 = tk.Label(self.root, text="Excel 2:")
        self.label_excel2.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_excel2 = tk.Entry(self.root, textvariable=self.excel_path2, width=50)
        self.entry_excel2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.button_excel2 = tk.Button(self.root, text="Browse", command=lambda: self.browse_excel(self.excel_path2))
        self.button_excel2.grid(row=1, column=2, padx=5, pady=5)

        # Excel file selection 3
        self.label_excel3 = tk.Label(self.root, text="Excel 3:")
        self.label_excel3.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_excel3 = tk.Entry(self.root, textvariable=self.excel_path3, width=50)
        self.entry_excel3.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.button_excel3 = tk.Button(self.root, text="Browse", command=lambda: self.browse_excel(self.excel_path3))
        self.button_excel3.grid(row=2, column=2, padx=5, pady=5)

         # Excel file selection 4
        self.label_excel4 = tk.Label(self.root, text="Excel 4:")
        self.label_excel4.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_excel4 = tk.Entry(self.root, textvariable=self.excel_path4, width=50)
        self.entry_excel4.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.button_excel4 = tk.Button(self.root, text="Browse", command=lambda: self.browse_excel(self.excel_path4))
        self.button_excel4.grid(row=3, column=2, padx=5, pady=5)

        # Email option
        self.radio_frame = tk.Frame(self.root)
        self.radio_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.radio_send = tk.Radiobutton(self.radio_frame, text="Send Email", variable=self.email_option, value="send")
        self.radio_send.pack(side=tk.LEFT, padx=10)
        self.radio_display = tk.Radiobutton(self.radio_frame, text="Display Email", variable=self.email_option, value="display")
        self.radio_display.pack(side=tk.LEFT, padx=10)

        # # V-Code file display
        # self.label_vcode = tk.Label(self.root, text="V-Code File:")
        # self.label_vcode.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        # self.entry_vcode = tk.Entry(self.root, textvariable=tk.StringVar(value=self.vcode_path), state='readonly', width=50)
        # self.entry_vcode.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Replace button
        self.button_replace = tk.Button(self.root, text="Execute", command=self.execute_action)
        self.button_replace.grid(row=5, column=1, padx=5, pady=20)

        logger.debug("Widgets created successfully")

    def browse_excel(self, string_var):
        logger.debug("Browse Excel button clicked")
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx *.xls *.xlsm *.csv")],
                title="Select Excel or CSV File"
            )
            if filename:
                string_var.set(filename)
                logger.info(f"Excel file selected: {filename}")
            else:
                logger.warning("No file selected in browse_excel")
        except Exception as e:
            logger.exception("Error in browse_excel")
            messagebox.showerror("Error", f"An error occurred while browsing for Excel file: {str(e)}")

    def execute_action(self):
        logger.debug("Execute action button clicked")
        excel_path1 = self.excel_path1.get()
        excel_path2 = self.excel_path2.get()
        excel_path3 = self.excel_path3.get()
        excel_path4 = self.excel_path4.get()
        
        if not any([excel_path1, excel_path2, excel_path3, excel_path4]):
            logger.warning("Excel file not selected correctly")
            messagebox.showerror("Error", "Please select a valid Excel file.")
            return

        try:
            logger.info(f"Invoking V-Code Replacer Service")
            VCodeService.execute(excel_path1, excel_path2, excel_path3, excel_path4)
            
            logger.info("V-Code replacement completed successfully")
            messagebox.showinfo("Success", "Replace V-Code step completed successfully!")
        except Exception as e:
            logger.exception("An error occurred during V-Code replacement")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            