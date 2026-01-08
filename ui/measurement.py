"""
Measurement Module - ReHealth
"""

import os
from datetime import datetime
from tkinter import messagebox

import ttkbootstrap as tb

from db.db_handler import save_metrics, get_all_days_metrics
from logic.calculations import bmi_calc, bmi_status
from logic.user import User
from ui.ui_handler import return_to_dashboard, BasePage


def _validate_positive_float(raw: str, field_name: str, unit_hint: str) -> tuple[bool, float, str]:
    """
    Validate a positive float input (e.g. height/weight).

    Args:
        raw: Raw entry text.
        field_name: Human-readable field name (e.g. "height").
        unit_hint: Unit hint used in the error message (e.g. "cm", "kg").

    Returns:
        (is_valid, value, error_message)
    """
    text = raw.strip()

    if not text:
        return False, 0.0, f"Please enter your {field_name} as a number in {unit_hint}."

    try:
        value = float(text)
    except ValueError:
        return False, 0.0, f"Please enter your {field_name} as a number in {unit_hint}."

    if value <= 0:
        return False, 0.0, f"{field_name.capitalize()} must be a positive number."

    return True, value, ""


def _make_metric_logs_dir() -> str:
    """
    Create (if needed) and return the absolute path to metric_logs.
    """
    directory = os.path.join(os.path.dirname(__file__), "..", "metric_logs")
    directory = os.path.abspath(directory)
    os.makedirs(directory, exist_ok=True)
    return directory


def _build_metrics_filename() -> str:
    """
    Build a dated metrics log filename.
    """
    current_date = datetime.now().strftime("%d-%m-%Y")
    return os.path.join(_make_metric_logs_dir(), f"metric_log_{current_date}.txt")


