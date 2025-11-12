#!/usr/bin/env python3
"""
ReHealth - Health Tracking Application
Main entry point for the application
"""

import os
import sys
from ui.login import App
import ttkbootstrap as tb

# Add the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """
    Main function to launch the ReHealth application
    """
    # Initialize the database
    from db.db_make import initialize_db
    initialize_db()

    # Create the main window and start the application
    root = tb.Window(themename="darkly")
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
