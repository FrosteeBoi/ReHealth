def bmi_calc(kg_weight, cm_height):
    # Converts height from cm to m before calculating BMI
    m_height = float(cm_height) / 100
    return round(float(kg_weight) / (m_height ** 2), 1)
