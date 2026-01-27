"""Food Module - ReHealth"""

from tkinter import messagebox

import ttkbootstrap as tb

from db.db_handler import save_food, get_last_7_days_calories_convert
from logic.user import User
from ui.ui_handler import return_to_dashboard, GraphTemplate, BasePage

MEAL_TYPE_OPTIONS = ["breakfast", "lunch", "dinner", "snack"]


def validate_food_name(food_name: str) -> tuple[bool, str]:
    """
    Validates the food name input.

    Args:
        food_name: Raw text input from the food name entry field.

    Returns:
        A tuple of (is_valid, error_message).
        If valid, error_message is empty.
    """
    if not food_name:
        return False, "Please enter the food name."
    return True, ""


def validate_calorie_amount(calorie_input: str) -> tuple[bool, str]:
    """
    Validates the calorie amount input.

    Args:
        calorie_input: Raw text input from the calorie entry field.

    Returns:
        A tuple of (is_valid, error_message).
        If valid, error_message is empty.
    """
    if not calorie_input:
        return False, "Please enter a calorie amount."

    if not calorie_input.isdigit():
        return False, "Calorie amount must be a number."

    if int(calorie_input) > 10000:
        return False, "Calorie amount must be under 10,000 calories"

    return True, ""


def validate_meal_type(meal_type: str) -> tuple[bool, str]:
    """
    Validates the meal type selection.

    Args:
        meal_type: Selected meal type from combobox.

    Returns:
        A tuple of (is_valid, error_message).
        If valid, error_message is empty.
    """
    if not meal_type:
        return False, "Please select a meal type."

    if meal_type.lower() not in MEAL_TYPE_OPTIONS:
        return False, "Please select a valid meal type from the dropdown."

    return True, ""


class Food(BasePage):
    """Food tracking screen: validates meal input, saves calories to the database, and displays a 7-day graph."""

    def __init__(self, root: tb.Window, user: User) -> None:
        """
        Args:
            root: Main application window.
            user: Logged-in user (used for user_id and username).
        """
        # Call parent constructor
        super().__init__(root, user, "Food")

    def _build_ui(self) -> None:
        """Build all UI components."""
        self._create_title()
        self._create_input_section()
        self._create_add_button()
        self._create_graph_section()

    def _create_title(self) -> None:
        """Create the main title label."""
        self.food_label = tb.Label(
            self.frame,
            text=f"{self.user.username}'s Food",
            font=("roboto", 18, "bold")
        )
        self.food_label.grid(row=0, column=0, pady=(20, 30), columnspan=2, padx=20)

    def _create_input_section(self) -> None:
        """Create the food name, calorie, and meal type input fields."""
        # Food name input
        self.food_entry_label = tb.Label(
            self.frame,
            text="Food Name:",
            font=("roboto", 14)
        )
        self.food_entry_label.grid(row=1, column=0, pady=(10, 10), padx=(20, 10), sticky="e")

        self.food_textbox = tb.Entry(self.frame, width=25)
        self.food_textbox.grid(row=1, column=1, pady=(10, 10), padx=(10, 20), sticky="w")

        # Calorie input
        self.calorie_label = tb.Label(
            self.frame,
            text="Calorie Amount:",
            font=("roboto", 14)
        )
        self.calorie_label.grid(row=2, column=0, pady=(10, 10), padx=(20, 10), sticky="e")

        self.calorie_textbox = tb.Entry(self.frame, width=25)  # Changed from self.foodframe
        self.calorie_textbox.grid(row=2, column=1, pady=(10, 10), padx=(10, 20), sticky="w")

        # Meal type selection
        self.meal_type_label = tb.Label(
            self.frame,
            text="Meal Type:",
            font=("roboto", 14)
        )
        self.meal_type_label.grid(row=3, column=0, pady=(10, 10), padx=(20, 10), sticky="e")

        self.meal_type_combobox = tb.Combobox(
            self.frame,
            values=MEAL_TYPE_OPTIONS,
            width=23
        )
        self.meal_type_combobox.grid(row=3, column=1, pady=(10, 10), padx=(10, 20), sticky="w")

    def _create_add_button(self) -> None:
        """Create the button to add food to database."""
        self.db_add_button = tb.Button(
            self.frame,
            text="Add to Database",
            command=self.database_inc
        )
        self.db_add_button.grid(row=4, column=0, pady=(30, 10), columnspan=2)

    def _create_graph_section(self) -> None:
        """Create the graph frame and initialise the graph widget."""
        self.graph_frame = tb.Frame(self.frame)
        self.graph_frame.grid(row=5, column=0, columnspan=2, pady=0, padx=20)

        self.calorie_graph = CalorieGraph(
            self.graph_frame,
            self.user,
            self.frame,
            self.root
        )

    def database_inc(self) -> None:
        """
        Validates user inputs and saves a food entry to the database.
        """
        foodname = self.food_textbox.get().strip()
        calorie_amount = self.calorie_textbox.get().strip()
        meal_type = self.meal_type_combobox.get().strip()

        # Validate food name
        name_valid, name_error = validate_food_name(foodname)
        if not name_valid:
            messagebox.showerror("Missing Information", name_error)
            self.food_textbox.focus()
            return

        # Validate calorie amount
        calorie_valid, calorie_error = validate_calorie_amount(calorie_amount)
        if not calorie_valid:
            messagebox.showerror("Invalid Input", calorie_error)
            self.calorie_textbox.focus()
            return

        # Validate meal type
        meal_valid, meal_error = validate_meal_type(meal_type)
        if not meal_valid:
            messagebox.showerror("Invalid Input", meal_error)
            self.meal_type_combobox.focus()
            return

        try:
            self._save_and_update(foodname, calorie_amount, meal_type)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save to database: {str(e)}")

    def _save_and_update(self, foodname: str, calorie_amount: str, meal_type: str) -> None:
        """
        Saves food entry to database and updates UI.

        Args:
            foodname: Name of the food item.
            calorie_amount: Calorie count as a string.
            meal_type: Type of meal (breakfast, lunch, dinner, snack).
        """
        # Save to database
        save_food(self.user.user_id, foodname, calorie_amount, meal_type.lower())

        # Show success message
        messagebox.showinfo(
            "Success",
            f"{foodname} ({calorie_amount} cals) saved as {meal_type}!"
        )

        # Clear inputs for next entry
        self.food_textbox.delete(0, 'end')
        self.calorie_textbox.delete(0, 'end')
        self.meal_type_combobox.set('')
        self.food_textbox.focus()

        # Refresh graph to show new data
        self.calorie_graph.refresh_graph()
        self.root.update_idletasks()


class CalorieGraph(GraphTemplate):
    def plot_data(self) -> None:
        self.ax.clear()
        days, calories = get_last_7_days_calories_convert(self.user.user_id)

        self.ax.plot(
            days,
            calories,
            marker='o',
            color='#4e73df',
            linewidth=2,
            markersize=8
        )

        self.style_axes("Days", "Calories", "Calories Over Time")
        self.canvas.draw()

    def get_graph_filename(self) -> str:
        return f"{self.user.username}_calories_graph_week.png"

    def return_to_dash(self) -> None:
        """
        Navigates back to the dashboard screen.
        """
        return_to_dashboard(self.parent_frame, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Food(root, test_user)
    root.mainloop()
