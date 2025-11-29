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
