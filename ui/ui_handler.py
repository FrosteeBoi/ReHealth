import os
from tkinter import messagebox
import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from abc import ABC, abstractmethod


def return_to_dashboard(frame, root, user):
    """
    Destroys current frame and returns user to the dashboard.
    """
    from ui.dashboard import Dashboard
    frame.destroy()
    Dashboard(root, user)


class GraphTemplate(ABC):
    """Template class designed for all user graphs"""

    def __init__(self, graph_frame, user, parent_frame, root):
        self.graph_frame = graph_frame
        self.user = user
        self.parent_frame = parent_frame
        self.root = root

        self._configure_frame()
        self._create_graph()
        self._create_buttons()

    def _configure_frame(self):
        self.graph_frame.grid(row=5, column=0, sticky="s")
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

    def _create_graph(self):
        self.fig = Figure(figsize=(6, 4), dpi=67, facecolor='#222222')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#2b3e50')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        self.plot_data()
        self.canvas_widget.grid(row=0, column=0, pady=(0, 10))

    @abstractmethod
    def plot_data(self):
        """Fetch and plot data - must be implemented by subclasses"""
        pass

    @abstractmethod
    def get_graph_filename(self):
        """Return filename for saving graph"""
        pass

    def style_axes(self, xlabel, ylabel, title):
        """Apply consistent styling to axes"""
        self.ax.set_xlabel(xlabel, color='#adb5bd')
        self.ax.set_ylabel(ylabel, color='#adb5bd')
        self.ax.set_title(title, color='#ffffff')
        self.ax.tick_params(colors='#adb5bd')

        for spine in self.ax.spines.values():
            spine.set_color('#adb5bd')

        self.ax.grid(True, alpha=0.2, color='#adb5bd')

    def refresh_graph(self):
        """Refresh graph with new data"""
        self.plot_data()

    def save_graph(self):
        """Save graph to images folder"""
        try:
            images_folder = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "images")
            )
            os.makedirs(images_folder, exist_ok=True)

            filename = os.path.join(images_folder, self.get_graph_filename())
            self.fig.savefig(filename, dpi=100, facecolor='#222222')

            messagebox.showinfo("Success", f"Graph saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph: {e}")

    def _create_buttons(self):
        button_frame = tb.Frame(self.graph_frame)
        button_frame.grid(row=1, column=0, pady=(0, 20))

        tb.Button(
            button_frame,
            text="Download",
            command=self.save_graph
        ).grid(row=0, column=0, padx=(0, 5))

        tb.Button(
            button_frame,
            text="Back to Dashboard",
            command=self.return_to_dashboard
        ).grid(row=0, column=1, padx=(5, 0))

    def return_to_dashboard(self):
        """Return to dashboard"""
        return_to_dashboard(self.parent_frame, self.root, self.user)


class BasePage(ABC):
    """Base class for ui in Rehealth pages"""

    def __init__(self, root, user, title):
        self.root = root
        self.user = user
        self.title = title

        self._configure_window()
        self._create_main_frame()
        self._build_ui()

    def _configure_window(self):
        """Standard window configuration"""
        self.root.geometry("490x630")
        self.root.title("ReHealth")

    def _create_main_frame(self):
        """Create the main frame - can be overridden"""
        self.frame = tb.Frame(self.root)
        self.frame.place(relx=0.5, rely=0, anchor="n")

    @abstractmethod
    def _build_ui(self):
        """Build UI components - must be implemented by subclasses"""
        pass

    def create_title_label(self, text):
        """Helper method for consistent title styling"""
        return tb.Label(
            self.frame,
            text=text,
            font=("roboto", 18, "bold")
        )

    def return_to_dashboard(self):
        """Navigate back to dashboard"""
        return_to_dashboard(self.frame, self.root, self.user)
