import tkinter as tk
from hmda.gui.app import GUI

def main():
    root = tk.Tk()
    gui = GUI(root)
    gui.run()

if __name__ == "__main__":
    main()