def _write_metrics_log(filename: str, username: str, records: list[tuple]) -> None:
    """
    Write measurement records to a text file.

    Args:
        filename: Full output path.
        username: Username for header.
        records: DB records in form (date, height, weight).
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Measurement Records for {username}\n")
        file.write(f"Downloaded on: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n")
        file.write("=" * 60 + "\n\n")

        for record in records:
            date, height, weight = record
            bmi = bmi_calc(weight, height)
            status = bmi_status(bmi)

            file.write(f"Date: {date}\n")
            file.write(f"Height: {height} cm\n")
            file.write(f"Weight: {weight} kg\n")
            file.write(f"BMI: {bmi} ({status})\n")
            file.write("-" * 60 + "\n")


class Measurement(BasePage):
    """GUI screen for recording height/weight and calculating BMI + exporting history."""

    def __init__(self, root: tb.Window, user: User) -> None:
        # Initialise state
        self.height_val: float = 0.0
        self.weight_val: float = 0.0
        self.bmi_val: float = 0.0

        # Call parent constructor
        super().__init__(root, user, "Measurement")

    def _build_ui(self) -> None:
        self._create_labels()
        self._create_input_section()
        self._create_buttons()

    def _create_labels(self) -> None:
        self.measure_label = tb.Label(
            self.frame,
            text=f"{self.user.username}'s Measurements",
            font=("roboto", 18, "bold"),
        )
        self.measure_label.grid(row=0, column=0, pady=(20, 30), columnspan=3, padx=20)

        self.height_value_label = tb.Label(
            self.frame,
            text="Height: 0 cm",
            font=("roboto", 14),
        )
        self.height_value_label.grid(row=1, column=0, columnspan=3, pady=(10, 10), padx=20)

        self.weight_value_label = tb.Label(
            self.frame,
            text="Weight: 0 kg",
            font=("roboto", 14),
        )
        self.weight_value_label.grid(row=2, column=0, columnspan=3, pady=(10, 10), padx=20)

        self.bmi_label = tb.Label(
            self.frame,
            text="BMI: 0",
            font=("roboto", 14),
        )
        self.bmi_label.grid(row=3, column=0, pady=(10, 30), columnspan=3, padx=20)

    def _create_input_section(self) -> None:
        self.height_label = tb.Label(
            self.frame,
            text="Record Your Height (cm):",
            font=("roboto", 14),
        )
        self.height_label.grid(row=4, column=0, pady=(10, 10), padx=(20, 10), sticky="e")

        self.height_entry = tb.Entry(self.frame, width=15)
        self.height_entry.grid(row=4, column=1, padx=(10, 10), pady=(10, 10), columnspan=2)

        self.weight_label = tb.Label(
            self.frame,
            text="Record Your Weight (kg):",
            font=("roboto", 14),
        )
        self.weight_label.grid(row=5, column=0, pady=(10, 10), padx=(20, 10), sticky="e")

        self.weight_entry = tb.Entry(self.frame, width=15)
        self.weight_entry.grid(row=5, column=1, padx=(10, 10), pady=(10, 10), columnspan=2)

    def _create_buttons(self) -> None:
        self.bmi_calc_button = tb.Button(
            self.frame,
            text="Calculate BMI",
            command=self.calculate_and_save_bmi,
        )
        self.bmi_calc_button.grid(row=6, column=0, columnspan=1, pady=(30, 10), padx=10)

        self.download_button = tb.Button(
            self.frame,
            text="Download Measurement History",
            command=self.download_records,
        )
        self.download_button.grid(row=6, column=1, columnspan=2, pady=(30, 10), padx=10)

        self.dash_button = tb.Button(
            self.frame,
            text="Back to Dashboard",
            command=self.return_to_dash,
        )
        self.dash_button.grid(row=7, column=0, columnspan=3, pady=(170, 20), padx=20)

    def calculate_and_save_bmi(self) -> None:
        """
        Validates inputs, calculates BMI, updates UI, and saves metrics.
        """
        height_text = self.height_entry.get()
        weight_text = self.weight_entry.get()

        ok_h, height, err_h = _validate_positive_float(height_text, "height", "cm")
        if not ok_h:
            messagebox.showerror("Invalid Input", err_h)
            self.height_entry.focus()
            return

        ok_w, weight, err_w = _validate_positive_float(weight_text, "weight", "kg")
        if not ok_w:
            messagebox.showerror("Invalid Input", err_w)
            self.weight_entry.focus()
            return

        try:
            self._save_and_update(height, weight)
        except Exception as exc:
            messagebox.showerror("Database Error", f"Failed to save to database: {exc}")
            self.weight_entry.focus()

    def _save_and_update(self, height_cm: float, weight_kg: float) -> None:
        """
        Calculates BMI, updates labels, saves metrics, and clears entries.
        """
        self.height_val = height_cm
        self.weight_val = weight_kg

        bmi_value = bmi_calc(weight_kg, height_cm)
        self.bmi_val = bmi_value

        self.height_value_label.config(text=f"Height: {self.height_val} cm")
        self.weight_value_label.config(text=f"Weight: {self.weight_val} kg")
        self.bmi_label.config(text=f"BMI: {self.bmi_val} ({bmi_status(self.bmi_val)})")

        save_metrics(self.user.user_id, float(height_cm), float(weight_kg))
        messagebox.showinfo("Saved", "Measurement data saved successfully.")

        self.height_entry.delete(0, "end")
        self.weight_entry.delete(0, "end")
        self.height_entry.focus()

    def download_records(self) -> None:
        """
        Downloads all past measurement records for the user to a text file.
        """
        try:
            records = get_all_days_metrics(self.user.user_id)

            if not records:
                messagebox.showinfo("No Records", "No measurement records found for this user.")
                return

            filename = _build_metrics_filename()
            _write_metrics_log(filename, self.user.username, records)

            messagebox.showinfo("Success", f"Records downloaded successfully to {filename}")

        except Exception as exc:
            messagebox.showerror("Error", f"Failed to download records: {exc}")

    def return_to_dash(self) -> None:
        """Returns to the dashboard screen."""
        return_to_dashboard(self.frame, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Measurement(root, test_user)
    root.mainloop()
