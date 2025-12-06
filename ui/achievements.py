import os
from datetime import datetime
from tkinter import messagebox
import ttkbootstrap as tb
from db.db_handler import get_total_steps, get_total_calories, get_total_sleep_hours, get_total_weight_lifted
from logic.calculations import get_rehealth_level, calculate_lifetime_score
from logic.user import User
from ui.ui_handler import return_to_dashboard


class Achievements:
    """
    Class created to view user achievements.
    """

    def __init__(self, root, user: User):
        """
        Main window for achievements initialised.
        """
        self.root = root
        self.user = user
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        # main frame
        self.achieveframe = tb.Frame(self.root)
        self.achieveframe.place(relx=0.5, rely=0, anchor="n")

        # Fetch totals and rank
        total_steps = get_total_steps(self.user.user_id)
        total_cals = get_total_calories(self.user.user_id)
        total_sleep = get_total_sleep_hours(self.user.user_id)
        total_weight = get_total_weight_lifted(self.user.user_id)
        user_score = calculate_lifetime_score(total_steps, total_sleep, total_weight)
        user_rank = get_rehealth_level(user_score)

        next_rank_name, progress_percent = self._get_progress_to_next_level(user_score)

        self.achieve_label = tb.Label(
            self.achieveframe,
            text=f"{self.user.username}'s Hall of Fame",
            font=("roboto", 18, "bold")
        )
        self.achieve_label.grid(row=0, column=0, pady=(20, 30), sticky="n")

        self.ranking_label = tb.Label(
            self.achieveframe,
            text=f"Current Rank: {user_rank}",
            font=("roboto", 14, "bold")
        )
        self.ranking_label.grid(row=1, column=0, pady=(5, 5), sticky="n")

        bar_colour = self._get_progress_bar_colour(user_rank)

        if next_rank_name is not None:

            self.progress_text_label = tb.Label(
                self.achieveframe,
                text=f"Progress to {next_rank_name}: {progress_percent:.1f}%",
                font=("roboto", 12)
            )
            self.progress_text_label.grid(row=2, column=0, pady=(5, 5), sticky="n")

            self.progress_bar = tb.Progressbar(
                self.achieveframe,
                orient="horizontal",
                mode="determinate",
                length=300,
                maximum=100,
                bootstyle=bar_colour
            )
            self.progress_bar.grid(row=3, column=0, pady=(0, 20), sticky="n")
            self.progress_bar["value"] = progress_percent
        else:

            self.progress_text_label = tb.Label(
                self.achieveframe,
                text="You are the #1 ReHealth User!",
                font=("roboto", 12, "bold")
            )
            self.progress_text_label.grid(row=2, column=0, pady=(5, 20), sticky="n")

        self.steps_label = tb.Label(
            self.achieveframe,
            text=f"Total Steps Taken: {total_steps:,}",
            font=("roboto", 14, "bold")
        )
        self.steps_label.grid(row=5, column=0, pady=10, sticky="n")

        self.cals_label = tb.Label(
            self.achieveframe,
            text=f"Total Calories Burnt: {total_cals:,}",
            font=("roboto", 14, "bold")
        )
        self.cals_label.grid(row=6, column=0, pady=10, sticky="n")

        self.sleep_label = tb.Label(
            self.achieveframe,
            text=f"Total Hours Slept: {total_sleep:.0f}",
            font=("roboto", 14, "bold")
        )
        self.sleep_label.grid(row=7, column=0, pady=10, sticky="n")

        self.weight_label = tb.Label(
            self.achieveframe,
            text=f"Total weight lifted: {total_weight:.0f}kg",
            font=("roboto", 14, "bold")
        )
        self.weight_label.grid(row=8, column=0, pady=10, sticky="n")

        self.dash_button = tb.Button(
            self.achieveframe,
            text="Back to Dashboard",
            command=self.return_to_dash,
            width=22
        )
        self.dash_button.grid(row=9, column=0, pady=(40, 10), sticky="n")

        self.achieveframe.grid_rowconfigure(9, minsize=200)

    def _get_progress_bar_colour(self, rank):
        """
        Returns the colour based on user rank.
        """
        rank_colours = {
            "Bronze Beginner": "warning",
            "Silver Strider": "secondary",
            "Gold Grinder": "success",
            "Platinum Pro": "info",
            "Diamond Elite": "primary",
            "Athlete": "success",
            "Olympian": "danger",
            "#1 ReHealth User": "primary",
        }

        return rank_colours.get(rank, "primary")

    def _get_progress_to_next_level(self, score):
        """
        returns how close the user is to the next rank
        """
        thresholds = [
            ("Bronze Beginner", 0, 500),
            ("Silver Strider", 500, 1000),
            ("Gold Grinder", 1000, 2000),
            ("Platinum Pro", 2000, 3500),
            ("Diamond Elite", 3500, 5000),
            ("Athlete", 5000, 7500),
            ("Olympian", 7500, 10000),
            ("#1 ReHealth User", 10000, None),
        ]

        if score >= 10000:
            return None, 100.0

        for i, (name, lower, upper) in enumerate(thresholds):
            if upper is None:
                continue
            if lower <= score < upper:
                next_rank_name, _, _ = thresholds[i + 1]
                progress = (score - lower) / (upper - lower) * 100
                return next_rank_name, progress

        return None, 0.0

    def return_to_dash(self):
        """
        Returns to the dashboard screen.
        """
        return_to_dashboard(self.achieveframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    test_user.user_id = 1  # TEMP for testing
    app = Achievements(root, test_user)
    root.mainloop()
