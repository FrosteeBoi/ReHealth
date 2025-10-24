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
