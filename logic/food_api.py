"""
USE OPEN FOOD FACTS INSTEAD
"""




import requests

api_key ="b00818ea914348ce8d881f52088d0e53"

class Consumable:
    def __init__(self, name, calories):
        self.name = name
        self.calories = calories

    def validate_input(self):
        if not self.name.strip() or not str(self.calories).isdigit():
            raise ValueError("Invalid input")

    def save_to_db(self, user_id):
        # Call your save_food function or equivalent
        pass

class Food(Consumable):
    def __init__(self, name, calories):
        super().__init__(name, calories)

class Drink(Consumable):
    def __init__(self, name, calories, volume_ml):
        super().__init__(name, calories)
        self.volume_ml = volume_ml

def fetch_food_from_api(food_name):
    url = f"https://api.spoonacular.com/food/ingredients/search?query={food_name}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get('results'):
        # Example: get calories from the first result if available
        food_result = data['results'][0]
        calories = 0

        # Spoonacular sometimes returns nutrition in a nested call; this is a simple example:
        if 'nutrition' in food_result and 'nutrients' in food_result['nutrition']:
            for nutrient in food_result['nutrition']['nutrients']:
                if nutrient['name'] == 'Calories':
                    calories = int(nutrient['amount'])
                    break

        return {"name": food_result['name'], "calories": calories}
    return None


api_data = fetch_food_from_api("banana")  # Example search
if api_data:
    food_obj = Food(api_data['name'], api_data['calories'])
    print(food_obj.name, food_obj.calories)
else:
    print("Food not found")