import ttkbootstrap as tb

from db.db_handler import (
    get_total_steps,
    get_total_sleep_hours,
    get_total_weight_lifted,
    get_weight
)
from logic.calculations import get_rehealth_level, calculate_lifetime_score, calories_burnt
from logic.user import User
from ui.ui_handler import return_to_dashboard, BasePage

rank_colours = {
    "Bronze Beginner": "warning",
    "Silver Strider": "secondary",
    "Golden Grinder": "success",
    "Platinum Pro": "info",
    "Diamond Elite": "primary",
    "Athlete": "success",
    "Olympian": "danger",
    "#1 ReHealth User": "primary",
}

rank_thresholds = [
    ("Bronze Beginner", 0, 500),
    ("Silver Strider", 500, 1000),
    ("Golden Grinder", 1000, 2000),
    ("Platinum Pro", 2000, 3500),
    ("Diamond Elite", 3500, 5000),
    ("Athlete", 5000, 7500),
    ("Olympian", 7500, 10000),
    ("#1 ReHealth User", 10000, None),
]


def _get_progress_bar_colour(rank):
    """
    Returns the colour based on user rank.
    """
    return rank_colours.get(rank, "primary")


def _get_progress_to_next_level(score):
    """
    returns how close the user is to the next rank
    """
    if score >= 10000:
        return None, 100.0

    for i, (_, lower, upper) in enumerate(rank_thresholds):
        if upper is None:
            continue
        if lower <= score < upper:
            next_rank_name, _, _ = rank_thresholds[i + 1]
            progress = (score - lower) / (upper - lower) * 100
            return next_rank_name, progress

    return None, 0.0


class Achievements(BasePage):
    """
    Class created to view user achievements.
    """

    def __init__(self, root, user: User):
        """
        Main window for achievements initialised.
        """
        self._load_user_stats_before_ui(user)

        # Call parent constructor
        super().__init__(root, user, "Achievements")

    def _load_user_stats_before_ui(self, user):
        """Load user stats that are needed before building UI"""
        self.total_steps = get_total_steps(user.user_id)
        self.total_cals = round(calories_burnt(self.total_steps, get_weight(user.user_id)))
        self.total_sleep = get_total_sleep_hours(user.user_id)
        self.total_weight = get_total_weight_lifted(user.user_id)

        self.user_score = calculate_lifetime_score(
            self.total_steps,
            self.total_sleep,
            self.total_weight,
        )
        self.user_rank = get_rehealth_level(self.user_score)

    def _build_ui(self):
        next_rank_name, progress_percent = _get_progress_to_next_level(
            self.user_score
        )
        bar_colour = _get_progress_bar_colour(self.user_rank)

        self.achieve_label = tb.Label(
            self.frame,
            text=f"{self.user.username}'s Hall of Fame",
            font=("roboto", 18, "bold"),
        )
        self.achieve_label.grid(row=0, column=0, pady=(20, 30), sticky="n")

        self.ranking_label = tb.Label(
            self.frame,
            text=f"Current Rank: {self.user_rank}",
            font=("roboto", 14, "bold"),
        )
        self.ranking_label.grid(row=1, column=0, pady=(5, 5), sticky="n")

        if next_rank_name is not None:
            self.progress_text_label = tb.Label(
                self.frame,
                text=f"Progress to {next_rank_name}: {progress_percent:.1f}%",
                font=("roboto", 12),
            )
            self.progress_text_label.grid(row=2, column=0, pady=(5, 5), sticky="n")

            self.progress_bar = tb.Progressbar(
                self.frame,
                orient="horizontal",
                mode="determinate",
                length=300,
                maximum=100,
                bootstyle=f"{bar_colour}-striped",
            )
            self.progress_bar.grid(row=3, column=0, pady=(0, 20), sticky="n")
            self.progress_bar["value"] = progress_percent
        else:
            self.progress_text_label = tb.Label(
                self.frame,
                text="You are the #1 ReHealth User!",
                font=("roboto", 12, "bold"),
            )
            self.progress_text_label.grid(row=2, column=0, pady=(5, 20), sticky="n")

        self.steps_label = tb.Label(
            self.frame,
            text=f"Total Steps Taken: {self.total_steps:,}",
            font=("roboto", 14, "bold"),
        )
        self.steps_label.grid(row=5, column=0, pady=10, sticky="n")

        self.cals_label = tb.Label(
            self.frame,
            text=f"Total Calories Burnt: {self.total_cals:,}",
            font=("roboto", 14, "bold"),
        )
        self.cals_label.grid(row=6, column=0, pady=10, sticky="n")

        self.sleep_label = tb.Label(
            self.frame,
            text=f"Total Hours Slept: {self.total_sleep:.0f}",
            font=("roboto", 14, "bold"),
        )
        self.sleep_label.grid(row=7, column=0, pady=10, sticky="n")

        self.weight_label = tb.Label(
            self.frame,
            text=f"Total weight lifted: {self.total_weight:.0f}kg",
            font=("roboto", 14, "bold"),
        )
        self.weight_label.grid(row=8, column=0, pady=10, sticky="n")

        self.dash_button = tb.Button(
            self.frame,
            text="Back to Dashboard",
            command=self.return_to_dash,
            width=22,
        )
        self.dash_button.grid(row=9, column=0, pady=(200, 10), sticky="n")

        self.frame.grid_rowconfigure(9, minsize=200)

    def return_to_dash(self):
        """
        Returns to the dashboard screen.
        """
        return_to_dashboard(self.frame, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    test_user.user_id = 1
    app = Achievements(root, test_user)
    root.mainloop()
