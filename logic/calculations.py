
from db.db_handler import get_weight

def bmi_calc(kg_weight, cm_height):
    # Converts height from cm to m before calculating BMI
    m_height = float(cm_height) / 100
    return round(float(kg_weight) / (m_height ** 2), 1)


def sleep_calc(sleep_duration, sleep_quality):
    # Calculates a sleep rating from 2 variables
    duration_var = (sleep_duration * 0.6) / 8
    quality_var = (sleep_quality / 5) * 0.4

    sleep_rating = duration_var + quality_var
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


