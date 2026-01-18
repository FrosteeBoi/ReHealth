"""Calculations Module - ReHealth"""


def bmi_calc(kg_weight, cm_height):
    """
    Calculates Body Mass Index (BMI) from weight and height.

    Args:
        kg_weight (float): Weight in kilograms.
        cm_height (float): Height in centimeters.

    Returns:
        float: BMI value rounded to 1 decimal place.

    Raises:
        ValueError: If height is zero or negative.
        TypeError: If inputs cannot be converted to float.
    """
    m_height = float(cm_height) / 100

    return round(float(kg_weight) / (m_height ** 2), 1)


def sleep_calc(sleep_duration, sleep_quality):
    """
    Calculates a balanced sleep rating between 0 and 1.
    Args:
        sleep_duration (float): Hours slept (0-24).
        sleep_quality (int): Subjective quality rating (1-5).
            1 = Poor sleep
            5 = Excellent sleep

    Returns:
        float: Sleep rating between 0.0 and 1.0, where 1.0 is optimal.
    """

    if sleep_duration < 7:
        duration_score = sleep_duration / 7.0
    elif 7 <= sleep_duration <= 9:
        duration_score = 1.0
    else:
        duration_score = max(0.7, 1.0 - (sleep_duration - 9) * 0.1)

    quality_score = sleep_quality / 5.0

    sleep_rating = (duration_score * 0.6) + (quality_score * 0.4)

    return sleep_rating


def bmi_status(bmi):
    """
    Classifies BMI value into health categories.

    Args:
        bmi (float): BMI value.

    Returns:
        str: Classification category:
            - "Underweight": BMI < 18.5
            - "Healthy": 18.5 ≤ BMI < 25
            - "Overweight": 25 ≤ BMI < 30
            - "Obese": BMI ≥ 30
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Healthy"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calories_burnt(steps, weight_kg):
    """
    Estimates calories burnt from walking based on steps and body weight.

    Args:
        steps (int): Number of steps taken.
        weight_kg (float): Body weight in kilograms.

    Returns:
        float: Estimated calories burnt, rounded to 2 decimal places.
    """
    # Calculate distance walked
    distance_m = steps * 0.78
    distance_km = distance_m / 1000

    # Calculate calories (default to 50 kcal/km if weight unknown)
    if weight_kg == 0.0:
        calories = distance_km * 50
    else:
        calories = weight_kg * distance_km

    return round(calories, 2)


def calculate_lifetime_score(lifetime_steps, lifetime_sleep_hours, lifetime_weight):
    """
    Calculate an overall ReHealth achievement score from lifetime activity.
    Args:
        lifetime_steps (int): Total steps taken across all time.
        lifetime_sleep_hours (float): Total hours slept across all time.
        lifetime_weight (float): Total weight lifted in kg across all time.

    Returns:
        int: ReHealth score (typically 0-10000+), where higher is better.
    """
    # Define conversion ratios for each metric and implement weights
    step_ratio = 10_000  # 10,000 steps = 1 point
    sleep_ratio = 8  # 8 hours = 1 point
    weight_ratio = 1_000  # 1,000 kg = 1 point

    step_points = lifetime_steps / step_ratio
    sleep_points = lifetime_sleep_hours / sleep_ratio
    weight_points = lifetime_weight / weight_ratio

    step_weight = 0.45  # Steps: 45%
    sleep_weight = 0.45  # Sleep: 45%
    weight_weight = 0.1  # Weight lifting: 10%

    # Calculate weighted score
    raw_score = (
            step_points * step_weight +
            sleep_points * sleep_weight +
            weight_points * weight_weight
    )

    # Scale to 0-10000+ range and convert to integer
    scaled_score = raw_score * 100

    return int(round(scaled_score))


def get_rehealth_level(score):
    """
    Convert a ReHealth score into a rank/achievement level.

    Args:
        score (int): ReHealth score from calculate_lifetime_score().

    Returns:
        str: Rank name corresponding to the score:
            - "Bronze Beginner": 0-499
            - "Silver Strider": 500-999
            - "Golden Grinder": 1000-1999
            - "Platinum Pro": 2000-3499
            - "Diamond Elite": 3500-4999
            - "Athlete": 5000-6999
            - "Olympian": 7000-9999
            - "#1 ReHealth User": 10000+
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
