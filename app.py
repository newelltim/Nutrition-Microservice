import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ----------------------------------------------------------------------
#  NUTRITIONIX CREDENTIALS
# ----------------------------------------------------------------------
# This works through Tim's App ID and Key, but you should be able to input your own Nutritionix Credentials.
NUTRITIONIX_APP_ID = os.environ.get("NUTRITIONIX_APP_ID", "09baffed")
NUTRITIONIX_APP_KEY = os.environ.get("NUTRITIONIX_APP_KEY", "9bdd9962c7eea07a127603b80d6fcc68")

# The Nutritionix "Natural Language" endpoint to parse multiple ingredients at once.
NUTRITIONIX_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"

# ----------------------------------------------------------------------
# HELPER FUNCTION: Call Nutritionix for Ingredient List
# ----------------------------------------------------------------------
def get_nutritionix_summary(ingredients):
    """
    Given a list of ingredient strings, call Nutritionix Natural Language endpoint
    through a single request.
    
    The response includes an array of "foods". Each "food" contains nutritional info which are:
      - nf_calories
      - nf_protein
      - nf_total_carbohydrate
      - nf_total_fat
    These are summed across all parsed foods and return a dictionary.

    Info about what we're doing:
    https://www.nutritionix.com/business/api
    """
    # Combine all ingredients into a single string, each ingredient on its own line
    query_string = "\n".join(ingredients)

    # Build the request payload
    body = {
        "query": query_string
    }

    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(NUTRITIONIX_URL, headers=headers, data=json.dumps(body))
    response.raise_for_status()  # Raise an error for bad status codes

    data = response.json()

    # The "foods" field is an array of parsed ingredient details
    foods = data.get("foods", [])

    total_calories = 0.0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0

    for food in foods:
        total_calories += food.get("nf_calories", 0)
        total_protein += food.get("nf_protein", 0)
        total_carbs += food.get("nf_total_carbohydrate", 0)
        total_fat += food.get("nf_total_fat", 0)

    return {
        "calories": total_calories,
        "protein": total_protein,
        "carbs": total_carbs,
        "fat": total_fat
    }

def scale_ingredient_string(ingredient_str, scalar):
    """
    Scale the numeric quantity in the ingredient string by the given scalar.
    E.g.: "1 cup rice" + scalar=2 => "2 cup rice"
    
    Very naive approach: we assume the first token in the string is the quantity.
    """
    parts = ingredient_str.split()
    if not parts:
        return ingredient_str

    try:
        quantity = float(parts[0])
    except ValueError:
        quantity = 1.0

    new_quantity = quantity * scalar
    parts[0] = str(new_quantity)

    return " ".join(parts)

# ----------------------------------------------------------------------
# ROUTE 1: /summary
# ----------------------------------------------------------------------
@app.route("/summary", methods=["POST"])
def get_summary():
    """
    POST /summary

    Expected JSON:
    {
      "ingredients": ["1 cup rice", "2 eggs", "1 tbsp olive oil"],
      "scalar": 1
    }

    Returns total nutritional info for all ingredients combined.
    """
    data = request.get_json()
    ingredients = data.get("ingredients", [])
    scalar = float(data.get("scalar", 1))

    # Call Nutritionix to get aggregated macros for the entire ingredient list
    base_summary = get_nutritionix_summary(ingredients)

    # Scale the final total if needed
    total_calories = base_summary["calories"] * scalar
    total_protein = base_summary["protein"] * scalar
    total_carbs = base_summary["carbs"] * scalar
    total_fat = base_summary["fat"] * scalar

    return jsonify({
        "summary": {
            "calories": round(total_calories, 2),
            "protein": round(total_protein, 2),
            "carbs": round(total_carbs, 2),
            "fat": round(total_fat, 2)
        }
    })

# ----------------------------------------------------------------------
# ROUTE 2: /scale-ingredients
# ----------------------------------------------------------------------
@app.route("/scale-ingredients", methods=["POST"])
def scale_ingredients():
    """
    POST /scale-ingredients

    Expected JSON:
    {
      "ingredients": ["1 cup rice", "2 eggs", "1 tbsp olive oil"],
      "scalar": 2
    }

    Returns scaled ingredient list:
    {
      "scaledIngredients": ["2 cup rice", "4 eggs", "2 tbsp olive oil"]
    }
    """
    data = request.get_json()
    ingredients = data.get("ingredients", [])
    scalar = float(data.get("scalar", 1))

    scaled_list = [scale_ingredient_string(ing, scalar) for ing in ingredients]

    return jsonify({"scaledIngredients": scaled_list})

# ----------------------------------------------------------------------
# ROUTE 3: /scale-summary
# ----------------------------------------------------------------------
@app.route("/scale-summary", methods=["POST"])
def scale_summary():
    """
    POST /scale-summary

    Expected JSON:
    {
      "calories": 500,
      "protein": 20.5,
      "carbs": 60.3,
      "fat": 20.1,
      "scalar": 2
    }

    Returns the scaled summary:
    {
      "summary": {
        "calories": 1000,
        "protein": 41,
        "carbs": 120.6,
        "fat": 40.2
      }
    }
    """
    data = request.get_json()

    calories = float(data.get("calories", 0))
    protein = float(data.get("protein", 0))
    carbs = float(data.get("carbs", 0))
    fat = float(data.get("fat", 0))
    scalar = float(data.get("scalar", 1))

    scaled_summary = {
        "calories": round(calories * scalar, 2),
        "protein": round(protein * scalar, 2),
        "carbs": round(carbs * scalar, 2),
        "fat": round(fat * scalar, 2)
    }

    return jsonify({"summary": scaled_summary})

# ----------------------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=3000, debug=True)
