#!/usr/bin/env python3

import os
import sys

import ttkbootstrap as tb

from ui.login import App

# Adds the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """
    Main function to launch the ReHealth application
    """
    # Creates main application window and starts it
    root = tb.Window(themename="darkly")
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
