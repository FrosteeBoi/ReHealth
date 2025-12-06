def bmi_calc(kg_weight, cm_height):
    # Converts height from cm to m before calculating BMI
    m_height = float(cm_height) / 100
    return round(float(kg_weight) / (m_height ** 2), 1)


def sleep_calc(sleep_duration, sleep_quality):
    """
    Calculates a balanced sleep rating between 0 and 1.
    - sleep_duration: hours slept (0–24)
    - sleep_quality: integer 1–5 (how refreshed you feel)
    """

    if sleep_duration < 7:
        duration_score = sleep_duration / 7.0  # 0 → 1
    elif 7 <= sleep_duration <= 9:
        duration_score = 1.0
    else:
        duration_score = max(0.7, 1.0 - (sleep_duration - 9) * 0.1)

    quality_score = sleep_quality / 5.0

    sleep_rating = (duration_score * 0.6) + (quality_score * 0.4)

    return sleep_rating


def bmi_status(bmi):
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
    Estimates calories burnt walking.
    """
    distance_m = steps * 0.78
    distance_km = distance_m / 1000

    if weight_kg == 0.0:
        calories = distance_km * 50
    else:
        calories = weight_kg * distance_km * 1

    return round(calories, 2)


def calculate_lifetime_score(lifetime_steps,
                             lifetime_sleep_hours,
                             lifetime_weight):
    """
    Calculate an overall ReHealth score from lifetime activity.
    """

    #   10,000 steps ≈ 1 step point
    #   8 hours sleep ≈ 1 sleep point
    #   1,000 kg lifted ≈ 1 weight point
    step_ratio = 10_000
    sleep_ratio = 8
    weight_ratio = 1_000

    step_points = lifetime_steps / step_ratio
    sleep_points = lifetime_sleep_hours / sleep_ratio
    weight_points = lifetime_weight / weight_ratio

    # --- Weights for each component ---
    # Steps: 40%, Sleep: 30%, Weight lifting: 30%
    step_weight = 0.4
    sleep_weight = 0.3
    weight_weight = 0.3

    raw_score = (
            step_points * step_weight +
            sleep_points * sleep_weight +
            weight_points * weight_weight
    )

    scaled_score = raw_score * 100

    return int(round(scaled_score))


def get_rehealth_level(score):
    """
    Convert a ReHealth score into a rank
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
