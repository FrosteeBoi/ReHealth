"""Calculations Module - ReHealth"""


def bmi_calc(kg_weight: float, cm_height: float) -> float:
    """
    Calculates user bmi

    Args:
        kg_weight (float): The user's weight.
        cm_height (float): The user's height.

    Returns:
        float: The user's bmi value

    Raises:
        ValueError: If height is zero or negative.
        TypeError: If inputs cannot be converted to float.
    """
    m_height = float(cm_height) / 100

    return round(float(kg_weight) / (m_height ** 2), 1)


def sleep_calc(sleep_duration: float, sleep_quality: float) -> float:
    """
    Calculates a balanced sleep rating between 0 and 1.
    Args:
        sleep_duration (float): Hours slept by the user.
        sleep_quality (float): Subjective sleep rating logged by the user.

    Returns:
        float: Final sleep rating for user ranging from 0 to 1.
    """
    if sleep_duration < 1:
        return 0
    if sleep_duration < 7:
        duration_score = sleep_duration / 7.0
    elif 7 <= sleep_duration <= 9:
        duration_score = 1.0
    else:
        duration_score = max(0.7, 1.0 - (sleep_duration - 9) * 0.1)
        # Increasingly penalise the user for each hour of sleep above 9
        # Ensure that this penalisation does not result in a duration score < 0.7

    quality_score = sleep_quality / 5.0

    sleep_rating = (duration_score * 0.6) + (quality_score * 0.4)

    return sleep_rating


def bmi_status(bmi: float) -> str:
    """
    Provides the user with a description of their bmi.

    Args:
        bmi (float):The user's bmi.

    Returns:
        str: A value from the options: Underweight, Healthy, Overweight and Obese.
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Healthy"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calories_burnt(steps: int, weight_kg: float) -> float:
    """
    Estimates calories burnt by the user based on steps and body weight.

    Args:
        steps (int): Number of steps taken by the user.
        weight_kg (float): The user's weight

    Returns:
        float: Estimated calories burnt by the user rounded.
    """
    # Estimate distance walked by the user
    distance_m = steps * 0.78
    distance_km = distance_m / 1000

    # Estimate cals burnt (default to 50 kcal/km if no weight provided by user)
    if weight_kg == 0.0:
        calories = distance_km * 50
    else:
        calories = weight_kg * distance_km

    return round(calories, 2)


def calculate_lifetime_score(
    lifetime_steps: int,
    lifetime_sleep_hours: float,
    lifetime_weight: float
) -> int:
    """
    Calculate an overall ReHealth achievement score from lifetime activity.
    Args:
        lifetime_steps (int): Total steps taken across all time.
        lifetime_sleep_hours (float): Total hours slept across all time.
        lifetime_weight (float): Total weight lifted in kg across all time.

    Returns:
        int: ReHealth score in the range of 0 to 10,000.
    """

    step_ratio = 10_000  # 10,000 steps = 1 point
    sleep_ratio = 8  # 8 hours = 1 point
    weight_ratio = 1_000  # 1,000 kg = 1 point

    step_points = lifetime_steps / step_ratio
    sleep_points = lifetime_sleep_hours / sleep_ratio
    weight_points = lifetime_weight / weight_ratio

    # Create a weighted score using steps, sleep and weight lifted
    # Each metric is factored appropriately.
    step_weight = 0.45
    sleep_weight = 0.45
    weight_weight = 0.1

    raw_score = (
            step_points * step_weight +
            sleep_points * sleep_weight +
            weight_points * weight_weight
    )

    # Scale to 0-10000+ range and convert to integer
    scaled_score = raw_score * 100

    return int(round(scaled_score))


def get_rehealth_level(score: int) -> str:
    """
    Convert a ReHealth score into a rank/achievement level using the user's score.

    Args:
        score (int): ReHealth score from calculate_lifetime_score().

    Returns:
        str: Rank name corresponding to the score:
            "Bronze Beginner"
            "Silver Strider"
            "Golden Grinder"
            "Platinum Pro"
            "Diamond Elite"
            "Athlete"
            "Olympian"
            "#1 ReHealth User"
    """
    if score < 500:
        return "Bronze Beginner"
    elif score < 1000:
        return "Silver Strider"
    elif score < 2000:
        return "Golden Grinder"
    elif score < 3500:
        return "Platinum Pro"
    elif score < 5000:
        return "Diamond Elite"
    elif score < 7000:
        return "Athlete"
    elif score < 10000:
        return "Olympian"
    else:
        return "#1 ReHealth User"
