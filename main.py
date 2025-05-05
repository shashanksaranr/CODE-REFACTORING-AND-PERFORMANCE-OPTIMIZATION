import tkinter as tk
from tkinter import messagebox
from matrix import Matrix  # Make sure your Matrix class is ready
from gui import MatrixGUI  # Import your GUI class from gui.py

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome")

        # You can customize the splash screen appearance here
        self.splash_label = tk.Label(root, text="Welcome to Matrix Calculator!", font=("Arial", 20))
        self.splash_label.pack(pady=100)

        # Call the method to transition to the main GUI after 2 seconds
        self.root.after(2000, self.show_main_gui)

    def show_main_gui(self):
        # Destroy the splash screen
        self.root.destroy()

        # Create a new window for the main GUI
        root = tk.Tk()
        gui = MatrixGUI(root)
        root.mainloop()

if __name__ == "__main__":
    splash_root = tk.Tk()  # Create a root window for the splash screen
    splash = SplashScreen(splash_root)
    splash_root.mainloop()
