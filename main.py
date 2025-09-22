#!/usr/bin/env python3


import os
import sys

# Adds the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports the main application class
from ui.login import App
import ttkbootstrap as tb

def main():
    """
    Main function to launch the ReHealth application
    """
    # Initialises the database
    from db.db_make import initialize_db
    initialize_db()
    
    # Creates main application window and starts it
    root = tb.Window(themename="darkly")
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()